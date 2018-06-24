import django_filters
from .models import Product,StockIn,UsingProduct,ReturningProduct

from django_select2.forms import Select2Widget

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        exclude = ()

class StockinFilter(django_filters.FilterSet):
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=Select2Widget
    )
    class Meta:
        model = StockIn
        fields = ['date_in', 'product', ]
        exclude = ()
        
class UsingProductFilter(django_filters.FilterSet):
    class Meta:
        model = UsingProduct
        exclude = ()

class ReturningProductFilter(django_filters.FilterSet):
    class Meta:
        model = ReturningProduct
        exclude = ()