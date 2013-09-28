from django.contrib.auth.models import User

from selectable.base import ModelLookup
from selectable.registry import registry


class UserLookup(ModelLookup):
    model = User
    search_fields = (
        'username__icontains',
        'first_name__icontains',
        'last_name__icontains',
        'email__icontains',
	    'background__icontains',
        )

    def get_item_value(self, item):
        # Display for currently selected item
        return item.first_name

    def get_item_id(self, item):
        return item.id

    def get_item_label(self, item):
        # Display for choice listings
        return u"%s (%s)" % (item.username, item.get_full_name())

registry.register(UserLookup)
