from django.db import models

from projects.models import Project
from locations.models import Location


class LocalAward(models.Model):
    project = models.ForeignKey(Project)
    location = models.ForeignKey(Location)
    title = models.CharField(max_length=100, blank=True)

    def is_eligible(self):
        if self.project.source_url:
            return True
        else:
            return False

class Nomination(models.Model):
    project = models.ForeignKey(Project)
    location = models.ForeignKey(Location)

class GlobalAwardClass(models.Model):
    title = models.CharField(max_length=150, unique=True, blank=True)
    class Meta:
        verbose_name = 'Global Award Class'
        verbose_name_plural = 'Global Award Classes'
    
    def __unicode__(self):
        return self.title

class GlobalAwardFinalist(models.Model):
    global_award_class = models.ForeignKey('GlobalAwardClass')
    project = models.ForeignKey(Project)
    best_in_class = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Global Award Finalist'
        verbose_name_plural = 'Global Award Finalists'
    def __unicode__(self):
        return '%s (%s)' % (self.project.title, self.global_award_class.title)