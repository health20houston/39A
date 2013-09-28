from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

from .models import Profile

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    email = forms.EmailField(label="Primary email",help_text='')
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = Profile
        exclude = ('user',)

    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='First Name')           
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, user):                                                     
        profile = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']                     
        user.last_name = self.cleaned_data['last_name']                       
        user.save()
        profile.user = user
        profile.save()
        self.save_m2m()

    class Meta:
        model = Profile
        exclude = ["user",]
        widgets = {'background': forms.CheckboxSelectMultiple}


