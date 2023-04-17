from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from shops.models import Banner


class HomeViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Класс тестов представления домашней страницы. Тест баннеров."""
        cls.url = reverse('home')
        cls.banner1 = Banner.objects.create(title='Banner 1', is_active=True)
        cls.banner2 = Banner.objects.create(title='Banner 2', is_active=False)
        image = SimpleUploadedFile("banner1.jpg", b"file_content", content_type="image/jpeg")
        cls.banner1.image = image
        cls.banner1.save()

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'shops/index.html')

    def test_view_queryset_only_includes_active_banners(self):
        response = self.client.get(self.url)
        banners = response.context['banners']

        self.assertIn(self.banner1, banners)
        self.assertNotIn(self.banner2, banners)
