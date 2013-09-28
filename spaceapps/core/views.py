from django.views.generic.base import TemplateView

from locations.models import Location
from projects.models import Project
from awards.models import GlobalAwardFinalist


class Home(TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):                                       
        context = super(Home, self).get_context_data(**kwargs)             
        context['locations'] = Location.objects.filter(private=False)   
        context['peoples_choice'] = Project.objects.filter(
        	hashtag__isnull=False).order_by('?') 
        context['global_winners'] = GlobalAwardFinalist.objects.filter(
        	best_in_class__isnull=False).order_by('?')
        return context

class Error(TemplateView):
    template_name = '500.html'

class Lost(TemplateView):
    template_name = '404.html'

class No(TemplateView):
    template_name = '403.html'