from django.contrib import admin
from django.utils.safestring import mark_safe
from imagekit.admin import AdminThumbnail
from catalog.models import Category, Product, Manufacturer, ProductImage


class CategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ['parent_cat', 'created_by', 'updated_by', ]
    list_display = ['id', 'get_image', 'parent_cat', 'name', 'slug', 'is_active', 'updated_by']
    list_display_links = ['id', "get_image", 'parent_cat', 'name', ]
    search_fields = ['name', 'description', 'slug', ]
    list_editable = ['is_active', ]
    list_filter = ['is_active', 'parent_cat', ]
    readonly_fields = ['id', 'slug', 'created_on', 'created_by', 'updated_on', 'updated_by', ]
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='50'>")

    get_image.short_description = "Img"


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', '__str__',)
    admin_thumbnail = AdminThumbnail(image_field='photo', template="./templates/catalog/admin/thumbnail.html")


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    max_num = 10
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]
    raw_id_fields = ['category', 'manufacturer', 'created_by', 'updated_by', ]
    list_display = ['id', 'get_image', 'name', 'category', 'manufacturer', 'sku',
                    'price', 'discount', 'actual_price', 'quantity', 'attributes', 'is_active', ]
    list_display_links = ['id', 'category', 'name', 'manufacturer', 'sku', ]
    search_fields = ['name', 'description', 'slug', ]
    readonly_fields = ['id', 'slug', 'actual_price', 'created_on', 'created_by', 'updated_on', 'updated_by', ]
    list_editable = ['is_active', ]

    save_on_top = True

    def get_image(self, obj):
        if obj.images:
            img = obj.images.get(product=obj.id)
            return mark_safe(f"<img src='{img.photo_medium.url}' width='50'")
        return None

    get_image.short_description = "Img"


class ManufacturerAdmin(admin.ModelAdmin):
    raw_id_fields = ['created_by', 'updated_by', ]
    list_display = ['id', 'name', 'slug', 'is_active', ]
    list_editable = ['is_active', ]
    readonly_fields = ['id', 'slug', 'created_on', 'created_by', 'updated_on', 'updated_by', ]
    save_on_top = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
