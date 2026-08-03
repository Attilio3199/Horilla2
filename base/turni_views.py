"""Import the MariaDB ``turni_creati`` dump into PostgreSQL.

The payroll checks read ``_turni_creati`` directly.  The table is deliberately
created from the supplied dump because its columns follow the scheduling
system's export and are not a Horilla model.
"""

import re

from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


TYPE_REPLACEMENTS = (
    (r"\btinyint\s*\(\s*1\s*\)(?:\s+unsigned\b)?", "BOOLEAN"),
    (r"\b(?:bigint)\s*\(\d+\)(?:\s+unsigned\b)?", "BIGINT"),
    (r"\b(?:mediumint|int)\s*\(\d+\)(?:\s+unsigned\b)?", "INTEGER"),
    (r"\bsmallint\s*\(\d+\)(?:\s+unsigned\b)?", "SMALLINT"),
    (r"\btinyint\s*\(\d+\)(?:\s+unsigned\b)?", "SMALLINT"),
    (r"\bdouble(?:\s+precision)?(?:\s*\(\d+,\d+\))?", "DOUBLE PRECISION"),
    (r"\bfloat(?:\s*\(\d+,\d+\))?", "REAL"),
    (r"\bdecimal\s*\((\d+),(\d+)\)", r"NUMERIC(\1,\2)"),
    (r"\b(?:datetime|timestamp)(?:\s*\(\d+\))?", "TIMESTAMP"),
    (r"\btime(?:\s*\(\d+\))?", "TIME"),
    (r"\byear(?:\s*\(\d+\))?", "SMALLINT"),
    (r"\b(?:longtext|mediumtext|text)\b", "TEXT"),
    (r"\b(?:longblob|blob)\b", "BYTEA"),
    (r"\bvarchar\s*\((\d+)\)", r"VARCHAR(\1)"),
    (r"\bchar\s*\((\d+)\)", r"CHAR(\1)"),
    (r"\b(?:enum|set)\s*\([^)]+\)", "TEXT"),
    (r"\bjson\b", "JSONB"),
    (r"\bbit\s*\(\d+\)", "BIT VARYING"),
)


def _matching_paren(text, opening):
    depth = 0
    for position in range(opening, len(text)):
        if text[position] == "(":
            depth += 1
        elif text[position] == ")":
            depth -= 1
            if depth == 0:
                return position
    raise ValueError("Parentesi non bilanciate nel dump SQL.")


def _split_columns(content):
    items, buffer, depth = [], [], 0
    for char in content:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        if char == "," and depth == 0:
            items.append("".join(buffer).strip())
            buffer = []
        else:
            buffer.append(char)
    if buffer:
        items.append("".join(buffer).strip())
    return [item for item in items if item]


def _postgres_ddl(sql, source_table):
    match = re.search(
        r"CREATE\s+TABLE\s+[`\"']?" + re.escape(source_table) + r"[`\"']?\s*\(",
        sql,
        re.I,
    )
    if not match:
        raise ValueError("CREATE TABLE della tabella turni non trovato.")
    opening = match.end() - 1
    closing = _matching_paren(sql, opening)
    columns = []
    for item in _split_columns(sql[opening + 1 : closing]):
        upper = item.upper().lstrip()
        if re.match(r"(?:UNIQUE\s+(?:KEY|INDEX)|KEY\s+|INDEX\s+)", upper):
            continue
        if upper.startswith("CONSTRAINT") and "KEY" in upper:
            continue
        item = re.sub(r"`([^`]+)`", r'"\1"', item)
        for pattern, replacement in TYPE_REPLACEMENTS:
            item = re.sub(pattern, replacement, item, flags=re.I)
        item = re.sub(r"\b(?:unsigned|zerofill|auto_increment|character set \S+|collate \S+)\b", "", item, flags=re.I)
        item = re.sub(r"\s+COMMENT\s+'(?:[^'\\]|\\.)*'", "", item, flags=re.I)
        item = re.sub(r"\bON\s+UPDATE\s+CURRENT_TIMESTAMP(?:\s*\(\d*\))?", "", item, flags=re.I)
        item = re.sub(r"DEFAULT\s+current_timestamp\s*\(\s*\d*\s*\)", "DEFAULT CURRENT_TIMESTAMP", item, flags=re.I)
        item = re.sub(r"DEFAULT\s+'0000-00-00(?:\s+00:00:00)?'", "DEFAULT NULL", item, flags=re.I)
        item = re.sub(
            r"DEFAULT\s+b'(\d)'",
            lambda match: "DEFAULT " + match.group(1),
            item,
            flags=re.I,
        )
        columns.append(re.sub(r"\s{2,}", " ", item).strip())
    return 'CREATE TABLE "_turni_creati" (\n    ' + ",\n    ".join(columns) + "\n);"


def _insert_statements(sql, source_table):
    pattern = re.compile(
        r"INSERT\s+INTO\s+[`\"']?" + re.escape(source_table) + r"[`\"']?\s*(?:\([^)]*\)\s*)?VALUES\s*.+?\)\s*;",
        re.I | re.S,
    )
    statements = []
    for match in pattern.finditer(sql):
        statement = re.sub(
            r"INSERT\s+INTO\s+[`\"']?" + re.escape(source_table) + r"[`\"']?",
            'INSERT INTO "_turni_creati"',
            match.group(0),
            count=1,
            flags=re.I,
        )
        statements.append(statement.replace("\\'", "''"))
    return statements


@login_required
@require_http_methods(["GET", "POST"])
def turni_import(request):
    if not request.user.is_staff:
        return HttpResponseBadRequest("Permesso negato.")
    if request.method == "GET":
        return render(request, "base/turni_import.html")

    dump_file = request.FILES.get("dump_file")
    if not dump_file or not dump_file.name.lower().endswith(".sql"):
        return render(request, "base/turni_import.html", {"error": "Seleziona un file .sql."})
    if dump_file.size > 50 * 1024 * 1024:
        return render(request, "base/turni_import.html", {"error": "Il file supera 50 MB."})
    sql = dump_file.read().decode("utf-8", errors="replace")
    found = re.search(r"CREATE\s+TABLE\s+[`\"']?(turni[_\w]*)[`\"']?", sql, re.I)
    if not found:
        return render(request, "base/turni_import.html", {"error": "Nel dump non è stata trovata la tabella turni_creati."})
    try:
        ddl = _postgres_ddl(sql, found.group(1))
        inserts = _insert_statements(sql, found.group(1))
        with transaction.atomic(), connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS "_turni_creati";')
            cursor.execute(ddl)
            for statement in inserts:
                cursor.execute(statement)
    except Exception as exc:
        return render(request, "base/turni_import.html", {"error": f"Errore durante l'importazione: {exc}"})
    return render(request, "base/turni_import.html", {"success": True, "rows_imported": len(inserts), "source_table": found.group(1)})
