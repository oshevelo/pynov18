from rest_framework import generics, permissions

from catalog.paginations import CatalogPagination
from catalog.serializers import CategorySerializer, CategoryDetailSerializer, ManufacturerSerializer, \
    ManufacturerDetailSerializer, ProductImageSerializer, ProductSerializer, ProductDetailSerializer, \
    ProductImageDetailSerializer
from .models import Category, Manufacturer, ProductImage, Product
from .permissions import CatalogCreateEditOrReadOnly


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = CatalogPagination
    permission_classes = [CatalogCreateEditOrReadOnly]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [CatalogCreateEditOrReadOnly]


class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.filter(is_active=True)
    serializer_class = ManufacturerSerializer
    pagination_class = CatalogPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ManufacturerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductImageList(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    pagination_class = CatalogPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('-pk')
    serializer_class = ProductSerializer
    pagination_class = CatalogPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
