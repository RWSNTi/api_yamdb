from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


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


class Review(models.Model):
    text = models.TextField('Отзыв')
    title = models.ForeignKey(Title, related_name='reviews',
                              verbose_name='Произведение',
                              on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews', verbose_name='Автор')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата отзыва')
    score = models.PositiveIntegerField('Оценка', blank=True, null=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    text = models.TextField(max_length=500, verbose_name='Текст комментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments', verbose_name='Автор')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата комментария')
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
