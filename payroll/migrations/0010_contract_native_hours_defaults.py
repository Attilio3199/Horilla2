from django.db import migrations


class Migration(migrations.Migration):
    """Allow legacy Italian contracts to populate newer mandatory schedule fields."""

    dependencies = [("payroll", "0009_ensure_contract_schedule_columns")]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE payroll_contract
                    ALTER COLUMN monday_hours SET DEFAULT 0,
                    ALTER COLUMN tuesday_hours SET DEFAULT 0,
                    ALTER COLUMN wednesday_hours SET DEFAULT 0,
                    ALTER COLUMN thursday_hours SET DEFAULT 0,
                    ALTER COLUMN friday_hours SET DEFAULT 0,
                    ALTER COLUMN saturday_hours SET DEFAULT 0,
                    ALTER COLUMN sunday_hours SET DEFAULT 0;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
