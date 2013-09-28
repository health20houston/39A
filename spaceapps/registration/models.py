from django.db import models
from django.contrib.auth.models import User

from locations.models import Location


class Registration(models.Model):
    location = models.ForeignKey(Location, default=None)
    user = models.ForeignKey(User, unique=True)
    check_in = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
