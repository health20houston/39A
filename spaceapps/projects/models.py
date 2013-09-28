from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from challenges.models import Challenge

class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    challenge = models.ForeignKey(Challenge, blank=True, null=True)
    source_url = models.URLField(max_length=200, blank=True)
    source_url_check_bypass = models.BooleanField(default=False)
    license = models.ForeignKey('License')
    video = models.URLField(max_length=200, blank=True)
    nominated = models.BooleanField(default=False) 
    remove_from_judging = models.BooleanField(default=False)
    reason_for_disqualification = models.TextField(
        max_length=500, 
        null=True, 
        default=None, 
        blank=True,
        )
    finalist = models.BooleanField(default=False)
    hashtag = models.CharField(
        max_length=100, 
        null=True, 
        default=None, 
        blank=True,
        )
    short_description = models.TextField(
        max_length=500, 
        null=True, 
        default=None, 
        blank=True,
        )

    class Meta:                                                                 
        verbose_name_plural = "Projects"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'projects:view_project', 
            kwargs={'slug': self.slug})

class License(models.Model):                                                   
    name = models.CharField(max_length=100, blank=True)                     
    url = models.URLField(max_length=200, blank=True)                          
                                                                                
    class Meta:                                                                 
        verbose_name_plural = "Licenses"
    
    def __unicode__(self):                                                      
        return self.name                                                    

class Team(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    request_text = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    
    class Meta:                                                                 
        verbose_name_plural = "Team"

class Resource(models.Model):                                           
    project = models.ForeignKey(Project)                                    
    title = models.CharField(max_length=100, blank=True)                        
    url = models.URLField(max_length=200, blank=True)                          
                                                                                
    class Meta:                                                                 
        verbose_name_plural = "Resources"
    
    def __unicode__(self):                                                      
        return self.title
