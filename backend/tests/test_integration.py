import os
from unittest.mock import patch

import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import EmployeeWorkHistory, Report

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
