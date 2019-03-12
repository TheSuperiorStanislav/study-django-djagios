from django.forms.models import modelform_factory
from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,)
from django.urls import reverse

from data_collector.models import DataPoint, Alert



# Create your views here.
class StatusView(TemplateView):
    template_name = 'status.html'

    def does_have_alert(self, data_point, alerts):
            for alert in alerts:
                if alert.node_name and data_point.node_name != alert.node_name:
                    continue
                if alert.data_type != data_point.data_type:
                    continue
                if alert.min_value is not None and data_point.data_value < alert.min_value:
                    return True
                if alert.max_value is not None and data_point.data_value > alert.max_value:
                    return True
                return False


    def get_context_data(self, **kwargs):
        ctx = super(StatusView, self).get_context_data(**kwargs)

        alerts = Alert.objects.filter(is_active = True)

        nodes_and_data_types = DataPoint.objects.all().values('node_name', 'data_type').distinct()

        status_data_dict = dict()
        for node_and_data_type in nodes_and_data_types:
            node_name = node_and_data_type['node_name']
            data_type = node_and_data_type['data_type']

            latest_data_point = DataPoint.objects.filter(
                node_name = node_name,
                data_type = data_type
            ).latest('datetime')
            latest_data_point.has_alert = self.does_have_alert(latest_data_point, alerts)
            
            data_point_map = status_data_dict.setdefault(node_name, dict())
            data_point_map[data_type] = latest_data_point
            
        ctx['status_data_dict'] = status_data_dict
        return ctx    

        
class AlertListView(ListView):
    template_name = 'alerts_list.html'
    model = Alert

class NewAlertView(CreateView):
    template_name = 'create_or_update_alert.html'
    model = Alert
    fields = [
        'data_type',
        'min_value',
        'max_value',
        'node_name',
        'is_active',
    ]

    def get_success_url(self):
        return reverse('alerts')

class EditAlertView(UpdateView):
    template_name = 'create_or_update_alert.html'
    model = Alert
    fields = [
        'data_type',
        'min_value',
        'max_value',
        'node_name',
        'is_active',
    ]

    def get_success_url(self):
        return reverse('alerts')
    
class DeleteAlertView(DeleteView):
    template_name = 'delete_alert.html'
    model = Alert
    
    def get_success_url(self):
        return reverse('alerts')
    
class RecordDataApiView(View):
    def post(self,request, *args, **kwargs):
        if request.META.get('HTTP_AUTH_SECRET') != 'secretkey':
            return HttpResponseForbidden('Auth key incorrect')
        form_class = modelform_factory(DataPoint, fields=[
            'node_name', 
            'data_type',
            'data_value'
        ])
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()