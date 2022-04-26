from django.urls import path
from .views import *

from django.conf.urls.static import static
from Score import settings


urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('basket/<str:user_name>/', basket, name='basket'),
    path('need_to_auth/', need_to_auth),
    path('add_to_cart_home/<int:id_prod>/', add_to_cart_home, name='add_to_cart_home'),
    path('base/', base, name='base'),
    path('product_list/<slug:slug_cat>/<slug:slug_mat>/<int:var_more_local>/', product_list, name='product_list'),
    path('news/', news, name='news'),
    path('message/', message, name='message'),
    path('product/<int:id_product>/', product, name='product'),
    path('delete_cart_product/<int:id_prod>/', delete_cart_product, name='delete_cart_product'),
    path('product_more/<slug:slug_cat>/<slug:slug_mat>/<int:var_more_local>/', product_more, name='product_more'),
    path('news_detail/<slug:slug_new>/', news_detail, name='news_detail'),
    path('write_coment/<slug:slug_new>', write_coment, name='write_coment'),
    path('issue_order/', issue_order, name='issue_order'),
    path('add_order/', AddOrder.as_view(), name='add_order'),
    path('order_all/', OrderAll.as_view(), name='order_all'),
    path('add_mail_list/', AddMailList.as_view(), name='add_mail_list'),
    path('registration/', Registration.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('add_registration/', AddRegistration.as_view(), name='add_registration'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
