from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from model_mommy import mommy

from .models import Challenge


class DetailTest(TestCase):
    def setUp(self):
        mommy.make('challenges.challenge', title = 'Moon', slug = 'moon',)

    def test_challenge_detail_unpublished(self):
        challenge = Challenge.objects.get(id=1)
        challenge.published = False
        challenge.save()
        response = self.client.get(
            reverse('challenges:view_challenge', args=("moon",))
            )
        self.assertNotEqual(response.status_code, 200)

    def test_challenge_detail_published(self):
        challenge = Challenge.objects.get(id=1)
        challenge.published = True
        challenge.save()
        response = self.client.get(
            reverse('challenges:view_challenge', args=("moon",))
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moon")

class ListTest(TestCase):
    def setUp(self):
        mommy.make(
            'challenges.challenge', 
            title = 'Moon', 
            slug = 'moon', 
            published = True,
            )

    def test_challenge_list(self):
        response = self.client.get(
            reverse('challenges:list_challenges',)
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moon")
