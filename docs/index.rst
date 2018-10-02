.. cookiecutter-backend documentation master file.

Welcome to Cookiecutter Backend's documentation!
================================================

A Cookiecutter_ template for Django backend projects, using only Django Rest Framework as
API interface. It includes several changes from the originial
`Cookiecutter Django project`_:

* Mandatory use of Docker.
* Don't use of Django frontend.
* Integration with Django Rest Framework
* Support for JWT ot of the box
* Integration with PostGIS (optional)
* Integration with OAuth (optional)
* Support for managing CORS headers (optional)

.. _`Cookiecutter Django project`: https://github.com/pydanny/cookiecutter-django
.. _cookiecutter: https://github.com/audreyr/cookiecutter

Contents:

.. toctree::
   :maxdepth: 2

   project-generation-options
   developing-locally-docker
   settings
   linters
   deployment-with-docker
   docker-postgres-backups

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. At some point it would be good to have a module index of the high level things we are doing. Then we can * :ref:`modindex` back in.
