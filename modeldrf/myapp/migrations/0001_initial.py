# Generated by Django 2.0 on 2017-12-19 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RandomPicker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('result', models.IntegerField(default=None)),
                ('status', models.CharField(default='', max_length=10)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
