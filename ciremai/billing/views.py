from django.shortcuts import render,HttpResponseRedirect

from django.template.response import TemplateResponse

from . import models,tables,forms,filters
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django_tables2 import SingleTableView, RequestConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .tables import TestGroupsTable,PatientsTable,SelectPatientsTable,JMTable
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


def direct_to_template(request,template,extra_context=None, **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('login')
    context=extra_context or {}
    context["params"]=kwargs
    for (key,value) in context.items():
        if callable(value):
            context[key]=value()
    return TemplateResponse(request, template, context)




# ######################
# ##   Helper Views   ##
# ######################
class UpdateUserProfile(LoginRequiredMixin,NamedFormsetsMixin,UpdateWithInlinesView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('home')

def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse_lazy('dashboard_billing'), permanent=True)
        else:
            messages.error(request, _("Wrong username and/or password."))

    return render(request,'registration/login_billing.html')

def show_dashboard(request):
    #suppliercount = models.Supplier.objects.all().count()
    #productcount = models.Product.objects.all().count()
    #context = {'suppliercount': suppliercount,'productcount':productcount}
    context = {}
    return render(request,'dashboard_billing.html',context)


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
        return render(request,'auth/avatar_change.html')
    
    context = {
        'avatar':avatar,
        'avatars':avatars,
        'upload_avatar_form':upload_avatar_form,
        'primary_avatar_form':primary_avatar_form,
        'next':next_override
        }
    context.update(extra_context)
    template_name = 'auth/avatar_change.html'
    return render(request, template_name, context)
    
            
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
            return render(request,'auth/avatar_change.html')
    context = {
        'avatar': avatar,
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        'next': next_override,
    }
    context.update(extra_context)
    template_name = 'auth/avatar_add.html'
    return render(request, template_name, context)    
            

# #################################
# ##   Billing Function Views  ##
# #################################


def report_jm(request):
    template = 'report/jm.html'
    #orders = models.Orders.objects.all()
    data = models.Orders.objects.all()
    
        
    
    if request.GET.get('order_date'):
        d_range = request.GET.get('order_date')
        #04/01/2018 - 04/30/2018
        start_date = d_range[:10]
        end_date = d_range[13:23]
        print start_date
        print end_date
        
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
    
def create_order_from_patient(request,patient_pk):
    patient = models.Patients.objects.get(pk=patient_pk)
    order = patient.create_order()
    return redirect('order_edit', pk=order.pk)

def order_print_receipt(request,order_pk):
    order = models.Orders.objects.get(pk=order_pk)
    template = 'billing/order_print_receipt.html'
    context = {'order':order}
    return render(request,template,context) 

def order_print_bill(request,order_pk):
    order = models.Orders.objects.get(pk=order_pk)
    template = 'billing/order_print_bill.html'
    context = {'order':order}
    return render(request,template,context) 

def order_print_worklist(request,order_pk):
    order = models.Orders.objects.get(pk=order_pk)
    template = 'billing/order_print_worklist.html'
    context = {'order':order}
    return render(request,template,context) 

def order_print_barcode(request,order_pk):
    order = models.Orders.objects.get(pk=order_pk)
    samples = models.OrderTests.objects.filter(order = order).values('test__specimen__id','test__specimen__suffix_code').distinct()
    print samples.query
    for sample in samples:
        #print sample
        #print order.number+sample['test__specimen__suffix_code']
        #print sample['test__specimen__id']
        models.OrderSamples.objects.get_or_create(order=order,specimen_id=sample['test__specimen__id'],sample_no=str(order.number+sample['test__specimen__suffix_code']))
    #print sample
    # Print label barcode disini
    labels = models.OrderSamples.objects.filter(order=order).values('sample_no','specimen__name')
    LF  = b'\x0A'
    """
    Form:
    [LF]N[LF]A128,16,0,0,1,1,N,"5953762"[LF]A16,104
                    ,0,0,1,1,N,""[LF]A8,48,0,0,1,1,N,"SUGENG SANTOS
                    O"[LF]A64,80,0,0,1,1,N,"1865342"[LF]A8,16,0,0,1
                    ,1,N,"Order Id :"[LF]A8,80,0,0,1,1,N,"RM :"[LF]
                    A352,80,3,0,1,1,N,"3091"[LF]A200,80,0,0,1,1,N,"
                    19/04/1969"[LF]B16,104,0,1,2,4,120,B,"5953762"[
                    LF]P2[LF][LF]
    Label:
    [LF]N[LF]A32,80,0,0,1,1,N,""[LF]A136,8,0,0,1,1,
                    N,"5953762"[LF]A368,120,3,0,1,1,N,"SERUM"[LF]A1
                    6,32,0,0,1,1,N,"SUGENG SANTOSO"[LF]A16,8,0,0,1,
                    1,N,"Order Id :"[LF]A16,56,0,0,1,1,N,"RM :"[LF]
                    A336,64,3,0,1,1,N,"3091"[LF]A208,48,0,0,1,1,N,"
                    19/04/1969"[LF]A72,48,0,0,1,1,N,"1865342"[LF]B3
                    2,80,0,1,2,4,136,B,"5953762SE"[LF]P1[LF][LF]
    """
    
    label_com = serial.Serial(port= settings.LABEL_PRINTER_PORT,baudrate=9600,
                                    timeout=10, writeTimeout=10,stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)
    for label in labels:
        #print label
        zpl_str = ''
        zpl_str = LF+'N'+LF
        zpl_str += 'A32,80,0,0,1,1,N,""'+LF
        zpl_str += 'A136,8,0,0,1,1,N,"'+order.number+'"'+LF
        zpl_str += 'A368,120,3,0,1,1,N,"'+label['specimen__name']+'"'+LF
        zpl_str += 'A16,32,0,0,1,1,N,"'+order.patient.name+'"'+LF
        zpl_str += 'A16,8,0,0,1,1,N,"Order Id :"'+LF
        zpl_str += 'A16,56,0,0,1,1,N,"RM :"'+LF
        zpl_str += 'A336,64,3,0,1,1,N,""'+LF # nomor urut
        zpl_str += 'A208,48,0,0,1,1,N,"'+order.patient.dob.strftime("%Y-%m-%d")+'"'+LF
        zpl_str += 'A72,48,0,0,1,1,N,"'+order.patient.patient_id+'"'+LF
        zpl_str += 'B32,80,0,1,2,4,136,B,"'+label['sample_no']+'"'+LF
        zpl_str += 'P1'+LF+LF
        
        #print zpl_str
        # print to COM
        
        label_com.write(zpl_str.encode())
        time.sleep(1)
        
        
    return redirect('order_detail', pk=order.pk)

def order_send_lis(request,order_pk):
    order = models.Orders.objects.get(pk=order_pk)
    # seding to LIS here
    ts = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    filename = settings.HL7_ORDER_DIR+'order_'+order.number+'_'+ts+'.hl7'
    handle1=open(filename,'w+')
    content_hl7 = ''
    content_hl7 += 'MSH|^~\&|BIL|BIL-DREAM|CIT-INFINITY|LabPK|||ORM^O01|'+ts+'||||||ER|\r'
    content_hl7 += 'PID|||'+order.patient.patient_id+'||'+order.patient.name+'||'+order.patient.gender.ext_code+'|'+DateFormat(order.patient.dob).format('Ymd')+'|||'+order.patient.address+'^^^||\r'
    content_hl7 += 'PV1|||||||||||'+order.doctor.ext_code+'^'+order.doctor.name+'^'+order.diagnosis.ext_code+'^'+order.diagnosis.name+'^^||\r'
    content_hl7 += 'ORC|NW|'+order.number+'|||'+order.origin.ext_code+'|'+order.origin.name+'|'+order.priority.ext_code+'|'+order.insurence.ext_code+'^'+order.insurence.name+'|'+ts+'||||||01||\r'
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
    table_data = models.Orders.objects.all()
    context_table_name = 'orderstable'
    filter_class = filters.OrderFilter
    table_pagination = 10
    
class EditOrder(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.Orders
    template_name = 'billing/orders_form.html'
    permission_required = 'billing.change_orders'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('orders_list')
    form_class = forms.OrderForm
    
    def post(self,request,*args,**kwargs):
        order = models.Orders.objects.get(number=request.POST['number'])
        form = forms.OrderForm(request.POST,instance=order)
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