from django.shortcuts import render
from django.views.generic import View

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
        return render(request, self.template_name, context)