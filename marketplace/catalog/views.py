from django.db.models import Count
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError
from datetime import datetime

def sort_products(request: Request, products):
    """
    Сортировка продуктов
    :param request:
    :param products:
    :return: products
    """
    sort = request.GET.get('sort')
    sortType = request.GET.get('sortType')

    if sortType == 'inc':
        sortType = '-'
    else:
        sortType = ''

    if sort == 'reviews':
        products = products.filter(active=True).annotate(count_reviews=Count('reviews')).order_by(
            f'{sortType}count_reviews').prefetch_related('images', 'reviews')
    else:
        products = products.filter(active=True).order_by(f'{sortType}{sort}').prefetch_related('images', 'reviews')
    return products


def filter_catalog(request: Request):
    """
    Фильтр каталога продуктов
    :param request:
    :return: catalog
    """
    title = request.query_params.get('filter[name]')
    available = request.query_params.get('filter[available]')
    freeDelivery = request.query_params.get('filter[freeDelivery]')
    tags = request.query_params.getlist('tags[]')
    min_price = (request.query_params.get('filter[minPrice]'))
    max_price = (request.query_params.get('filter[maxPrice]'))
    category = request.META['HTTP_REFERER'].split('/')[4]

    catalog = Product.objects

    if category:
        try:
            catalog = catalog.filter(category_id=category)
        except:
            if str(category).startswith('?filter='):
                title = str(category).split('=')[1]
            else:
                category = ''

    if available == 'true':
        if freeDelivery == 'true':
            if len(tags) != 0:
                catalog = (catalog.filter(
                    title__iregex=title, price__range=(min_price, max_price), count__gt=0, freeDelivery=True,
                    tags__in=tags).prefetch_related('images', 'tags'))
            else:
                catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price), count__gt=0,
                                         freeDelivery=True).prefetch_related('images')
        elif len(tags) != 0:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price), count__gt=0,
                                     tags__in=tags).prefetch_related('images', 'tags')
        else:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price),
                                     count__gt=0).prefetch_related('images')
    elif freeDelivery == 'true':
        if len(tags) != 0:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price), freeDelivery=True,
                                     tags__in=tags).prefetch_related('images', 'tags')
        else:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price),
                                     freeDelivery=True).prefetch_related('images')
    elif len(tags) != 0:
        catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price),
                                 tags__in=tags).prefetch_related('images', 'tags')
    else:
        catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price)).prefetch_related('images')

    return catalog


class ProductsList(APIView):
    """
    Вью списка продуктов
    """
    def get(self, request: Request):
        products = filter_catalog(request)
        products = sort_products(request, products)
        serialized = ProductSerializer(products, many=True)
        return Response({"items": serialized.data})


class BannersList(APIView):
    """
    Вью баннеров главной страницы
    """
    def get(self, request: Request):
        cat = Category.objects.filter(favourite=True)
        banners = Product.objects.filter(limited_edition=True)

        serialized = ProductSerializer(banners, many=True)
        return Response(serialized.data)


class LimitedList(APIView):
    """
    Вью продуктов ограниченого тиража
    """
    def get(self, request: Request):
        products = Product.objects.filter(limited_edition=True)
        serialized = ProductSerializer(products, many=True)
        return Response(serialized.data)


class PopularList(APIView):
    """
    Вью популярных продуктов
    """
    def get(self, request: Request):
        products = Product.objects.filter(active=True).annotate(count_reviews=Count('reviews')).order_by('-count_reviews')
        serialized = ProductSerializer(products, many=True)
        return Response(serialized.data)


class CategoriesList(APIView):
    """
    Вью категорий
    """
    def get(self, request: Request):
        categories = Category.objects.filter(parent=None)
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class ProductDetail(APIView):
    """
    Вью детального отображения продукта
    """
    def get(self, request: Request, pk):
        product = Product.objects.get(pk=pk)
        serialized = ProductSerializer(product, many=False)
        return Response(serialized.data)


class TagsList(APIView):
    """
    Вью тэгов
    """
    def get(self, request: Request):
        tags = Tag.objects.all()
        data = TagsProductSerializer(tags, many=True)
        return Response(data.data)


class SalesList(APIView):
    """
    Вью продуктов со скидкой
    """
    def get(self, request: Request):
        sales = Sale.objects.all()
        serialized = SaleSerializer(sales, many=True)
        return Response({"items": serialized.data})

class CreateReviewView(CreateModelMixin, GenericAPIView):
    """
    Представление для создания отзывов о продукте
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            return Response({"error": "Missing 'pk' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        request.data['product'] = pk
        request.data['date'] = str(datetime.now())
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        reviews = Reviews.objects.filter(product=pk)
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)