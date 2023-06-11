import datetime
from rest_framework import serializers
from .models import Product, Tag, Reviews, ProductSpecification, Category, CategoryIcon, Sale


class ProductSpecificationSerializer(serializers.ModelSerializer):
    """
    Сериалайзер спецификации продуктов
    """
    class Meta:
        model = ProductSpecification
        fields = "id", "name", "value"


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериалайзер отзывов о продукте
    """
    date = serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = ['author', 'email', 'text', 'rate', 'date', 'product']

    def get_date(self, instance):
        date = instance.date + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(date, '%d.%m.%Y %H:%M')


class TagsProductSerializer(serializers.ModelSerializer):
    """
    Сериалайзер тэгов
    """
    class Meta:
        model = Tag
        fields = 'id', 'name'


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериалайзер продуктов
    """
    images = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, required=False)
    tags = TagsProductSerializer(many=True, required=False)
    specifications = ProductSpecificationSerializer(many=True, required=False)
    price = serializers.SerializerMethodField()

    def get_images(self, instance):
        images = []
        images_tmp = instance.images.all()
        for image in images_tmp:
            images.append({"src": f"/media/{image.__str__()}", "alt": image.name})
        return images

    def get_price(self, instance):
        salePrice = instance.sales.first()
        if salePrice:
            return salePrice.salePrice
        return instance.price

    class Meta:
        model = Product
        fields = "__all__"


class CategoryIconSerializer(serializers.ModelSerializer):
    """
    Сериалайзер изображения категорий продуктов
    """
    class Meta:
        model = CategoryIcon
        fields = "id", "src", "alt"


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер субкатегорий
    """
    image = CategoryIconSerializer(many=False, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер категорий
    """
    image = CategoryIconSerializer(many=False, required=False)
    subcategories = SubCategorySerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = "__all__"


class SaleSerializer(serializers.ModelSerializer):
    """
    Сериалайзер скидок
    """
    images = serializers.SerializerMethodField()
    title = serializers.StringRelatedField()
    href = serializers.StringRelatedField()
    price = serializers.StringRelatedField()
    dateFrom = serializers.DateField(format='%d.%b')
    dateTo = serializers.DateField(format='%d.%b')

    def get_images(self, instance):
        images = []
        images_tmp = instance.product.images.all()
        for image in images_tmp:
            images.append({"src": f"/media/{image.__str__()}", "alt": image.name})
        return images

    class Meta:
        model = Sale
        fields = '__all__'