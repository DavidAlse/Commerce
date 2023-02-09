# Generated by Django 3.2.7 on 2022-07-17 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_remove_bid_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='auction', to='auctions.auctionlisting'),
            preserve_default=False,
        ),
    ]