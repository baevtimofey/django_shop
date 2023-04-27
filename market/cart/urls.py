from django.urls import path
from cart.views import CartView, AddToCartView, RemoveFromCartView, DeleteToCartView, Step1View, Step2View, Step3View, \
    Step4View, success_message

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<int:product_id>', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:product_id>', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('delete/<int:product_id>', DeleteToCartView.as_view(), name='delete_from_cart'),
    path('step1/', Step1View.as_view(), name='step1'),
    path('step2/', Step2View.as_view(), name='step2'),
    path('step3/', Step3View.as_view(), name='step3'),
    path('step4/', Step4View.as_view(), name='step4'),
    path('success/', success_message, name='success'),
]
