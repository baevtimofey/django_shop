from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, ListView

from account.models import HistorySearch
from order.models import Order
from shops.models import Shop
from users.models import User
from .services import change_profile, ShopManager


class AccountUser(DetailView):
    """Представления для отображения информации о пользователе на странице аккаунта. """

    template_name = 'account/account.j2'
    context_object_name = 'user'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)
        context['last_order'] = Order.objects.select_related('user').filter(user=self.request.user).last()
        if hasattr(user, 'shop'):
            context['shop'] = True
            return context
        context['shop'] = False
        return context


class ProfileUser(LoginRequiredMixin, SuccessMessageMixin, View):
    """Представления для редактирования профиля пользователя."""

    template_name = 'account/profile.j2'

    def get_success_url(self):
        """Возвращаемый URL при успешном выполнении методов."""
        return reverse('account:profile_user', kwargs={'pk': self.kwargs['pk']})

    def get_queryset(self):
        """Queryset модели пользователя."""
        return get_object_or_404(User, pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        """Получение страницы для редактирования профиля."""
        context = {
            'user': self.get_queryset()
        }
        return render(self.request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        """Метод изменения данных пользователя."""
        data = self.request.POST

        if self.request.FILES:
            file = self.request.FILES['avatar']
            info = change_profile(data=data, user_id=self.request.user.pk, file=file)
        else:
            info = change_profile(data=data, user_id=self.request.user.pk)

        messages.add_message(self.request, messages.INFO, info)
        return HttpResponseRedirect(self.get_success_url())


class RegShopView(SuccessMessageMixin, View):
    """Представление для регистрации магазина."""

    template_name = 'account/reg_shop.j2'

    def get_success_url(self):
        """Возвращаемый URL при успешном выполнении методов."""
        return reverse('account:account_user', kwargs={'pk': self.kwargs['pk']})

    def get(self, request, *args, **kwargs):
        """Получение страницы для добавления магазина."""
        return render(self.request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        """Добавление магазина."""
        data = self.request.POST
        user_pk = self.request.user.pk

        shop = ShopManager(data=data, user_pk=user_pk)
        shop_create = shop.create()

        messages.add_message(self.request, messages.INFO, shop_create)
        return HttpResponseRedirect(self.get_success_url())


class UpdateShopView(SuccessMessageMixin, View):
    """Представление для редактирования магазина."""

    template_name = 'account/update_shop.j2'

    def get_object(self, queryset=None):
        """Возвращение объекта магазина."""
        return get_object_or_404(Shop, user_id=self.kwargs.get('pk'))

    def get_success_url(self):
        """Возвращаемый URL при успешном выполнении методов."""
        return reverse_lazy('account:update_shop', kwargs={'pk': self.kwargs['pk']})

    def get(self, request, *args, **kwargs):
        """Получение страницы для редактирования магазина."""
        context = {
            'shop': self.get_object()
        }
        return render(self.request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        """Редактирование магазина."""
        data = self.request.POST
        user_pk = self.request.user.pk

        shop = ShopManager(data=data, user_pk=user_pk)
        shop_update = shop.update()

        messages.add_message(self.request, messages.INFO, shop_update)
        return HttpResponseRedirect(self.get_success_url())


class HistorySearchView(ListView):
    """ Представление для отображения страницы истории просмотров пользователя """
    template_name = 'account/history.j2'
    context_object_name = 'history'

    def get_queryset(self):
        queryset = HistorySearch.objects.get(user=self.request.user.pk)
        return queryset
