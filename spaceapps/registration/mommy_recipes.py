from django.contrib.auth.models import User

from model_mommy.recipe import Recipe, foreign_key, seq
from locations.models import Location

from .models import Registration


location = Recipe(
    Location,
    name = 'San Francisco',
    slug = 'san-francisco',
    description = 'San Francisco',
    timezone = '-8.0',
    country = 'US',
    continent = 'NA',
    lat = '0',
    lon = '0',
    capacity = '100'
    )

location_full = Recipe(
    Location,
    name = 'San Francisco',
    slug = 'san-francisco',
    description = 'San Francisco',
    timezone = '-8.0',
    country = 'US',
    continent = 'NA',
    lat = '0',
    lon = '0',
    capacity = '0'
    )

location_closed = Recipe(
    Location,
    name = 'San Francisco',
    slug = 'san-francisco',
    description = 'San Francisco',
    timezone = '-8.0',
    country = 'US',
    continent = 'NA',
    lat = '0',
    lon = '0',
    capacity = '0'
    )

location_private = Recipe(
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
    private = True
    )

location_mars = Recipe(
    Location,
    name = 'Mars',
    slug = 'mars',
    description = 'Mars',
    timezone = '-8.0',
    city = 'Mars',
    country = 'US',
    continent = 'NA',
    lat = '0',
    lon = '0',
    capacity = '100'
    )

registration = Recipe(
    Registration,
    location = foreign_key(location),
    # user = foreign_key(user),
    )