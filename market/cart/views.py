from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic.base import RedirectView, TemplateView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from cart.cart import Cart
from cart.models import Order
from cart.forms import UserForm, DeliveryForm, PaymentForm, CommentForm
from shops.models import Offer


class CartView(TemplateView):
    template_name = 'cart/cart1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = Cart(self.request)
        context['cart_items'] = cart_items
        return context


class AddToCartView(RedirectView):
    url = reverse_lazy('cart:cart')

    def get_redirect_url(self, *args, **kwargs):
        product_id = self.kwargs['product_id']
        quantity = int(self.request.GET.get('quantity', 1))
        cart = Cart(self.request)
        offer = Offer.objects.get(id=product_id)
        cart.add(offer=offer, quantity=quantity, update_quantity=False)
        return super().get_redirect_url(*args, **kwargs)


class DeleteToCartView(RedirectView):
    url = reverse_lazy('cart:cart')

    def get_redirect_url(self, *args, **kwargs):
        product_id = self.kwargs['product_id']
        quantity = int(self.request.GET.get('quantity', -1))
        cart = Cart(self.request)
        offer = Offer.objects.get(id=product_id)
        cart.add(offer=offer, quantity=quantity, update_quantity=False)
        return super().get_redirect_url(*args, **kwargs)


class RemoveFromCartView(RedirectView):
    url = reverse_lazy('cart:cart')

    def get_redirect_url(self, *args, **kwargs):
        product_id = self.kwargs['product_id']
        cart = Cart(self.request)
        offer = Offer.objects.get(id=product_id)
        cart.remove(offer=offer)
        return super().get_redirect_url(*args, **kwargs)


class Step1View(LoginRequiredMixin, FormView):
    template_name = 'order/step1.html'
    form_class = UserForm
    success_url = reverse_lazy('cart:step2')
    login_url = reverse_lazy('users:register_user')

    def get_initial(self):
        user = self.request.user
        full_name = f"{user.last_name} {user.surname} {user.first_name}"
        return {'full_name': full_name, 'email': user.email, 'phone_number': user.phone_number}

    def form_valid(self, form):
        user_data = {'full_name': form.cleaned_data['full_name'],
                     'email': form.cleaned_data['email'],
                     'phone_number': form.cleaned_data['phone_number']}
        cart = Cart(self.request)
        cart.add_user_data(form)
        return super().form_valid(form)


class Step2View(LoginRequiredMixin, FormView):
    template_name = 'order/step2.html'
    form_class = DeliveryForm
    success_url = reverse_lazy('cart:step3')

    def form_valid(self, form):
        shipping_data = {
            'delivery_option': form.cleaned_data['delivery_option'],
            'delivery_address': form.cleaned_data['delivery_address'],
            'delivery_city': form.cleaned_data['delivery_city']
        }

        cart = Cart(self.request)
        cart.add_shipping_data(form)

        return super().form_valid(form)


class Step3View(LoginRequiredMixin, FormView):
    template_name = 'order/step3.html'
    form_class = PaymentForm
    success_url = reverse_lazy('cart:step4')

    def form_valid(self, form):
        payment_data = {
            'payment_option': form.cleaned_data['payment_option'],
        }
        cart = Cart(self.request)
        cart.add_payment_data(form)
        return super().form_valid(form)


class Step4View(LoginRequiredMixin, CreateView):
    model = Order
    form_class = CommentForm
    template_name = 'order/step4.html'
    success_url = reverse_lazy('cart:success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['order_items'] = cart
        context['user_data'] = cart.get_user_data()
        context['shipping_data'] = cart.get_shipping_data()
        context['payment_data'] = cart.get_payment_data()

        return context

    def form_valid(self, form):
        cart = Cart(self.request)

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.full_name = cart.get_user_data()['full_name']
            self.object.delivery_option = cart.get_shipping_data()['delivery_option']
            self.object.delivery_address = cart.get_shipping_data()['delivery_address']
            self.object.delivery_city = cart.get_shipping_data()['delivery_city']
            self.object.payment_option = cart.get_payment_data()['payment_option']
            self.object.comment = form.cleaned_data['comment']
            self.object.save()
            self.object.add_items_from_cart(cart)
            cart.clear()

        return super().form_valid(form)


def success_message(request):
    context = {}
    return render(request, 'order/payment.html', context)
