# Generated by Django 5.1.3 on 2025-02-09 16:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nesis_app", "0003_alter_asset_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="crmuser",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
