from django.db.models import Min, Count
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.translation import gettext_lazy as _
from django.views import generic

from products.models import Category, Product
from shops.models import Offer


class CategoriesListView(generic.ListView):
    """ Представление для отображения меню категорий каталога """
    model = Category
    template_name = 'products/categories.html'
    context_object_name = 'categories'


class ProductsByCategoryView(generic.ListView):
    """ Представление для отображения каталога товаров """
    model = Offer
    template_name = 'products/products.html'
    context_object_name = 'offers'
    paginate_by = 20

    def get_queryset(self):
        self.category = Category.objects.get(id=self.kwargs['pk'])
        queryset = Offer.objects.select_related('shop', 'product').filter(product__category=self.category).order_by(
            '-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.category
        return context


class ProductDetailView(generic.DetailView):
    """ Представление для отображения детальной страницы продукта """
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product.objects.annotate(
            min_price=Min('offers__price')).annotate(num_reviews=Count('offers__reviews')).prefetch_related(
            'product_properties', 'product_images', 'offers', 'offers__reviews'), pk=kwargs['object'].pk
        )
        context['default_alt'] = _('Изображение продукта')
        context['categories'] = get_list_or_404(Category)
        return context
