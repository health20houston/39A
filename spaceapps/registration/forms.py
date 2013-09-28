from django.forms import ModelForm
from django.forms.widgets import RadioSelect, RadioFieldRenderer, RadioInput
from django.utils.safestring import mark_safe

from locations.models import Location

from .models import Registration


class LocationRadioInput(RadioInput):

    def __unicode__(self):
        return self.render()

class LocationRadioRenderer(RadioFieldRenderer):

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield LocationRadioInput(
                self.name,
                self.value,
                self.attrs.copy(),
                choice,
                i,
                )

    def __getitem__(self, idx):
        choice = self.choices[idx]
        return LocationRadioInput(
            self.name,
            self.value,
            self.attrs.copy(),
            choice,
            idx,
            )

    def render(self):
        locations = []
        for item in self:
            location = Location.objects.get(city=item.choice_label)
            availability = (location.capacity -
                Registration.objects.filter(location=location).count()
                )
            if availability <= 0 or location.open == False:
                item.attrs = {'disabled': 'disabled'}
            locations.append(u'%s' % item)
        return mark_safe(u'\n'.join([u'%s\n' % i for i in locations]))

class RegistrationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['location'].choices = [
            (item.id, item.city) for item in Location.objects.all()
            ]

    class Meta:
        model = Registration
        exclude = ('user', 'check_in',)
        widgets = {
                'location': RadioSelect(renderer=LocationRadioRenderer)
            }
