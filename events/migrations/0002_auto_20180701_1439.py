# Generated by Django 2.0.6 on 2018-07-01 18:39

from django.db import migrations
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmeta',
            name='teams',
            field=djongo.models.fields.ArrayReferenceField(on_delete=django.db.models.deletion.CASCADE, related_query_name='teams', to='teams.Team'),
        ),
    ]