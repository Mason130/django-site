# Generated by Django 4.1 on 2022-08-30 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="message",
            field=models.CharField(max_length=1000),
        ),
    ]
