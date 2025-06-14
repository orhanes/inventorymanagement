# Generated by Django 4.1 on 2024-03-07 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0033_remove_deliverybill_billno_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="deliverybill",
            name="billno",
            field=models.AutoField(default=123, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="deliverybill",
            name="delivery",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bill",
                to="transactions.delivery",
            ),
        ),
    ]
