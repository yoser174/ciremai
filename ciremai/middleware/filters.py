import django_filters


from .models import ReceivedSamples

class ReceivedSamplesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = ReceivedSamples
        fields = ['lastmodification','supergroup']