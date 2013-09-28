.. highlight:: bash

Installation
============

Prerequisites
-------------

39A requires the following software prior to installation:

* git
* virtualenv
* pip

Install the prerequisites as follows:

Ubuntu
++++++

::
	
	$ sudo apt-get install build-essential python-dev git-core python-setuptools
	$ sudo easy_install pip
	$ sudo pip install virtualenv

OSX
+++

* Install commandline tools: https://developer.apple.com/downloads/
* Install git: https://code.google.com/p/git-osx-installer/

::

	$ sudo easy_install pip
	$ sudo pip install virtualenv

Environment Setup
-----------------

In your home directory or another location of your choosing::

	$ mkdir ~/.virtualenvs
	$ virtualenv ~/.virtualenvs/39A
	$ git clone https://github.com/nasa/39A.git ~/39A	

Activate Environment
--------------------

To work with 39A, you must activate the appropriate virtual environment (per terminal environment).  To do so, open a terminal::

	$ source ~/.virtualenvs/39A/bin/activate
	$ export SECRET_KEY="insert-random-complex-key"
	
Replace "insert-random-complex-key" from above with random text.  A good source for this random key is https://www.grc.com/passwords.html.  This process will need to be repeated whenever opening a new terminal to work with the project.
	
Setup
-----

With your environment created and activated, install dependencies and create your database::
	
	$ cd ~/39A
	$ pip install -r requirements.txt
	$ cd ~/39A/spaceapps
	$ python manage.py syncdb --settings=spaceapps.settings.dev
	$ python manage.py migrate --settings=spaceapps.settings.dev


Running the Development Server
------------------------------

::

	$ cd ~/39A/spaceapps
	$ python manage.py runserver 0.0.0.0:8080 --settings=spaceapps.settings.dev
