# Generated by Django 4.2.5 on 2023-10-06 13:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expenses', '0007_alter_historicallogs_title_alter_logs_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HistoricalLogs',
            new_name='HistoricalLog',
        ),
        migrations.RenameModel(
            old_name='Logs',
            new_name='Log',
        ),
        migrations.AlterModelOptions(
            name='historicallog',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical log', 'verbose_name_plural': 'historical logs'},
        ),
    ]