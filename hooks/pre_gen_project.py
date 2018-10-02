"""
Based on Cookiecutter Django project:
https://github.com/pydanny/cookiecutter-django
"""
from __future__ import print_function

import sys

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

project_slug = "{{ cookiecutter.project_slug }}"
if hasattr(project_slug, "isidentifier"):
    assert project_slug.isidentifier(), "'{}' project slug is not a valid Python identifier.".format(
        project_slug
    )

assert "\\" not in "{{ cookiecutter.author_name }}", "Don't include backslashes in author name."
