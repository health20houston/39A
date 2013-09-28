from django.contrib.sites.models import Site

def site(request):
    try:
        site = Site.objects.get_current()
        return {
            'site': site,
        }
    except Site.DoesNotExist:
        # always return a dict, no matter what!
        return {'site':''} # an empty string