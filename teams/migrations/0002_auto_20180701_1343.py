# Generated by Django 2.0.6 on 2018-07-01 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamstats',
            options={'ordering': ['loses', '-wins', '-draws', '-goals']},
        ),
    ]
