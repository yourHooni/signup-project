# Generated by Django 4.1 on 2022-08-27 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("phone_certification", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PhoneCertification",
            fields=[
                ("created_at", models.DateTimeField(auto_created=True, auto_now=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("mobile_carrier_code", models.CharField(max_length=4)),
                ("phone_number", models.CharField(max_length=20)),
                ("user_name", models.CharField(max_length=4)),
                ("birth", models.CharField(max_length=6)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]