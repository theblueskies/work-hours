from rest_framework.serializers import ModelSerializer

from api.models import Report


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = ('employee_id', 'pay_period', 'hours_worked', 'amount_paid')

    def to_representation(self, obj):
        instance = super(ReportSerializer, self).to_representation(obj)
        instance['lower'] = obj.pay_period.lower
        instance['upper'] = obj.pay_period.upper
        return instance
