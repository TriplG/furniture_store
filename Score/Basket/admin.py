from django.contrib import admin
from .models import *


class MaterialAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",), 'image_80_80': ("image",)}


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(Basket_Products)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Client)
admin.site.register(News, NewsAdmin)
admin.site.register(Coments)
admin.site.register(Order)
admin.site.register(StatusOrder)
admin.site.register(OrderProducts)
admin.site.register(MailingList)











