from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("employee", "0006_restore_italian_employee_data")]

    operations = [
        migrations.AddField(model_name="historicalemployeeworkinformation", name="work_area_type", field=models.CharField(blank=True, choices=[("SEDE", "SEDE"), ("NEGOZI", "NEGOZI")], max_length=10, null=True, verbose_name="Work Area Type")),
        migrations.AddField(model_name="historicalemployeeworkinformation", name="department_code", field=models.CharField(blank=True, max_length=30, null=True, verbose_name="Department Code")),
        migrations.AddField(model_name="historicalemployeeworkinformation", name="store_code", field=models.CharField(blank=True, max_length=30, null=True, verbose_name="Store Code")),
        migrations.AddField(model_name="historicalemployeeworkinformation", name="store_name", field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Store")),
        migrations.AddField(model_name="historicalemployeeworkinformation", name="export_payslip", field=models.BooleanField(default=False, verbose_name="Esporta Cedolino")),
        migrations.AddField(model_name="historicalemployeeworkinformation", name="mirror_payslip", field=models.BooleanField(default=False, verbose_name="Cedolino Speculare")),
        migrations.AddField(model_name="historicalemployeeworkinformation", name="premi", field=models.BooleanField(default=False, verbose_name="Premi")),
        migrations.AlterField(model_name="historicalemployeeworkinformation", name="salary_hour", field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=15, null=True, verbose_name="Salary Per Hour")),
    ]
