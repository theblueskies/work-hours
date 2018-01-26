from django.db import models

keys = ['date','hours worked','employee id', 'job group']


class WorkHistory(models.Model):
    date = models.DateField()
    employee_id = models.PositiveIntegerField()
    hours_worked = models.DecimalField(max_digits=6, decimal_places=1)
    job_group = models.CharField(max_length=1)
