from django.test import TestCase
from shops.models import Shop, Offer, Banner
from products.models import Product, Property
import os


class ShopModelTest(TestCase):
    """Класс тестов модели Магазин"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = Property.objects.create(name='тестовая характеристика')
        cls.product = Product.objects.create(
            name='тестовый продукт',
        )
        cls.product.property.set([cls.property])
        cls.shop = Shop.objects.create(name='тестовый магазин')
        cls.offer = Offer.objects.create(shop=cls.shop, product=cls.product, price=25)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        ShopModelTest.property.delete()
        ShopModelTest.product.delete()
        ShopModelTest.shop.delete()
        ShopModelTest.offer.delete()

    def test_verbose_name(self):
        shop = ShopModelTest.shop
        field_verboses = {
            'name': 'название',
            'products': 'товары в магазине',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(shop._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        shop = ShopModelTest.shop
        max_length = shop._meta.get_field('name').max_length
        self.assertEqual(max_length, 512)


class OfferModelTest(TestCase):
    """Класс тестов модели Предложение магазина"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = Product.objects.create(
            name='тестовый продукт',
        )
        cls.shop = Shop.objects.create(name='тестовый магазин')
        cls.offer = Offer.objects.create(shop=cls.shop, product=cls.product, price=35)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        OfferModelTest.product.delete()
        OfferModelTest.shop.delete()
        OfferModelTest.offer.delete()

    def test_verbose_name(self):
        offer = OfferModelTest.offer
        field_verboses = {
            'price': 'цена',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(offer._meta.get_field(field).verbose_name, expected_value)

    def test_price_max_digits(self):
        offer = OfferModelTest.offer
        max_digits = offer._meta.get_field('price').max_digits
        self.assertEqual(max_digits, 10)

    def test_price_decimal_places(self):
        offer = OfferModelTest.offer
        decimal_places = offer._meta.get_field('price').decimal_places
        self.assertEqual(decimal_places, 2)


class BannerManagerTestCase(TestCase):
    """Класс тестов менеджера баннеров"""
    def setUp(self):
        Banner.objects.create(
            title='Banner 1',
            description='Banner 1 description',
            is_active=True,
            link='https://example.com'
        )
        Banner.objects.create(
            title='Banner 2',
            description='Banner 2 description',
            is_active=True,
            link='https://example.com'
        )
        Banner.objects.create(
            title='Banner 3',
            description='Banner 3 description',
            is_active=False,
            link='https://example.com'
        )
        Banner.objects.create(
            title='Banner 4',
            description='Banner 4 description',
            is_active=True,
            link='https://example.com'
        )

    def test_get_active_banners(self):
        active_banners = Banner.objects.get_active_banners()
        self.assertEqual(len(active_banners), 3)
        for banner in active_banners:
            self.assertTrue(banner.is_active)

    def test_active_banners_random_order(self):
        active_banners_1 = Banner.objects.get_active_banners()
        active_banners_2 = Banner.objects.get_active_banners()
        self.assertNotEqual(active_banners_1, active_banners_2)


class BannerTestCase(TestCase):
    """Класс тестов модели Баннер"""
    def test_create_banner(self):
        banner = Banner.objects.create(
            image='banners/banner.jpg',
            title='MAVIC PRO 5 MINI DRONE',
            description='Get the best phone you ever seen with modern Windows OS plus 70% Off this summer',
            is_active=True,
            link='https://example.com'
        )

        self.assertEqual(os.path.basename(banner.image.path), 'banner.jpg')
        self.assertEqual(banner.title, 'MAVIC PRO 5 MINI DRONE')
        self.assertEqual(banner.description, 'Get the best phone you ever seen with modern Windows OS plus 70% Off '
                                             'this summer')
        self.assertTrue(banner.is_active)
        self.assertEqual(banner.link, 'https://example.com')
        self.assertEqual(str(banner), 'MAVIC PRO 5 MINI DRONE')
