import csv
import os
from calendar import monthrange
from datetime import datetime

from psycopg2._range import DateTimeTZRange

from api.models import  EmployeeWorkHistory


def get_date_range(date):
    month = monthrange(date.year, date.month)
    if date.day>15:
        lower_date = date.replace(day=16)
        upper_date = date.replace(day=month[1])
    else:
        lower_date = date.replace(day=month[0])
        upper_date = date.replace(day=15)

    return DateTimeTZRange(lower=lower_date, upper=upper_date, bounds='[]')
