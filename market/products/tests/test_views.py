import os

from config.settings import FIXTURE_DIRS
from django.db.models import Min, Count
from django.db.models import Q
from django.shortcuts import get_list_or_404
from django.test import TestCase, Client
from django.test import signals
from django.urls import reverse
from jinja2 import Template as Jinja2Template
from products.models import Category, Product
from shops.models import Offer

ORIGINAL_JINJA2_RENDERER = Jinja2Template.render


def instrumented_render(template_object, *args, **kwargs):
    """ Переопределение метода рендеринга шаблонов Jinja2 """

    context = dict(*args, **kwargs)
    signals.template_rendered.send(
        sender=template_object,
        template=template_object,
        context=context
    )
    return ORIGINAL_JINJA2_RENDERER(template_object, *args, **kwargs)


Jinja2Template.render = instrumented_render


class ProductsByCategoryViewTest(TestCase):
    """ Тестирование представления для отображения товаров конкретной категории """

    fixtures = [
        "004_groups.json",
        "005_users.json",
        "010_shops.json",
        "015_categories.json",
        "020_products.json",
        "030_offers.json",
    ]

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.get(id=15)
        self.offers = Offer.objects.select_related('shop', 'product').filter(product__category=self.category)
        self.url = reverse("products:products_by_category", kwargs={'pk': self.category.pk})
        self.response = self.client.get(self.url)

    def test_view_returns_correct_HTTP_status(self):
        """ Тестирование возврата корректного http-кода при открытии страницы товаров конкретной категории """

        self.assertEqual(self.response.status_code, 200)

    def test_view_renders_desired_template(self):
        """ Тестирование испоьзования ожидаемого шаблона для рендеринга страницы """

        self.assertTemplateUsed(self.response, "products/products.j2")

    def test_products_by_category_count_is_correct(self):
        """ Тестирование количества выводимых товаров, принадлежащих конкретной категории """

        self.assertTrue(len(self.response.context_data['filter'].qs) == self.offers.count())

    def test_products_filtering_by_name(self):
        """ Тестирование корректности фильтрации товаров по названию """

        response = self.client.get(self.url + "?price_min=&price_max=&product_name=лопата#")
        desired_offers = self.offers.filter(product__name__icontains='лопата')
        for offer in desired_offers:
            self.assertContains(response, offer.product.name)
        undesired_offers = self.offers.exclude(product__name__icontains='лопата')
        for offer in undesired_offers:
            self.assertNotContains(response, offer.product.name)

    def test_products_filtering_by_price(self):
        """ Тестирование корректности фильтрации товаров по цене """

        response = self.client.get(self.url + "?price_min=300&price_max=600&product_name=#")
        desired_offers = self.offers.filter(price__gte=300, price__lte=600)
        for offer in desired_offers:
            self.assertContains(response, offer.product.name)
        undesired_offers = self.offers.filter(Q(price__gte=600) | Q(price__lte=300))
        for offer in undesired_offers:
            self.assertNotContains(response, offer.product.name)

    def test_products_filtering_by_shop(self):
        """ Тестирование корректности фильтрации товаров по названию магазина """

        response = self.client.get(self.url + "?price_min=&price_max=&product_name=&multiple_shops=1#")
        desired_offers = self.offers.filter(shop__id__in=['1'])
        for offer in desired_offers:
            self.assertContains(response, offer.product.name)
        undesired_offers = self.offers.exclude(shop__id__in=['1'])
        for offer in undesired_offers:
            self.assertNotContains(response, offer.product.name)

    def test_products_filtering_by_name_and_price(self):
        """ Тестирование корректности фильтрации товаров по названию товара и цене одновременно """

        response = self.client.get(self.url + "?price_min=400&price_max=600&product_name=лопата#")
        desired_offers = self.offers.filter(price__gte=400, price__lte=600, product__name__icontains='лопата')
        for offer in desired_offers:
            self.assertContains(response, offer.product.name)
        undesired_offers = self.offers.exclude(price__gte=400, price__lte=600, product__name__icontains='лопата')
        for offer in undesired_offers:
            self.assertNotContains(response, offer.product.name)

    def test_products_filtering_by_name_and_shop(self):
        """ Тестирование корректности фильтрации товаров по названию товара и названию магазина одновременно """

        response = self.client.get(self.url + "?price_min=&price_max=&product_name=лопата&multiple_shops=1#")
        desired_offers = self.offers.filter(shop__id__in=['1'], product__name__icontains='лопата')
        for offer in desired_offers:
            self.assertContains(response, offer.product.name)
        undesired_offers = self.offers.exclude(shop__id__in=['1'], product__name__icontains='лопата')
        for offer in undesired_offers:
            self.assertNotContains(response, offer.product.name)

    def test_products_filtering_by_price_and_shop(self):
        """ Тестирование корректности фильтрации товаров по названию магазина и цене одновременно """

        response = self.client.get(self.url + "?price_min=500&price_max=600&product_name=&multiple_shops=1#")
        desired_offers = self.offers.filter(shop__id__in=['1'], price__gte=500, price__lte=600)
        for offer in desired_offers:
            self.assertContains(response, offer.product.name)
        undesired_offers = self.offers.exclude(shop__id__in=['1'], price__gte=500, price__lte=600)
        for offer in undesired_offers:
            self.assertNotContains(response, offer.product.name)

    def test_products_filtering_by_name_and_price_and_shop(self):
        """ Тестирование корректности фильтрации товаров по названию товара, названию магазина и цене одновременно """

        response = self.client.get(self.url + "?price_min=500&price_max=600&product_name=лопата&multiple_shops=1#")
        desired_offers = self.offers.filter(product__name__icontains='лопата', shop__id__in=['1'], price__gte=500,
                                            price__lte=600)
        for offer in desired_offers:
            self.assertContains(response, offer.product.name)
        undesired_offers = self.offers.exclude(product__name__icontains='лопата', shop__id__in=['1'], price__gte=500,
                                               price__lte=600)
        for offer in undesired_offers:
            self.assertNotContains(response, offer.product.name)


class ProductDetailViewTest(TestCase):
    """ Тестирование представления для отображения детальной страницы продукта """
    fixtures = os.listdir(*FIXTURE_DIRS)

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.annotate(
            min_price=Min('offers__price')).annotate(num_reviews=Count('product_reviews')).prefetch_related(
            'product_properties', 'product_images', 'offers', 'product_reviews').get(id=6)
        self.response = self.client.get(self.product.get_absolute_url())

    def test_view_returns_correct_HTTP_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_renders_desired_template(self):
        self.assertTemplateUsed(self.response, "products/product.html")

    def test_context_is_correct(self):
        self.assertEqual(self.response.context['default_alt'], 'Изображение продукта')
        self.assertEqual(self.response.context['categories'], get_list_or_404(Category))
        self.assertEqual(self.response.context['product'], self.product)
