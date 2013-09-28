from django.contrib.auth.models import User

from model_mommy.recipe import Recipe, foreign_key, seq

from .models import Location


san_francisco = Recipe(
    Location,
    name = 'San Francisco',
    slug = 'san-francisco',
    description = 'San Francisco',
    timezone = '-8.0',
    city = 'San Francisco',
    country = 'US',
    continent = 'NA',
    lat = '0',
    lon = '0',
    capacity = '100'
    )

