# Generated by Django 4.1 on 2025-04-20 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0003_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="kep_address",
            field=models.CharField(max_length=200, verbose_name="KEP Adresi"),
        ),
    ]
