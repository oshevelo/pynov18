from rest_framework import generics

from catalog.paginations import CatalogPagination
from .models import Category, Manufacturer, ProductImage, Product
from serializers import CategorySerializer, CategoryDetailSerializer, ManufacturerSerializer, \
    ManufacturerDetailSerializer, ProductImageSerializer, ProductSerializer, ProductDetailSerializer, \
    ProductImageDetailSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = CatalogPagination


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.filter(is_active=True)
    serializer_class = ManufacturerSerializer
    pagination_class = CatalogPagination


class ManufacturerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerDetailSerializer


class ProductImageList(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    pagination_class = CatalogPagination


class ProductImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageDetailSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('-pk')
    serializer_class = ProductSerializer
    pagination_class = CatalogPagination


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
