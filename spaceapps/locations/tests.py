from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from model_mommy import mommy

from .models import Location


class DetailTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'no@no.no', 'password')
        mommy.make_recipe('locations.san_francisco')

    def test_location_detail(self):
        response = self.client.get(
            reverse('locations:detail', args=("san-francisco",))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "San Francisco")

    def test_location_detail_related(self):
        mommy.make('projects.team', user=User.objects.get(username='test'))
        self.client.login(username='test', password='password')
        self.client.get(reverse('registration:base') + 'san-francisco/')
        response = self.client.get(
            reverse('locations:detail', args=("san-francisco",))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visit Project")

    def test_location_detail_sponsor(self):
        mommy.make(
            'locations.sponsor', 
            location = Location.objects.get(name='San Francisco'),
            name = 'John Glenn'
            )
        response = self.client.get(
            reverse('locations:detail', args=("san-francisco",))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Glenn")

    def test_location_detail_lead(self):
        mommy.make(
            'locations.lead', 
            location = Location.objects.get(name='San Francisco'),
            lead = User.objects.get(username='test'),
            )
        response = self.client.get(
            reverse('locations:detail', args=("san-francisco",))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email")

    def test_location_detail_resource(self):
        mommy.make(
            'locations.resource', 
            location = Location.objects.get(name='San Francisco'),
            name = 'John Glenn'
            )
        response = self.client.get(
            reverse('locations:detail', args=("san-francisco",))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Glenn")

class ListTest(TestCase):
    def setUp(self):
        mommy.make_recipe('locations.san_francisco')

    def test_list_locations(self):
        response = self.client.get(
            reverse('locations:list')
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "San Francisco")


class EditTest(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'no@no.no', 'password')
        User.objects.create_superuser('super', 'no@no.no', 'password')
        mommy.make_recipe('locations.san_francisco')

    def test_can_edit_location_unauthenticated(self):
        response = self.client.get(
            reverse('locations:edit', args=('san-francisco',))
            )
        self.assertNotEqual(response.status_code, 200)

    def test_can_edit_location_unprivileged(self):
        self.client.login(username='test', password='password')
        response = self.client.get(
            reverse('locations:edit', args=('san-francisco',))
            )
        self.assertEqual(response.status_code, 403)

    def test_can_edit_location_as_lead(self):
        mommy.make(
            'locations.lead', 
            location = Location.objects.get(name='San Francisco'),
            lead = User.objects.get(username='test'),
            )
        self.client.login(username='test', password='password')
        response = self.client.get(
            reverse('locations:edit', args=('san-francisco',))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "San Francisco")

    def test_can_edit_location_as_super(self):
        self.client.login(username='super', password='password')
        response = self.client.get(
            reverse('locations:edit', args=('san-francisco',))
            )
        self.assertEqual(response.status_code, 200)

    def test_edit_location(self):
        self.client.login(username='super', password='password')
        response = self.client.post(
            reverse('locations:edit', args=('san-francisco',)), {
                'name': 'San Francisco',
                'slug': 'san-francisco',
                'description': 'Description',
                'timezone': '-8.0',
                'city': 'San Francisco',
                'country': 'US',
                'continent': 'NA',
                'lat': '0',
                'lon': '0',
                'capacity': '100',
                'sponsor-TOTAL_FORMS': '0',
                'sponsor-INITIAL_FORMS': '0',
                'lead-TOTAL_FORMS': '0',
                'lead-INITIAL_FORMS': '0',
                'localaward-TOTAL_FORMS': '0',
                'localaward-INITIAL_FORMS': '0',
                'nomination-TOTAL_FORMS': '0',
                'nomination-INITIAL_FORMS': '0',
                'resource-TOTAL_FORMS': '0',
                'resource-INITIAL_FORMS': '0', 
            }),

        self.assertTrue(Location.objects.get(description='Description'))

class AttendeesTest(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'no@no.no', 'password')
        User.objects.create_superuser('super', 'no@no.no', 'password')
        mommy.make_recipe('locations.san_francisco')

    def test_view_attendees_unauthenticated(self):
        response = self.client.get(
            reverse('locations:attendees', args=('san-francisco',))
            )
        self.assertNotEqual(response.status_code, 200)

    def test_view_attendees_unprivilged(self):
        self.client.login(username='test', password='password')
        response = self.client.get(
            reverse('locations:attendees', args=('san-francisco',))
            )
        self.assertNotEqual(response.status_code, 200)

    def test_view_attendees_as_lead(self):
        mommy.make(
            'locations.lead', 
            location = Location.objects.get(name='San Francisco'),
            lead = User.objects.get(username='test'),
            )
        self.client.login(username='test', password='password')
        self.client.get(reverse('registration:base') + 'san-francisco/')
        response = self.client.get(
            reverse('locations:attendees', args=('san-francisco',))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "no@no.no")

    def test_view_attendees_as_super(self):
        self.client.login(username='super', password='password')
        self.client.get(reverse('registration:base') + 'san-francisco/')
        response = self.client.get(
            reverse('locations:attendees', args=('san-francisco',))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "no@no.no")

class CSVTest(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'no@no.no', 'password')
        User.objects.create_superuser('super', 'no@no.no', 'password')
        mommy.make_recipe('locations.san_francisco')
        self.client.login(username='test', password='password')
        self.client.get(reverse('registration:base') + 'san-francisco/')

    def test_export_attendees_unauthenticated(self):
        response = self.client.get(
            reverse('locations:export', args=('san-francisco',))
            )
        self.assertNotEqual(response.status_code, 200)

    def test_export_attendees_unprivilged(self):
        self.client.login(username='test', password='password')
        response = self.client.get(
            reverse('locations:export', args=('san-francisco',))
            )
        self.assertNotEqual(response.status_code, 200)

    def test_export_attendees_as_lead(self):
        mommy.make(
            'locations.lead', 
            location = Location.objects.get(name='San Francisco'),
            lead = User.objects.get(username='test'),
            )
        self.client.login(username='test', password='password')
        response = self.client.get(
            reverse('locations:export', args=('san-francisco',))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "no@no.no")

    def test_export_attendees_as_super(self):
        self.client.login(username='super', password='password')
        self.client.get(reverse('registration:base') + 'san-francisco/')
        response = self.client.get(
            reverse('locations:export', args=('san-francisco',))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "no@no.no")

class RelatedTest(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'no@no.no', 'password')
        mommy.make_recipe('locations.san_francisco')
        self.client.login(username='test', password='password')
        self.client.get(
            reverse('registration:register', args=('san-francisco',))
            )
        mommy.make('projects.team', user=User.objects.get(username='test'))

    def test_related_projects(self):
        response = self.client.get(
            reverse('locations:related', args=('san-francisco',))
            )
        print response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "project")