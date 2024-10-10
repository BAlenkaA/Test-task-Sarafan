from django.contrib import admin

from apps.categories.models import Category, Subcategory


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SubcategoryInline]
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'parent_category')
    search_fields = ('title',)

    def parent_category(self, obj):
        return obj.category.title if obj.category else 'Нет'

    parent_category.short_description = 'Родительская категория'
