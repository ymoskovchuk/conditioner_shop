
from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.core.mail import send_mail
import datetime

from .models import Category, Order, CartProduct, Product
from .mixins import *
from .forms import OrderForm, LoginForm, RegistrationForm
from .utils import recalc_cart
from .filters import ProductFilter


def callback_view(request):

    phone = request.POST.get('phone')
    context = {}
    send_mail('Передзвоніть на телефон',
              f'Користувач з телефоном: {phone}  просить передзвонити',
              'ripka.climat@gmail.com',
              ['ripka.climat@gmail.com']
              )
    return HttpResponseRedirect('/')


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart
        }
        return render(request, 'base.html', context)


class ProductDetailView(CartMixin, DetailView):

    category = Product.category
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, DetailView):

    queryset = Category.objects.all()
    category_products = Product.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productfilter = ProductFilter(self.request.GET, queryset=self.category_products)
        self.category_products = productfilter.qs
        context['cart'] = self.cart
        context['category_products'] = self.category_products
        context['category_slug'] = self.get_object().slug
        context['filter'] = productfilter
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'category_detail,html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter()
        return context


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успішно доданий до корзини")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успішно видалений")
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кількість успішно змінена")
        return HttpResponseRedirect('/cart/')


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    def post(self, request, *args, **kwargs):

        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            send_mail(f'Нове замовлення #{new_order.id}',
                      f'Ім*я - {new_order.first_name}, '
                      f'Прізвище - {new_order.last_name}, '
                      f'Номер телефону - {new_order.phone}, '
                      f'Адреса - {new_order.address}, '
                      f'Тип замовлення - {new_order.buying_type}, '
                      f'Дата замовлення - {datetime.datetime.now()}, '
                      f'Товари - {Order.objects.filter(customer=Customer.objects.get(user=request.user)).last().cart.products.all()}, '
                      f'Коментар: {new_order.comment}',
                      'ripka.climat@gmail.com',
                      ['ripka.climat@gmail.com'],
                      fail_silently=False
                      )
            messages.add_message(request, messages.INFO, f"Дякуємо за замовлення! Ми зв'яжемось з вами")
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, 'login.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, 'registration.html', context)


class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        categories = Category.objects.all()
        return render(
            request,
            'profile.html',
            {'orders': orders, 'cart': self.cart, 'categories': categories}
        )


class InstallationView(View):

    def get(self, request, *args, **kwargs):
        return render(request, template_name='installation.html')


class PaymentDeliveryView(View):

    def get(self, request, *args, **kwargs):
        return render(request, template_name='payment_delivery.html')


class ServiceView(View):

    def get(self, request, *args, **kwargs):
        return render(request, template_name='service.html')


class ContactsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, template_name='contacts.html')