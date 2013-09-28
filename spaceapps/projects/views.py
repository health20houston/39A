from time import strftime
import csv

from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse

from awards.models import LocalAward, Nomination
from braces.views import (
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    SuperuserRequiredMixin,
    )
from challenges.models import Challenge
from profiles.models import Profile
from registration.models import Registration

from .models import Project, Team, Resource
from .forms import (
    TeamFormSet,
    ResourceFormSet,
    ProjectForm,
    )


class Detail(DetailView):
    model = Project 

    def get_context_data(self, **kwargs):
        context = {}
        context_object_name = self.get_context_object_name(self.object)
        if context_object_name:
            context[context_object_name] = self.object
        context.update(kwargs)
        context['resources'] = Resource.objects.filter(
            project=self.object
            )
        context['team'] = Team.objects.filter(
            project=self.object
            )
        context['awards'] = LocalAward.objects.filter(
            project=self.object
            )
        context['nomination'] = Nomination.objects.filter(project=self.object)
        return super(Detail, self).get_context_data(**context) 

class List(ListView):
    queryset = Project.objects.order_by('challenge').reverse()

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['user_projects'] = Team.objects.filter(
                user=self.request.user
                )
        return context

class Create(LoginRequiredMixin, CreateView):
    model = Project

    def form_valid(self, form):
        context = self.get_context_data()
        team_form = context['team_form']
        resource_form = context['resource_form']
        if (team_form.is_valid() and resource_form.is_valid()): 
            self.object = form.save()
            team_form.instance = self.object
            team_form.save(commit=False)
            for i in team_form:
                try: 
                    i.instance.project.id
                except:
                    pass
                else:
                    i.instance.approved = True
                    i.save()
            resource_form.instance = self.object
            resource_form.save()
            submitter = Team(
                project = self.object,
                user = self.request.user,
                approved = True,
                )
            submitter.save()
            return super(Create, self).form_valid(form)  
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):
        initial = super(Create, self).get_initial()
        if self.kwargs['slug']:
            initial['challenge'] = Challenge.objects.get(
                slug=self.kwargs['slug'],
                )
        return initial

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        if self.request.POST:
            context['team_form'] = TeamFormSet(
                self.request.POST, 
                prefix='team',
                )
            context['resource_form'] = ResourceFormSet(
                self.request.POST, 
                prefix='resource',
                )
        else:
            context['team_form'] = TeamFormSet(prefix='team')
            context['resource_form'] = ResourceFormSet(prefix='resource')
        return context

class Edit(LoginRequiredMixin, UpdateView):
    model = Project 
    form_class = ProjectForm

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        context = self.get_context_data()
        team_form = context['team_form']
        resource_form = context['resource_form']
        if (resource_form.is_valid()):
            self.object = form.save()
            team_form.instance = self.object
            team_form.save()
            resource_form.instance = self.object
            resource_form.save()
            return super(Edit, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        if self.request.POST:
            context['team_form'] = TeamFormSet(
                self.request.POST, 
                prefix='team',
                instance=self.object,
                )
            context['resource_form'] = ResourceFormSet(
                self.request.POST, 
                prefix='resource',
                instance=self.object,
                )
        else:
            context['team_form'] = TeamFormSet(
                instance=self.object, 
                prefix='team',
                )
            context['resource_form'] = ResourceFormSet(
                instance=self.object, 
                prefix='resource',
                )
        return context

class Delete(LoginRequiredMixin, DeleteView):
    model = Project 
    success_url = reverse_lazy('list')

class Judging(ListView):
    queryset = Project.objects.filter(finalist=True).order_by('category')
#    template_name = 'projects/project_judging.html'

class VoteBox(Detail):
    template_name = 'projects/project_votebox.html'