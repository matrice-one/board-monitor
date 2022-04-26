# Generated by Django 4.0.4 on 2022-04-22 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='historic',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_surname', models.CharField(max_length=70, verbose_name='Name and surname')),
                ('origin', models.TextField(max_length=800, verbose_name='Origin')),
                ('destination', models.TextField(max_length=800, verbose_name='Destination')),
                ('status', models.TextField(max_length=800, verbose_name='Status')),
                ('signature_mode', models.TextField(max_length=800, verbose_name='Signature Mode')),
                ('company', models.TextField(max_length=800, verbose_name='Company')),
            ],
        ),
    ]