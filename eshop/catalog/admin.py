from django.contrib import admin
from django.utils.safestring import mark_safe

from catalog.models import Category, Product, Manufacturer


class CategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ['parent_cat', ]
    list_display = ['id', 'get_image', 'parent_cat', 'name', 'slug', 'is_active', ]
    list_display_links = ['id', "get_image", 'parent_cat', 'name', ]
    search_fields = ['name', 'description', 'slug', ]
    list_editable = ['is_active', ]
    list_filter = ['is_active', 'parent_cat', ]
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at', 'created_by', 'updated_by']
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='50'")

    get_image.short_description = "Img"


class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ['category', 'manufacturer', 'created_by', 'updated_by', ]
    list_display = ['id', 'get_image', 'name', 'category', 'manufacturer', 'sku',
                     'price', 'discount', 'quantity', 'attributes', 'is_active',]
    list_display_links = ['id', "get_image", 'category', 'name', 'manufacturer', 'sku', ]
    search_fields = ['name', 'description', 'slug', ]
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at', 'created_by', 'updated_by']
    list_editable = ['is_active', ]

    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='50'")

    get_image.short_description = "Img"


class ManufacturerAdmin(admin.ModelAdmin):
    raw_id_fields = ['created_by', 'updated_by', ]
    list_display = ['id', 'name', 'slug', 'is_active', ]
    list_editable = ['is_active', ]
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at', 'created_by', 'updated_by']
    save_on_top = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
