import django_tables2 as tables

from .models import TestGroups,Tests,Orders,Patients
from .custom.custom_columns import ModelDetailLinkColumn, IncludeColumn, CssFieldColumn, LabelIconColumn,ButtonColumn

from django.utils.translation import ugettext_lazy as _

class TestGroupsTable(tables.Table):
    #name = ModelDetailLinkColumn(accessor='name')
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
    #name = ModelDetailLinkColumn(accessor='name')
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
    #name = ModelDetailLinkColumn(accessor='name')
    edit_order = IncludeColumn(
        'includes/billing/orders_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    
    class Meta:
        model = Orders
        exclude = ('id')
        #sequence = ('number')
        fields = ('order_date','number','priority','origin','patient.patient_id','patient.name','note')
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
                            extra_class="btn-info",
                            condition = '1',
                            onclick = "location.href='{% url 'create_order_from_patient' record.pk %}'",
                            verbose_name=_(''),orderable=False)
    
    class Meta:
        model = Patients
        exclude = ('id')