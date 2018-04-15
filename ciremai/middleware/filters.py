import django_filters


from .models import ReceivedSamples
from billing.models import Orders

class ReceivedSamplesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = ReceivedSamples
        fields = ['lastmodification','supergroup']
        
class OrderFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(lookup_expr='icontains')
    patient__patient_id = django_filters.CharFilter(lookup_expr='icontains')
    patient__name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Orders
        fields = ['number','patient__patient_id','patient__name']