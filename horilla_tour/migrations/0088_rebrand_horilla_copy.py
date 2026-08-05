from django.db import migrations


def replace_brand(value):
    if not value:
        return value
    return value.replace("Horilla", "Godzilla").replace("horilla", "godzilla")


def rebrand_tour_copy(apps, schema_editor):
    Tour = apps.get_model("horilla_tour", "Tour")
    TourStep = apps.get_model("horilla_tour", "TourStep")

    for tour in Tour.objects.all().only("id", "title", "description"):
        title = replace_brand(tour.title)
        description = replace_brand(tour.description)
        if title != tour.title or description != tour.description:
            Tour.objects.filter(pk=tour.pk).update(
                title=title,
                description=description,
            )

    for step in TourStep.objects.all().only("id", "title", "description"):
        title = replace_brand(step.title)
        description = replace_brand(step.description)
        if title != step.title or description != step.description:
            TourStep.objects.filter(pk=step.pk).update(
                title=title,
                description=description,
            )


class Migration(migrations.Migration):
    dependencies = [("horilla_tour", "0087_seed_faq_view_tour")]

    operations = [migrations.RunPython(rebrand_tour_copy, migrations.RunPython.noop)]
