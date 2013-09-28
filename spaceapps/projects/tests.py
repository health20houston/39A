from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from model_mommy import mommy

from .models import Project


class DetailTest(TestCase):
    def setUp(self):
        mommy.make('projects.project', title = 'Apollo', slug = 'apollo',)

    def test_project_detail(self):
        response = self.client.get(
            reverse('projects:view_project', args=("apollo",))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apollo")

class ListTest(TestCase):
    def setUp(self):
        mommy.make('projects.project', title = 'Apollo', slug = 'apollo',)

    def test_list_projects(self):
        response = self.client.get(
            reverse('projects:list')
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apollo")

class CreateTest(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'no@no.no', 'password')
        User.objects.create_superuser('super', 'no@no.no', 'password')

    def test_create_project_unauthenticated(self):
        response = self.client.get(
            reverse('projects:create',)
            )
        self.assertNotEqual(response.status_code, 200)