import csv
import io
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from api.models import WorkHistory

from django.core.cache import cache

class PayrollFileUpload(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.data['file'].read().decode('utf-8')

        io_string = io.StringIO(file_obj)
        for row in csv.DictReader(io_string, delimiter=',', quotechar='|'):
            if row['date'] == 'report id':
                continue

            date = datetime.strptime(row['date'], '%d/%m/%Y')
            work_history = WorkHistory(date=date,
                                       employee_id=row['employee id'],
                                       hours_worked=row['hours worked'],
                                       job_group=row['job group']
                                      )
            work_history.save()

        return Response(status=HTTP_201_CREATED)


class GetReport(APIView):
    def get(self, request, format=None):
        value = cache.get("foo")
        if value:
            return Response({'value': 'obtained'})
        cache.set("foo", "value")
        return Response({'value': 'value not obtained. value set'})
