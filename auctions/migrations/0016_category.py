# Generated by Django 3.2.7 on 2022-07-02 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_rename_startingbid_auctionlisting_starting_bid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listings', models.ManyToManyField(related_name='category', to='auctions.auctionListing')),
            ],
        ),
    ]