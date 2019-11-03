# Generated by Django 2.2.6 on 2019-11-02 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('counter_number', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('name', models.CharField(default='Ex: Nama Loket', max_length=100)),
                ('is_draft', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('number', models.IntegerField(default=0)),
                ('codec_time', models.DateField(auto_now_add=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('is_draft', models.BooleanField(default=False)),
                ('counter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counters.Counter')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
