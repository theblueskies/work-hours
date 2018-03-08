import datetime
from unittest.mock import patch

import pytest

from api.async_tasks import process_records
from api.models import EmployeeWorkHistory, Report
from api.util import get_date_range


pytestmark = [pytest.mark.django_db]


@patch('api.models.EmployeeWorkHistory')
@patch('api.async_tasks.cache')
def test_no_records_processed_for_nonexistent_redis_key(mock_cache, mock_history):
    mock_cache.get.return_value = None
    process_records('1', 2)
    assert mock_history.save.call_count == 0


@patch('api.async_tasks.cache')
def test_records_processed_with_cached_data(mock_cache):
    mock_cache.get.return_value = {'date': datetime.datetime(2018, 2, 9),
                                   'employee_id': 1,
                                   'hours_worked': 10,
                                   'job_group': 'A'
                                  }
    process_records('1', 1)
    employee_work_history = EmployeeWorkHistory.objects.first()
    report_instance = Report.objects.first()

    assert EmployeeWorkHistory.objects.count() == 1
    assert employee_work_history.date == datetime.date(year=2018, month=2, day=9)
    assert employee_work_history.employee_id == mock_cache.get.return_value['employee_id']
    assert employee_work_history.hours_worked == mock_cache.get.return_value['hours_worked']
    assert employee_work_history.job_group == mock_cache.get.return_value['job_group']

    assert Report.objects.count() == 1
    assert report_instance.employee_id == 1
    assert report_instance.amount_paid == 100
    assert report_instance.hours_worked == 10
    assert report_instance.pay_period == get_date_range(datetime.datetime(2018, 2, 9, 0, 0))
