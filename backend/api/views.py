import csv
import io
from datetime import datetime

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from psycopg2.extras import DateRange

from api.models import EmployeeWorkHistory, Report
from api.util import get_date_range


class PayrollFileUpload(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.data['file'].read().decode('utf-8')

        io_string = io.StringIO(file_obj)
        work_history_queue = []
        for row in csv.DictReader(io_string, delimiter=',', quotechar='|'):
            if row['date'] == 'report id':
                report_id = row['hours worked'] # The report ID is stored in this column
                # import pdb; pdb.set_trace()
                if EmployeeWorkHistory.objects.filter(report_id=report_id).first():
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

        self.process_records(work_history_queue, report_id=report_id)

        return Response(status=HTTP_201_CREATED)

    def process_records(self, work_history_queue, report_id):
        for row in work_history_queue:
            work_history = EmployeeWorkHistory(date=row['date'],
                                               employee_id=row['employee_id'],
                                               hours_worked=row['hours_worked'],
                                               job_group=row['job_group'],
                                               report_id=report_id
                                              )
            work_history.save()
            date_range = get_date_range(row['date'])
            report_qs = Report.objects.filter(pay_period__contains=row['date']).filter(id=row['employee_id'])

            if report_qs:
                existing_hours = float(report_qs.first().hours_worked)
                rp = Report(employee_id=row['employee_id'],
                            pay_period=date_range,
                            hours_worked=existing_hours + float(row['hours_worked']),
                            amount_paid=123.45)

            if not report_qs:
                rp = Report(employee_id=row['employee_id'],
                            pay_period=date_range,
                            hours_worked=float(row['hours_worked']),
                            amount_paid=123.45)

            rp.save()










class GetReport(APIView):
    def get(self, request, format=None):
        value = cache.get("foo")
        if value:
            return Response({'value': 'obtained'})
        cache.set("foo", "value")
        return Response({'value': 'value not obtained. value set'})
