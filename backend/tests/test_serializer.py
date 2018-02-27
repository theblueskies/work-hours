import pytest
from collections import OrderedDict
from datetime import datetime

from api.models import Report
from api.serializers import ReportSerializer
from api.util import get_date_range


pytestmark = [pytest.mark.django_db]


def generate_report_instances(date_range):
    for i in range(2):
        instance = Report(
            employee_id=i+1,
            pay_period=date_range,
            hours_worked=25.00,
            amount_paid=100
        )
        instance.save()


def test_serializer():
    #Make a static date for test purposes
    date_range = get_date_range(datetime(2018, 2, 9, 7, 18, 33, 568876))
    generate_report_instances(date_range)

    reports = Report.objects.all()
    serializer = ReportSerializer(reports, many=True)
    expected_data = [OrderedDict([
                        ('employee_id', 1),
                        ('pay_period', '{"bounds": "[]", "lower": "2018-02-01T07:18:33.568876", "upper": "2018-02-15T07:18:33.568876"}'),
                        ('hours_worked', '25.00'),
                        ('amount_paid', '100.00'),
                        ('lower', datetime(2018, 2, 1, 7, 18, 33, 568876)),
                        ('upper', datetime(2018, 2, 15, 7, 18, 33, 568876))]),
                     OrderedDict([
                         ('employee_id', 2),
                         ('pay_period', '{"bounds": "[]", "lower": "2018-02-01T07:18:33.568876", "upper": "2018-02-15T07:18:33.568876"}'),
                         ('hours_worked', '25.00'),
                         ('amount_paid', '100.00'),
                         ('lower', datetime(2018, 2, 1, 7, 18, 33, 568876)),
                         ('upper', datetime(2018, 2, 15, 7, 18, 33, 568876))])
                     ]

    assert serializer.data == expected_data
