import csv
from time import strftime

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView

from registration.models import Registration
from projects.models import Project, Team
from awards.models import (
    LocalAward, 
    Nomination, 
    )

from .models import Location, Lead
from .forms import (
    LocationForm, 
    CheckInFormSet,
    SponsorFormSet,
    LeadFormSet,
    ResourceFormSet,
    AwardFormSet,
    NominationFormSet
    )


def get_teams(location):
    users = Registration.objects.filter(location=location)  
    teams = []
    for i in users:
        try:
            Team.objects.filter(user=i.user)
        except Team.DoesNotExist:
            pass
        else:
            for i in Team.objects.filter(user=i.user):
                teams.append(i.id)
    return teams

def get_projects(location):
    projects = []
    if get_teams(location):
        for i in get_teams(location):
            team = Team.objects.get(id=i)
            project = Project.objects.get(id=team.project.id)
            projects.append(project.id)
        return projects

class Detail(DetailView):
    model = Location

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        context['related_teams'] = Team.objects.filter(
            id__in=get_teams(context['object'])).order_by('project')
        context['awards'] = LocalAward.objects.filter(
            location=context['object']
            )
        context['nomination'] = Nomination.objects.filter(location=self.object)
        return context

class List(ListView):
    queryset = Location.objects.filter(private=False)

class Edit(UpdateView):
    model = Location 
    form_class = LocationForm

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        context = self.get_context_data()
        sponsor_form = context['sponsor_form']
        lead_form = context['lead_form']
        resource_form = context['resource_form']
        award_form = context['localaward_form']
        nomination_form = context['nomination_form']
        if (form.is_valid() and
            sponsor_form.is_valid() and
            lead_form.is_valid() and
            resource_form.is_valid() and
            award_form.is_valid() and
            nomination_form.is_valid()):
            self.object = form.save()
            sponsor_form.instance = self.object
            sponsor_form.save()
            lead_form.instance = self.object
            lead_form.save()
            resource_form.instance = self.object
            resource_form.save()
            award_form.instance = self.object
            award_form.save()
            nomination_form.instance = self.object
            nomination_form.save()
            # messages.success(self.request, 'Your form has been saved!')
            return super(Edit, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        context['leads'] = Lead.objects.filter(location=self.object)
        # initial_awards = []
        # for i in LocalAward.objects.filter(location=self.object):
        #     initial_awards.append({'title': i.title, 'project': i.project.id})
        if self.request.POST:
            context['sponsor_form'] = SponsorFormSet(
                self.request.POST,
                self.request.FILES,
                prefix='sponsor',
                instance=self.object)
            context['lead_form'] = LeadFormSet(
                self.request.POST, 
                prefix='lead',
                instance=self.object)
            context['resource_form'] = ResourceFormSet(
                self.request.POST, 
                prefix='resource',
                instance=self.object)
            context['localaward_form'] = AwardFormSet(
                self.request.POST,
                projects=get_projects(self.object),
                instance=self.object,
                prefix='localaward')
            context['nomination_form'] = NominationFormSet(
                self.request.POST,
                projects=get_projects(self.object),                                      
                instance=self.object,                                         
                prefix='nomination')
        else:
            context['sponsor_form'] = SponsorFormSet(
                instance=self.object, 
                prefix='sponsor')
            context['lead_form'] = LeadFormSet(
                instance=self.object, 
                prefix='lead')
            context['resource_form'] = ResourceFormSet(
                instance=self.object, 
                prefix='resource')
            context['localaward_form'] = AwardFormSet(
                instance=self.object,
                projects=get_projects(self.object),
                prefix='localaward')
            context['nomination_form'] = NominationFormSet(                     
                projects=get_projects(self.object),                                      
                instance=self.object,                                         
                prefix='nomination')
        return context

    def render_to_response(self, context, **response_kwargs):
        lead = Lead.objects.filter(                         
            location=self.object, lead=self.request.user)
        if lead or self.request.user.is_superuser:
            return super(Edit, self).render_to_response(context,
                **response_kwargs)
        else:
            raise PermissionDenied

class Attendees(TemplateView):

    template_name = 'locations/location_attendees.html'
    model = Location

    def get_context_data(self, **kwargs):
        context = super(Attendees, self).get_context_data(**kwargs)
        location = Location.objects.get(slug=kwargs['slug'])
        context['leads'] = Lead.objects.filter(location=location)
        context['attendees'] = Registration.objects.filter(location=location)
        lead = Lead.objects.filter(location=location, lead=self.request.user)
        if lead or self.request.user.is_superuser:
            return context
        else:
            raise PermissionDenied

class Streaming(DetailView):
    model = Location
    template_name = 'locations/location_streaming.html'

class Sponsors(ListView):
    queryset = Location.objects.filter(private=False)
    locations = Location.objects.all()
    template_name = 'locations/location_sponsors.html'

class Visualize(ListView):
    queryset = Location.objects.filter(private=False)
    template_name = 'locations/location_visualize.html'

class CSV(View):
    def get(self, request, *args, **kwargs):
        location = Location.objects.get(slug=kwargs['slug']) 
        attendees = Registration.objects.filter(location=location)
        lead = Lead.objects.filter(                                             
            location=location, lead=self.request.user)                       
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename=%s %s Attendees.csv' % (
            strftime("%Y-%m-%dT%H:%M:%SZ"), 
            location.slug))
        
        writer = csv.writer(response)
        writer.writerow([
            'Slug',
            'First Name', 
            'Last Name', 
            'Email',
            'Backgrounds',
            "City of Residence",
            "State/Province of Residence",
            "Country of Residence"])
        for i in attendees:
            try:
                profile = i.user.get_profile()
                backgrounds = ','.join(
                    [background.title 
                    for background 
                    in profile.background.all()]
                    )
                city = profile.city
                state = profile.state
                country = profile.country
            except:
                backgrounds = "Not Provided"
                city = ""
                state = ""
                country = ""
            writer.writerow([
                location.slug,
                i.user.first_name.encode('utf-8'), 
                i.user.last_name.encode('utf-8'),
                i.user.email.encode('utf-8'),
                backgrounds,
                city.encode('utf-8'),
                state.encode('utf-8'),
                country.encode('utf-8')])
        if lead or self.request.user.is_superuser:                              
            return response          
        else:                                                                   
            raise PermissionDenied

class Related(View):
    def get(self, request, *args, **kwargs):                                   
        location = Location.objects.get(slug=kwargs['slug'])
        projects = get_projects(location)
        return HttpResponse(
            Project.objects.get(id=i).get_absolute_url() for i in projects
            )



