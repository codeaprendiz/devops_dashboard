# Generated by Django 2.0.5 on 2018-08-15 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('splunkAutomation', '0010_auto_20180813_1217'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExecuteCommand',
            new_name='GenericIssue',
        ),
    ]