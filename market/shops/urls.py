from django.urls import path
from shops.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
