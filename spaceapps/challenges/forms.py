from django.forms import ModelForm
from django.forms.models import inlineformset_factory

import selectable.forms as selectable

from .lookups import UserLookup
from .models import (
    Challenge, 
    ChallengeSponsor,
    ChallengeAuthor,
    ChallengeDataset,)


class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge

class AuthorForm(ModelForm):
    class Meta(object):
        model = ChallengeAuthor
        widgets = {
            'author': selectable.AutoCompleteSelectWidget(
                lookup_class=UserLookup
                ),
        }

SponsorFormSet = inlineformset_factory(
        Challenge, 
        ChallengeSponsor, 
        extra=1,
        )

AuthorFormSet = inlineformset_factory(
        Challenge,
        ChallengeAuthor,
        form=AuthorForm,
        extra=1,
        )

DataFormSet = inlineformset_factory(
        Challenge,
        ChallengeDataset,
        extra=1,
        )
