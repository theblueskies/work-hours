from __future__ import absolute_import, unicode_literals

import os
from string import ascii_uppercase

from django.core.cache import cache
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings')

app = Celery('payroll')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


def generate_payscale():
    return dict(zip(list(ascii_uppercase), [10 * i for i in range(1, 27, 1)]))

@app.task(bind=True)
def process_records(self, report_id, count):
    from api.models import EmployeeWorkHistory, Report
    from api.util import get_date_range

    payscale = generate_payscale()

    for counter in range(count):
        key = str(report_id) + '-' + str(counter)
        item = cache.get(key)
        if item:
            work_history = EmployeeWorkHistory(date=item['date'],
                                               employee_id=item['employee_id'],
                                               hours_worked=item['hours_worked'],
                                               job_group=item['job_group'],
                                               report_id=report_id
                                              )
            work_history.save()

            date_range = get_date_range(item['date'])
            report_qs = Report.objects.filter(pay_period__contains=item['date']).filter(employee_id=item['employee_id'])

            # If there is an existing pay period for a specific user, then add the hours to that instance
            if report_qs:
                existing_hours = float(report_qs.first().hours_worked)
                existing_instance = report_qs.first()
                existing_instance.hours_worked = existing_hours + float(item['hours_worked'])
                # Calculate their cumulative pay for the pay period
                existing_instance.amount_paid += float(item['hours_worked']) * payscale[item['job_group'].upper()]
                existing_instance.save()

            # Create a new instance for the user and pay period range
            if not report_qs:
                new_report = Report(employee_id=item['employee_id'],
                                    pay_period=date_range,
                                    hours_worked=float(item['hours_worked']),
                                    amount_paid=float(item['hours_worked']) * payscale[item['job_group'].upper()])

                new_report.save()
