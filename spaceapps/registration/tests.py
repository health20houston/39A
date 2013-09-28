from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from model_mommy import mommy


class ListTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'no@no.no', 'password')
        registration = mommy.make_recipe('registration.location')

    def test_list_locations(self):
        response = self.client.get(reverse('registration:base'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "San Francisco")

class CreateTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'no@no.no', 'password')

    def test_registration_unauthenticated(self):
        registration = mommy.make_recipe('registration.location')
        response = self.client.get(reverse('registration:base') + 
            'san-francisco/')
        self.assertEqual(response.status_code, 302)

    def test_registration_open(self):
        registration = mommy.make_recipe('registration.location')
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('registration:base') + 
            'san-francisco/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thanks!")
        self.assertEqual(len(mail.outbox), 1)

    def test_registration_full(self):
        registration = mommy.make_recipe('registration.location_full')
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('registration:base') + 
            'san-francisco/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Oh no!")

    def test_registration_closed(self):
        registration = mommy.make_recipe('registration.location_closed')
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('registration:base') + 
            'san-francisco/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Oh no!")

    def test_registration_location_does_not_exist(self):
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('registration:base') + 
            'mars/')
        self.assertEqual(response.status_code, 404)

    def test_registration_location_private(self):
        registration = mommy.make_recipe('registration.location_private')
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('registration:base'))
        self.assertNotContains(response, "San Francisco")

class EditTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'no@no.no', 'password')        
        mommy.make_recipe('registration.location_mars')

    def test_edit_registration_unauthenticated(self):
        response = self.client.get(reverse('registration:edit'))
        self.assertEqual(response.status_code, 302)

    def test_edit_registration(self):
        mommy.make_recipe('registration.location')
        self.client.login(username='test', password='password')
        self.client.get(reverse('registration:base') + 'san-francisco/')
        response = self.client.get(reverse('registration:edit'))
        self.assertContains(response, "Choose your Venue")

    def test_edit_registration_confirm(self):
        mommy.make_recipe('registration.location')
        self.client.login(username='test', password='password')
        self.client.get(reverse('registration:base') + 'san-francisco/')
        response = self.client.post(
            reverse('registration:edit'),
            { 'location': '2' },
            )
        self.assertEqual(response.status_code, 302)

    def test_edit_registration_full(self):
        registration = mommy.make_recipe('registration.location_full')
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('registration:base') + 'mars/')
        response = self.client.get(reverse('registration:edit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 
            '<input disabled="disabled" name="location" type="radio" '
            'value="2" />',
            )

    def test_edit_registration_closed(self):
        registration = mommy.make_recipe('registration.location_closed')
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('registration:base') + 'mars/')
        response = self.client.get(reverse('registration:edit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 
            '<input disabled="disabled" name="location" type="radio" '
            'value="2" />',
            )

class DeleteTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'no@no.no', 'password')
        registration = mommy.make_recipe('registration.location')

    def test_delete_registration_unauthenticated(self):
        response = self.client.get(reverse('registration:delete'))
        self.assertEqual(response.status_code, 302)

    def test_delete_registration(self):
        self.client.login(username='test', password='password')
        self.client.get(reverse('registration:base') + 'san-francisco/')
        response = self.client.get(reverse('registration:delete'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cancel Registration")

    def test_delete_registration_confirm(self):
        self.client.login(username='test', password='password')
        self.client.get(reverse('registration:base') + 'san-francisco/')
        response = self.client.post(reverse('registration:delete'))
        self.assertRedirects(response, reverse('registration:base'))
