# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.contrib import admin
from .book_parser import parser_json

from .models import Book, BookParserJSON
from .models import Library, LibraryCity
from .models import Author, Publisher, Genre, Language, Format, Series

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory', 'library', 'author', 'genre', 'year', 'pages', 'lang', 'price', 'format', 'image_preview', )
    list_editable = ('library', )
    list_filter = ('genre', 'author', 'series', 'publisher', 'city', )
    search_fields = ('name', 'inventory', 'author', )

    def image_preview(self, obj):
        if obj.image:
            return u'<img src="%s%s" width="40" height="40" />' % (settings.MEDIA_URL, obj.image)
        else:
            return ''
    image_preview.short_description = 'Изображение'
    image_preview.allow_tags = True
    image_preview.admin_order_field = 'image'

class BookParserJSONAdmin(admin.ModelAdmin):
    list_display = ('file', 'created', 'book_count', )
    list_filter = ('created', )

    def save_model(self, request, obj, form, change):
        super(BookParserJSONAdmin, self).save_model(request, obj, form, change)

        file = os.path.join(settings.MEDIA_ROOT, obj.file.file.name)
        data = open(file, 'r').read()

        i=0
        books = parser_json(data)
        for book in books:
            try:
                library_city, created = LibraryCity.objects.get_or_create(name=book['library_city'])
                library, created = Library.objects.get_or_create(name=book['library'], city=library_city)
            except :
                continue
            try:
                book_obj, created = Book.objects.get_or_create(
                    name=book['name'],
                    inventory=book['inventory'],
                    isbn=book['isbn'],
                    isbn10=book['isbn10'],
                    library=library,
                )

                author, created = Author.objects.get_or_create(name=book['author'])
                publisher, created = Publisher.objects.get_or_create(name=book['publisher'])
                genre, created = Genre.objects.get_or_create(name=book['genre'])
                language, created = Language.objects.get_or_create(name=book['language'])
                format, created = Format.objects.get_or_create(name=book['format'])
                series, created = Series.objects.get_or_create(name=book['series'])

                book_obj.author = author
                book_obj.publisher = publisher
                book_obj.genre = genre
                book_obj.language = language
                book_obj.format = format
                book_obj.series = series
                book_obj.library = library

                book_obj.bbk1 = book['bbk1']
                book_obj.bbk1_name = book['bbk1_name']
                book_obj.bbk2 = book['bbk2']
                book_obj.bbk2_name = book['bbk2_name']
                book_obj.content_type = book['content_type']
                book_obj.city = book['city']
                book_obj.year = book['year']
                book_obj.pages = book['pages']
                book_obj.price = book['price']

                book_obj.save()
            except :
                continue

            if i > 10:
                break2
            i += 1

        obj.book_count = i
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
