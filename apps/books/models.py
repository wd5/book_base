# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    """
    Авторы книг.
    """
    name = models.CharField('Автор', max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Publisher(models.Model):
    """
    Издатель.
    """
    name = models.CharField('Издатель', max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Издатель'
        verbose_name_plural = 'Издательство'

class Genre(models.Model):
    """
    Жанр (раздел).
    """
    name = models.CharField('Раздер', max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Language(models.Model):
    """
    Язык книги.
    """
    name = models.CharField('Язык', max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

class Format(models.Model):
    """
    Формат книги.
    """
    name = models.CharField('Формат', max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Формат'
        verbose_name_plural = 'Формат книги'

class Series(models.Model):
    name = models.CharField('Серия', max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'

class LibraryCity(models.Model):
    name = models.CharField('Город', max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Город'
        verbose_name_plural = 'Город библиотеки'

class Library(models.Model):
    name = models.CharField('Библиотека', max_length=64)
    city = models.ForeignKey(LibraryCity, verbose_name='Город')

    def __unicode__(self):
        return '%s [%s]' % (self.name, self.city.name)

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Библиотека'
        verbose_name_plural = 'Библиотеки'

class Book(models.Model):
    name = models.CharField('Название', max_length=256)
    inventory = models.PositiveIntegerField('Инвентарный номер')
    volume = models.CharField('Том', max_length=16, blank=True, null=True)
    author = models.ForeignKey(Author, verbose_name='Автор', blank=True, null=True)
    isbn = models.CharField('ISBN', max_length=20, blank=True, null=True)
    isbn10 = models.CharField('ISBN-10', max_length=20, null=True, blank=True)
    bbk1 = models.CharField('BBK1', max_length=32, blank=True, null=True)
    bbk1_name = models.CharField('BBK2', max_length=128, blank=True, null=True)
    bbk2 = models.CharField('BBK2', max_length=32, blank=True, null=True)
    bbk2_name = models.CharField('BBK2', max_length=128, blank=True, null=True)
    genre = models.ForeignKey(Genre, verbose_name='Жанр', blank=True, null=True)
    series = models.ForeignKey(Series, verbose_name='Серия', blank=True, null=True)
    content_type = models.CharField('Тип', max_length=128, blank=True, null=True)
    publisher = models.ForeignKey(Publisher, verbose_name='Издатель', blank=True, null=True)
    city = models.CharField('Город', max_length=32, blank=True, null=True)
    year = models.CharField('Год издания', max_length=16, blank=True, null=True)
    pages = models.CharField('Страниц', max_length=16, blank=True, null=True)
    lang = models.ForeignKey(Language, verbose_name='Язык', blank=True, null=True)
    price = models.CharField('Стоиомость', max_length=32, blank=True, null=True)
    format = models.ForeignKey(Format, verbose_name='Формат', blank=True, null=True)
    image = models.ImageField('Превьюшка', upload_to='books_image', blank=True, null=True)

    library = models.ForeignKey(Library, verbose_name='Библиотека')

    update = models.DateTimeField('Обновлена', auto_now=True)
    created = models.DateTimeField('Создана', auto_now_add=True)

    def get_city_name(self):
        return self.library.city.name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

class BookParserJSON(models.Model):
    file = models.FileField('Файл', upload_to='books_json')
    created = models.DateTimeField('Импортирован', auto_now_add=True)
    book_count = models.PositiveIntegerField('Кол-во книг', editable=False, default=0)

    class Meta:
        ordering = ['created', ]
        verbose_name = 'Импорт'
        verbose_name_plural = 'Импорт из JSON'

class BookRead(models.Model):
    book = models.ForeignKey(Book, verbose_name='Книга')
    user = models.ForeignKey(User, verbose_name='Пользователь')
    added = models.DateTimeField('Добавлена', auto_now_add=True)

    class Meta:
        ordering = ['added', ]
        verbose_name = 'Буду читать'
        verbose_name_plural = 'Буду читать'

class OrderBook(models.Model):
    book = models.ForeignKey(Book, verbose_name='Книга')
    user = models.ForeignKey(User, verbose_name='Пользователь')
    library = models.ForeignKey(Library, verbose_name='Библиотека')
    phone = models.CharField('Телефон', max_length=16)
    added = models.DateTimeField('Оформлен', auto_now_add=True)

    class Meta:
        ordering = ['added', ]
        unique_together = ('book', 'user', )
        verbose_name = 'Буду читать'
        verbose_name_plural = 'Буду читать'