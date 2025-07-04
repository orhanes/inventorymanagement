# Generated by Django 4.1 on 2025-05-30 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0024_alter_vehicletype_options_vehicletype_is_deleted_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehiclebrand",
            name="is_deleted",
            field=models.BooleanField(default=False, verbose_name="Silindi"),
        ),
        migrations.AlterField(
            model_name="vehiclebrand",
            name="vehicle_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="common.vehicletype",
                verbose_name="Araç Türü",
            ),
        ),
    ]
