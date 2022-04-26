from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import View

import smtplib

from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.db.models import *


var_more = 1


def base(request):
    products = Product.objects.all()
    # basket = Basket.objects.get(owner=request.user)

    context = {
        'title': 'Главная страница',
        'products': products,

    }
    return render(request, 'Basket/base.html', context=context)


def index(request):
    products = Product.objects.all()
    # basket = Basket.objects.get(owner=request.user)

    context = {
        'title': 'Главная страница',
        'products': products,
        # 'user': user,
        # 'basket': basket
    }
    return render(request, 'Basket/index.html', context=context)


def about(request):
    context = {
        'title': 'Информация'
    }
    return render(request, 'Basket/about.html', context=context)


def basket(request, user_name):
    # products = Basket_Products.objects.filter(user=request.user)
    # basket = Basket.objects.get(owner=request.user)
    basket_products = Basket_Products.objects.filter(user=request.user)

    context = {
        'basket_products': basket_products,
        'title': 'Корзина',
    }
    return render(request, 'Basket/basket.html', context=context)


def need_to_auth(request):
    context = {}
    return render(request, 'Basket/need_to_auth.html', context=context)


def add_to_cart_home(request, id_prod):
    basket_add_to_cart_home = Basket.objects.get(owner=request.user)
    product_add_to_cart_home = Product.objects.get(pk=id_prod)
    qty = int(request.POST.get('qty'))
    for i in range(qty):
        basket_products_add = Basket_Products.objects.create(
            user=basket_add_to_cart_home.owner, basket=basket_add_to_cart_home, product=product_add_to_cart_home
        )
        basket_add_to_cart_home.amount_products += 1
        basket_add_to_cart_home.final_price += product_add_to_cart_home.price
        basket_add_to_cart_home.save()
        # return HttpResponseRedirect(f'/basket/{request.user}/')
    return HttpResponseRedirect(f'/basket/{request.user}/')


def product(request, id_product):
    product1 = Product.objects.get(pk=id_product)

    context = {
        'product1': product1,
    }
    return render(request, 'Basket/product.html', context=context)


# def product_list(request):
#     products = Product.objects.all()
#     category = Category.objects.all()
#     material = Material.objects.all()
#     context = {
#         'products': products,
#         'category': category,
#         'material': material,
#         'title': 'Продукты'
#     }
#     return render(request, 'Basket/product_list.html', context=context)


def news(request):
    novelty_0_4 = News.objects.all()[: 4]
    search_query = request.GET.get('search', '')
    if search_query:
        novelty = News.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    else:
        novelty = News.objects.all()

    coments = Coments.objects.filter(news=novelty)
    context = {
        'novelty_0_4': novelty_0_4,
        'title': 'Новости',
        'novelty': novelty,
        'coments': coments,
    }
    return render(request, 'Basket/news.html', context=context)


def news_detail(request, slug_new):

    novelty = News.objects.get(slug=slug_new)
    novelty_0_4 = News.objects.all()[: 4]
    coments = Coments.objects.filter(news=novelty)
    count_com = coments.count()
    context = {
        'title': novelty.title,
        'novelty': novelty,
        'novelty_0_4': novelty_0_4,
        'coments': coments,
        'count_com': count_com,

    }
    return render(request, 'Basket/news_detail.html', context=context)


def write_coment(request, slug_new):
    comment = request.POST.get('comment')
    novelty = News.objects.get(slug=slug_new)
    comment_add = Coments.objects.create(
        news=novelty, user=request.user, message=comment
    )
    return HttpResponseRedirect(f'/news_detail/{slug_new}/')


def reply_coment(request, slug_new):
    comment = request.POST('comment', f'{request.user}, ')
    return HttpResponseRedirect(f'/news_detail/{slug_new}#text/')


def message(request):
    context = {
        'title': 'Сообщение'
    }
    return render(request, 'Basket/message.html', context=context)


def delete_cart_product(request, id_prod):
    basket_product = Basket_Products.objects.get(pk=id_prod)
    obj_basket = Basket.objects.get(owner=request.user)
    obj_basket.amount_products -= 1
    obj_basket.final_price -= basket_product.product.price
    obj_basket.save()
    basket_product.delete()

    return HttpResponseRedirect(f'/basket/{request.user}/')


def product_more(request, slug_cat, slug_mat, var_more_local):
    products = Product.objects.all()
    if (products.count() - var_more_local) >= 5:
        var_more_local += 5
    else:
        var_more_local += (products.count() - var_more_local)
    return HttpResponseRedirect(f'/product_list/{slug_cat}/{slug_mat}/{var_more_local}/')


def product_list(request, slug_cat, slug_mat, var_more_local):
    search_query = request.GET.get('search', '')
    if Category.objects.filter(slug=slug_cat).count() == 1 and Material.objects.filter(slug=slug_mat).count() == 1:
        category = Category.objects.get(slug=slug_cat)
        material = Material.objects.get(slug=slug_mat)
        cat_url = category.slug
        mat_url = material.slug
        cat_name = category.name
        mat_name = material.name
        if search_query:
            products = Product.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query), category=category, material=material)
        else:
            products = Product.objects.filter(category=category, material=material)
    elif Category.objects.filter(slug=slug_cat).count() == 0 and Material.objects.filter(slug=slug_mat).count() == 1:
        material = Material.objects.get(slug=slug_mat)
        category = Category.objects.all()
        cat_url = 'net_categoriy'
        mat_url = material.slug
        cat_name = 'Нет категории'
        mat_name = material.name
        if search_query:
            products = Product.objects.filter(Q(title__icontains=search_query), material=material)
        else:
            products = Product.objects.filter(material=material)
    elif Category.objects.filter(slug=slug_cat).count() == 1 and Material.objects.filter(slug=slug_mat).count() == 0:
        material = Material.objects.all()
        category = Category.objects.get(slug=slug_cat)
        cat_url = category.slug
        mat_url = 'lyuboy_material'
        cat_name = category.name
        mat_name = 'Любой материал'
        if search_query:
            products = Product.objects.filter(Q(title__icontains=search_query), category=category)
        else:
            products = Product.objects.filter(category=category)
    elif Category.objects.filter(slug=slug_cat).count() == 0 and Material.objects.filter(slug=slug_mat).count() == 0:
        category = Category.objects.all()
        material = Material.objects.all()
        cat_url = 'net_categoriy'
        mat_url = 'lyuboy_material'
        cat_name = 'Нет категории'
        mat_name = 'Любой материал'
        if search_query:
            products = Product.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        else:
            products = Product.objects.all()

    category_all = Category.objects.all()
    material_all = Material.objects.all()


    more_number = var_more_local

    products_pagin = products.all()[:more_number]

    context = {
        'products': products,
        'category': category,
        'material': material,
        'title': 'Продукты',
        'cat_url': cat_url,
        'mat_url': mat_url,
        'mat_name': mat_name,
        'cat_name': cat_name,
        'category_all': category_all,
        'material_all': material_all,
        'base_cat': 'net_categoriy',
        'base_mat': 'lyuboy_material',
        'products_pagin': products_pagin,
        'more_number': more_number

    }
    return render(request, 'Basket/product_list.html', context=context)


def issue_order(request):
    basket = Basket.objects.get(owner=request.user)
    basket_products = Basket_Products.objects.filter(basket=basket)


    context = {
        'title': 'Оформление заказа',
        'basket': basket,
        'basket_products': basket_products,

    }
    return render(request, 'Basket/issue_order.html', context=context)


class AddOrder(View):
    def post(self, request):
        print(request.POST)
        if 'qwerty' in request.POST:
            delivery = True
        else:
            delivery = False

        # Добавление заказа(Order)
        order_add = Order.objects.create(
            client=request.user, delivery=delivery, message_order=request.POST.get('message'), status_order=StatusOrder.objects.get(status_name='Заказ в пути')
        )
        # Добавление товаров в заказ(OrderProducts)
        bp = Basket_Products.objects.filter(user=request.user)
        lst = []
        for i in bp:
            order_product_add = OrderProducts.objects.create(
                order=order_add, product=i.product
            )
            lst.append(order_product_add)
        order_add.order_products.add(*lst)
        # Очищение корзины
        obj_basket = Basket.objects.get(owner=request.user)
        obj_basket.amount_products = 0
        obj_basket.final_price = 0
        obj_basket.save()
        bp.delete()

        # Обновление данных клиента
        client_update = Client.objects.get(user=request.user)
        client_update.street = request.POST.get('street')
        client_update.house = request.POST.get('house')
        client_update.number_apartment = request.POST.get('number_apartment')
        client_update.mail = request.POST.get('email')
        client_update.number_phone = request.POST.get('nomber')
        client_update.save()
        user = User.objects.get(username=request.user)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        return redirect('/order_all/')


class OrderAll(View):
    def get(self, request):
        order = Order.objects.filter(client=request.user)
        order_products = OrderProducts.objects.filter(order=order)
        sum_order = OrderProducts.objects.aggregate(Sum('product__price')).get('product__price__sum')


        client = Client.objects.get(user=request.user)

        context = {
            'order': order,
            'order_products': order_products,
            'sum_order': sum_order,
            'client': client,
        }

        return render(request, 'Basket/confirmation.html', context=context)


class AddMailList(View):
    def post(self, request):
        print(request.POST)
        print(request.POST.get('MAIL'))
        add_mail = MailingList.objects.create(
            email=request.POST.get('MAIL')
        )

        return redirect('/')


class Registration(View):
    def get(self, request):


        context = {

        }

        return render(request, 'Basket/registration.html', context=context)


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'Basket/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'

        return context

    def get_success_url(self):
        return reverse_lazy('home')


class AddRegistration(View):
    def post(self, request):
        create_user = User.objects.create_user(request.POST.get('name'), request.POST.get('email'), request.POST.get('password'))
        create_user.first_name = request.POST.get('first_name')
        create_user.last_name = request.POST.get('last_name')
        create_user.save()

        create_client = Client.objects.create(
            user=create_user, street=request.POST.get('street'), house=request.POST.get('house'), number_apartment=request.POST.get('apartament'), mail=request.POST.get('email'), number_phone=request.POST.get('numbet_phone')
        )
        print(request.POST)
        return redirect('/login/')
