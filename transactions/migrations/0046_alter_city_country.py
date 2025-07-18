# Generated by Django 4.1 on 2024-04-03 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0045_alter_city_options_alter_country_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="city",
            name="country",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="transactions.country"
            ),
        ),
    ]
