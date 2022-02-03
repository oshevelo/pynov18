from django.contrib.auth.models import User
from django.db import models

from django.utils.text import slugify

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
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, blank=True, null=True,
                                 related_name='products')
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.PROTECT, blank=True, null=True,
                                     related_name='products')
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=9, default=0, decimal_places=2, blank=True, null=True)
    discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    attributes = models.JSONField(blank=True, null=True)
    is_deleted = models.BooleanField(verbose_name='is deleted', default=False)

    @property
    def actual_price(self):
        return self.price * self.discount if self.discount else self.price

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


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
