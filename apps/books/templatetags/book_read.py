# -*- coding: utf-8 -*-

from django import template
from django.template import Library
from annoying.functions import get_object_or_None

from ..models import BookRead

register = Library()

@register.tag
def is_read(parser, token):
    bits = token.contents.split()
    bits_count = len(bits)
    if bits_count == 5:
        # Вернуть как переменную
        tag_name, request, book, delimiter, render_as = token.split_contents()
        return WillReadNode(request, book, render_as)
    elif bits_count == 3:
        # Вывести в указанное место
        tag_name, request, book = token.split_contents()
        return WillReadNode(request, book)

class WillReadNode(template.Node):
    def __init__(self, request, book, render_as=None):
        self.render_as = render_as
        self.book = template.Variable(book)
        self.request = template.Variable(request)

    def render(self, context):
        book = self.book.resolve(context)
        request = self.request.resolve(context)

        will_not_read = False # Не буду читать

        if request.user.is_authenticated():
            book=get_object_or_None(BookRead,
                user=request.user,
                book__id=book
            )
            if book: will_not_read = True
        else:
            will_not_read = book.id in request.session.get('read_ids', {})

        if self.render_as:
            # Отобразить как переменную
            context[self.render_as] = will_not_read
            return ''
        else:
            return will_not_read # Вывести в указанное место
