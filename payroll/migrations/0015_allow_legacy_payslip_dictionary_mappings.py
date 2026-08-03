from django.db import migrations


class Migration(migrations.Migration):
    """A time type can legitimately map to multiple payroll codes in legacy data."""

    dependencies = [("payroll", "0014_legacy_contract_and_employee_views")]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE payslip_dizionario DROP CONSTRAINT IF EXISTS payslip_dizionario_codice_tipo_orario_key;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
