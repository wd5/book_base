# -*- coding: utf-8 -*-

from django.forms.models import ModelForm
from .models import OrderBook

class MakeOrderForm(ModelForm):
    class Meta:
        model = OrderBook
        fields = ('book', 'phone', 'library', )