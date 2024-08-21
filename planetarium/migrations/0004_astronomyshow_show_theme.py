# Generated by Django 5.1 on 2024-08-20 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planetarium", "0003_remove_astronomyshow_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="astronomyshow",
            name="show_theme",
            field=models.ManyToManyField(
                related_name="astronomy_shows", to="planetarium.showtheme"
            ),
        ),
    ]
