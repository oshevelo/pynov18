from rest_framework import serializers

from catalog.models import Category, Manufacturer, ProductImage, Product, ProductImageRelated


class CategoryNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', ]


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    parent_cat = CategoryNestedSerializer(required=False, allow_null=True, )
    image = serializers.ImageField(use_url=True, allow_null=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent_cat', 'slug', 'image', 'is_active', ]

    def create(self, validated_data):
        parent_cat_data = validated_data.pop('parent_cat')
        cat = Category.objects.create(**validated_data)
        cat.parent_cat = Category.objects.filter(pk=parent_cat_data.get('id')).first()
        cat.save()
        return cat


class CategoryDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    parent_cat = CategoryNestedSerializer(allow_null=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent_cat', 'slug', 'image', 'is_active', ]

    def update(self, obj, data):
        parent_cat_data = data.pop('parent_cat')
        obj = super().update(obj, data)
        if parent_cat_data:
            parent_cat = Category.objects.filter(id=parent_cat_data['id']).first()
            obj.parent_cat = parent_cat
        else:
            obj.parent_cat = None
        obj.save()

        return obj


class ManufacturerNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'image']


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'image']


class ManufacturerDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'description', 'slug', 'image', 'is_active']


class ImageNestedSerializer(serializers.ModelSerializer):
    original = serializers.ImageField(required=False, allow_null=True)
    big_image = serializers.ImageField(read_only=True)
    small_image = serializers.ImageField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ['original', 'big_image', 'small_image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'original', 'big_image', 'small_image', ]


class ProductImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'original', 'big_image', 'small_image']


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryNestedSerializer()
    manufacturer = ManufacturerNestedSerializer()
    images = ImageNestedSerializer(required=False, allow_null=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'description', 'slug', 'category', 'manufacturer', 'images', 'attributes',
                  'price', 'actual_price', 'discount', 'quantity', 'is_active', 'is_available', ]

    def create(self, validated_data):
        category = validated_data.pop('category')
        manufacturer = validated_data.pop('manufacturer')
        images = validated_data.pop('images')
        product = Product.objects.create(**validated_data)
        product.category = Category.objects.filter(pk=category.get('id')).first()
        product.manufacturer = Manufacturer.objects.filter(pk=manufacturer.get('id')).first()
        product.images.set(images)
        product.save()
        return product


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryNestedSerializer(required=False, allow_null=True, )
    manufacturer = ManufacturerNestedSerializer(required=False, allow_null=True, )
    images = ImageNestedSerializer(required=False, allow_null=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'description', 'slug', 'category', 'manufacturer', 'images', 'attributes',
                  'price', 'actual_price', 'discount', 'quantity', 'is_active', 'is_available', ]

    def update(self, obj, data):
        print(data)
        category = data.pop('category')
        manufacturer = data.pop('manufacturer')
        images = data.pop('images')
        obj = super().update(obj, data)

        obj.category = Category.objects.filter(pk=category.get('id')).first()
        obj.manufacturer = Manufacturer.objects.filter(pk=manufacturer.get('id')).first()
        obj.images.set(images)

        obj.save()
        return obj
