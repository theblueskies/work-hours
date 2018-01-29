import csv
import os
from calendar import monthrange
from datetime import datetime

from psycopg2._range import DateTimeTZRange

from api.models import  EmployeeWorkHistory


def make_records():
    filename=(os.getcwd()+ '/tests/sample_test.csv')
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['date'] == 'report id':
                continue

            date = datetime.strptime(row['date'], '%d/%m/%Y')
            print(date)
            work_history = EmployeeWorkHistory(date=date,
                                       employee_id=row['employee id'],
                                       hours_worked=row['hours worked'],
                                       job_group=row['job group']
                                      )
            work_history.save()


def get_date_range(date):
    month = monthrange(date.year, date.month)
    if date.day>15:
        lower_date = date.replace(day=16)
        upper_date = date.replace(day=month[1])
    else:
        lower_date = date.replace(day=month[0])
        upper_date = date.replace(day=15)

    return DateTimeTZRange(lower=lower_date, upper=upper_date, bounds='[]')
