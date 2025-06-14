# Generated by Django 4.1 on 2024-02-26 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0012_alter_buyer_country"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buyer",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="transactions.country",
                verbose_name="Ülke",
            ),
        ),
    ]
