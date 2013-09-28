.. highlight:: bash

Customization
============
In order to make use of 39A, you will need to define a number of settings and customize the presentation of 39A's various applications.  

Settings
--------
The settings files for 39A are located within the 39A/spaceapps/settings directory and are divided into a base settings file and deployment specific settings files which inherit from the base file.  General settings that are not dependent on a deployment context go in the base settings file, while settings particular to specific deployments go in corresponding named settings files.

Minimal settings that need to be defined in a deployment include the particular `database`_ and `mail transfer agent`_ to use.  For outgoing email, `Mandrill`_ and `djrill`_ are recommended.

.. _database: https://docs.djangoproject.com/en/1.5/ref/settings/#databases
.. _mail transfer agent: https://docs.djangoproject.com/en/1.5/ref/settings/#email-backend
.. _Mandrill: https://mandrill.com/
.. _djrill: https://github.com/brack3t/Djrill

The `SECRET_KEY`_ setting has been removed from version controlled settings files and must instead be instantiated as an environment variable.  One approach to achieving this is described in the installation documentation.

.. _SECRET_KEY: https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-SECRET_KEY

The site name and corresponding domain can be specified in the django admin site.

Styles
------
39A utilizes the `Compass`_ and `Foundation 4`_ frameworks for styles and layout.  Installation and related documentation for these frameworks may be found at http://compass-style.org/install/ and http://foundation.zurb.com/docs/sass.html.

.. _Compass: http://compass-style.org/
.. _Foundation 4: http://foundation.zurb.com/

On Ubuntu, the prerequisites for compiling the stylesheets are as follows::

	$ sudo apt-get install ruby1.9.3
	$ sudo gem install compass zurb-foundation
	$ cd ~/39A/spaceapps/static
	$ compass watch

Once :code:`compass watch` is initialized, any changes made to the stylesheets in 39A/spaceapps/static/sass will automatically compile the resulting css into the 39A/spaceapps/static/stylesheets directory.

Templates
---------
Templates for 39A are located in the spaceapps/templates directory.  Most templates inherit from base.html, with specific template files covering only layout and presentation information for a particular application.