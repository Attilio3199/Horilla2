# Generated manually to restore legacy payroll controls

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("payroll", "0003_alter_payrollsettings_position")]

    operations = [
        migrations.CreateModel(
                    name='PayslipControlloRegola',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('direzione', models.CharField(choices=[('APP_TO_CED', 'App (turni) -> Cedolino'), ('CED_TO_APP', 'Cedolino -> App (turni)')], max_length=20, verbose_name='Direzione controllo')),
                        ('sorgente_valore', models.CharField(help_text='Valore sorgente: CODICE_TIPO_ORARIO (APP_TO_CED) oppure cod_voce (CED_TO_APP).', max_length=100, verbose_name='Sorgente')),
                        ('modalita', models.CharField(choices=[('ANY', 'Any (almeno una destinazione)'), ('SUM', 'Somma (somma destinazioni)')], default='ANY', max_length=10, verbose_name='Modalita')),
                        ('no_somma_stesso_giorno', models.BooleanField(default=False, help_text='Se attivo, nel controllo ANY non consente copertura tramite somma di piu destinazioni.', verbose_name='No somma stesso giorno')),
                        ('attivo', models.BooleanField(default=True, verbose_name='Attiva')),
                        ('priorita', models.IntegerField(default=100, verbose_name='Priorita')),
                        ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='Note')),
                    ],
                    options={
                        'verbose_name': 'Regola controllo cedolini',
                        'verbose_name_plural': 'Regole controllo cedolini',
                        'db_table': 'payslip_controllo_regole',
                        'ordering': ['direzione', 'priorita', 'sorgente_valore'],
                    },
                ),
        migrations.CreateModel(
                    name='PayslipDizionario',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('codice_tipo_orario', models.CharField(help_text='Valore del campo CODICE_TIPO_ORARIO in orari.turni_creati', max_length=100, verbose_name='CODICE_TIPO_ORARIO (turni_creati)')),
                        ('cod_voce', models.CharField(blank=True, help_text='Valore del campo cod_voce in payslip_presenze da confrontare (4 cifre con zero padding, es. 0300)', max_length=4, null=True, verbose_name='Codice Voce (payslip_presenze)')),
                        ('tipo_ora', models.CharField(choices=[('consuntivo', 'Consuntivo (Ora_Cons_Inizio / Ora_Cons_Fine)'), ('previsionale', 'Previsionale (Ora_Prev_Inizio / Ora_Prev_Fine)')], default='consuntivo', help_text='Indica se usare gli orari consuntivi o preventivi per il calcolo', max_length=20, verbose_name='Tipo orario da usare')),
                        ('attivo', models.BooleanField(default=False, help_text='Se disabilitato, questa voce viene ignorata nel controllo incrociato', verbose_name='Verifica attiva')),
                        ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='Note')),
                    ],
                    options={
                        'verbose_name': 'Dizionario Presenze ↔ Orari',
                        'verbose_name_plural': 'Dizionario Presenze ↔ Orari',
                        'db_table': 'payslip_dizionario',
                        'ordering': ['codice_tipo_orario'],
                    },
                ),
        migrations.CreateModel(
                    name='PayslipPresenze',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('dl', models.CharField(blank=True, max_length=20, null=True)),
                        ('fil', models.CharField(blank=True, max_length=20, null=True)),
                        ('cc', models.CharField(blank=True, max_length=20, null=True)),
                        ('rag_soc', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ragione Sociale')),
                        ('matricola', models.CharField(blank=True, max_length=20, null=True)),
                        ('lavoratore', models.CharField(blank=True, max_length=100, null=True)),
                        ('qp', models.CharField(blank=True, max_length=10, null=True)),
                        ('data_ass', models.DateField(blank=True, null=True, verbose_name='Data Assunzione')),
                        ('livello', models.CharField(blank=True, max_length=10, null=True)),
                        ('desc_liv', models.CharField(blank=True, max_length=50, null=True, verbose_name='Descrizione Livello')),
                        ('pt', models.CharField(blank=True, max_length=10, null=True)),
                        ('perc_pt', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='% PT')),
                        ('perc_turn', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='% Turn')),
                        ('mese', models.IntegerField(verbose_name='Mese')),
                        ('anno', models.IntegerField(verbose_name='Anno')),
                        ('matricola_mese_anno', models.CharField(blank=True, help_text='Concatenazione di matricola_mese_anno', max_length=50, null=True, verbose_name='Matricola_Mese_Anno')),
                        ('cod_voce', models.IntegerField(blank=True, null=True, verbose_name='Codice Voce')),
                        ('desc_voce', models.CharField(blank=True, max_length=100, null=True, verbose_name='Descrizione Voce')),
                        ('aliq_voce', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='Aliquota Voce')),
                        ('day_1', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_2', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_3', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_4', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_5', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_6', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_7', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_8', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_9', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_10', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_11', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_12', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_13', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_14', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_15', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_16', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_17', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_18', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_19', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_20', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_21', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_22', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_23', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_24', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_25', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_26', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_27', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_28', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_29', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_30', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('day_31', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                        ('ore_tot', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True, verbose_name='Ore Totali')),
                        ('gg_tot', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='Giorni Totali')),
                        ('periodo_elab', models.CharField(blank=True, max_length=20, null=True, verbose_name='Periodo Elaborazione')),
                        ('cod_dip', models.CharField(blank=True, max_length=50, null=True, verbose_name='Codice Dipendente')),
                    ],
                    options={
                        'verbose_name': 'Payslip Presenze',
                        'verbose_name_plural': 'Payslip Presenze',
                        'db_table': 'payslip_presenze',
                    },
                ),
        migrations.CreateModel(
                    name='PayslipControlloRegolaDestinazione',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('destinazione_valore', models.CharField(max_length=100, verbose_name='Destinazione')),
                        ('attivo', models.BooleanField(default=True, verbose_name='Attiva')),
                        ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='Note')),
                        ('regola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinazioni', to='payroll.payslipcontrolloregola', verbose_name='Regola')),
                    ],
                    options={
                        'verbose_name': 'Destinazione regola controllo',
                        'verbose_name_plural': 'Destinazioni regole controllo',
                        'db_table': 'payslip_controllo_regole_destinazioni',
                        'ordering': ['regola_id', 'destinazione_valore'],
                    },
                ),
        migrations.AddConstraint(
                    model_name='payslipcontrolloregola',
                    constraint=models.UniqueConstraint(fields=('direzione', 'sorgente_valore'), name='uniq_controllo_regola_direzione_sorgente'),
                ),
    ]

