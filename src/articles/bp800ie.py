# coding=utf-8
from datetime import date


from categories import *
from models import Page, LocalizedPage
from utilities import html_from_markdown_url

bp800ie_step1 = Page(
    # title='BP800 ie',
    # slug='bp800-ie-step1',
    template='md.html',
    # lang='it',
    date=date(2026, 10, 8),
    changefreq='monthly',
    priority=0.8,
    # md=html_from_markdown_url('src/articles/garage/bp800ie/bp800ie_step1.md'),
    # description='Come costruire un trattore con motore bicilindrico a iniezione autocostruito.',
    og_image='https://ci8.it/images/share/bp800-ie.jpg',
    category=garage,
    # TODO: remove
    robots='noindex, nofollow',
    tags=[
        ('speeduino', 'Speeduino'),
        ('twin-engine', 'Twin engine'),
        ('efi', 'EFI'),
        ('tractor-pulling', 'Tractor Pulling'),
    ],
    localized_pages = [
        LocalizedPage(
            title='BP800 i.e. - Intro',
            slug='bp800-ie-intro',
            # template='glossary.html',
            description='How to build a tractor with a custom-built, fuel-injected twin-cylinder engine.',
            md=html_from_markdown_url('src/articles/garage/bp800ie/bp800ie_step1_en.md'),
        ),
        LocalizedPage(
            title='BP800 i.e. - Introduzione',
            slug='bp800-ie-introduzione',
            # template='glossary.html',
            lang='it',
            description='Come costruire un trattore con motore bicilindrico a iniezione autocostruito.',
            md=html_from_markdown_url('src/articles/garage/bp800ie/bp800ie_step1_it.md'),
        ),
    ],
)

# arduino_uno
# arduino_ide
# build_custom_arduino_board


