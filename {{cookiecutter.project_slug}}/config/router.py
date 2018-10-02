from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from {{ cookiecutter.project_slug }}.users.api.v1.viewsets import (
    UserViewSet,
    RequestRestoreCodeViewSet,
    RestorePasswordViewSet,
    VerifyViewSet,
    me
)


app_name = 'api_v1'

router = routers.DefaultRouter()
router.register('request_restore_code', viewset=RequestRestoreCodeViewSet, base_name="request_restore_code")
router.register('restore_password', viewset=RestorePasswordViewSet, base_name="restore_password")
router.register('verify_email', viewset=VerifyViewSet, base_name="verify_email")
router.register('users', viewset=UserViewSet)

urlpatterns = [
    path('users/me/', me, kwargs={'pk': 'me'}),
    path('', include(router.urls)),
]
