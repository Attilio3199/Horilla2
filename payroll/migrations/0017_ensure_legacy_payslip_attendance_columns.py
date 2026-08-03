from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("payroll", "0016_ensure_legacy_payslip_amount_columns")]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE payslip_presenze
                    ADD COLUMN IF NOT EXISTS dl varchar(20), ADD COLUMN IF NOT EXISTS fil varchar(20), ADD COLUMN IF NOT EXISTS cc varchar(20),
                    ADD COLUMN IF NOT EXISTS rag_soc varchar(100), ADD COLUMN IF NOT EXISTS matricola varchar(20), ADD COLUMN IF NOT EXISTS lavoratore varchar(100),
                    ADD COLUMN IF NOT EXISTS qp varchar(10), ADD COLUMN IF NOT EXISTS data_ass date, ADD COLUMN IF NOT EXISTS livello varchar(10),
                    ADD COLUMN IF NOT EXISTS desc_liv varchar(50), ADD COLUMN IF NOT EXISTS pt varchar(10), ADD COLUMN IF NOT EXISTS perc_pt numeric(5,2),
                    ADD COLUMN IF NOT EXISTS perc_turn numeric(5,2), ADD COLUMN IF NOT EXISTS mese integer, ADD COLUMN IF NOT EXISTS anno integer,
                    ADD COLUMN IF NOT EXISTS cod_voce integer, ADD COLUMN IF NOT EXISTS desc_voce varchar(100), ADD COLUMN IF NOT EXISTS aliq_voce numeric(10,4),
                    ADD COLUMN IF NOT EXISTS day_1 numeric(8,4), ADD COLUMN IF NOT EXISTS day_2 numeric(8,4), ADD COLUMN IF NOT EXISTS day_3 numeric(8,4),
                    ADD COLUMN IF NOT EXISTS day_4 numeric(8,4), ADD COLUMN IF NOT EXISTS day_5 numeric(8,4), ADD COLUMN IF NOT EXISTS day_6 numeric(8,4),
                    ADD COLUMN IF NOT EXISTS day_7 numeric(8,4), ADD COLUMN IF NOT EXISTS day_8 numeric(8,4), ADD COLUMN IF NOT EXISTS day_9 numeric(8,4),
                    ADD COLUMN IF NOT EXISTS day_10 numeric(8,4), ADD COLUMN IF NOT EXISTS day_11 numeric(8,4), ADD COLUMN IF NOT EXISTS day_12 numeric(8,4),
                    ADD COLUMN IF NOT EXISTS day_13 numeric(8,4), ADD COLUMN IF NOT EXISTS day_14 numeric(8,4), ADD COLUMN IF NOT EXISTS day_15 numeric(8,4),
                    ADD COLUMN IF NOT EXISTS day_16 numeric(8,4), ADD COLUMN IF NOT EXISTS day_17 numeric(8,4), ADD COLUMN IF NOT EXISTS day_18 numeric(8,4),
                    ADD COLUMN IF NOT EXISTS day_19 numeric(8,4), ADD COLUMN IF NOT EXISTS day_20 numeric(8,4), ADD COLUMN IF NOT EXISTS day_21 numeric(8,4),
                    ADD COLUMN IF NOT EXISTS day_22 numeric(8,4), ADD COLUMN IF NOT EXISTS day_23 numeric(8,4), ADD COLUMN IF NOT EXISTS day_24 numeric(8,4),
                    ADD COLUMN IF NOT EXISTS day_25 numeric(8,4), ADD COLUMN IF NOT EXISTS day_26 numeric(8,4), ADD COLUMN IF NOT EXISTS day_27 numeric(8,4),
                    ADD COLUMN IF NOT EXISTS day_28 numeric(8,4), ADD COLUMN IF NOT EXISTS day_29 numeric(8,4), ADD COLUMN IF NOT EXISTS day_30 numeric(8,4),
                    ADD COLUMN IF NOT EXISTS day_31 numeric(8,4), ADD COLUMN IF NOT EXISTS ore_tot numeric(8,4), ADD COLUMN IF NOT EXISTS gg_tot numeric(6,4),
                    ADD COLUMN IF NOT EXISTS periodo_elab varchar(20), ADD COLUMN IF NOT EXISTS matricola_mese_anno varchar(50), ADD COLUMN IF NOT EXISTS cod_dip varchar(50);
                ALTER TABLE payslip_presenze ALTER COLUMN month SET DEFAULT 0, ALTER COLUMN year SET DEFAULT 0;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
