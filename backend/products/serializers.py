from rest_framework import serializers
import cloudinary.uploader
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        image = validated_data.pop('image', None)

        if image:
            upload_result = cloudinary.uploader.upload(image, folder="UStore_Products")
            validated_data['image'] = upload_result['secure_url']

        return Product.objects.create(**validated_data)
