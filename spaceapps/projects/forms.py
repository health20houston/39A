from django.forms import ModelForm
from django.forms.models import inlineformset_factory

import selectable.forms as selectable

from .lookups import UserLookup
from .models import (
    Project, 
    Team,
    Resource,
    )


class LocationForm(ModelForm):
    class Meta:
        model = Project 

class TeamForm(ModelForm):
    class Meta(object):
        model = Team 
        exclude = ('request_text', 'approved',)
        widgets = {
            'user': selectable.AutoCompleteSelectWidget(
                lookup_class=UserLookup)
            }

TeamFormSet = inlineformset_factory(
        Project, 
        Team, 
        form = TeamForm,
        extra=1,
        )

ResourceFormSet = inlineformset_factory(
        Project,
        Resource,
        extra=1,
        )

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = (
            'category', 
            'source_url_check_bypass', 
            'nominated', 
            'remove_from_judging', 
            'reason_for_disqualification', 
            'finalist', 
            'hashtag', 
            'award_class',
            )