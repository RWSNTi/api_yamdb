from django.db import models
from django.utils.text import slugify


class CategoryAbstract(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CategoryAbstract, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(CategoryAbstract):
    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Genre(CategoryAbstract):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    category = models.ForeignKey(
        Category, verbose_name='Категория',
        on_delete=models.PROTECT, related_name='titles')
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание', blank=True, null=True)
    year = models.PositiveSmallIntegerField('Год')
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return f'{self.name} - {self.category.name}'

    @property
    def rating(self):
        rating = self.reviews.aggregate(models.Avg('score')).get('score__avg')
        return rating
