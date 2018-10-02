Cookiecutter Backend
====================

Inspired in `Cookiecutter Django project`_ by Daniel Roy Greenfeld.

This is the Cookiecutter template to build backend projects. It
includes several changes from the originial
`Cookiecutter Django project`_:

Features
---------

* Mandatory use of Docker.
* Don't use of Django frontend.
* Integration with Django Rest Framework
* Support for JWT ot of the box

Optional Integrations
---------------------

* Integration with PostGIS (optional)
* Integration with OAuth (optional)
* Support for managing CORS headers

Usage
------

First, get Cookiecutter.::

    $ pip install "cookiecutter>=1.4.0"

Now run it against this repo::

    $ cookiecutter https://github.com/marcosgabarda/cookiecutter-backend

Django Rest Framework
---------------------

The integration with Django Rest Framework comes with some default behavior.

* Every ``IntegrityException`` is handle as a ``Bad Request`` error
* Pagination using page number by default
* You can set the page size using ``page_size`` query param
* ``User`` resource out of the box

Custom Admin Theme
------------------

You can customize the Django Admin by setting the styles in the ``static/admin/css/theme.css``
file. By default, this file has the originial values from the admin site, but
they can be personalized and addapted to the project.

.. _`Cookiecutter Django project`: https://github.com/pydanny/cookiecutter-django
