# -*- coding: utf-8 -*-

import json

def parser_json(json_data):
    books = []

    try:
        json_books = json.loads(json_data)
    except :
        return books

    for book in json_books:
        books.append({
            'inventory': book.get('inventory', '').replace('null', ''),
            'name': book.get('name', '').replace('null', ''),
            'volume': book.get('volume', ''),
            'author': book.get('autor', ''),
            'isbn': book.get('isbn', '').replace('null', ''),
            'isbn10': book.get('isbn10', '').replace('null', ''),
            'bbk1': book.get('BBK1', ''),
            'bbk1_name': book.get('BBK1_name', ''),
            'bbk2': book.get('BBK2', ''),
            'bbk2_name': book.get('BBK2_name', ''),
            'genre': book.get('genre', ''),
            'series': book.get('series', ''),
            'content_type': book.get('content_type', ''),
            'publisher': book.get('publisher', ''),
            'city': book.get('city', ''),
            'year': book.get('year', ''),
            'pages': book.get('pages', ''),
            'language': book.get('lang', ''),
            'price': book.get('price', ''),
            'format': book.get('format', ''),
            'library': book.get('Lib_Name', ''),
            'library_city': book.get('Lib_City', ''),
        })
    return books
