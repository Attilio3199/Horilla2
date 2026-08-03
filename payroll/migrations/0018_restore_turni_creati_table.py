from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("payroll", "0017_ensure_legacy_payslip_attendance_columns")]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE SEQUENCE IF NOT EXISTS payroll_variazioneoraria_id_seq;
                ALTER TABLE payroll_variazioneoraria ALTER COLUMN id SET DEFAULT nextval('payroll_variazioneoraria_id_seq');
                CREATE TABLE IF NOT EXISTS _turni_creati (
                    id bigint PRIMARY KEY, "Neg" varchar(3) NOT NULL, "Descrizione" varchar(100) NOT NULL,
                    "CODICEPERSONALE" varchar(100), "Data" date NOT NULL, "Ora_Prev_Inizio" time,
                    "Ora_Prev_Fine" time, "Ora_Cons_Inizio" time, "Ora_Cons_Fine" time,
                    "GiornoSettimana" varchar(20) NOT NULL, "Turno" varchar(20), "UtenteModifica" varchar(25) NOT NULL,
                    "DataModifica" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, "Blocco" integer DEFAULT 1,
                    "CODICE_TIPO_ORARIO" varchar(40), "Annotazioni" varchar(100)
                );
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
