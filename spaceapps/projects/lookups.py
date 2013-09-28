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
    )
    #  filters = {'is_active': True, }

    def get_item_value(self, item):
        # Display for currently selected item
        return item.get_full_name()

    def get_item_id(self, item):
        return item.id

    def get_item_label(self, item):
        # Display for choice listings
        return u"%s (%s***@%s)" % (
            item.get_full_name().title(), 
            item.email.split('@', 1)[0][:2],
            item.email.split('@', 1)[1])

registry.register(UserLookup)
