# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django_tables2 import SingleTableView, RequestConfig
from django.conf import settings

from . import models,tables,filters,forms


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
    

