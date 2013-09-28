import csv
from time import strftime

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse

from braces.views import (
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    SuperuserRequiredMixin,
    )
from projects.models import Project

from .models import (
    Challenge, 
    ChallengeSponsor, 
    ChallengeAuthor, 
    ChallengeDataset,
    )
from .forms import (
    ChallengeForm, 
    SponsorFormSet,
    AuthorFormSet,
    DataFormSet,
    )


class Detail(DetailView):
    queryset = Challenge.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = {}
        context_object_name = self.get_context_object_name(self.object)
        if context_object_name:
            context[context_object_name] = self.object
        context.update(kwargs)
        context['related_projects'] = Project.objects.filter(
            challenge=self.object
            ) 
        context['sponsors'] = ChallengeSponsor.objects.filter(
            challenge=self.object
            )
        context['authors'] = ChallengeAuthor.objects.filter(
            challenge=self.object
            )
        context['data'] = ChallengeDataset.objects.filter(
            challenge=self.object
            )
        if self.request.user.is_authenticated():
            authors = ChallengeAuthor.objects.filter(
                challenge=self.object, author=self.request.user
                )
            if authors or self.request.user.has_perm(
                'challenges.change_challenge'):     
                context['is_privileged'] = True
        return super(Detail, self).get_context_data(**context)

class List(ListView):
    queryset = Challenge.objects.filter(published=True)

class Create(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Challenge
    form_class = ChallengeForm
    permission_required = 'challenges.add_challenge'

    def form_valid(self, form):
        context = self.get_context_data()
        sponsor_form = context['sponsor_form']
        author_form = context['author_form']
        data_form = context['data_form']
        if (sponsor_form.is_valid() and 
            author_form.is_valid() and 
            data_form.is_valid()):
            self.object = form.save()
            sponsor_form.instance = self.object
            sponsor_form.save()
            author_form.instance = self.object
            author_form.save()
            data_form.instance = self.object
            data_form.save()
            return super(Create, self).form_valid(form)  
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        if self.request.POST:
            context['sponsor_form'] = SponsorFormSet(
                self.request.POST, 
                prefix='sponsor',
                )
            context['author_form'] = AuthorFormSet(
                self.request.POST, 
                prefix='author',
                )
            context['data_form'] = DataFormSet(
                self.request.POST, 
                prefix='data',
                )
        else:
            context['sponsor_form'] = SponsorFormSet(prefix='sponsor')
            context['author_form'] = AuthorFormSet(prefix='author')
            context['data_form'] = DataFormSet(prefix='data')
        return context

class Edit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Challenge
    form_class = ChallengeForm
    permission_required = 'challenges.change_challenge'

    def dispatch(self, request, *args, **kwargs):
        authors = ChallengeAuthor.objects.filter(
            challenge__slug=kwargs['slug'], author=request.user)
        if authors or request.user.has_perm('challenges.change_challenge'):
            return super(Edit, self).dispatch(
                request, 
                *args, 
                **kwargs
                )
        else:
            raise PermissionDenied

    def form_valid(self, form):
        """
        If the forms are valid, save the associated models.
        """
        context = self.get_context_data()
        sponsor_form = context['sponsor_form']
        author_form = context['author_form']                                    
        data_form = context['data_form']                                        
        if (sponsor_form.is_valid() and                                         
            author_form.is_valid() and                                          
            data_form.is_valid()):                                              
            self.object = form.save()                                       
            sponsor_form.instance = self.object                             
            sponsor_form.save()                                             
            author_form.instance = self.object                              
            author_form.save()                                              
            data_form.instance = self.object                                
            data_form.save()
            return super(Edit, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        if self.request.POST:
            context['sponsor_form'] = SponsorFormSet(
                self.request.POST,
                prefix='sponsor',
                instance=self.object,
                )
            context['author_form'] = AuthorFormSet(
                self.request.POST, 
                prefix='author',
                instance=self.object,
                )
            context['data_form'] = DataFormSet(
                self.request.POST, 
                prefix='data',
                instance=self.object,
                )
        else:
            context['sponsor_form'] = SponsorFormSet(
                instance=self.object, 
                prefix='sponsor',
                )
            context['author_form'] = AuthorFormSet(
                instance=self.object, 
                prefix='author',
                )
            context['data_form'] = DataFormSet(
                instance=self.object, 
                prefix='data',
                )
        return context

class Delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Challenge
    success_url = reverse_lazy('list_challenges')
    permission_required = 'challenges.delete_challenge'

    def dispatch(self, request, *args, **kwargs):                               
        authors = ChallengeAuthor.objects.filter(                               
            challenge__slug=kwargs['slug'], author=request.user)                
        if authors or request.user.has_perm('challenges.delete_challenge'):     
            return super(Delete, self).dispatch(                         
                request,                                                        
                *args,                                                          
                **kwargs
                )                                                       
        else:                                                                   
            raise PermissionDenied