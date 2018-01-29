import os

import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import EmployeeWorkHistory

pytestmark = [pytest.mark.django_db]


class TestFileEndpoint(APITestCase):
    def _create_test_file(self, path):
        f = open(path, 'r')
        return {'file': f}

    def test_upload_file(self):
        filename=(os.getcwd()+ '/tests/sample_test.csv')
        data = self._create_test_file(filename)
        url = reverse('upload')

        response = self.client.post(url, data, format='multipart')
        assert response.status_code == 201
        import pdb; pdb.set_trace()
        assert EmployeeWorkHistory.objects.count() == 32
