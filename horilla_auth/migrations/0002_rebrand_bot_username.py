from django.db import migrations


def rebrand_bot_username(apps, schema_editor):
    HorillaUser = apps.get_model("horilla_auth", "HorillaUser")
    HorillaUser.objects.filter(username="Horilla Bot").update(username="Godzilla Bot")


class Migration(migrations.Migration):
    dependencies = [("horilla_auth", "0001_initial")]

    operations = [migrations.RunPython(rebrand_bot_username, migrations.RunPython.noop)]
