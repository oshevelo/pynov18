import decimal
from io import BytesIO

from django.core.validators import MinValueValidator
from unidecode import unidecode

from PIL import Image
from django.core.files import File
from django.db import models
from django.utils.text import slugify

from apps_generic.whodidit.models import WhoDidIt


def make_thumbnail(image, name_prefix="", quality=85, basewidth=600):
    """Makes thumbnails of given size from given image"""
    im = Image.open(image)
    wpercent = (basewidth / float(im.size[0]))
    hsize = int((float(im.size[1]) * float(wpercent)))
    im = im.resize((basewidth, hsize), Image.ANTIALIAS)
    thumb_io = BytesIO()  # create a BytesIO object
    im.save(thumb_io, 'PNG', quality=quality)  # save image to BytesIO object
    thumbnail = File(thumb_io, name=name_prefix + image.name)  # create a django friendly File object

    return thumbnail


class Category(WhoDidIt):
    name = models.CharField(verbose_name="category", max_length=255)
    parent_cat = models.ForeignKey("self", verbose_name="parent_category", on_delete=models.PROTECT,
                                   blank=True,
                                   null=True, )
    description = models.TextField(verbose_name="description", max_length=2000, blank=True, null=True)
    slug = models.SlugField(verbose_name="slug", unique=True, editable=False)
    image = models.ImageField(verbose_name="image", upload_to="categories/%Y/%m/%d", blank=True)

    is_active = models.BooleanField(verbose_name="is_active", default=True)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(unidecode(value), allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Manufacturer(WhoDidIt):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False)
    image = models.ImageField(upload_to="manufacturers/%Y/%m/%d", blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        value = str(self.name)
        self.slug = slugify(unidecode(value), allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"


class ProductImage(WhoDidIt):
    original = models.ImageField(upload_to="products/original/%Y/%m/%d", blank=True, null=True)
    big_image = models.ImageField(upload_to="products/big/%Y/%m/%d", editable=False, blank=True, null=True, )
    small_image = models.ImageField(upload_to="products/small/%Y/%m/%d", editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.big_image = make_thumbnail(self.original, quality=90, basewidth=400, name_prefix="", )
        self.small_image = make_thumbnail(self.original, quality=90, basewidth=150, name_prefix="", )
        super().save(*args, **kwargs)

    def get_file_path(self):
        pass

    def str(self):
        return f"{self.original.name}"

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class Product(WhoDidIt):
    name = models.CharField(max_length=512)
    description = models.TextField(max_length=20000, blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, blank=True, null=True,
                                 related_name='products')
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.PROTECT, blank=True, null=True,
                                     related_name='products')
    sku = models.CharField(max_length=12)
    images = models.ManyToManyField(ProductImage, through='ProductImageRelated', related_name='products')
    attributes = models.JSONField(blank=True, null=True)
    price = models.DecimalField(max_digits=9, default=0, decimal_places=2, blank=True, null=True,
                                validators=[MinValueValidator(0, 'Min value is 0')])
    discount = models.PositiveIntegerField(default=0, blank=True, null=True, help_text="in percent")
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    @property
    def actual_price(self):
        return self.price - (self.price * decimal.Decimal(self.discount / 100)) if self.discount else self.price

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(unidecode(value), allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImageRelated(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    description = models.CharField(max_length=64, blank=True)
    date_joined = models.DateField(auto_now_add=True)
