# Generated by Django 4.2.19 on 2025-03-15 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("professors", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="rating",
            field=models.IntegerField(
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
            ),
        ),
    ]
