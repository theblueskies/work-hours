import csv
import json
import io
from datetime import datetime

from django.core.cache import cache
from django.http import HttpResponse
from django.template import loader
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from psycopg2.extras import DateRange

from api.async_tasks import process_records
from api.models import EmployeeWorkHistory, Report
from api.serializers import ReportSerializer


class PayrollFileUpload(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request, format=None):
        template = loader.get_template('api/upload_get.html')
        context = {}
        return HttpResponse(template.render(context, request))


    def post(self, request, format=None):
        context = {'file_already_uploaded': False}
        template = loader.get_template('api/upload_result.html')
        file_obj = request.data['file'].read().decode('utf-8')

        io_string = io.StringIO(file_obj)
        work_history_queue = []

        try:
            for row in csv.DictReader(io_string, delimiter=',', quotechar='|'):
                if row['date'] == 'report id':
                    report_id = row['hours worked'] # The report ID is stored in this column

                    if EmployeeWorkHistory.objects.filter(report_id=int(report_id)).exists():
                        context['error'] = 'File has already been uploaded'
                        return HttpResponse(template.render(context, request), status=400)
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
            process_records.delay(report_id, len(work_history_queue))
            return HttpResponse(template.render(context, request), status=201)

        except KeyError:
            context['error'] = 'Corrupt File / Keys missing in file. Please try again'
            return HttpResponse(template.render(context, request), status=400)



class GetReport(APIView):
    def get(self, request, format=None):
        template = loader.get_template('api/report.html')
        reports = Report.objects.all().order_by('pay_period')
        serialized = ReportSerializer(reports, many=True)
        context = {'headers': ['Employee ID', 'Pay Period', 'Amount Paid'],
                   'data': serialized.data}
        return HttpResponse(template.render(context, request), status=200)
