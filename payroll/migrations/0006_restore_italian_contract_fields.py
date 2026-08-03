# Restores the contract extensions and level history from Horilla.

import django.core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("payroll", "0005_restore_legacy_payslip_imports"),
    ]

    operations = [
        migrations.AddField(model_name="contract", name="tipo_contratto", field=models.IntegerField(blank=True, choices=[(1, "Tirocinanti"), (2, "Apprendistato"), (3, "Determinato"), (4, "Indeterminato"), (5, "cocopro"), (6, "GI GROUP"), (7, "infojobmetis"), (8, "ranstad"), (9, "voucher")], null=True, verbose_name="Tipo Contratto")),
        migrations.AddField(model_name="contract", name="lun", field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name="Lunedì")),
        migrations.AddField(model_name="contract", name="mar", field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name="Martedì")),
        migrations.AddField(model_name="contract", name="mer", field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name="Mercoledì")),
        migrations.AddField(model_name="contract", name="gio", field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name="Giovedì")),
        migrations.AddField(model_name="contract", name="ven", field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name="Venerdì")),
        migrations.AddField(model_name="contract", name="sab", field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name="Sabato")),
        migrations.AddField(model_name="contract", name="dom", field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name="Domenica")),
        migrations.AlterField(model_name="contract", name="note", field=models.TextField(blank=True, max_length=255, null=True)),
        migrations.CreateModel(
            name="ContractLevel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True, verbose_name="Created At")),
                ("is_active", models.BooleanField(default=True, verbose_name="Is Active")),
                ("badge_id", models.CharField(max_length=50, verbose_name="Badge ID")),
                ("lvl", models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name="Livello")),
                ("data_decorrenza", models.DateField(verbose_name="Data decorrenza")),
                ("note", models.TextField(blank=True, max_length=255, null=True, verbose_name="Note")),
                ("created_by", models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name="Created By")),
                ("modified_by", models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="%(class)s_modified_by", to=settings.AUTH_USER_MODEL, verbose_name="Modified By")),
                ("employee_id", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="contract_levels", to="employee.employee", verbose_name="Employee")),
            ],
            options={"verbose_name": "Livello Contratto", "verbose_name_plural": "Livelli Contratto", "db_table": "payroll_contract_lvl", "ordering": ["-data_decorrenza", "-id"]},
        ),
    ]
