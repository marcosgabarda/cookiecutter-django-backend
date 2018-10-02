{% if cookiecutter.use_oauth == 'y' -%}
from oauth2_provider.models import Application
{%- endif %}
from rest_framework import status
from rest_framework.test import APITestCase

from {{ cookiecutter.project_slug }}.users.models import User
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory


class UserAPITests(APITestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_list_users(self):
        UserFactory.create_batch(size=10)
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/v1/users/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(1, data["count"])

    def test_register_user(self):
        users = User.objects.all().count()
        data = {"email": "new@example.com", "password": "secure"}
        response = self.client.post("/api/v1/users/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(users + 1, User.objects.all().count())
        user = User.objects.get(email=data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_get_me(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/v1/users/me/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("id", data)

    def test_update_me(self):
        self.client.force_authenticate(self.user)
        data = {
            "email": "client1@example.com",
            "password": "new_password",
        }
        response = self.client.patch("/api/v1/users/me/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(data["email"], user.email)
        self.assertTrue(user.check_password(data["password"]))


class VerifyEmailAPITests(APITestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_request_restore_code(self):
        self.user.is_email_verified = False
        self.user.save()
        self.assertFalse(self.user.is_email_verified)
        data = {
            "verification_code": self.user.verification_code,
        }
        response = self.client.post(
            "/api/v1/verify_email/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.is_email_verified)


class RestorePasswordAPITests(APITestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_request_restore_code(self):
        self.assertIsNone(self.user.restore_password_code)
        data = {
            "email": self.user.email,
        }
        response = self.client.post(
            "/api/v1/request_restore_code/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(pk=self.user.pk)
        self.assertIsNotNone(user.restore_password_code)

    def test_restore_password(self):
        self.user.send_restore_code()
        data = {
            "password": "new_password",
            "repeat_password": "new_password",
            "restore_password_code": self.user.restore_password_code,
        }
        response = self.client.post(
            "/api/v1/restore_password/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.check_password(data["password"]))


{% if cookiecutter.use_oauth == 'y' -%}
class AuthAPITests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.password = "password"
        self.user.set_password(self.password)
        self.user.save()
        self.app = Application(
            authorization_grant_type=Application.GRANT_PASSWORD,
            client_type=Application.CLIENT_CONFIDENTIAL,
        )
        self.app.save()
        credentials = base64.b64encode('{}:{}'.format(self.app.client_id, self.app.client_secret).encode()).decode()
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + credentials

    def test_obtain_token(self):
        data = {
            "grant_type": Application.GRANT_PASSWORD,
            "username": self.user.username,
            "password": self.password,
        }
        response = self.client.post(
            '/api/v1/auth/token/',
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('access_token', data)

    def test_bad_access_token(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer dummy'
        response = self.client.get(
            '/api/v1/users/me/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_access_token(self):
        data = {
            "grant_type": Application.GRANT_PASSWORD,
            "username": self.user.username,
            "password": self.password,
        }
        response = self.client.post(
            '/api/v1/auth/token/',
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('refresh_token', data)
        data = {
            "grant_type": "refresh_token",
            "refresh_token": data["refresh_token"],
            "client_id": self.app.client_id,
            "client_secret": self.app.client_secret,
        }
        response = self.client.post(
            '/api/v1/auth/token/',
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('access_token', data)
{%- endif %}
