import csv
import os
from datetime import datetime

from api.models import  WorkHistory


def make_records():
    filename=(os.getcwd()+ '/tests/sample_test.csv')
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['date'] == 'report id':
                continue

            date = datetime.strptime(row['date'], '%d/%m/%Y')
            print(date)
            work_history = WorkHistory(date=date,
                                       employee_id=row['employee id'],
                                       hours_worked=row['hours worked'],
                                       job_group=row['job group']
                                      )
            work_history.save()

make_records()
