# coding=utf-8
from datetime import date

from categories import *
from models import Page, LocalizedPage

glossary_page = Page(
    date=date(2020, 12, 23),
    changefreq='monthly',
    priority=0.9,
    category=electronics,
    tags=[
        ('electronics', 'Electronics'),
    ],
    words=[
        ('avr', 'Atmel AVR', 'a family of RISC microcontrollers'),
    ],
    localized_pages=[
        LocalizedPage(
            title='Electronics Glossary',
            slug='electronics-glossary',
            template='glossary.html',
            description='List of words and definitions relating to the electronics.',
            words=[
                ('avr', 'Atmel AVR', 'a family of RISC microcontrollers'),
            ],
        ),
        LocalizedPage(
            title='Glossario di Elettronica',
            slug='glossario-di-elettronica',
            template='glossary.html',
            lang='it',
            description='Elenco di parole e definizioni relative all\'elettronica.',
            words=[
                ('avr', 'Atmel AVR', 'una famiglia di microcontrollori RISC'),
            ],
        ),
    ],
)
