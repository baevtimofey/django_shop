from django.test import TestCase
from django.utils import timezone
from cart.models import *


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='ivan', email='ivan@mail.ru', password='Password123')
        self.delivery = Delivery.objects.create(delivery_option='Delivery', express_delivery_fee=500, order_total_for_free_delivery=2000, delivery_fee=200)
        self.property = Property.objects.create(name='Property 1',)
        self.category = Category.objects.create(name='Category 1', description="Description 1")
        self.product = Product.objects.create(name='Product 1', category=self.category,)
        self.product.property.add(self.property)
        self.productproperty = ProductProperty.objects.create(product=self.product, property=self.property, value=1)
        self.shop = Shop.objects.create(name='Shop 1')
        self.shop.products.add(self.product)
        self.offer = Offer.objects.create(shop=self.shop, product=self.product, price=90)
        self.order = Order.objects.create(user=self.user, status='created', delivery=self.delivery, delivery_adress='Novgorod')
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_order_str_method(self):
        expected = f'Order {self.order.id}'
        self.assertEqual(str(self.order), expected)

    def test_order_get_total_cost_method(self):
        expected = self.offer.price * self.order_item.quantity
        self.assertEqual(self.order.get_total_cost(), expected)

    def test_order_save_method(self):
        self.order.status = 'paid'
        self.order.save()
        now = timezone.now()
        self.assertEqual(self.order.payment_date.date(), now.date())

    def test_order_item_str_method(self):
        expected = f'{self.order_item.id}'
        self.assertEqual(str(self.order_item), expected)