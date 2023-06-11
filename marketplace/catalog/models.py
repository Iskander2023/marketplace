from django.db import models


def category_image_directory_path(instance: "CategoryIcon", filename):
    """
    Получение пути для загрузки иконки категории
    :param instance: экземпляр класса
    :param filename: имя загружаемого файла
    :return: путь для загрузки файла
    """
    if instance.category.parent:
        return f"catalog/icons/{instance.category.parent}/{instance.category}/{filename}"
    else:
        return f"catalog/icons/{instance.category}/{filename}"


class Category(models.Model):
    """
    Модель категории товаров
    """
    title = models.CharField(max_length=128, db_index=True, verbose_name='название')
    active = models.BooleanField(default=False, verbose_name='активная')
    parent = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, related_name="subcategories", verbose_name='родитель')
    favourite = models.BooleanField(default=False, verbose_name='избраная категория')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = "pk",

    def href(self):
        """
        Получение ссылки
        :return: ссылка
        """
        return f"/catalog/{self.pk}"

    def __str__(self):
        return self.title


class CategoryIcon(models.Model):
    """
    Модель изображения категории
    """
    src = models.FileField(upload_to=category_image_directory_path, max_length=500, verbose_name='изображение')
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name="image", blank=True, null=True, verbose_name='категория')

    class Meta:
        verbose_name = "Category icon"
        verbose_name_plural = "Category icons"
        ordering = ["pk"]

    def alt(self):
        return self.category.title

    def href(self):
        return self.src

    def __str__(self):
        return f"icon of {self.category.title}"


def product_image_directory_path(instanse: "ProductImage", filename):
    return f"products/images/{instanse.product.pk}/{filename}"


class Product(models.Model):
    """
    Модель продукта
    """
    title = models.CharField(max_length=128, null=False, blank=False, verbose_name='название')
    description = models.CharField(max_length=256, null=False, blank=True, verbose_name='описание')
    fullDescription = models.TextField(null=False, blank=True, verbose_name='полное описание')
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, null=False, verbose_name='цена')
    count = models.IntegerField(default=0, null=False, verbose_name='количество')
    date = models.DateTimeField(auto_now_add=True, null=False, verbose_name='дата создания')
    freeDelivery = models.BooleanField(default=True, verbose_name='бесплатная доставка')
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченая серия')
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=2, null=False, verbose_name='рейтинг')
    active = models.BooleanField(default=False, verbose_name='активный')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='категория')

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["pk", ]

    def __str__(self):
        return self.title


class ProductSpecification(models.Model):
    """
    Модель характеристик конкретного продукта
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="specifications", verbose_name='продукт')
    name = models.CharField(max_length=256, default="", verbose_name='название')
    value = models.CharField(max_length=256, default="", verbose_name='значение')

    class Meta:
        verbose_name = "Product specification"
        verbose_name_plural = "Product specifications"


class ProductImage(models.Model):
    """
    Модель изображения продукта
    """
    name = models.CharField(max_length=128, null=False, blank=True, verbose_name='название')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="product")
    image = models.FileField(upload_to=product_image_directory_path, verbose_name='изображение')

    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = "Product images"
        ordering = ["pk", ]

    def src(self):
        return self.image

    def __str__(self):
        return f"/{self.image}"


class Tag(models.Model):
    """
    Модель тэга
    """
    name = models.CharField(max_length=128, null=False, blank=True, verbose_name='название')
    product = models.ManyToManyField(Product, related_name="tags", verbose_name="тэг")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["pk", ]

    def __str__(self):
        return self.name


class Reviews(models.Model):
    """
    Модель отзыва о продукте
    """
    author = models.CharField(max_length=128, verbose_name='автор')
    email = models.EmailField(max_length=256, verbose_name='емейл')
    text = models.TextField(verbose_name='текст комментария')
    rate = models.PositiveSmallIntegerField(blank=False, default=5, verbose_name='оценка')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="reviews", verbose_name="продукт")

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["pk", ]

    def __str__(self):
        return f"{self.author}: {self.product.title}"


class Sale(models.Model):
    """
    Модель продуктов со скидкой
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    salePrice = models.DecimalField(max_digits=10, db_index=True, decimal_places=2, default=0, verbose_name='цена по скидке')
    dateFrom = models.DateField(default='', verbose_name='старт продаж')
    dateTo = models.DateField(blank=True, null=True, verbose_name='окончание продаж')

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def price(self):
        """
        Получение первоначальной цены продукта
        :return: цена
        """
        return self.product.price

    def title(self):
        """
        Получение названия продукта
        :return: название продукта
        """
        return self.product.title

    def href(self):
        """
        Получение ссылки на детальную страницу продукта
        :return: ссылка
        """
        return f'/product/{self.product.pk}'

    def __str__(self):
        return self.product.title
