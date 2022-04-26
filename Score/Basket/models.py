import sys

from django.db import models
from django.contrib.auth.models import User

from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


class Category(models.Model):
    slug = models.SlugField()
    name = models.CharField(verbose_name='Название категории', max_length=25)

    def __str__(self):
        return self.name


class Material(models.Model):
    slug = models.SlugField()
    name = models.CharField(verbose_name='Название категории', max_length=25)

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    street = models.CharField(verbose_name='', max_length=100)
    house = models.PositiveIntegerField(verbose_name='')
    number_apartment = models.PositiveIntegerField(verbose_name='')
    mail = models.CharField(verbose_name='Электронная почта', max_length=100)
    number_phone = models.CharField(verbose_name='Номер телефона', max_length=100)


class Product(models.Model):
    material = models.ForeignKey(Material, verbose_name='Категория', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название продукта', max_length=25)
    image = models.ImageField(verbose_name='Изображение', null=True)
    description = models.TextField(verbose_name='Описание товара', null=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=9, decimal_places=2)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        new_img = img.convert('RGB')
        resized_new_img = new_img.resize((548, 460), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_img.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile(
            filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        )
        super().save(*args, **kwargs)


class Basket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    amount_products = models.PositiveIntegerField(verbose_name='Количество товаров', default=0)
    final_price = models.PositiveIntegerField(verbose_name='Итоговая цена', default=0)

    def __str__(self):
        return f'Корзина пользователя {self.owner.first_name}'


class Basket_Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    basket = models.ForeignKey(Basket, verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)

    def __str__(self):
        return f'Продукты корзины пользователя {self.user.first_name}'


class News(models.Model):
    slug = models.SlugField()
    time_create = models.DateTimeField()
    image = models.ImageField(upload_to="news/%Y/%m/%d/")
    image_80_80 = models.ImageField(upload_to="image80_80/%Y/%m/%d/", verbose_name='Изображение 80*80')
    title = models.CharField(max_length=255)
    content = models.TextField()


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        image = self.image_80_80
        img = Image.open(image)
        new_img = img.convert('RGB')
        resized_new_img = new_img.resize((80, 80), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_img.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image_80_80.name.split('.'))
        self.image_80_80 = InMemoryUploadedFile(
            filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        )
        super().save(*args, **kwargs)


class Coments(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # number_coment = models.PositiveIntegerField()
    message = models.CharField(verbose_name='', max_length=500)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Сообщение {self.user.username} новости {self.news}'


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    delivery = models.BooleanField(verbose_name='Доставка')
    message_order = models.TextField(verbose_name='Примечания к заказу', null=True)
    status_order = models.ForeignKey('StatusOrder', on_delete=models.CASCADE, verbose_name='Статус заказа')
    order_products = models.ManyToManyField('OrderProducts', verbose_name='Продукты', blank=True, related_name='related_order')

    def __str__(self):
        return f'Заказ №{self.pk}'


class StatusOrder(models.Model):
    status_name = models.CharField(verbose_name='Статус', max_length=25)

    def __str__(self):
        return self.status_name


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title


class MailingList(models.Model):
    email = models.EmailField(verbose_name="Почта")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email