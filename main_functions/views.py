from django.db import transaction
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View

from .models import Conditioner, Invertor, Category, LatestProducts, Customer, Cart, CartProduct
# from .mixins import CategoryDetailMixin, CartMixin
# from .forms import OrderForm
# from .utils import recalc_cart


def test_view(request):
    return render(request, 'base.html', {})


class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'conditioner': Conditioner,
        'invertor': Invertor
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['ct_model'] = self.model._meta.model_name
    #     context['cart'] = self.cart
    #     return context
