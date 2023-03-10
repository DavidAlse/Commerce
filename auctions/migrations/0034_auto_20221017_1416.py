# Generated by Django 3.2.7 on 2022-10-17 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_auto_20220911_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='Blurb',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='Price',
            field=models.FloatField(default=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='Image',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
