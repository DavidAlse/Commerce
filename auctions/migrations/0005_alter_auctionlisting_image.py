# Generated by Django 3.2.7 on 2022-03-30 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20220329_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='Image',
            field=models.URLField(),
        ),
    ]