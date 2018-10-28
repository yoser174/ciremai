import django_tables2 as tables
from pprint import pprint

from .models import TestGroups,Tests,Orders,Patients,Doctors
from .custom.custom_columns import ModelDetailLinkColumn, IncludeColumn, CssFieldColumn, LabelIconColumn,ButtonColumn
from django.contrib.humanize.templatetags.humanize import intcomma

from django.utils.translation import ugettext_lazy as _


class ColumnWithThausandSeparator(tables.Column):
    def render(self,value):
        return intcomma(value)

class TestGroupsTable(tables.Table):
    edit_test_group = IncludeColumn(
        'includes/testgroups_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    
    class Meta:
        model = TestGroups
        exclude = ('id')
        sequence = ('name', 'sort')
        order_by = ('sort',)
        
class TestsTable(tables.Table):
    edit_test = IncludeColumn(
        'includes/tests_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    
    class Meta:
        model = Tests
        exclude = ('id')
        sequence = ('name', 'sort')
        order_by = ('sort',)
        
class OrdersTable(tables.Table):
    get_total_price = tables.Column(verbose_name= _('Price' ))
    edit_order = IncludeColumn(
        'includes/billing/orders_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    
    def render_get_total_price(self, value):
        return intcomma(value)
        
    
    class Meta:
        model = Orders
        exclude = ('id')
        #sequence = ('number')
        fields = ('order_date','status','number','priority','origin','patient.patient_id','patient.name','get_total_price')
        order_by = ('-number',)
        
        
        
        
class PatientsTable(tables.Table):
    edit_order = IncludeColumn(
        'includes/billing/patient_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    
    class Meta:
        model = Patients
        fields = ('patient_id','name','gender','dob','address',)
        exclude = ('id')
        
        
class SelectPatientsTable(tables.Table):
    use_product = ButtonColumn(gl_icon="external-link",
                            extra_class="btn-primary",
                            condition = '1',
                            onclick = "location.href='{% url 'create_order_from_patient' record.pk %}'",
                            verbose_name=_(''),orderable=False)
    
    class Meta:
        model = Patients
        fields = ('patient_id','name','gender','dob','address',)
        exclude = ('id')
        

class DoctorsTable(tables.Table):
    edit_order = IncludeColumn(
        'includes/billing/doctor_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    
    class Meta:
        model = Doctors
        fields = ('name','address',)
        exclude = ('id')
        



class JMTable(tables.Table):
    export_formats = ['csv', 'xls']
    ColumnWithThausandSeparator('get_sub_total_price_tariff')
    ColumnWithThausandSeparator('get_sub_total_price_service')
    
    class Meta:
        model = Orders
        fields = ('order_date','number','priority','patient','insurance','origin','get_test_str','doctor','get_sub_total_price_tariff','get_sub_total_price_service',)
        exclude = ('id')
        template = 'django_tables2/bootstrap.html'
 
class OriginTable(tables.Table):
    export_formats = ['csv', 'xls']
    class Meta:
        model = Orders
        fields = ('origin__name','number__count',)
        exclude = ('id')
        template = 'django_tables2/bootstrap.html'
               
class InsuranceTable(tables.Table):
    export_formats = ['csv', 'xls']
    class Meta:
        model = Orders
        fields = ('insurance__name','number__count',)
        exclude = ('id')
        template = 'django_tables2/bootstrap.html'
        
class TestsTable(tables.Table):
    export_formats = ['csv', 'xls']
    class Meta:
        model = Orders
        fields = ('order_items__test__name','number__count',)
        exclude = ('id')
        template = 'django_tables2/bootstrap.html'
        
        