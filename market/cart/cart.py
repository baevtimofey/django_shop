from decimal import Decimal
from django.conf import settings
from shops.models import Offer


class Cart:
    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_user_data(self, form):
        """
        Добавить данные пользователя в корзину.
        """
        self.session['user_data'] = form.cleaned_data
        self.save()

    def add_shipping_data(self, form):
        """
        Добавить данные о доставке в корзину.
        """
        self.session['shipping_data'] = form.cleaned_data
        self.save()

    def add_payment_data(self, form):
        """
        Добавить данные об оплате в корзину.
        """
        self.session['payment_data'] = form.cleaned_data
        self.save()

    def get_user_data(self):
        """
        Получить данные пользователя из корзины.
        """
        return self.session.get('user_data')

    def get_shipping_data(self):
        """
        Получить данные о доставке из корзины.
        """
        return self.session.get('shipping_data')

    def get_payment_data(self):
        """
        Получить данные об оплате из корзины.
        """
        return self.session.get('payment_data')

    def add(self, offer, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        if not offer:
            return
        product_id = str(offer.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(offer.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Сохранение изменений корзины.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        if 'modified' not in self.session:
            self.session['modified'] = True
        else:
            self.session.modified = True

    def remove(self, offer):
        """
        Удаление товара из корзины.
        """
        if not offer:
            return
        product_id = str(offer.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        offer_ids = self.cart.keys()
        offers = Offer.objects.filter(id__in=offer_ids)
        for offer in offers:
            self.cart[str(offer.id)]['offer'] = offer

        for item in self.cart.values():
            if 'offer' not in item:
                continue
            item['price'] = Decimal(item['offer'].price)
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        """
        Удаление корзины из сессии.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
