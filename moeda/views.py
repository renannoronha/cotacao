from django.shortcuts import render
from base.views import BaseView

# Create your views here.
class MoedaView(BaseView):
    template_name = 'moeda/moeda.html'
    title = 'Moeda'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['title'] = 'Cotação'
        return render(request, self.template_name, context)