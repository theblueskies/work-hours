# Generated by Django 2.0.1 on 2018-01-29 20:46

import django.contrib.postgres.fields.ranges
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeWorkHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('employee_id', models.PositiveIntegerField()),
                ('hours_worked', models.DecimalField(decimal_places=1, max_digits=6)),
                ('job_group', models.CharField(max_length=1)),
                ('report_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.PositiveIntegerField()),
                ('pay_period', django.contrib.postgres.fields.ranges.DateTimeRangeField()),
                ('hours_worked', models.DecimalField(decimal_places=2, max_digits=8)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
    ]
