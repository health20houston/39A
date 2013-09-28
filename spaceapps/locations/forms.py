from django.forms import Form, ModelForm, CharField, ChoiceField
from django.forms.models import (
    modelformset_factory, 
    inlineformset_factory, 
    BaseInlineFormSet,
    )
from django.forms.formsets import formset_factory, BaseFormSet

import selectable.forms as selectable
from awards.models import LocalAward, Nomination
from registration.models import Registration
from projects.models import Project

from .lookups import UserLookup
from .models import (
    Location, 
    Sponsor,
    Lead,
    Resource,
    )


class LocalAwardForm(Form):
    def __init__(self, projects, *args, **kwargs):
        super(LocalAwardForm, self).__init__(*args, **kwargs)
        self.fields['project'] = ChoiceField(choices=projects)

    choices=(('1', 'First',))

    title = CharField(max_length=100)
    project = ChoiceField(choices=choices)

class LocationForm(ModelForm):
    class Meta:
        model = Location 
        exclude = ('name', 'slug', 'private', 'start', 'end' )

class LeadForm(ModelForm):
    class Meta(object):
        model = Lead
        widgets = {
            'lead': selectable.AutoCompleteSelectWidget(
                lookup_class=UserLookup)
            }

class CheckInForm(ModelForm):
    test = 'happy'

    class Meta(object):
        model = Registration
        # fields = ('check_in', )

CheckInFormSet = modelformset_factory(
        Registration,
        form=CheckInForm,
        extra=0,
        )

SponsorFormSet = inlineformset_factory(
        Location, 
        Sponsor, 
        extra=1,
        )

LeadFormSet = inlineformset_factory(
        Location,
        Lead,
        form=LeadForm,
        extra=1,
        )

ResourceFormSet = inlineformset_factory(
        Location,
        Resource,
        extra=1,
        )

class LocalAwardBaseFormSet(BaseFormSet):
    def __init__(self, projects, *args, **kwargs):
        self.projects = projects
        super(LocalAwardBaseFormSet, self).__init__(*args, **kwargs)

    def _construct_forms(self):
        self.forms = []
        for i in xrange(self.total_form_count()):
            self.forms.append(self._construct_form(i, projects=self.projects))

LocalAwardFormSet = formset_factory(
    LocalAwardForm, 
    formset=LocalAwardBaseFormSet, 
    extra=1,
    )

class AwardBaseFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.projects = kwargs.pop('projects')
        super(AwardBaseFormSet, self).__init__(*args, **kwargs)

    def _construct_forms(self):
        self.forms = []
        for i in xrange(self.total_form_count()):
            self.forms.append(self._construct_form(i, projects=self.projects))

class AwardForm(ModelForm):
    class Meta:
        model = LocalAward

    def __init__(self, *args, **kwargs):
        projects = kwargs.pop('projects')
        super(AwardForm, self).__init__(*args, **kwargs)
        if projects is not None:
            self.fields['project'].queryset = Project.objects.filter(
                id__in=projects).distinct()

AwardFormSet = inlineformset_factory(
        Location,
        LocalAward,
        form=AwardForm,
        formset=AwardBaseFormSet,
        extra=1,
        ) 

class NominationForm(ModelForm):
    class Meta:
        model = LocalAward

    def __init__(self, *args, **kwargs):
        projects = kwargs.pop('projects')
        super(NominationForm, self).__init__(*args, **kwargs)
        if projects is not None:
            self.fields['project'].queryset = Project.objects.filter(
                id__in=projects).distinct()
        
NominationFormSet = inlineformset_factory(
    Location,
    Nomination,
    form=NominationForm,
    formset=AwardBaseFormSet,
    extra=2,
    max_num=2,
    )

