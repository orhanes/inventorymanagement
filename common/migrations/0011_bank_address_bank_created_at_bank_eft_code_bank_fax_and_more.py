# Generated by Django 4.1 on 2025-05-05 23:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0010_bank_position_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="bank",
            name="address",
            field=models.TextField(blank=True, null=True, verbose_name="Adres"),
        ),
        migrations.AddField(
            model_name="bank",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Oluşturulma Tarihi",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bank",
            name="eft_code",
            field=models.CharField(
                blank=True, max_length=120, null=True, verbose_name="EFT Kodu"
            ),
        ),
        migrations.AddField(
            model_name="bank",
            name="fax",
            field=models.CharField(
                blank=True, max_length=120, null=True, verbose_name="Fax"
            ),
        ),
        migrations.AddField(
            model_name="bank",
            name="is_deleted",
            field=models.BooleanField(default=False, verbose_name="Silindi"),
        ),
        migrations.AddField(
            model_name="bank",
            name="phone",
            field=models.CharField(
                blank=True, max_length=120, null=True, verbose_name="Telefon"
            ),
        ),
        migrations.AddField(
            model_name="bank",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Güncellenme Tarihi"
            ),
        ),
        migrations.AddField(
            model_name="bank",
            name="website",
            field=models.URLField(blank=True, null=True, verbose_name="Web Sitesi"),
        ),
    ]
