from django.contrib import admin
from . import models


# Register your models here.
# admin.site.register(models.cars)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'stock', 'category', 'created_date', 'modified_date', 'is_available']
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ['created_date', 'modified_date']
    search_fields = ['product_name']


class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active']
    list_editable = ['is_active']
    list_filter = ['product', 'variation_category', 'variation_value', 'is_active']
    search_fields = ['product', 'variation_category', 'variation_value']



admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Variation, VariationAdmin)
