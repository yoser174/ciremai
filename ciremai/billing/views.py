from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from . import models,tables,forms,filters
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django_tables2 import SingleTableView, RequestConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from .tables import TestGroupsTable,PatientsTable,SelectPatientsTable,JMTable,InsuranceTable,TestsTable,OriginTable
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,reverse,get_object_or_404
from django.core.urlresolvers import reverse_lazy
from extra_views.advanced import UpdateWithInlinesView,NamedFormsetsMixin, CreateWithInlinesView,InlineFormSet,ModelFormMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .custom.mixins import UpdateWithInlinesAndModifiedByMixin,CreateWithInlinesAndModifiedByMixin
from avatar.forms import PrimaryAvatarForm,UploadAvatarForm 
from avatar.views import _get_avatars
from avatar.models import Avatar
from avatar.signals import avatar_updated
from avatar.utils import invalidate_cache
import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.dateformat import DateFormat
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
import serial,time

from datetime import datetime, timedelta, time

from labels import Label


# ######################
# ##   Helper Views   ##
# ######################
@login_required(login_url='login_billing')
class UpdateUserProfile(LoginRequiredMixin,NamedFormsetsMixin,UpdateWithInlinesView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'auth/user_form_billing.html'
    success_url = reverse_lazy('home_billing')

def login_user(request):
    logout(request)
    next_url = request.GET.get('next','')
    
    
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        next_url = request.POST.get('next','')
        

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next_url<>'':
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect(reverse_lazy('dashboard_billing'), permanent=True)
        else:
            messages.error(request, _("Wrong username and/or password."))
            
            
    context = {'next':next_url}
    return render(request,'registration/login_billing.html',context)

@login_required(login_url='login_billing')
def show_dashboard(request):
    today = datetime.now().date()
    ordercount_today = models.Orders.objects.filter(order_date__gte=today).count()
    patientcount_today = models.Patients.objects.filter(dateofcreation__gte=today).count()
    context = {'ordercount_today': ordercount_today,'patientcount_today':patientcount_today}
    next_url = request.GET.get('next')
    if next_url:
        return HttpResponseRedirect(next_url)
    else:
        return render(request,'dashboard_billing.html',context)

@login_required(login_url='login_billing')
def AvatarChange(request,extra_context=None,next_override=None,upload_form=UploadAvatarForm,primary_form=PrimaryAvatarForm,
                 *args,**kwargs):
    if extra_context is None:
        extra_context = {}
        
    avatar, avatars = _get_avatars(request.user)
    if avatar:
        kwargs = {'initial':{'choice':avatar.id}}
    else:
        kwargs = {}
    upload_avatar_form = upload_form(user=request.user, **kwargs)
    primary_avatar_form = primary_form(request.POST or None,
                                       user=request.user,
                                       avatars=avatars, **kwargs)
    
    if request.method == 'POST':
        updated = False
        if 'choice' in request.POST and primary_avatar_form.is_valid():
            avatar = Avatar.objects.get(id=primary_avatar_form.cleaned_data['choice'])
            avatar.primary = True
            avatar.save()
            updated = True
            invalidate_cache(request.user)
            messages.success(request, _("Successfully updated your avatar."))
        if updated:
            avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
        return render(request,'auth/avatar_change_billing.html')
    
    context = {
        'avatar':avatar,
        'avatars':avatars,
        'upload_avatar_form':upload_avatar_form,
        'primary_avatar_form':primary_avatar_form,
        'next':next_override
        }
    context.update(extra_context)
    template_name = 'auth/avatar_change_billing.html'
    return render(request, template_name, context)
    
@login_required(login_url='login_billing')           
def AvatarAdd(request,extra_context=None,next_override=None,upload_form=UploadAvatarForm,*args,**kwargs):
    if extra_context is None:
        extra_context = {}
    avatar,avatars = _get_avatars(request.user)
    upload_avatar_form = upload_form(request.POST or None,
                                     request.FILES or None,
                                     user = request.user)
    if request.method == 'POST' and 'avatar' in request.FILES:
        if upload_avatar_form.is_valid():
            avatar = Avatar(user=request.user, primary=True)
            image_file = request.FILES['avatar']
            avatar.avatar.save(image_file.name,image_file)
            avatar.save()
            invalidate_cache(request.user)
            messages.success(request, _("Successfully uploaded a new avatar."))
            avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
            return render(request,'auth/avatar_change_billing.html')
    context = {
        'avatar': avatar,
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        'next': next_override,
    }
    context.update(extra_context)
    template_name = 'auth/avatar_add_billing.html'
    return render(request, template_name, context)    



# #################################
# ##         Report Views        ##
# #################################
@login_required(login_url='login_billing')
def report_tests(request):
    template = 'report/insurance.html'
    data = models.Orders.objects.values('order_items__test__name').annotate(Count('number')).order_by()
      
    if request.GET.get('order_date'):
        d_range = request.GET.get('order_date')
        #04/01/2018 - 04/30/2018
        start_date = d_range[:10]
        end_date = d_range[13:23]
 
        data = data.filter(order_date__range=[start_date,end_date] )
        
        
    filter = filters.TestsFilter(request.GET,queryset=data)
    orderstable = TestsTable(data)
    orderstable.paginate(page=request.GET.get('page', 1), per_page=10)
    
    
    RequestConfig(request).configure(orderstable)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, orderstable)
        return exporter.response('table.{}'.format(export_format))

        
    context = {'orderstable':orderstable,'filter':filter}
    return render(request,template,context)  

@login_required(login_url='login_billing')
def report_insurance(request):
    template = 'report/insurance.html'
    data = models.Orders.objects.values('insurance__name').annotate(Count('number')).order_by()
      
    if request.GET.get('order_date'):
        d_range = request.GET.get('order_date')
        #04/01/2018 - 04/30/2018
        start_date = d_range[:10]
        end_date = d_range[13:23]
 
        data = data.filter(order_date__range=[start_date,end_date] )
        
        
    filter = filters.InsuranceFilter(request.GET,queryset=data)
    orderstable = InsuranceTable(data)
    orderstable.paginate(page=request.GET.get('page', 1), per_page=10)
    
    
    RequestConfig(request).configure(orderstable)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, orderstable)
        return exporter.response('table.{}'.format(export_format))

        
    context = {'orderstable':orderstable,'filter':filter}
    return render(request,template,context)  

@login_required(login_url='login_billing')
def report_origin(request):
    template = 'report/origin.html'
    data = models.Orders.objects.values('origin__name').annotate(Count('number')).order_by()
      
    if request.GET.get('order_date'):
        d_range = request.GET.get('order_date')
        #04/01/2018 - 04/30/2018
        start_date = d_range[:10]
        end_date = d_range[13:23]
 
        data = data.filter(order_date__range=[start_date,end_date] )
        
        
    filter = filters.OriginFilter(request.GET,queryset=data)
    orderstable = OriginTable(data)
    orderstable.paginate(page=request.GET.get('page', 1), per_page=10)
    
    
    RequestConfig(request).configure(orderstable)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, orderstable)
        return exporter.response('table.{}'.format(export_format))

        
    context = {'orderstable':orderstable,'filter':filter}
    return render(request,template,context)  
    
@login_required(login_url='login_billing')
def report_jm(request):
    template = 'report/jm.html'
    data = models.Orders.objects.all()
    today = datetime.now().date()
      
    if request.GET.get('order_date'):
        d_range = request.GET.get('order_date')
        start_date = d_range[:10]
        end_date = d_range[13:23]
    else:
        start_date = today
        end_date = today
        
    data = data.filter(order_date__range=[start_date,end_date] )
    
    filter = filters.JMFilter(request.GET,queryset=data)
    orderstable = JMTable(data)
    orderstable.paginate(page=request.GET.get('page', 1), per_page=10)
    
    
    RequestConfig(request).configure(orderstable)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, orderstable)
        return exporter.response('table.{}'.format(export_format))

        
    context = {'orderstable':orderstable,'filter':filter}
    return render(request,template,context)  
    

            

# #################################
# ##   Billing Function Views  ##
# #################################
@login_required(login_url='login_billing')
def home(request):
    template = 'index_billing.html'
    org_lab_name = models.Parameters.objects.filter(name = 'ORG_LAB_NAME')
    org_lab_address = models.Parameters.objects.filter(name = 'ORG_LAB_ADDRESS')
    context = {'org_lab_name':org_lab_name,'org_lab_address':org_lab_address}
    return render(request,template,context) 

@login_required(login_url='login_billing')
def order_patient(request):
    if request.method == 'POST':  
        patient_pk = request.POST.get('patient','')  
        return redirect('create_order_from_patient',patient_pk=patient_pk)
    else:
        template = 'select/select_patient.html'
        patients = models.Patients.objects.all()
        data = models.Patients.objects.all()
        if request.GET.get('patient_id'):
            data = data.filter(patient_id__contains=request.GET.get('patient_id') )
        if request.GET.get('name'):
            data = data.filter(name__contains=request.GET.get('name') )
               
        filter = filters.PatientFilter(request.GET,queryset=patients)
        patienttable = SelectPatientsTable(data)
        patienttable.paginate(page=request.GET.get('page', 1), per_page=10)
        
        context = {'patienttable':patienttable,'filter':filter}
        return render(request,template,context)  
    
@login_required(login_url='login_billing')
def order_add_patient(request):
    if request.method == 'POST':
        form = forms.PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('create_order_from_patient',patient_pk=patient.pk)
        else:
            template = 'select/add_patient.html'
            context = {'form':form}
            return render(request,template,context)
    else:
        template = 'select/add_patient.html'
        context = {'form':forms.PatientForm}
        return render(request,template,context)
    
@login_required(login_url='login_billing')   
def create_order_from_patient(request,patient_pk):
    patient = models.Patients.objects.get(pk=patient_pk)
    order = patient.create_order()
    return redirect('order_edit', pk=order.pk)

@login_required(login_url='login_billing') 
def order_print_receipt(request,order_pk):
    order = models.Orders.objects.get(pk=order_pk)
    org_lab_name = models.Parameters.objects.filter(name = 'ORG_LAB_NAME')
    org_lab_address = models.Parameters.objects.filter(name = 'ORG_LAB_ADDRESS')
    org_lab_city = models.Parameters.objects.filter(name = 'ORG_LAB_CITY')
    template = 'billing/order_print_receipt.html'
    context = {'order':order,'org_lab_name':org_lab_name,'org_lab_address':org_lab_address,'org_lab_city':org_lab_city}
    return render(request,template,context) 

@login_required(login_url='login_billing') 
def order_print_bill(request,order_pk):
    order = models.Orders.objects.get(pk=order_pk)
    org_lab_name = models.Parameters.objects.filter(name = 'ORG_LAB_NAME')
    org_lab_address = models.Parameters.objects.filter(name = 'ORG_LAB_ADDRESS')
    org_lab_city = models.Parameters.objects.filter(name = 'ORG_LAB_CITY')
    template = 'billing/order_print_bill.html'
    context = {'order':order,'org_lab_name':org_lab_name,'org_lab_address':org_lab_address,'org_lab_city':org_lab_city}
    return render(request,template,context) 

@login_required(login_url='login_billing') 
def order_print_worklist(request,order_pk):
    order = models.Orders.objects.get(pk=order_pk)
    org_lab_name = models.Parameters.objects.filter(name = 'ORG_LAB_NAME')
    org_lab_address = models.Parameters.objects.filter(name = 'ORG_LAB_ADDRESS')
    org_lab_city = models.Parameters.objects.filter(name = 'ORG_LAB_CITY')
    template = 'billing/order_print_worklist.html'
    context = {'order':order,'org_lab_name':org_lab_name,'org_lab_address':org_lab_address,'org_lab_city':org_lab_city}
    return render(request,template,context) 

@login_required(login_url='login_billing') 
def order_print_barcode(request,order_pk):
    order = models.Orders.objects.get(pk=order_pk)
    
    MESSAGE_TAGS = {
    messages.ERROR: 'danger'
    }
    
    printer_id = request.GET.get('printer')
    
    p_label = Label()
    p_label.set_order_id(order_pk)
    p_label.set_labelprinter_id(printer_id)
    
    not_err,msg = p_label.print_label()
    
    if not_err:
        messages.info(request,msg)
    else:
        messages.error(request, 'Error when printer label [%s]' % msg,extra_tags='danger')
        
    
    
        
        
    return redirect('order_detail', pk=order.pk)

@login_required(login_url='login_billing') 
def order_send_lis(request,order_pk):
    order = models.Orders.objects.get(pk=order_pk)
    # seding to LIS here
    ts = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    filename = settings.HL7_ORDER_DIR+'order_'+order.number+'_'+ts+'.hl7'
    handle1=open(filename,'w+')
    content_hl7 = ''
    content_hl7 += 'MSH|^~\&|BIL|BIL-DREAM|CIT-INFINITY|LabPK|||ORM^O01|'+ts+'||||||ER|\r'
    content_hl7 += 'PID|||'+order.patient.patient_id+'||'+order.patient.name+'||'+order.patient.gender.ext_code+'|'+DateFormat(order.patient.dob).format('Ymd')+'|||'+order.patient.address+'^^^||\r'
    #content_hl7 += 'PV1|||||||||||'+order.doctor.ext_code+'^'+order.doctor.name+'^'+order.diagnosis.ext_code+'^'+order.diagnosis.name+'^^||\r'
    content_hl7 += 'PV1|||||||||||'+order.doctor.ext_code+'^'+order.doctor.name+'^^^^||\r'
    content_hl7 += 'ORC|NW|'+order.number+'|||'+order.origin.ext_code+'|'+order.origin.name+'|'+order.priority.ext_code+'|'+order.insurance.ext_code+'^'+order.insurance.name+'|'+ts+'||||||01||\r'
    i = 1
    for tes in order.order_items.all():
        content_hl7 += 'OBR|'+str(i)+'|||'+tes.test.ext_code+'|'+tes.test.name+'||'+ts+'||||A\r'
        i += 1
    handle1.write(content_hl7)
    handle1.close()
    messages.info(request, 'Created file HL7 ['+filename+']')
    return redirect('order_detail', pk=order.pk)
    
    
    
    

# ###################
# ##   Base Views  ##
# ###################

class PaginatedTableView(SingleTableView):
    filter_class = None

    def __init__(self, **kwargs):
        super(PaginatedTableView, self).__init__(**kwargs)
        self.object_list = self.model.objects.all()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        config = RequestConfig(request)
        table = self.table_class(self.object_list)
        config.configure(table)
        table.paginate(page=request.GET.get('page', 1), per_page=self.table_pagination)
        context[self.context_table_name] = table
        return self.render_to_response(context)

class FilteredSingleTableView(SingleTableView):
    filter_class = None

    def get_table_data(self):
        data = super(FilteredSingleTableView, self).get_table_data()
        self.filter = self.filter_class(self.request.GET, queryset=data)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(FilteredSingleTableView, self).get_context_data(**kwargs)
        context['filter'] = self.filter
        return context
    
class ListTestGroups(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.TestGroups
    permission_required = 'billing.view_testgroups'
    login_url = settings.LOGIN_URL_BILLING
    table_class = TestGroupsTable
    table_data = models.TestGroups.objects.all()
    context_table_name = 'testgroupstable'
    filter_class = filters.TestGroupFilter
    table_pagination = 10
    
class CreateTestGroup(LoginRequiredMixin,PermissionRequiredMixin,
                     NamedFormsetsMixin,CreateWithInlinesAndModifiedByMixin):
    model = models.TestGroups
    permission_required = 'billing.add_testgroups'
    login_url = settings.LOGIN_URL_BILLING
    fields = ['name','sort']
    success_url = reverse_lazy('testgroups_list')
    
class ViewTestGroup(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.TestGroups
    permission_required = 'billing.view_testgroups'
    login_url = settings.LOGIN_URL_BILLING
    
class EditTestGroup(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.TestGroups
    permission_required = 'billing.change_testgroups'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('testgroups_list')
    form_class = forms.TestGroupForm


class DeleteTestGroup(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.TestGroups
    permission_required = 'billing.delete_testgroups'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('testgroups_list')
    table_pagination = 10
    
    
class ListTests(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.Tests
    permission_required = 'billing.view_tests'
    login_url = settings.LOGIN_URL_BILLING
    table_class = tables.TestsTable
    table_data = models.Tests.objects.all()
    context_table_name = 'teststable'
    filter_class = filters.TestFilter
    table_pagination = 10
    
class CreateTests(LoginRequiredMixin,PermissionRequiredMixin,
                     NamedFormsetsMixin,CreateWithInlinesAndModifiedByMixin):
    model = models.Tests
    permission_required = 'billing.add_tests'
    login_url = settings.LOGIN_URL_BILLING
    fields = ['test_group','name','sort']
    success_url = reverse_lazy('tests_list')
    
class ViewTests(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Tests
    permission_required = 'billing.view_tests'
    login_url = settings.LOGIN_URL_BILLING
    
class EditTests(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.Tests
    permission_required = 'billing.change_tests'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('tests_list')
    form_class = forms.TestForm


class DeleteTests(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Tests
    permission_required = 'billing.delete_testgroups'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('tests_list')
    table_pagination = 10
    
    
class ListOrders(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.Orders
    permission_required = 'billing.view_orders'
    login_url = settings.LOGIN_URL_BILLING
    table_class = tables.OrdersTable
    table_data = models.Orders.objects.filter()
    context_table_name = 'orderstable'
    filter_class = filters.OrderFilter
    table_pagination = 10
    
    
class EditOrder(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.Orders
    template_name = 'billing/orders_form.html'
    permission_required = 'billing.change_orders'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('orders_list')
    form_class = forms.OrderForm2
    
    def post(self,request,*args,**kwargs):
        order = models.Orders.objects.get(number=request.POST['number'])
        form = forms.OrderForm2(request.POST,instance=order)
        if form.is_valid():
            form.save()
            tes = models.OrderTests.objects.filter(order=order)
            tes.delete()
            for test in form.cleaned_data['test_selections']:
                order_item = models.OrderTests()
                order_item.order = order
                order_item.test = test
                order_item.save()
            return redirect('order_detail', pk=order.pk)
        
        return render(request,self.template_name,{'form':form})
    
class ViewOrder(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Orders
    permission_required = 'billing.view_orders'
    login_url = settings.LOGIN_URL_BILLING
    
    def get_context_data(self, **kwargs):
        context = super(ViewOrder, self).get_context_data(**kwargs)
        context['samples'] = models.OrderSamples.objects.filter(order_id=self.kwargs['pk'])
        context['labelprinters'] = models.LabelPrinters.objects.filter(active=True)
        context['MENU_BTN_PRINT_RECEIPT'] = models.Parameters.objects.filter(name='MENU_BTN_PRINT_RECEIPT')[0]
        context['MENU_BTN_PRINT_BILL'] = models.Parameters.objects.filter(name='MENU_BTN_PRINT_BILL')[0]
        context['MENU_BTN_PRINT_BARCODE'] = models.Parameters.objects.filter(name='MENU_BTN_PRINT_BARCODE')[0]
        return context


class DeleteOrder(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Orders
    permission_required = 'billing.delete_order'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('orders_list')
    table_pagination = 10
    

class ListPatients(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.Patients
    permission_required = 'billing.view_patients'
    login_url = settings.LOGIN_URL_BILLING
    table_class = PatientsTable
    table_data = models.Patients.objects.all()
    context_table_name = 'patientstable'
    filter_class = filters.PatientFilter
    table_pagination = 10

class CreatePatient(LoginRequiredMixin,PermissionRequiredMixin,
                     NamedFormsetsMixin,CreateWithInlinesView):
    model = models.Patients
    permission_required = 'billing.add_patients'
    login_url = settings.LOGIN_URL_BILLING
    fields = ['patient_id','name','gender','dob','address',]
    success_url = reverse_lazy('patients_list')
    
class ViewPatients(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Patients
    permission_required = 'billing.view_patients'
    login_url = settings.LOGIN_URL_BILLING
    
class EditPatient(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.Patients
    permission_required = 'billing.change_patient'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('patients_list')
    form_class = forms.PatientForm


class DeletePatient(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Patients
    permission_required = 'billing.delete_patient'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('patient_list')
    table_pagination = 10
    
class Listjm(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.Orders
    permission_required = 'billing.view_patients'
    login_url = settings.LOGIN_URL_BILLING
    table_class = JMTable
    table_data = models.Orders.objects.all()
    context_table_name = 'patientstable'
    filter_class = filters.JMFilter
    table_pagination = 10