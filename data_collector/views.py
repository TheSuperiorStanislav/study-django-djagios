from django.views.generic import TemplateView

from data_collector.models import DataPoint



# Create your views here.
class StatusView(TemplateView):
    template_name = 'status.html'

    def get_context_data(self, **kwargs):
        ctx = super(StatusView, self).get_context_data(**kwargs)

        nodes_and_data_types = DataPoint.objects.all().values('node_name', 'data_type').distinct()

        status_data_dict = dict()
        for node_and_data_type in nodes_and_data_types:
            node_name = node_and_data_type['node_name']
            data_type = node_and_data_type['data_type']

            data_point_map = status_data_dict.setdefault(node_name, dict())
            data_point_map[data_type] = DataPoint.objects.filter(
                node_name = node_name,
                data_type = data_type
                ).latest('datetime')
            print(data_point_map)
            
        ctx['status_data_dict'] = status_data_dict
        return ctx    
