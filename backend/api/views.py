import csv
import json
import io
from datetime import datetime

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from psycopg2.extras import DateRange

from api.models import EmployeeWorkHistory, Report
# from payroll.celery_task import process_records
from api.async_tasks import process_records

class PayrollFileUpload(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.data['file'].read().decode('utf-8')

        io_string = io.StringIO(file_obj)
        work_history_queue = []

        for row in csv.DictReader(io_string, delimiter=',', quotechar='|'):
            if row['date'] == 'report id':
                report_id = row['hours worked'] # The report ID is stored in this column

                if EmployeeWorkHistory.objects.filter(report_id=int(report_id)).exists():
                    return Response(
                        {'error': 'This report has already been uploaded'},
                        status=HTTP_400_BAD_REQUEST
                    )
            else:
                date = datetime.strptime(row['date'], '%d/%m/%Y')
                work_history_queue.append({'date': date,
                                           'employee_id': row['employee id'],
                                           'hours_worked': row['hours worked'],
                                           'job_group': row['job group']
                                          })

        for counter in range(len(work_history_queue)):
            key = str(report_id) + '-' + str(counter)
            # Dump all the rows in Redis and get the celery worker to ingest it later
            cache.set(key, work_history_queue[counter])

        # Calls the async celery task
        process_records(report_id, len(work_history_queue))
        return Response(status=HTTP_201_CREATED)


class GetReport(APIView):
    def get(self, request, format=None):
        value = cache.get("foo")
        if value:
            return Response({'value': 'obtained'})
        cache.set("foo", "value")
        return Response({'value': 'value not obtained. value set'})
