from django.test import TestCase
from products.models import *
from cart.cart import *


class CartTestCase(TestCase):
    def setUp(self):
        self.property1 = Property.objects.create(name='Property 1')
        self.category = Category.objects.create(name='Category 1', description="Description 1")
        self.product = Product.objects.create(name='Product 1', category=self.category)
        self.productproperty = ProductProperty.objects.create(product=self.product, property=self.property1, value=1)
        self.product.property.add(self.property1)
        self.shop = Shop.objects.create(name='Shop 1')
        self.shop.products.add(self.product)
        self.offer = Offer.objects.create(shop=self.shop, product=self.product, price=100)
        self.cart = Cart(self.client.session)

    def test_add_to_cart(self):
        self.cart.add(self.product)

        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.get_total_price(), self.offer.price)

    def test_update_cart(self):
        self.cart.add(self.product)
        self.cart.add(self.product, quantity=2, update_quantity=True)

        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.get_total_price(), self.offer.price * 3)

    def test_remove_from_cart(self):
        self.cart.add(self.product)
        self.cart.remove(self.product)

        self.assertEqual(len(self.cart), 0)
        self.assertEqual(self.cart.get_total_price(), Decimal('0'))

    def test_clear_cart(self):
        self.cart.add(self.product)
        self.cart.clear()

        self.assertEqual(len(self.cart), 0)
        self.assertEqual(self.cart.get_total_price(), Decimal('0'))
