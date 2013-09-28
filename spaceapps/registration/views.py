from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.views import redirect_to_login

from braces.views import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuperuserRequiredMixin,
    )
from locations.models import Location

from .models import Registration
from .forms import RegistrationForm


class List(ListView):
    queryset = Location.objects.filter(private=False)
    template_name = 'registration/registration_list.html'

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        try:
            self.request.session['location']
        except:
            pass
        else:
            context['highlight'] = Location.objects.filter(
                slug=self.request.session['location'],
                )
        return context

class Create(LoginRequiredMixin, CreateView):
    model = Registration
    success_url = reverse_lazy('base')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                Registration.objects.get(user=request.user)
            except Registration.DoesNotExist:
                location = get_object_or_404(
                    Location,
                    slug=kwargs['slug']
                    )
                if location.is_full() or not location.open:
                    return render(
                        request,
                        'registration/registration_full.html',
                        { "object": location }
                        )
                else:
                    object = Registration(
                        user = request.user,
                        location = Location.objects.get(slug=kwargs['slug'])
                        )
                    object.save()

                    confirmation = get_template(
                        'registration/registration_email_confirmation.html')
                    context = Context({
                        'user': request.user,
                        'location': object.location 
                        })
                    email = EmailMessage('Registration Confirmation',
                        confirmation.render(context),
                        'noreply <noreply@.org>',
                        [request.user.email]
                        )
                    email.send()

                    try:
                        request.session['location']
                    except:
                        pass
                    else:
                        del request.session['location']
                    return render(
                        request,
                        'registration/registration_detail.html',
                        {"already_registered": True,
                        "object": object }
                        )
            else:
                registration = Registration.objects.get(user=request.user)
                return render(
                    request,
                    'registration/registration_detail.html',
                    {"already_registered": True,
                    "object": registration })
        else:
            request.session['location'] = kwargs['slug']
            return redirect_to_login(request.get_full_path())

class Edit(LoginRequiredMixin, UpdateView):
    model = Registration
    form_class = RegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                Registration.objects.get(user=request.user)
            except Registration.DoesNotExist:
                return redirect('/register')
            else:
                return super(Edit, self).dispatch(
                    request,
                    *args,
                    **kwargs)
        else:
            return redirect_to_login(request.get_full_path())

    def get_object(self, queryset=None):
        try:
            Registration.objects.get(user=self.request.user)
        except Registration.DoesNotExist:
            pass
        else:
            return Registration.objects.get(user=self.request.user)

    def get_success_url(self):
        return '/register/%s' % self.object.location.slug

class Delete(LoginRequiredMixin, DeleteView):
    model = Registration
    success_url = reverse_lazy('registration:base')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                Registration.objects.get(user=request.user)
            except Registration.DoesNotExist:
                return redirect('/register')
            else:
                return super(Delete, self).dispatch(
                    request,
                    *args,
                    **kwargs)
        else:
            return redirect_to_login(request.get_full_path())

    def get_object(self, queryset=None):
        try:
            Registration.objects.get(user=self.request.user)
        except Registration.DoesNotExist:
            pass
        else:
            return Registration.objects.get(user=self.request.user)