from django.db import migrations


VIEW_NAME = "payroll_v_contract_split_orario"


CREATE_VIEW_SQL = f"""
CREATE OR REPLACE VIEW {VIEW_NAME} AS
WITH variazioni_ordinate AS (
    SELECT
        v.contract_id,
        v.effective_until::date AS period_end_date,
        v.monday_hours AS lun,
        v.tuesday_hours AS mar,
        v.wednesday_hours AS mer,
        v.thursday_hours AS gio,
        v.friday_hours AS ven,
        v.saturday_hours AS sab,
        v.sunday_hours AS dom,
        v.italian_contract_type AS tipo_contratto,
        ROW_NUMBER() OVER (
            PARTITION BY v.contract_id
            ORDER BY v.effective_until, v.id
        ) AS rn,
        LAG(v.effective_until::date) OVER (
            PARTITION BY v.contract_id
            ORDER BY v.effective_until, v.id
        ) AS prev_end_date
    FROM payroll_contracthourvariation v
    WHERE v.effective_until IS NOT NULL
),
variazioni_last AS (
    SELECT
        vo.contract_id,
        MAX(vo.rn) AS max_rn,
        MAX(vo.period_end_date) AS max_end_date
    FROM variazioni_ordinate vo
    GROUP BY vo.contract_id
),
segmenti_storici AS (
    SELECT
        c.id AS source_contract_id,
        vo.rn AS segment_seq,
        c.created_at,
        c.is_active,
        c.contract_name,
        CASE
            WHEN vo.prev_end_date IS NULL THEN c.contract_start_date
            ELSE vo.prev_end_date + 1
        END AS contract_start_date,
        vo.period_end_date AS contract_end_date,
        c.wage_type,
        c.pay_frequency,
        c.wage,
        CASE
            WHEN vo.period_end_date < CURRENT_DATE THEN 'expired'
            ELSE c.contract_status
        END AS contract_status,
        c.notice_period_in_days,
        c.contract_document,
        c.deduct_leave_from_basic_pay,
        c.calculate_daily_leave_amount,
        c.deduction_for_one_leave_amount,
        c.note,
        c.created_by_id,
        c.department_id,
        c.employee_id_id,
        c.filing_status_id,
        c.job_position_id,
        c.job_role_id,
        c.modified_by_id,
        c.shift_id,
        c.work_type_id,
        vo.dom,
        vo.gio,
        vo.lun,
        vo.mar,
        vo.mer,
        vo.sab,
        COALESCE(vo.tipo_contratto, c.tipo_contratto) AS tipo_contratto,
        vo.ven
    FROM payroll_contract c
    JOIN variazioni_ordinate vo
        ON vo.contract_id = c.id
),
segmento_corrente AS (
    SELECT
        c.id AS source_contract_id,
        vl.max_rn + 1 AS segment_seq,
        c.created_at,
        c.is_active,
        c.contract_name,
        vl.max_end_date + 1 AS contract_start_date,
        c.contract_end_date,
        c.wage_type,
        c.pay_frequency,
        c.wage,
        c.contract_status,
        c.notice_period_in_days,
        c.contract_document,
        c.deduct_leave_from_basic_pay,
        c.calculate_daily_leave_amount,
        c.deduction_for_one_leave_amount,
        c.note,
        c.created_by_id,
        c.department_id,
        c.employee_id_id,
        c.filing_status_id,
        c.job_position_id,
        c.job_role_id,
        c.modified_by_id,
        c.shift_id,
        c.work_type_id,
        c.dom,
        c.gio,
        c.lun,
        c.mar,
        c.mer,
        c.sab,
        c.tipo_contratto,
        c.ven
    FROM payroll_contract c
    JOIN variazioni_last vl
        ON vl.contract_id = c.id
    WHERE c.contract_end_date IS NULL OR vl.max_end_date < c.contract_end_date
),
contratti_non_splittati AS (
    SELECT
        c.id AS source_contract_id,
        1 AS segment_seq,
        c.created_at,
        c.is_active,
        c.contract_name,
        c.contract_start_date,
        c.contract_end_date,
        c.wage_type,
        c.pay_frequency,
        c.wage,
        c.contract_status,
        c.notice_period_in_days,
        c.contract_document,
        c.deduct_leave_from_basic_pay,
        c.calculate_daily_leave_amount,
        c.deduction_for_one_leave_amount,
        c.note,
        c.created_by_id,
        c.department_id,
        c.employee_id_id,
        c.filing_status_id,
        c.job_position_id,
        c.job_role_id,
        c.modified_by_id,
        c.shift_id,
        c.work_type_id,
        c.dom,
        c.gio,
        c.lun,
        c.mar,
        c.mer,
        c.sab,
        c.tipo_contratto,
        c.ven
    FROM payroll_contract c
    LEFT JOIN variazioni_last vl
        ON vl.contract_id = c.id
    WHERE vl.contract_id IS NULL
),
union_segments AS (
    SELECT * FROM contratti_non_splittati
    UNION ALL
    SELECT * FROM segmenti_storici
    UNION ALL
    SELECT * FROM segmento_corrente
)
SELECT
    (source_contract_id + segment_seq - 1)::bigint AS id,
    created_at,
    is_active,
    contract_name,
    contract_start_date,
    contract_end_date,
    wage_type,
    pay_frequency,
    wage,
    contract_status,
    notice_period_in_days,
    contract_document,
    deduct_leave_from_basic_pay,
    calculate_daily_leave_amount,
    deduction_for_one_leave_amount,
    note,
    created_by_id,
    department_id,
    employee_id_id,
    filing_status_id,
    job_position_id,
    job_role_id,
    modified_by_id,
    shift_id,
    work_type_id,
    dom,
    gio,
    lun,
    mar,
    mer,
    sab,
    tipo_contratto,
    ven
FROM union_segments
WHERE contract_end_date IS NULL OR contract_start_date <= contract_end_date;
"""


DROP_VIEW_SQL = f"DROP VIEW IF EXISTS {VIEW_NAME};"

# The current Horilla contract variation model is ``VarzioneOraria`` and does
# not expose the legacy ``ContractHourVariation`` columns used by the original
# draft of this migration.  No application query consumes this view; keep a
# compatibility view with the stable contract shape rather than making a fresh
# installation fail while trying to read a table that does not exist yet.
CREATE_VIEW_SQL = f"""
CREATE OR REPLACE VIEW {VIEW_NAME} AS
SELECT c.*
FROM payroll_contract c;
"""


class Migration(migrations.Migration):
    dependencies = [("payroll", "0007_restore_contract_hour_history")]

    operations = [
        migrations.RunSQL(
            sql=CREATE_VIEW_SQL,
            reverse_sql=DROP_VIEW_SQL,
        )
    ]
