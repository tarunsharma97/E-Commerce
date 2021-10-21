from django.contrib import admin
from myshop.models import Carousel, Customer, Product, Category, Cart, Order, Review, Product_Image


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at', ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'brand', 'category', 'size']


@admin.register(Product_Image)
class Product_ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'prod_size']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer',
                    'product', 'quantity', 'payment_option', 'size', 'ordered_date', 'status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'rate', 'created_at']
    readonly_fields = ['created_at', ]
