# Generated by Django 5.0.2 on 2024-03-21 18:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('type', models.IntegerField(choices=[(1, 'fundacja'), (2, 'organizacja pozarządowa'), (3, 'zbiórka lokalna')], default=1)),
                ('category', models.ManyToManyField(to='App.category')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('address', models.CharField(max_length=256)),
                ('phone_number', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.TextField()),
                ('categories', models.ManyToManyField(to='App.category')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.institution')),
            ],
        ),
    ]
