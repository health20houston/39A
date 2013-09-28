Features
========
As a hackathon event website, 39A provides the following features:

Locations
---------
The overall hackathon occurs in one or more physical locations.  At each of these locations, there may be one or more local event leads, sponsors, and resources.  Event leads are individuals holding user accounts which are designated by a global administrator as managing a specific event.  Such designation affords the local lead administrative rights to the specific location.  These rights include the ability to:

* Edit the location description
* View attendee information (users registered for the location)
* Define venue capacity
* Designate local sponsors

Sponsors are individuals or groups which provide support or resources for the location.  Identification of sponsors includes:

* Sponsor Name
* Sponsor Image or Logo
* Sponsor URL

Resources may be any web accessible asset, including local datasets, venue information, or similar.

Checkins
++++++++
A checkin concept was contemplated and initially stubbed out, but ultimately went unimplemented.

Registration
------------
Registration ties users together with locations.  During the user account creation process, users are invited to register to attend a physical location.  Once registered, users receive email notification confirming their registration, and are able to subsequently edit their registration.  This is important as a user registration decrements the location's capacity.  When capacity has been reached, no further registrations for that location are permitted.

To register, users must first create an account at '/account/signup'.  Account management is handled by `django-allauth`_, which supports authentication from a number of social providers, including GitHub and OpenId, among others.

.. _django-allauth: https://django-allauth.readthedocs.org/en/latest/

Challenges
----------
Challenges are problem statements published by the event organizers defining a set possible tasks which users can solve by creating projects.

Projects
--------
Projects organize the activities of an individual or team and present their work product.  Projects are typically associated with challenges which they address, but may also be freestanding.  Projects are created adhoc by users.

Awards
------
Awards are a means to recognize projects for their submitted contributions.  Awards are divided into two groups: local awards and global awards.  Local awards are created and issued by local leads for their specific venue if one or more of a project's team members attended their venue.  Local leads may also nominate projects from their location for global award consideration.  Global awards recognize projects in a series of categories defined by the event organizers.





