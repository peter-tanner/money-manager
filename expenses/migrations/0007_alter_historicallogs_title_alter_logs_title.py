# Generated by Django 4.2.5 on 2023-10-06 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0006_logs_historicallogs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicallogs',
            name='title',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='logs',
            name='title',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
