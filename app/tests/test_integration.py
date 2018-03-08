import os
from collections import OrderedDict
from datetime import datetime
from unittest.mock import patch

import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import Report
from api.serializers import ReportSerializer
from api.util import get_date_range
from tests.test_serializer import generate_report_instances


pytestmark = [pytest.mark.django_db]


class TestFileUploadEndpoint(APITestCase):
    def _create_test_file(self, path):
        f = open(path, 'r')
        return {'file': f}

    @patch('api.views.process_records')
    @patch('api.views.cache')
    def test_upload_file(self, mock_cache_set, mock_process_records):
        filename=(os.getcwd()+ '/tests/sample_test.csv')
        data = self._create_test_file(filename)
        url = reverse('upload')

        response = self.client.post(url, data, format='multipart')
        assert response.status_code == 201
        assert mock_cache_set.set.call_count == 32
        # From the sample file, report_id='43' and number of valid Work History rows are 32
        mock_process_records.delay.assert_called_once_with('43', 32)


class TestGetReport(APITestCase):
    def test_get_report(self):
        #Make a static date for test purposes
        date_range = get_date_range(datetime(2018, 2, 9, 7, 18, 33, 568876))
        generate_report_instances(date_range)
        expected_data = [OrderedDict([
                            ('employee_id', 1),
                            ('pay_period', '{"bounds": "[]", "lower": "2018-02-03T07:18:33.568876", "upper": "2018-02-15T07:18:33.568876"}'),
                            ('hours_worked', '25.00'),
                            ('amount_paid', '100.00')]),
                         OrderedDict([
                             ('employee_id', 2),
                             ('pay_period', '{"bounds": "[]", "lower": "2018-02-03T07:18:33.568876", "upper": "2018-02-15T07:18:33.568876"}'),
                             ('hours_worked', '25.00'),
                             ('amount_paid', '100.00')])
                         ]

        url = reverse('report')

        response = self.client.get(url)
        assert response.status_code == 200
        assert response.context['data'] == ReportSerializer(Report.objects.all(), many=True).data
