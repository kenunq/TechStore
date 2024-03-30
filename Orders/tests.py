from rest_framework.test import APITestCase

from goods.models import Basket, Category, Product
from Orders.models import Order, UserInfo
from user.models import User


# Create your tests here.


class OrdersTest(APITestCase):
    @classmethod
    def setUp(cls):
        cls.user1_username = cls.user1_password = "user1"

        cls.user1 = User.objects.create_user(cls.user1_username, "user1@yandex.ru", cls.user1_password)

        cls.category1 = Category.objects.create(name="category1", description="desc for category1")

        cls.product1 = Product.objects.create(
            name="Product1",
            description="desc for product1",
            price=100.20,
            category=cls.category1,
            brand="test",
            available_quantity=10,
            is_published=True,
        )

        cls.basket = Basket.objects.create(user=cls.user1, product=cls.product1, quantity=3)

        cls.user_info_data = {
            "country": "Russia",
            "city": "Moscow",
            "street": "Lenina",
            "postal_code": "123456",
            "phone_number": "1234567890",
            "email": "user1@yandex.ru",
        }

    def test_create_order(self):
        response = self.client.post(
            "/auth/jwt/create/",
            data={"username": self.user1_username, "password": self.user1_password},
        )
        self.assertEquals(response.status_code, 200)
        token = response.data["access"]

        response = self.client.post(
            "/api/v1/user-info/",
            data=self.user_info_data,
            headers={"Authorization": f"JWT {token}"},
        )
        self.assertEquals(response.status_code, 201)
        self.assertTrue(UserInfo.objects.filter(user=self.user1).exists())
        self.assertTrue(Order.objects.filter(user=self.user1).exists())
        self.assertFalse(Basket.objects.filter(user=self.user1).exists())

    def test_get_orders(self):
        response = self.client.post(
            "/auth/jwt/create/",
            data={"username": self.user1_username, "password": self.user1_password},
        )
        self.assertEquals(response.status_code, 200)
        token = response.data["access"]

        response = self.client.post(
            "/api/v1/user-info/",
            data=self.user_info_data,
            headers={"Authorization": f"JWT {token}"},
        )
        self.assertEquals(response.status_code, 201)

        response = self.client.get("/api/v1/order/", headers={"Authorization": f"JWT {token}"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)
