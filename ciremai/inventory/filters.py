import django_filters
from .models import Product,StockIn,UsingProduct,ReturningProduct

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        exclude = ()

class StockinFilter(django_filters.FilterSet):
    class Meta:
        model = StockIn
        exclude = ()
        
class UsingProductFilter(django_filters.FilterSet):
    class Meta:
        model = UsingProduct
        exclude = ()

class ReturningProductFilter(django_filters.FilterSet):
    class Meta:
        model = ReturningProduct
        exclude = ()