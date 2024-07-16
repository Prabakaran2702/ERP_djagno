from django.contrib import admin
from .models import ProductMaster, Category
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Category', 'is_active')  # Display fields in the admin list view

@admin.register(ProductMaster)
class ProductMasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'published_date', 'category')  # Display fields in the admin list view
    list_filter = ('category',)  # Add filters on the right sidebar based on category
    search_fields = ('name', 'desc', 'category')  # Add a search bar at the top for name and description
