from django.test import TestCase
from rest_framework.test import APITestCase

from goods.models import Product, Category, Feature, ProductFeature, Basket
from user.models import User


# Create your tests here.

class Test_ProductsAPI(APITestCase):

    @classmethod
    def setUp(cls):
        cls.user1_username = cls.user1_password = 'user1'
        cls.user2_username = cls.user2_password = 'user2'
        cls.user1_email, cls.user2_email = 'user1@yandex.ru', 'user2@yandex.ru'

        cls.user1 = User.objects.create_user(cls.user1_username, cls.user1_email, cls.user1_password)
        cls.user2 = User.objects.create_user(cls.user2_username, cls.user2_email, cls.user2_password)

        cls.category1 = Category.objects.create(
            name="category1",
            description="desc for category1"
        )

        cls.feature1 = Feature.objects.create(name='Feature 1', description='Description for Feature 1')

        cls.product1 = Product.objects.create(
            name="Product1",
            description="desc for product1",
            price=100.20,
            category=cls.category1,
            brand="test",
            available_quantity=10,
            is_published=True,
        )

        cls.product_feature1 = ProductFeature.objects.create(product=cls.product1, feature=cls.feature1, value='Value for Feature 1')

    def test_get_products(self):

        response = self.client.get('/api/v1/products/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 3)

    def test_get_reteieve_product(self):
        response = self.client.get(f'/api/v1/products/{self.product1.id}/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 12)

    def test_add_product_to_basket(self):
        response = self.client.post('/auth/jwt/create/', data={
            'username': self.user1_username,
            'password':self.user1_password
        })

        self.assertEquals(response.status_code, 200)
        token = response.data['access']

        response = self.client.get(f'/api/v1/products/{self.product1.id}/add-to-basket/')

        self.assertEquals(response.status_code, 401)

        response = self.client.get(f'/api/v1/products/{self.product1.id}/add-to-basket/',
                                   headers={'Authorization': f'JWT {token}'})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['status'], 'product add to basket')

        self.assertTrue(Basket.objects.filter(user_id=self.user1.id).exists())



