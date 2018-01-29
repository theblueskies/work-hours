from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import DateRangeField, DateTimeRangeField
from psycopg2._range import DateTimeTZRange

keys = ['date','hours worked','employee id', 'job group']


class EmployeeWorkHistory(models.Model):
    date = models.DateField()
    employee_id = models.PositiveIntegerField()
    hours_worked = models.DecimalField(max_digits=6, decimal_places=1)
    job_group = models.CharField(max_length=1)
    report_id = models.PositiveIntegerField()


class Report(models.Model):
    employee_id = models.PositiveIntegerField()
    pay_period = DateTimeRangeField()
    hours_worked = models.DecimalField(max_digits=8, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
