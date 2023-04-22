import os

from django.db.models import Min, Count
from django.shortcuts import get_list_or_404
from django.test import TestCase, Client
from django.urls import reverse

from config.settings import FIXTURE_DIRS
from products.models import Category, Product
from shops.models import Offer


class CategoriesListViewTest(TestCase):
    """ Тестирование представления меню категорий каталога"""
    fixtures = [
        "015_categories.json",
    ]

    def setUp(self):
        self.client = Client()
        self.categories = Category.objects.all()
        url = reverse("products:categories_list")
        self.response = self.client.get(url)

    def test_view_returns_correct_HTTP_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_renders_desired_template(self):
        self.assertTemplateUsed(self.response, "products/categories.html")

    def test_categories_count_is_correct(self):
        self.assertTrue(len(self.response.context['categories']) == self.categories.count())


class ProductsByCategoryViewTest(TestCase):
    """ Тестирование представления для отображения товаров конкретной категории """
    fixtures = [
        "005_users.json",
        "015_categories.json",
        "020_products.json",
        "010_shops.json",
        "030_offers.json",
    ]

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.get(id=15)
        self.offers = Offer.objects.select_related('shop', 'product').filter(product__category=self.category)
        url = reverse("products:products_by_category", kwargs={'pk': self.category.pk})
        self.response = self.client.get(url)

    def test_view_returns_correct_HTTP_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_renders_desired_template(self):
        self.assertTemplateUsed(self.response, "products/products.html")

    def test_products_by_category_count_is_correct(self):
        self.assertTrue(len(self.response.context['offers']) == self.offers.count())


class ProductDetailViewTest(TestCase):
    """ Тестирование представления для отображения детальной страницы продукта """
    fixtures = os.listdir(*FIXTURE_DIRS)

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.annotate(
            min_price=Min('offers__price')).annotate(num_reviews=Count('offers__reviews')).prefetch_related(
            'product_properties', 'product_images', 'offers', 'offers__reviews').get(id=6)
        self.response = self.client.get(self.product.get_absolute_url())

    def test_view_returns_correct_HTTP_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_renders_desired_template(self):
        self.assertTemplateUsed(self.response, "products/product.html")

    def test_context_is_correct(self):
        self.assertEqual(self.response.context['default_alt'], 'Изображение продукта')
        self.assertEqual(self.response.context['categories'], get_list_or_404(Category))
        self.assertEqual(self.response.context['product'], self.product)
