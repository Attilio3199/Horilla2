from django.db import migrations


class Migration(migrations.Migration):
    """Bridge renamed rule-destination columns during the legacy data import."""

    dependencies = [("payroll", "0011_ensure_legacy_contract_level_columns")]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE payslip_controllo_regole_destinazioni
                    ADD COLUMN IF NOT EXISTS regola_id bigint NULL,
                    ADD COLUMN IF NOT EXISTS destinazione_valore varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS attivo boolean NULL;
                ALTER TABLE payslip_controllo_regole_destinazioni
                    ALTER COLUMN rule_id DROP NOT NULL,
                    ALTER COLUMN destination_value SET DEFAULT '',
                    ALTER COLUMN active SET DEFAULT true;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
