# Generated by Django 2.2.5 on 2019-10-14 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airbnb', '0004_scene'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='neighborhood',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='transit',
            field=models.TextField(blank=True, null=True),
        ),
    ]
