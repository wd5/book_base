# -*- coding: utf-8 -*-

import os
import thread
import threading
from django.conf import settings
from django.contrib import admin
from .book_parser import parser_json

from .models import Book, BookParserJSON
from .models import Library, LibraryCity
from .models import Author, Publisher, Genre, Language, Format, Series

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'taked', 'library', 'author', 'genre', 'year', 'image_preview', )
    list_editable = ('library', 'taked', )
    list_filter = ('genre', 'author', 'series', 'publisher', )
    search_fields = ('name', 'author', )

    def image_preview(self, obj):
        if obj.image:
            return u'<img src="%s%s" width="40" height="40" />' % (settings.MEDIA_URL, obj.image)
        else:
            return ''
    image_preview.short_description = 'Изображение'
    image_preview.allow_tags = True
    image_preview.admin_order_field = 'image'

    def get_name(self, obj):
        return obj.name[:57]
    get_name.short_description = 'Название'
    get_name.allow_tags = True
    get_name.admin_order_field = 'name'

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

class BookParserJSONAdmin(admin.ModelAdmin):
    list_display = ('file', 'created', 'book_count', )
    list_filter = ('created', )

    def _save_books(self, data):
        i=0
        books = parser_json(data)
        for book in books:
            print '%s > begin' % i
            library_city_name=book['library_city'].replace('null', '').strip()
            library_name=book['library'].replace('null', '').strip()
            try:
                library_city, created = LibraryCity.objects.get_or_create(name=library_city_name)
                library, created = Library.objects.get_or_create(name=library_name, city=library_city)
            except :
                continue
            try:
                name = book['name'].replace('null', '').strip()
                inventory = book['inventory'].replace('null', '').strip()
                book_obj, created = Book.objects.get_or_create(
                    name=name,
                    inventory=inventory
                )

                if not book['author'] or book['author'] != 'null':
                    author, created = Author.objects.get_or_create(name=book['author'])
                else:
                    author = None
                if not book['publisher'] or book['publisher'] != 'null':
                    publisher, created = Publisher.objects.get_or_create(name=book['publisher'])
                else:
                    publisher = None
                if not book['genre'] or book['genre'] != 'null':
                    genre, created = Genre.objects.get_or_create(name=book['genre'])
                else:
                    genre = None
                if not book['language'] or book['language'] != 'null':
                    language, created = Language.objects.get_or_create(name=book['language'])
                else:
                    language = None
                if not book['format'] or book['format'] != 'null':
                    format, created = Format.objects.get_or_create(name=book['format'])
                else:
                    format = None
                if not book['series'] or book['series'] != 'null':
                    series, created = Series.objects.get_or_create(name=book['series'])
                else:
                    series = None

                book_obj.author = author
                book_obj.publisher = publisher
                book_obj.genre = genre
                book_obj.language = language
                book_obj.format = format
                book_obj.series = series
                book_obj.library = library

                book_obj.bbk1 = book['bbk1'].replace('null', '').strip()
                book_obj.bbk1_name = book['bbk1_name'].replace('null', '').strip()
                book_obj.bbk2 = book['bbk2'].replace('null', '').strip()
                book_obj.bbk2_name = book['bbk2_name'].replace('null', '').strip()
                book_obj.content_type = book['content_type'].replace('null', '').strip()
                book_obj.city = book['city'].replace('null', '').strip()
                book_obj.year = book['year'].replace('null', '').strip()
                book_obj.pages = book['pages'].replace('null', '').strip()
                book_obj.price = book['price'].replace('null', '').strip()

                book_obj.save()
            except Exception, e:
                print '%s >>> except' % i
                continue
            print '%s > end' % i
            i += 1



    def save_model(self, request, obj, form, change):
        super(BookParserJSONAdmin, self).save_model(request, obj, form, change)

        file = os.path.join(settings.MEDIA_ROOT, obj.file.file.name)
        data = open(file, 'r').read()

        t1 = FuncThread(self._save_books, data)
        t1.start()
        t1.join()

        obj.book_count = 123
        obj.save()

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Format)
admin.site.register(Series)

admin.site.register(Library)
admin.site.register(LibraryCity)

admin.site.register(Book, BookAdmin)
admin.site.register(BookParserJSON, BookParserJSONAdmin)
