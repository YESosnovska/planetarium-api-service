# Generated by Django 5.1 on 2024-08-25 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("planetarium", "0005_rename_show_theme_astronomyshow_show_themes_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="showtheme",
            name="shows",
        ),
    ]
