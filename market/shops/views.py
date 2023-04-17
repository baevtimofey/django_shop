from django.views.generic import ListView

from .models import Banner


class HomeView(ListView):
    """
    Представление главной страницы.
    Пока получает только активные баннеры.
    """
    model = Banner
    queryset = Banner.objects.get_active_banners()
    template_name = 'shops/index.html'
    context_object_name = 'banners'
