# Generated by Django 2.2.5 on 2019-10-28 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airbnb', '0007_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]