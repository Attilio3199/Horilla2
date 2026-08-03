from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("payroll", "0015_allow_legacy_payslip_dictionary_mappings")]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE payslip_importi
                    ADD COLUMN IF NOT EXISTS mese integer NULL,
                    ADD COLUMN IF NOT EXISTS anno integer NULL,
                    ADD COLUMN IF NOT EXISTS neg varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS matricola varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS importo numeric NULL;
                ALTER TABLE payslip_importi
                    ALTER COLUMN month SET DEFAULT 0,
                    ALTER COLUMN year SET DEFAULT 0;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
