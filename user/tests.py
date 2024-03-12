from django.test import TestCase
from rest_framework.test import APITestCase

from user.models import User


# Create your tests here.


class Test_User(APITestCase):
    @classmethod
    def setUp(cls):
        cls.user1_username = "username_1"
        cls.user1_password = "password_1"
        cls.user1_email = "user1@yandex.ru"
        cls.user1_name = "user1"
        cls.user1_birthday = "2000-01-01"
        cls.user1_sex = "Женщина"

    def test_register_user(self):
        # response = self.client.post('/auth/users/', data={
        #     'username': self.user1_username,
        #     'email': self.user1_email,
        #     'password': self.user1_password
        # })
        response = self.client.post(
            "/auth/users/",
            data={
                "username": self.user1_username,
                "email": self.user1_email,
                "password": self.user1_password,
                "name": self.user1_name,
                "birthday": self.user1_birthday,
                "gender": self.user1_sex,
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=self.user1_username).exists())

    def test_login_user(self):
        response = self.client.post(
            "/auth/users/",
            data={
                "username": self.user1_username,
                "email": self.user1_email,
                "password": self.user1_password,
                "name": self.user1_name,
                "birthday": self.user1_birthday,
                "gender": self.user1_sex,
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=self.user1_username).exists())

        response = self.client.post(
            "/auth/jwt/create/",
            data={"username": self.user1_username, "password": self.user1_password},
        )

        self.assertEquals(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_profile_user(self):
        response = self.client.post(
            "/auth/users/",
            data={
                "username": self.user1_username,
                "email": self.user1_email,
                "password": self.user1_password,
                "name": self.user1_name,
                "birthday": self.user1_birthday,
                "gender": self.user1_sex,
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=self.user1_username).exists())

        response = self.client.post(
            "/auth/jwt/create/",
            data={"username": self.user1_username, "password": self.user1_password},
        )

        self.assertEquals(response.status_code, 200)
        token = response.data["access"]

        response = self.client.get(
            "/auth/users/me/", headers={"Authorization": f"JWT {token}"}
        )
        self.assertEquals(response.status_code, 200)
        user_data = {
            "username": self.user1_username,
            "name": self.user1_name,
            "birthday": self.user1_birthday,
            "gender": self.user1_sex,
            "email": self.user1_email,
        }
        self.assertEquals(response.data, user_data)

    def test_refresh_user(self):
        response = self.client.post(
            "/auth/users/",
            data={
                "username": self.user1_username,
                "email": self.user1_email,
                "password": self.user1_password,
                "name": self.user1_name,
                "birthday": self.user1_birthday,
                "gender": self.user1_sex,
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=self.user1_username).exists())

        response = self.client.post(
            "/auth/jwt/create/",
            data={"username": self.user1_username, "password": self.user1_password},
        )

        self.assertEquals(response.status_code, 200)
        token = response.data["access"]

        response = self.client.post(
            "/auth/jwt/refresh/",
            data={"refresh": response.data["refresh"]},
            headers={"Authorization": f"JWT {token}"},
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_reset_password(self):
        response = self.client.post(
            "/auth/users/",
            data={
                "username": self.user1_username,
                "email": self.user1_email,
                "password": self.user1_password,
                "name": self.user1_name,
                "birthday": self.user1_birthday,
                "gender": self.user1_sex,
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=self.user1_username).exists())

        response = self.client.post(
            "/auth/users/reset_password/", data={"email": self.user1_email}
        )
        self.assertEquals(response.status_code, 204)

    def test_reset_username(self):
        response = self.client.post(
            "/auth/users/",
            data={
                "username": self.user1_username,
                "email": self.user1_email,
                "password": self.user1_password,
                "name": self.user1_name,
                "birthday": self.user1_birthday,
                "gender": self.user1_sex,
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=self.user1_username).exists())

        response = self.client.post(
            "/auth/users/reset_username/", data={"email": self.user1_email}
        )
        self.assertEquals(response.status_code, 204)

    def test_set_username(self):
        response = self.client.post(
            "/auth/users/",
            data={
                "username": self.user1_username,
                "email": self.user1_email,
                "password": self.user1_password,
                "name": self.user1_name,
                "birthday": self.user1_birthday,
                "gender": self.user1_sex,
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=self.user1_username).exists())

        response = self.client.post(
            "/auth/jwt/create/",
            data={"username": self.user1_username, "password": self.user1_password},
        )

        self.assertEquals(response.status_code, 200)
        token = response.data["access"]

        response = self.client.post(
            "/auth/users/set_username/",
            data={"current_password": self.user1_password, "new_username": "username2"},
            headers={"Authorization": f"JWT {token}"},
        )
        self.assertEquals(response.status_code, 204)

        self.assertEquals(User.objects.get(name=self.user1_name).username, "username2")
