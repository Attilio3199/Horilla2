from django.db import migrations


class Migration(migrations.Migration):
    """Retain the complete legacy payroll-body row while supporting the new view."""

    dependencies = [("payroll", "0012_ensure_legacy_payslip_rule_destination_columns")]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE payslip_corpo
                    ADD COLUMN IF NOT EXISTS mese integer NULL,
                    ADD COLUMN IF NOT EXISTS anno integer NULL,
                    ADD COLUMN IF NOT EXISTS codice_dl varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS denominazione varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS filiale varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS c_costo integer NULL,
                    ADD COLUMN IF NOT EXISTS reparto integer NULL,
                    ADD COLUMN IF NOT EXISTS matricola varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS cognome varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS nome varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS qp varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS assunzione date NULL,
                    ADD COLUMN IF NOT EXISTS anzianita date NULL,
                    ADD COLUMN IF NOT EXISTS cod_pos integer NULL,
                    ADD COLUMN IF NOT EXISTS data_pos date NULL,
                    ADD COLUMN IF NOT EXISTS liq varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS cod_voce integer NULL,
                    ADD COLUMN IF NOT EXISTS descrizione_voce varchar(255) NULL,
                    ADD COLUMN IF NOT EXISTS aliq_perc_lav numeric NULL,
                    ADD COLUMN IF NOT EXISTS unita numeric NULL,
                    ADD COLUMN IF NOT EXISTS dato_base_imponibile numeric NULL,
                    ADD COLUMN IF NOT EXISTS importo_ctr_lav numeric NULL,
                    ADD COLUMN IF NOT EXISTS db_tfr numeric NULL,
                    ADD COLUMN IF NOT EXISTS imp_tfr_ctr_dl numeric NULL;
                ALTER TABLE payslip_corpo
                    ALTER COLUMN month SET DEFAULT 0,
                    ALTER COLUMN year SET DEFAULT 0,
                    ALTER COLUMN employee_number SET DEFAULT '',
                    ALTER COLUMN surname SET DEFAULT '',
                    ALTER COLUMN first_name SET DEFAULT '',
                    ALTER COLUMN code SET DEFAULT 0,
                    ALTER COLUMN description SET DEFAULT '';
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
