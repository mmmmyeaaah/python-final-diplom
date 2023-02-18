from rest_framework import serializers
from shops.models import Shop, Category, Product, ProductParameter, ProductInfo


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id',)


class ProductParameterSerializer(serializers.Serializer):
    parameter = serializers.StringRelatedField()
    value = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = '__all__'
        read_only_fields = ('id',)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = '__all__'
        read_only_fields = ('id',)
