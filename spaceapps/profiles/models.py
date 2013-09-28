from django.db import models
from django.contrib.auth.models import User

class Background(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

BACKGROUND = (                                                              
        ('1', 'Developer'),                                                       
        ('2', 'Designer/Artist'),                                                   
        ('3', 'Student'),
        ('4', 'Subject Matter Expert'),
        ('5', 'Entrepreneur'),                                                   
    ) 

class Profile(models.Model):
    user = models.OneToOneField(User)
    allow_contact = models.BooleanField(default=False,
        help_text=('Designates that this user may be contacted by email.'))
    background = models.ManyToManyField(Background, blank=True)
    skype = models.CharField(max_length=32, blank=True)
    twitter = models.CharField(max_length=15, blank=True)
    github = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=32, blank=True)
    state = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=32, blank=True)

    class Meta:
        verbose_name = ('profile')
        verbose_name_plural = ('profiles')

    def __unicode__(self):
        return unicode(self.user)

