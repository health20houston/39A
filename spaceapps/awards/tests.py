from django.test import TestCase
from django.core.urlresolvers import reverse


class AwardsTest(TestCase):
    def test_awards_list(self):
        response = self.client.get(reverse('awards:list'))
        self.assertEqual(response.status_code, 200)