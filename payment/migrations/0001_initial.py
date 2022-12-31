# Generated by Django 4.1.4 on 2022-12-31 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("borrowing", "0002_alter_borrow_actual_return_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(choices=[(0, "Pending"), (1, "Paid")])),
                ("type", models.BooleanField(choices=[(0, "Payment"), (1, "Fine")])),
                ("session_url", models.URLField(max_length=255)),
                ("session_id", models.CharField(max_length=255)),
                ("money_to_pay", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "borrowing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="borrowing.borrow",
                    ),
                ),
            ],
        ),
    ]