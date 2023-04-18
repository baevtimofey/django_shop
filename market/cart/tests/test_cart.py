from django.test import TestCase, Client
from products.models import *
from cart.cart import *
from users.models import User


class CartTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.property = Property.objects.create(name='Property 1')
        cls.category = Category.objects.create(name='Category 1', description="Description 1")
        cls.product = Product.objects.create(name='Product 1', category=cls.category)
        ProductProperty.objects.create(product=cls.product, property=cls.property, value=1)
        cls.product.property.add(cls.property)
        cls.shop = Shop.objects.create(name='Shop 1')
        Offer.objects.create(product=cls.product, shop=cls.shop, price=10.0)
        cls.shop.products.add(cls.product)
        cls.offer = Offer.objects.create(shop=cls.shop, product=cls.product, price=100)
        cls.session = {}
        cls.client = Client()
        cls.request = cls.client.request().wsgi_request
        cls.request.session.update(cls.session)
        cls.cart = Cart(cls.request)

    def test_add_to_cart(self):
        self.cart.add(self.offer)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.get_total_price(), self.offer.price)

    def test_update_cart(self):
        self.cart.add(self.offer)
        self.cart.add(self.offer, quantity=2, update_quantity=True)

        self.assertEqual(len(self.cart), 2)
        self.assertEqual(self.cart.get_total_price(), self.offer.price * 2)

    def test_remove_from_cart(self):
        self.cart.add(self.offer)
        self.cart.remove(self.offer)

        self.assertEqual(len(self.cart), 0)
        self.assertEqual(self.cart.get_total_price(), Decimal('0'))

    def test_clear_cart(self):
        self.cart.add(self.offer)
        self.cart.remove(self.offer)
        self.cart.clear()

        self.assertEqual(len(self.cart), 0)
        self.assertEqual(self.cart.get_total_price(), Decimal('0'))