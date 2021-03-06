# Generated by Django 2.0.1 on 2018-06-21 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Team Name')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TeamStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', models.PositiveSmallIntegerField(default=0, verbose_name='Goals')),
                ('wins', models.PositiveSmallIntegerField(default=0, verbose_name='Wins')),
                ('loses', models.PositiveSmallIntegerField(default=0, verbose_name='Loses')),
                ('draws', models.PositiveSmallIntegerField(default=0, verbose_name='Draws')),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='teams.Team')),
            ],
            options={
                'ordering': ['loses', '-wins', '-draws'],
            },
        ),
    ]
