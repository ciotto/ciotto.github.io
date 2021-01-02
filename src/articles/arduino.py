# coding=utf-8
from datetime import date


from categories import *
from models import Page
from utilities import html_from_markdown_url

intro_to_arduino_page = Page(
    title='Introduzione ad Arduino',
    slug='introduzione-ad-arduino',
    template='md.html',
    lang='it',
    date=date(2020, 12, 23),
    changefreq='monthly',
    priority=0.8,
    md=html_from_markdown_url('src/electronics/boards/arduino/introduzione_ad_arduino.md'),
    description='Capiamo le basi di come funziona Arduino e i motivi per cui è così diffuso.',
    og_image='https://ci8.it/images/share/arduino-uno.jpg',
    category=arduino,
    tags=[
        ('arduino', 'Arduino'),
        ('arduino-ide', 'Arduino IDE'),
        ('arduino-bootloader', 'Arduino bootloader'),
    ]
)

# arduino_uno
# arduino_ide
# build_custom_arduino_board


