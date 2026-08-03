# Restores the contract-hour history table from Horilla.

import base.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import payroll.models.models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("payroll", "0006_restore_italian_contract_fields")]

    operations = [
        migrations.CreateModel(
                    name='VarzioneOraria',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created At')),
                        ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                        ('contract_name', models.CharField(blank=True, max_length=250, verbose_name='Contract')),
                        ('contract_start_date', models.DateField(verbose_name='Data Inizio')),
                        ('contract_end_date', models.DateField(blank=True, null=True, verbose_name='Data Fine')),
                        ('wage_type', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly'), ('hourly', 'Hourly')], default='monthly', max_length=250, verbose_name='Wage Type')),
                        ('pay_frequency', models.CharField(blank=True, choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('semi_monthly', 'Semi-Monthly')], default='monthly', max_length=20, null=True, verbose_name='Pay Frequency')),
                        ('wage', models.FloatField(default=0, null=True, verbose_name='Basic Salary')),
                        ('contract_status', models.CharField(choices=[('draft', 'Draft'), ('active', 'Active'), ('expired', 'Expired'), ('terminated', 'Terminated')], default='draft', max_length=250, verbose_name='Status')),
                        ('notice_period_in_days', models.IntegerField(default=30, validators=[payroll.models.models.min_zero], verbose_name='Notice Period')),
                        ('deduct_leave_from_basic_pay', models.BooleanField(default=True, verbose_name='Deduct From Basic Pay')),
                        ('calculate_daily_leave_amount', models.BooleanField(default=True, verbose_name='Calculate Daily Leave Amount')),
                        ('deduction_for_one_leave_amount', models.FloatField(blank=True, default=0, null=True, verbose_name='Deduction For One Leave Amount')),
                        ('tipo_contratto', models.IntegerField(blank=True, choices=[(1, 'Tirocinanti'), (2, 'Apprendistato'), (3, 'Determinato'), (4, 'Indeterminato'), (5, 'cocopro'), (6, 'GI GROUP'), (7, 'infojobmetis'), (8, 'ranstad'), (9, 'voucher')], null=True, verbose_name='Tipo Contratto')),
                        ('lun', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Lunedì')),
                        ('mar', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Martedì')),
                        ('mer', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Mercoledì')),
                        ('gio', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Giovedì')),
                        ('ven', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Venerdì')),
                        ('sab', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Sabato')),
                        ('dom', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Domenica')),
                        ('attachment', models.FileField(blank=True, null=True, upload_to='payroll/variazioni_orarie/', verbose_name='Allegato')),
                        ('note', models.TextField(blank=True, max_length=255, null=True)),
                        ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variazioni_orarie', to='payroll.contract', verbose_name='Contratto')),
                        ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                        ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variazioni_orarie', to='base.department', verbose_name='Department')),
                        ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variazioni_orarie', to='employee.employee', verbose_name='Dipendente')),
                        ('filing_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variazioni_orarie', to='payroll.filingstatus', verbose_name='Filing Status')),
                        ('job_position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variazioni_orarie', to='base.jobposition', verbose_name='Job Position')),
                        ('job_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variazioni_orarie', to='base.jobrole', verbose_name='Job Role')),
                        ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
                        ('shift', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variazioni_orarie', to='base.employeeshift', verbose_name='Shift')),
                        ('work_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variazioni_orarie', to='base.worktype', verbose_name='Work Type')),
                    ],
                    options={
                        'verbose_name': 'Variazione Oraria',
                        'verbose_name_plural': 'Variazioni Orarie',
                        'db_table': 'payroll_variazioneoraria',
                        'ordering': ['-contract_start_date'],
                    },
                ),
    ]

