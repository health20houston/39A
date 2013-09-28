from time import strftime
import csv

from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from braces.views import (
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    SuperuserRequiredMixin,
    )

from .models import LocalAward, GlobalAwardFinalist, Nomination


class Awards(TemplateView):
    template_name = 'awards/awards_list.html'

    def get_context_data(self, **kwargs):
        context = super(Awards, self).get_context_data(**kwargs)
        context['localawards'] = LocalAward.objects.all().order_by('location')
        context['nominations'] = Nomination.objects.all()
        context['globalawardfinalists'] = GlobalAwardFinalist.objects.all()
        return context

class Admin(SuperuserRequiredMixin, Awards):
    template_name = 'awards/awards_admin.html'

    def get_context_data(self, **kwargs):
        context = super(Awards, self).get_context_data(**kwargs)                  
        context['localawards'] = LocalAward.objects.all().order_by('location')
        context['nominations'] = Nomination.objects.all()
        context['globalawardfinalists'] = GlobalAwardFinalist.objects.all()
        return context

class Judging(ListView):
    queryset = GlobalAwardFinalist.objects.all().order_by('global_award_class')
    template_name = 'awards/award_judging.html'
