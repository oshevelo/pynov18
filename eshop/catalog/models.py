import decimal
import os
import uuid

from django.db import models
from django.utils.text import slugify
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill

from apps_generic.whodidit.models import WhoDidIt


class Category(WhoDidIt):
    name = models.CharField(verbose_name="category", max_length=255)
    description = models.TextField(verbose_name="description", max_length=2000, blank=True, null=True)
    slug = models.SlugField(verbose_name="slug", unique=True, editable=False)
    image = models.ImageField(verbose_name="image", upload_to="categories/%Y/%m/%d", blank=True)
    parent_cat = models.ForeignKey("self", verbose_name="parent_category", on_delete=models.PROTECT,
                                   blank=True,
                                   null=True, )
    is_active = models.BooleanField(verbose_name="is_active", default=True)
    is_deleted = models.BooleanField(verbose_name='is deleted', default=False)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(WhoDidIt):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, blank=True, null=True,
                                 related_name='products')
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.PROTECT, blank=True, null=True,
                                     related_name='products')
    sku = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=9, default=0, decimal_places=2, blank=True, null=True)
    discount = models.PositiveIntegerField(default=0, blank=True, null=True, help_text="in percent")
    quantity = models.PositiveIntegerField(default=0)
    attributes = models.JSONField(blank=True, null=True)
    is_deleted = models.BooleanField(verbose_name='is deleted', default=False)

    @property
    def actual_price(self):
        return self.price * decimal.Decimal(self.discount / 100) if self.discount else self.price

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(WhoDidIt):
    def get_file_path(self, filename):
        extension = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), extension)
        return os.path.join("products", filename)

    photo = models.ImageField(upload_to=get_file_path, max_length=256, blank=True, null=True)
    photo_small = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
                                  ResizeToFill(50, 50)], source='photo',
                                 format='JPEG', options={'quality': 90})
    photo_medium = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
                                   ResizeToFit(300, 200)], source='photo',
                                  format='JPEG', options={'quality': 90})
    photo_big = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
                                ResizeToFit(640, 480)], source='photo',
                               format='JPEG', options={'quality': 90})
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='images')

    def __str__(self):
        return f"{self.product.name} "


class Manufacturer(WhoDidIt):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False)
    image = models.ImageField(upload_to="manufacturers/%Y/%m/%d", blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(verbose_name='is deleted', default=False)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"
