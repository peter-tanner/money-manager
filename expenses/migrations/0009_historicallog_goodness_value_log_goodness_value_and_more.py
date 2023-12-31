# Generated by Django 4.2.5 on 2023-10-08 09:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0008_rename_historicallogs_historicallog_rename_logs_log_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallog',
            name='goodness_value',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(-10.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AddField(
            model_name='log',
            name='goodness_value',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(-10.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AddConstraint(
            model_name='log',
            constraint=models.CheckConstraint(check=models.Q(('goodness_value__gte', -10.0), ('goodness_value__lte', 10.0)), name='log_goodness_value_range'),
        ),
    ]
