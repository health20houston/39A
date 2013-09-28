from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Challenge(models.Model):
    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField()
    description = models.TextField()
    category = models.ForeignKey('Category')
    internal = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    image = models.ImageField(upload_to="challenge", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Challenges"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'view_challenge', 
            kwargs={'slug': self.slug})

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"
    
    def __unicode__(self):
        return self.name

class ChallengeSponsor(models.Model):
    challenge = models.ForeignKey(Challenge)
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name 

class ChallengeAuthor(models.Model):
    challenge = models.ForeignKey(Challenge)
    author = models.ForeignKey(User)
    is_public = models.BooleanField(default=False)

class ChallengeDataset(models.Model):
    challenge = models.ForeignKey(Challenge)
    title = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)
    description = models.TextField()

    def __unicode__(self):
        return self.title
