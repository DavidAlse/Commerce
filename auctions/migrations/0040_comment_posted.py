# Generated by Django 3.2.7 on 2022-11-02 21:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0039_auto_20221026_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='posted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
