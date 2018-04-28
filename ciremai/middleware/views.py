# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django_tables2 import SingleTableView, RequestConfig
from django.conf import settings

from . import models,tables,filters,forms
from billing.models import Orders,OrderTests,Tests


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
    
    

def show_all_orders(request):
    orders = Orders.objects.all()
    ordertable = tables.OrderResultTable(orders)
    ordertable.paginate(page=request.GET.get('page', 1), per_page=10)
    tempate = 'middleware/list_orders.html'
    context = {'ordertable':ordertable}
    return render(request,tempate,context)

def order_results(request,pk):
    if request.method == 'POST': 
        for p_tes in request.POST:
            if p_tes.startswith('test_'):
                o_order = Orders.objects.get(pk=pk)
                o_test = Tests.objects.get(pk=p_tes.split('_')[1])
                # get unit and refrange
                #m_test_unit = 
                if request.POST.get( p_tes, '')<>'':
                    o_result = models.Results(order=o_order,test=o_test,alfa_result=request.POST.get( p_tes, ''))
                    o_result.save()
                    # try delete existing result
                    try:
                        o_orderresult = models.OrderResults.objects.get(order=o_order,test=o_test)
                        o_orderresult.delete()
                    except models.OrderResults.DoesNotExist,e:
                        print 'recrod doesnot exist. skip delete'
                    # try get unit
                    s_unit = ''
                    try:
                        test_unit = models.TestParameters.objects.get(test=o_test)
                        print test_unit
                        s_unit = test_unit.unit
                    except models.TestParameters.DoesNotExist,e:
                        print 'Doesnt have unit'
                    o_orderresult = models.OrderResults.objects.get_or_create(order=o_order,test=o_test,result=o_result,validation_status=1,unit=s_unit)
    else:
        # cek if record OrderResults exist if not create it based on order
        order_tests = OrderTests.objects.filter(order_id=pk)
        #print order_tests
        for ot in order_tests:
            # try get unit
            o_tes = models.OrderResults.objects.get_or_create(order_id=pk,test_id=ot.test_id)
            s_unit = ''
            try:
                test_unit = models.TestParameters.objects.get(pk=ot.test_id)
                s_unit = test_unit.unit
                print s_unit
            except models.TestParameters.DoesNotExist,e:
                print 'Doesnt have unit'
            o_tes = models.OrderResults.objects.get(order_id=pk,test_id=ot.test_id)
            o_tes.unit = s_unit
            o_tes.save()
            
            #print ot.test_id
            #print o_tes
            # try get child
            try:
                m_tes = Tests.objects.filter(parent_id=ot.test_id)
                if m_tes.count() > 0:
                    #print ' ada child'
                    c_tes = models.OrderResults.objects.get(order_id=pk,test_id=ot.test_id)
                    #print c_tes.is_header=1
                    #print c_tes
                    c_tes.is_header=1
                    c_tes.save()
                    for child in  m_tes:
                        s_unit = ''
                        try:
                            test_unit = models.TestParameters.objects.get(pk=child.id)
                            s_unit = test_unit.unit
                            print s_unit
                        except models.TestParameters.DoesNotExist,e:
                            print 'Doesnt have unit'
                        m_child = models.OrderResults.objects.get_or_create(order_id=pk,test_id=child.id,unit=s_unit)
                        #print child.id
                        # last try for child
                        try:
                            m_child_child = Tests.objects.filter(parent_id=child.id)
                            if m_child_child.count()>0:
                                c_child = models.OrderResults.objects.get(order_id=pk,test_id=child.id)
                                c_child.is_header=1
                                c_child.save()
                                #print 'header jg'
                                
                            for child_child in m_child_child:
                                m_child_child = models.OrderResults.objects.get_or_create(order_id=pk,test_id=child_child.id)
                        except Tests.DoesNotExist,e:
                            print 'doesnt have child child'
            except Tests.DoesNotExist,e:
                print 'doesnt have child'
            
            
            #print o_tes
            

    orders = Orders.objects.get(pk=pk)
    ordertests = models.OrderResults.objects.filter(order = orders).values('test_id',
                                                                           'test__test_group__name',
                                                                           'test__name',
                                                                           'test__result_type',
                                                                           'result__alfa_result',
                                                                           'is_header',
                                                                           'unit',
                                                                           'ref_range',
                                                                           'validation_status').order_by('test__test_group__sort','test__sort')
    print ordertests
    tempate = 'middleware/order_results.html'
    context = {'orders':orders,'ordertests':ordertests}
    return render(request,tempate,context)



#####################
# Middleware function
#####################

def orders(request):
    template = 'middleware/list_orders.html'
    #context = {'form':forms.PatientForm}
    context = {}
    return render(request,template,context)


# ###################
# ##   Base Views  ##
# ###################

class ListReceivedSample(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.ReceivedSamples
    permission_required = 'billing.view_orders'
    login_url = settings.LOGIN_URL_BILLING
    table_class = tables.ReceivedSamplesTable
    table_data = models.ReceivedSamples.objects.all()
    context_table_name = 'receivedsamplestable'
    filter_class = filters.ReceivedSamplesFilter
    table_pagination = 10
    
class ListResults(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.Orders
    permission_required = 'billing.view_orders'
    login_url = settings.LOGIN_URL_BILLING
    table_class = tables.OrderResultTable
    table_data = models.Orders.objects.all()
    context_table_name = 'orderstable'
    filter_class = filters.OrderFilter
    table_pagination = 10
    

