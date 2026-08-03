from django.db import migrations


class Migration(migrations.Migration):
    """Restore the two SQL export views used by the legacy Horilla instance."""

    dependencies = [("payroll", "0013_ensure_legacy_payslip_body_columns")]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS payroll_variazioneoraria (
                    id bigint PRIMARY KEY, created_at timestamptz NULL, is_active boolean NOT NULL DEFAULT true,
                    contract_name varchar(250) NOT NULL DEFAULT '', contract_start_date date NOT NULL,
                    contract_end_date date NULL, wage_type varchar(250) NOT NULL DEFAULT 'monthly',
                    pay_frequency varchar(20) NULL, wage double precision NULL, contract_status varchar(250) NOT NULL DEFAULT 'draft',
                    notice_period_in_days integer NOT NULL DEFAULT 30, deduct_leave_from_basic_pay boolean NOT NULL DEFAULT true,
                    calculate_daily_leave_amount boolean NOT NULL DEFAULT true, deduction_for_one_leave_amount double precision NULL,
                    tipo_contratto integer NULL, lun numeric(10,2) NULL DEFAULT 0, mar numeric(10,2) NULL DEFAULT 0,
                    mer numeric(10,2) NULL DEFAULT 0, gio numeric(10,2) NULL DEFAULT 0, ven numeric(10,2) NULL DEFAULT 0,
                    sab numeric(10,2) NULL DEFAULT 0, dom numeric(10,2) NULL DEFAULT 0, note text NULL,
                    contract_id bigint NOT NULL, created_by_id bigint NULL, department_id bigint NULL, employee_id_id bigint NOT NULL,
                    filing_status_id bigint NULL, job_position_id bigint NULL, job_role_id bigint NULL, modified_by_id bigint NULL,
                    shift_id bigint NULL, work_type_id bigint NULL, attachment varchar(100) NULL
                );

                CREATE OR REPLACE VIEW dipendenti AS
                SELECT e.badge_id AS cod_dip, e.is_active AS attivo, e.employee_first_name AS nome,
                    e.employee_last_name AS cognome, e.email, e.phone AS telefono,
                    e.domicilio_address AS domicilio_indirizzo, e.domicilio_citta AS domicilio_comune,
                    e.domicilio_zip AS domicilio_cap,
                    trim(substring(e.docimicilio_provincia::text, '\\((.*?)\\)'))::varchar(100) AS domicilio_provinica,
                    e.residenza_address AS residenza_indirizzo, e.residenza_citta AS residenza_comune,
                    e.residenza_zip AS residenza_cap,
                    trim(substring(e.residenza_provincia::text, '\\((.*?)\\)'))::varchar(100) AS residenza_provincia,
                    e.dob AS nascita_data, e.nascita_citta, e.nascita_provincia, e.gender AS sesso,
                    e.codice_fiscale, e.categoria_protetta, e.codice_paghe, eb.account_number AS iban,
                    ew.work_area_type, ew.department_code AS reparto_interno, ew.store_code AS negozio_codice,
                    ew.store_name AS negozio_siglia, ew.export_payslip AS esporta_cedolino,
                    ew.mirror_payslip AS cedolino_speculare, ew.premi
                FROM employee_employee e
                LEFT JOIN employee_employeebankdetails eb ON eb.employee_id_id = e.id
                LEFT JOIN employee_employeeworkinformation ew ON ew.employee_id_id = e.id;

                CREATE OR REPLACE VIEW contratti AS
                WITH variazioni AS (
                    SELECT v.*, row_number() OVER (PARTITION BY v.contract_id ORDER BY v.contract_end_date, v.id) AS seq,
                        lag(v.contract_end_date) OVER (PARTITION BY v.contract_id ORDER BY v.contract_end_date, v.id) AS prev_end
                    FROM payroll_variazioneoraria v WHERE v.contract_end_date IS NOT NULL
                ), segmenti AS (
                    SELECT c.id, v.seq, CASE WHEN v.prev_end IS NULL THEN c.contract_start_date ELSE v.prev_end + 1 END AS data_inizio,
                        v.contract_end_date AS data_fine, v.lun, v.mar, v.mer, v.gio, v.ven, v.sab, v.dom,
                        coalesce(v.tipo_contratto, c.tipo_contratto) AS tipo_contratto
                    FROM payroll_contract c JOIN variazioni v ON v.contract_id = c.id
                    UNION ALL
                    SELECT c.id, 1, c.contract_start_date, c.contract_end_date, c.lun, c.mar, c.mer, c.gio, c.ven, c.sab, c.dom, c.tipo_contratto
                    FROM payroll_contract c WHERE NOT EXISTS (SELECT 1 FROM variazioni v WHERE v.contract_id = c.id)
                    UNION ALL
                    SELECT c.id, max(v.seq) + 1, max(v.contract_end_date) + 1, c.contract_end_date,
                        c.lun, c.mar, c.mer, c.gio, c.ven, c.sab, c.dom, c.tipo_contratto
                    FROM payroll_contract c JOIN variazioni v ON v.contract_id = c.id
                    GROUP BY c.id, c.contract_end_date, c.lun, c.mar, c.mer, c.gio, c.ven, c.sab, c.dom, c.tipo_contratto
                    HAVING c.contract_end_date IS NULL OR max(v.contract_end_date) < c.contract_end_date
                )
                SELECT e.badge_id, s.lun, s.mar, s.mer, s.gio, s.ven, s.sab, s.dom, s.tipo_contratto,
                    s.data_inizio AS contract_start_date, s.data_fine AS contract_end_date,
                    c.id + s.seq - 1 AS id, c.created_at, c.is_active, c.contract_name, c.wage_type,
                    c.pay_frequency, c.wage, CASE WHEN s.data_fine < current_date THEN 'expired'::varchar ELSE c.contract_status END AS contract_status,
                    c.notice_period_in_days, c.contract_document, c.deduct_leave_from_basic_pay,
                    c.calculate_daily_leave_amount, c.deduction_for_one_leave_amount, c.note, c.created_by_id,
                    c.department_id, c.employee_id_id, c.filing_status_id, c.job_position_id, c.job_role_id,
                    c.modified_by_id, c.shift_id, c.work_type_id
                FROM segmenti s JOIN payroll_contract c ON c.id = s.id
                LEFT JOIN employee_employee e ON e.id = c.employee_id_id
                WHERE s.data_fine IS NULL OR s.data_inizio <= s.data_fine;
            """,
            reverse_sql="DROP VIEW IF EXISTS contratti; DROP VIEW IF EXISTS dipendenti;",
        ),
    ]
