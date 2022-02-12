from django.contrib import admin
from imagekit.admin import AdminThumbnail

from catalog.models import Category, Product, Manufacturer, ProductImage, ProductImageRelated


class CategoryAdmin(admin.ModelAdmin):
    admin_thumbnail = AdminThumbnail(image_field='image', template="./templates/catalog/admin/thumbnail.html")
    raw_id_fields = ['parent_cat', 'created_by', 'updated_by', ]
    list_display = ['id', 'admin_thumbnail', 'parent_cat', 'name', 'slug', 'is_active', 'updated_by']
    list_display_links = ['id', 'parent_cat', 'name', ]
    search_fields = ['name', 'description', 'slug', ]
    list_editable = ['is_active', ]
    list_filter = ['is_active', 'parent_cat', ]
    readonly_fields = ['id', 'slug', 'created_on', 'created_by', 'updated_on', 'updated_by', ]
    save_on_top = True


class ManufacturerAdmin(admin.ModelAdmin):
    admin_thumbnail = AdminThumbnail(image_field='image', template="./templates/catalog/admin/thumbnail.html")
    raw_id_fields = ['created_by', 'updated_by', ]
    list_display = ['id', 'admin_thumbnail', 'name', 'slug', 'is_active', ]
    list_editable = ['is_active', ]
    readonly_fields = ['id', 'slug', 'created_on', 'created_by', 'updated_on', 'updated_by', ]
    save_on_top = True


class ProductImageInline(admin.StackedInline):
    model = ProductImageRelated
    max_num = 10
    extra = 0


class ProductImageAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('id', 'admin_thumbnail', 'original', 'big_image', 'small_image',)
    admin_thumbnail = AdminThumbnail(image_field='original', template="./templates/catalog/admin/thumbnail.html")
    save_on_top = True


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]
    raw_id_fields = ['category', 'manufacturer', 'created_by', 'updated_by', ]
    list_display = ['id', 'name', 'category', 'manufacturer', 'sku',
                    'price', 'discount', 'actual_price', 'quantity', 'is_active', ]
    list_display_links = ['id', 'category', 'name', 'manufacturer', 'sku', ]
    search_fields = ['name', 'description', 'slug', ]
    readonly_fields = ['id', 'slug', 'actual_price', 'created_on', 'created_by', 'updated_on', 'updated_by', ]
    list_editable = ['is_active', ]
    save_on_top = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
