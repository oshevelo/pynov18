from django.contrib.auth.models import User
from django.db import models

from django.utils.text import slugify


class Categories(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False)
    image = models.ImageField(blank=True)
    parent_cat = models.ForeignKey("Categories", on_delete=models.PROTECT, blank=True, null=True, )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='category_creator')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='category_updater')

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Category: {self.name}"

    class Meta:
        db_table = "categories"


class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False)
    image = models.ImageField(blank=True)
    category = models.ForeignKey("Categories", on_delete=models.PROTECT, blank=True, null=True,
                                 related_name='product_category')
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.PROTECT, blank=True, null=True,
                                     related_name='product_manufacturer')
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    old_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    attributes = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='product_creator')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='product_updater')

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Product: {self.name}"

    class Meta:
        db_table = "products"


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False)
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='manufacturer_creator')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='manufacturer_updater')

    def __str__(self):
        return f"Category: {self.name}"

    class Meta:
        db_table = "manufacturer"
