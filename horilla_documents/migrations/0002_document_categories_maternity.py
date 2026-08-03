from django.db import migrations, models
import django.db.models.deletion
import horilla_documents.models


class Migration(migrations.Migration):
    dependencies = [("employee", "0007_historicalemployeeworkinformation_italian_fields"), ("horilla_documents", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="DocumentCategory",
            fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=200, unique=True, verbose_name="Category"))],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="DocumentSubCategory",
            fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=200, verbose_name="Sub Category")), ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subcategories", to="horilla_documents.documentcategory"))],
        ),
        migrations.CreateModel(
            name="Maternita",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("n_figlio", models.PositiveIntegerField(verbose_name="Child number")), ("nome_figlio", models.CharField(blank=True, max_length=255, null=True)),
                ("data_comunicazione", models.DateTimeField(blank=True, null=True)), ("data_prevista_parto", models.DateTimeField(blank=True, null=True)),
                ("sedia_maternita", models.CharField(blank=True, choices=[("SI", "Yes"), ("NO", "No")], max_length=10, null=True)),
                ("sostituta", models.CharField(blank=True, max_length=255, null=True)), ("id_sostituta", models.CharField(blank=True, max_length=255, null=True)),
                ("data_nascita", models.DateTimeField(blank=True, null=True)), ("data_rientro", models.DateTimeField(blank=True, null=True)),
                ("negozio", models.CharField(blank=True, max_length=255, null=True)), ("documento", models.FileField(blank=True, null=True, upload_to="documents/maternita/comunicazioni/")), ("note", models.TextField(blank=True, null=True)),
                ("employee_id", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="maternita_set", to="employee.employee")),
            ], options={"ordering": ["employee_id", "n_figlio"]},
        ),
        migrations.AddConstraint(model_name="documentsubcategory", constraint=models.UniqueConstraint(fields=("name", "category"), name="unique_document_subcategory")),
        migrations.AddConstraint(model_name="maternita", constraint=models.UniqueConstraint(fields=("employee_id", "n_figlio"), name="unique_maternity_child")),
        migrations.AddField(model_name="document", name="category", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="horilla_documents.documentcategory")),
        migrations.AddField(model_name="document", name="subcategory", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="horilla_documents.documentsubcategory")),
        migrations.AddField(model_name="document", name="document_date", field=models.DateField(blank=True, null=True, verbose_name="Document Date")),
        migrations.AddField(model_name="document", name="start_date", field=models.DateField(blank=True, null=True, verbose_name="Start Date")),
        migrations.AddField(model_name="document", name="upload_date", field=models.DateTimeField(blank=True, null=True, verbose_name="Upload Date")),
        migrations.AddField(model_name="document", name="notes", field=models.TextField(blank=True, null=True, verbose_name="Notes")),
        migrations.AddField(model_name="document", name="beneficiario", field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Beneficiary")),
        migrations.AddField(model_name="document", name="maternita", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="documents", to="horilla_documents.maternita", verbose_name="Maternity")),
        migrations.AlterField(model_name="document", name="title", field=models.CharField(blank=True, max_length=250, null=True)),
        migrations.AlterField(model_name="document", name="document", field=models.FileField(blank=True, null=True, upload_to=horilla_documents.models.document_upload_path, verbose_name="Document")),
    ]
