from django.db import migrations


class Migration(migrations.Migration):
    """Keep the legacy level history alongside Horilla's native representation."""

    dependencies = [("payroll", "0010_contract_native_hours_defaults")]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE payroll_contract_lvl
                    ADD COLUMN IF NOT EXISTS created_by_id bigint NULL,
                    ADD COLUMN IF NOT EXISTS modified_by_id bigint NULL,
                    ADD COLUMN IF NOT EXISTS lvl integer NULL,
                    ADD COLUMN IF NOT EXISTS data_decorrenza date NULL,
                    ADD COLUMN IF NOT EXISTS employee_id_id bigint NULL;
                ALTER TABLE payroll_contract_lvl
                    ALTER COLUMN level SET DEFAULT 0,
                    ALTER COLUMN effective_date SET DEFAULT DATE '1970-01-01',
                    ALTER COLUMN employee_id DROP NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
