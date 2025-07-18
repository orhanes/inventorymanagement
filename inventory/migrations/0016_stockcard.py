# Generated by Django 4.1 on 2025-05-18 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0015_alter_stock_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="StockCard",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "lot",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="LOT"
                    ),
                ),
                (
                    "heat_no",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Döküm No"
                    ),
                ),
                (
                    "quality",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Kalite"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Cinsi"
                    ),
                ),
                ("quantity", models.IntegerField(default=1, verbose_name="Adet")),
                (
                    "length",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="Boy"
                    ),
                ),
                (
                    "std",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Standart"
                    ),
                ),
                (
                    "operator",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Operatör"
                    ),
                ),
                (
                    "package_no",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Paket No"
                    ),
                ),
                (
                    "origin",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Menşei"
                    ),
                ),
                ("date", models.DateField(blank=True, null=True, verbose_name="Tarih")),
                (
                    "serial_number",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Seri No"
                    ),
                ),
                (
                    "qr_code",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="stock_qr/",
                        verbose_name="QR Kod",
                    ),
                ),
                (
                    "barcode",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="stock_barcode/",
                        verbose_name="Barkod",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "stock",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cards",
                        to="inventory.stock",
                        verbose_name="Ürün",
                    ),
                ),
            ],
            options={
                "verbose_name": "Stok Kartı",
                "verbose_name_plural": "Stok Kartları",
            },
        ),
    ]
