from rest_framework.serializers import ModelSerializer

from api.models import Report


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = ('employee_id', 'pay_period', 'hours_worked', 'amount_paid')
