from django.shortcuts import render
from django.views.generic import View

from moeda.models import Moeda

# Create your views here.
class BaseView(View):
    def get_context_data(self, **kwargs):
        context = {
            'version': 1,
        }
        return context

class HomeView(BaseView):
    template_name = 'base/home.html'
    title = 'Página Inicial'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['title'] = 'Cotações'
        context['moedas'] = Moeda.objects.all()
        return render(request, self.template_name, context)