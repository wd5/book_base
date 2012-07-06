# -*- coding: utf-8 -*-

from django import template
from django.template import Library
from annoying.functions import get_object_or_None

from ..models import OrderBook

register = Library()

@register.tag
def is_take(parser, token):
    bits = token.contents.split()
    bits_count = len(bits)
    if bits_count == 5:
        # Вернуть как переменную
        tag_name, request, book, delimiter, render_as = token.split_contents()
        return HasBookTakeNode(request, book, render_as)
    elif bits_count == 3:
        # Вывести в указанное место
        tag_name, request, book = token.split_contents()
        return HasBookTakeNode(request, book)

class HasBookTakeNode(template.Node):
    def __init__(self, request, book, render_as=None):
        self.render_as = render_as
        self.book = template.Variable(book)
        self.request = template.Variable(request)

    def render(self, context):
        book = self.book.resolve(context)
        request = self.request.resolve(context)

        if not request.user.is_authenticated():
            return ''

        order=get_object_or_None(OrderBook, user=request.user, book=book)

        if self.render_as:
            # Отобразить как переменную
            context[self.render_as] = order
            return ''
        else:
            return order # Вывести в указанное место