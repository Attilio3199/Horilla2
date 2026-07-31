import django.core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import employee.models


class Migration(migrations.Migration):
    dependencies = [("employee", "0005_alter_employee_phone_and_more")]

    operations = [
        migrations.AddField(model_name="employee", name="domicilio_address", field=models.TextField(blank=True, max_length=200, null=True)),
        migrations.AddField(model_name="employee", name="domicilio_country", field=models.CharField(blank=True, max_length=100, null=True)),
        migrations.AddField(model_name="employee", name="domicilio_state", field=models.CharField(blank=True, max_length=100, null=True)),
        migrations.AddField(model_name="employee", name="domicilio_zip", field=models.CharField(blank=True, max_length=20, null=True)),
        migrations.AddField(model_name="employee", name="domicilio_citta", field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Domicilio Città")),
        migrations.AddField(model_name="employee", name="docimicilio_provincia", field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Domicilio Provincia")),
        migrations.AddField(model_name="employee", name="residenza_country", field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Residenza Country")),
        migrations.AddField(model_name="employee", name="residenza_state", field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Residenza State")),
        migrations.AddField(model_name="employee", name="residenza_address", field=models.TextField(blank=True, max_length=200, null=True, verbose_name="Residenza Address")),
        migrations.AddField(model_name="employee", name="residenza_zip", field=models.CharField(blank=True, max_length=20, null=True, verbose_name="Residenza ZIP")),
        migrations.AddField(model_name="employee", name="residenza_citta", field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Residenza Città")),
        migrations.AddField(model_name="employee", name="residenza_provincia", field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Residenza Provincia")),
        migrations.AddField(model_name="employee", name="nascita_citta", field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Nascita Città")),
        migrations.AddField(model_name="employee", name="nascita_provincia", field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Nascita Provincia")),
        migrations.AddField(model_name="employee", name="codice_fiscale", field=models.CharField(blank=True, max_length=16, null=True, validators=[employee.models.validate_codice_fiscale], verbose_name="Codice Fiscale")),
        migrations.AddField(model_name="employee", name="categoria_protetta", field=models.BooleanField(default=False, verbose_name="Categoria Protetta")),
        migrations.AddField(model_name="employee", name="codice_paghe", field=models.CharField(blank=True, max_length=64, null=True, verbose_name="Codice Paghe")),
        migrations.AddField(model_name="employee", name="is_new_employee", field=models.BooleanField(default=True)),
        migrations.AddField(model_name="employeeworkinformation", name="work_area_type", field=models.CharField(blank=True, choices=[("SEDE", "SEDE"), ("NEGOZI", "NEGOZI")], max_length=10, null=True, verbose_name="Work Area Type")),
        migrations.AddField(model_name="employeeworkinformation", name="department_code", field=models.CharField(blank=True, max_length=30, null=True, verbose_name="Department Code")),
        migrations.AddField(model_name="employeeworkinformation", name="store_code", field=models.CharField(blank=True, max_length=30, null=True, verbose_name="Store Code")),
        migrations.AddField(model_name="employeeworkinformation", name="store_name", field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Store")),
        migrations.AddField(model_name="employeeworkinformation", name="export_payslip", field=models.BooleanField(default=False, verbose_name="Esporta Cedolino")),
        migrations.AddField(model_name="employeeworkinformation", name="mirror_payslip", field=models.BooleanField(default=False, verbose_name="Cedolino Speculare")),
        migrations.AddField(model_name="employeeworkinformation", name="premi", field=models.BooleanField(default=False, verbose_name="Premi")),
        migrations.AlterField(model_name="employeeworkinformation", name="salary_hour", field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=15, null=True, verbose_name="Salary Per Hour")),
        migrations.CreateModel(name="DutyRole", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True, null=True, verbose_name="Created At")),
            ("is_active", models.BooleanField(default=True, verbose_name="Is Active")),
            ("title", models.CharField(max_length=100, unique=True, verbose_name="Mansione")),
            ("created_by", models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name="Created By")),
            ("modified_by", models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="%(class)s_modified_by", to=settings.AUTH_USER_MODEL, verbose_name="Modified By")),
        ], options={"verbose_name": "Duty Role", "verbose_name_plural": "Duty Roles"}),
        migrations.CreateModel(name="EmployeeDutyHistory", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True, null=True, verbose_name="Created At")),
            ("is_active", models.BooleanField(default=True, verbose_name="Is Active")),
            ("start_date", models.DateField(verbose_name="DataInizioMansione")),
            ("end_date", models.DateField(blank=True, null=True, verbose_name="DataFineMansione")),
            ("created_by", models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name="Created By")),
            ("modified_by", models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="%(class)s_modified_by", to=settings.AUTH_USER_MODEL, verbose_name="Modified By")),
            ("employee_id", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="duty_histories", to="employee.employee", verbose_name="Employee")),
            ("duty_role_id", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="employee.dutyrole", verbose_name="Mansione")),
        ], options={"verbose_name": "Employee Duty History", "verbose_name_plural": "Employee Duty Histories", "ordering": ["-start_date", "-id"]}),
    ]
