# Generated by Django 2.0.6 on 2018-07-01 17:45

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0002_auto_20180701_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True)),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('closed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EventMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Hockey', 'Underwater Hockey'), ('Rugby', 'Underwater Rugby')], default='Hockey', max_length=6, verbose_name='Event Type')),
                ('grade', models.CharField(choices=[('Masters', 'Masters'), ('Elite', 'Elite'), ('Junior', 'Junior'), ('Beginner', 'Beginner'), ('Friendly', 'Friendly')], default='Friendly', max_length=8, verbose_name='Competition Level')),
                ('age_group', models.PositiveSmallIntegerField(choices=[(0, 'Open'), (19, 'U19'), (23, 'U23')], default=0, verbose_name='Age Group')),
                ('gender', models.CharField(choices=[('Co-ed', 'Co-ed Teams'), ('Gendered', 'Gendered Teams'), ('Male', 'Male Only'), ('Female', 'Female Only')], default='Co-ed', max_length=8, verbose_name='Gender Competing')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('teams', djongo.models.fields.ArrayReferenceField(on_delete=django.db.models.deletion.CASCADE, related_query_name='teams', to='teams.TeamStats')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('name', 'date')},
        ),
    ]
