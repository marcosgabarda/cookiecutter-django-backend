from django.urls import path

from {{ cookiecutter.project_slug }}.emails.views import PreviewEmailView

app_name = 'emails'
urlpatterns = [
    path('previews/', PreviewEmailView.as_view(), name='preview'),
]
