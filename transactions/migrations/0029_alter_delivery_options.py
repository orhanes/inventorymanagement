# Generated by Django 4.1 on 2024-03-07 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0028_deliverybill_alter_delivery_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="delivery",
            options={"verbose_name": "Nakliye", "verbose_name_plural": "Nakliyeler"},
        ),
    ]
