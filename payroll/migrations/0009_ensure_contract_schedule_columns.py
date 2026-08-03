from django.db import migrations


class Migration(migrations.Migration):
    """Repair databases where the legacy migration was recorded but not applied."""

    dependencies = [("payroll", "0008_create_contract_split_view")]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE payroll_contract
                    ADD COLUMN IF NOT EXISTS tipo_contratto integer NULL,
                    ADD COLUMN IF NOT EXISTS lun numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS mar numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS mer numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS gio numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS ven numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS sab numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS dom numeric(10, 2) NULL DEFAULT 0;
                ALTER TABLE payroll_historicalcontract
                    ADD COLUMN IF NOT EXISTS tipo_contratto integer NULL,
                    ADD COLUMN IF NOT EXISTS lun numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS mar numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS mer numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS gio numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS ven numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS sab numeric(10, 2) NULL DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS dom numeric(10, 2) NULL DEFAULT 0;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
