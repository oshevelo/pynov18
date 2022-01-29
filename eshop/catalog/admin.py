from django.contrib import admin

from catalog.models import Categories, Products, Manufacturer


class CategoriesAdmin(admin.ModelAdmin):
    pass


class ProductsAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ManufacturerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
