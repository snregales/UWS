# Generated by Django 2.0.6 on 2018-07-03 05:26

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import scheduler.models.matches
import scheduler.models.teams
import teams.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0002_auto_20180701_1439'),
        ('referees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixedEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Foul',
            fields=[
                ('code', models.SlugField(max_length=2, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1)),
                ('concluded', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-concluded'],
            },
        ),
        migrations.CreateModel(
            name='GroupMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teams', djongo.models.fields.ArrayModelField(model_container=teams.models.ParticipantStats, model_form_class=teams.models.ParticipantStatsForm)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scheduler.Group')),
            ],
            options={
                'ordering': ['group'],
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('scheduled', models.DateTimeField()),
                ('event', models.CharField(blank=True, max_length=255, null=True)),
                ('group', models.CharField(max_length=2, null=True)),
                ('playoff', models.BooleanField(default=False)),
                ('winner', models.CharField(max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['event', 'group', 'scheduled'],
            },
        ),
        migrations.CreateModel(
            name='MatchMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateTimeField(null=True)),
                ('teams', djongo.models.fields.ArrayModelField(model_container=scheduler.models.teams.Competitor, model_form_class=scheduler.models.teams.CompetitorForm)),
                ('time_line', djongo.models.fields.ArrayModelField(model_container=scheduler.models.matches.TimeLine, model_form_class=scheduler.models.matches.TimeLineForm)),
                ('final', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('match', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scheduler.Match')),
                ('referee', models.ForeignKey(limit_choices_to={'certified': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='referees.Referee')),
            ],
            options={
                'ordering': ['match', '-started', 'final'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='match',
            unique_together={('scheduled', 'event', 'group')},
        ),
        migrations.AddField(
            model_name='groupmeta',
            name='matches',
            field=djongo.models.fields.ArrayReferenceField(on_delete=django.db.models.deletion.CASCADE, related_query_name='matches', to='scheduler.Match'),
        ),
        migrations.AddField(
            model_name='fixedevent',
            name='groups',
            field=djongo.models.fields.ArrayReferenceField(on_delete=django.db.models.deletion.CASCADE, to='scheduler.Group'),
        ),
        migrations.AddIndex(
            model_name='matchmeta',
            index=models.Index(fields=['-updated', 'timestamp'], name='last_modified'),
        ),
    ]
