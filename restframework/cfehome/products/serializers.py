from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from . import validators
from api.serializers import UserPublicSerializer

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk', read_only=True)
    title = serializers.CharField()

class PrimaryProductSerializer(serializers.ModelSerializer):
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    owner = UserPublicSerializer(source='user', read_only=True)
    # related_products = ProductInlineSerializer(source='user.product_set.all', read_only=True, many=True)
    # my_discount = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk')
    edit_url = serializers.SerializerMethodField(read_only=True)
    # email = serializers.EmailField(write_only=True)
    title = serializers.CharField(validators=[validators.validate_title_no_hello, validators.unique_product_title])
    # name = serializers.CharField(source='title', read_only=True)
    # email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Product
        fields = [ 'url', 'owner', 'edit_url', 'title', 'content', 'price', 'sales_price']
        
    # def validate_title(self, value):
    #     querySet = Product.objects.filter(title__iexact=value)
    #     if querySet.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value
    
    # def create(self, validated_data):
    #     # return Product.objects.create(**validated_data)
    #     # email = validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     # print(obj, email)
    #     return obj
    
    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     # instance.title = validated_data.get('title')
    #     # return instance
    #     return super().update(instance, validated_data)
        
    # def get_url(self, obj):
    #     # return f"/api/products/{obj.pk}/"
    #     request = self.context.get('request')
    #     if request is None:
    #         return None
    #     return reverse("product-detail", kwargs={"pk": obj.pk}, request=request)
    
    def get_edit_url(self, obj):
        # return f"/api/products/{obj.pk}/"
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)
        
    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
    
    def get_my_user_data(self, obj):
        # user = self.context.request.user
        return {
            "username": obj.user.username
        }
    
class SecondaryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'sales_price']
        