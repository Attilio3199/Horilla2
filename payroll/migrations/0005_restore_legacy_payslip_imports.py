# Generated manually to restore legacy payroll import tables

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("payroll", "0004_restore_legacy_payslip_controls")]

    operations = [
        migrations.CreateModel(
                    name='PayslipImporti',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('mese', models.IntegerField(verbose_name='Mese')),
                        ('anno', models.IntegerField(verbose_name='Anno')),
                        ('neg', models.CharField(blank=True, max_length=50, null=True, verbose_name='NEG')),
                        ('badge_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='Badge ID')),
                        ('matricola', models.CharField(blank=True, max_length=20, null=True, verbose_name='Matricola')),
                        ('importo', models.DecimalField(blank=True, decimal_places=4, max_digits=15, null=True, verbose_name='Importo')),
                    ],
                    options={
                        'verbose_name': 'Premio importato',
                        'verbose_name_plural': 'Premi importati',
                        'db_table': 'payslip_importi',
                        'ordering': ['anno', 'mese', 'badge_id'],
                    },
                ),
        migrations.CreateModel(
                    name='PayslipCorpo',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('mese', models.IntegerField(verbose_name='Mese')),
                        ('anno', models.IntegerField(verbose_name='Anno')),
                        ('codice_dl', models.CharField(max_length=20, verbose_name='Codice DL')),
                        ('denominazione', models.CharField(max_length=100, verbose_name='Denominazione')),
                        ('filiale', models.CharField(blank=True, max_length=20, null=True, verbose_name='Filiale')),
                        ('c_costo', models.IntegerField(blank=True, null=True, verbose_name='C.Costo')),
                        ('reparto', models.IntegerField(blank=True, null=True, verbose_name='Reparto')),
                        ('matricola', models.CharField(max_length=20, verbose_name='Matricola')),
                        ('cognome', models.CharField(max_length=100, verbose_name='Cognome')),
                        ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                        ('qp', models.CharField(blank=True, max_length=10, null=True, verbose_name='QP')),
                        ('assunzione', models.DateField(blank=True, null=True, verbose_name='Data assunzione')),
                        ('anzianita', models.DateField(blank=True, null=True, verbose_name='Data anzianità')),
                        ('cod_pos', models.IntegerField(blank=True, null=True, verbose_name='Cod. posizione')),
                        ('data_pos', models.DateField(blank=True, null=True, verbose_name='Data posizione')),
                        ('liq', models.CharField(blank=True, max_length=20, null=True, verbose_name='Liquidazione')),
                        ('cod_voce', models.IntegerField(verbose_name='Cod. voce')),
                        ('descrizione_voce', models.CharField(max_length=100, verbose_name='Descrizione voce')),
                        ('aliq_perc_lav', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='Aliq./%lav.')),
                        ('unita', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='h/g/n /%d.l.')),
                        ('dato_base_imponibile', models.DecimalField(blank=True, decimal_places=4, max_digits=15, null=True, verbose_name='Dato base/imponibile')),
                        ('importo_ctr_lav', models.DecimalField(blank=True, decimal_places=4, max_digits=15, null=True, verbose_name='Importo/ctr lav')),
                        ('db_tfr', models.DecimalField(blank=True, decimal_places=4, max_digits=15, null=True, verbose_name='D.B. TFR')),
                        ('imp_tfr_ctr_dl', models.DecimalField(blank=True, decimal_places=4, max_digits=15, null=True, verbose_name='Imp. TFR/ctr.dl')),
                        ('payslip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='corpo_rows', to='payroll.payslip', verbose_name='Busta paga')),
                    ],
                    options={
                        'verbose_name': 'Corpo busta paga',
                        'verbose_name_plural': 'Corpo buste paga',
                        'db_table': 'payslip_corpo',
                        'ordering': ['anno', 'mese', 'matricola', 'cod_voce'],
                    },
                ),
    ]

