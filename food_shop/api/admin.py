from django.contrib import admin

from .models import Category, CustomUser, Product, ShoppigCart, Subcategory


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('id',)


class ShoppigCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount')
    list_filter = ('user',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ShoppigCart, ShoppigCartAdmin)
