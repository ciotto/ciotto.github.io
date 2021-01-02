from articles.arduino import *
from categories import *
from models import Page
from utilities import html_from_markdown_url

haier_t32x_page = Page(
    title='Haier T32X robot',
    slug='haier-t32x',
    template='md.html',
    date=date(2019, 4, 18),
    changefreq='monthly',
    priority=0.8,
    md=html_from_markdown_url('https://raw.githubusercontent.com/ciotto/teardown/master/haier-t32x/README.md'),
    description='Reverse engineering the Haier T325 Cleaning Robot.',
    og_image='https://ci8.it/images/share/haier_t32x.jpg',
    category=teardowns,
    tags=[
        ('teardown', 'Teardown'),
        ('reversing', 'Reversing'),
        ('stm32', 'STM32'),
        ('swd', 'SWD'),
        ('uart', 'UART'),
        ('st-link', 'ST-Link'),
        ('openocd', 'OpenOCD'),
        ('hardware-security', 'Hardware Security'),
        ('gdb', 'GDB'),
    ]
)
digipass_go_6_page = Page(
    title='DIGIPASS GO 6',
    slug='digipass-go-6',
    template='md.html',
    date=date(2019, 4, 18),
    changefreq='monthly',
    priority=0.8,
    md=html_from_markdown_url('https://raw.githubusercontent.com/ciotto/teardown/master/digipass-go-6/README.md'),
    description='Reverse engineering the Vasco DIGIPASS GO 6.',
    og_image='https://ci8.it/images/share/digipass_go_6.jpg',
    category=teardowns,
    tags=[
        ('teardown', 'Teardown'),
        ('reversing', 'Reversing'),
    ]
)
multiple_choice_test_omr_page = Page(
    title='Multiple Choice Test OMR',
    slug='multiple-choice-test-omr',
    template='md.html',
    date=date(2020, 1, 17),
    changefreq='monthly',
    priority=0.8,
    md=html_from_markdown_url('src/electronics/teardowns/multiple_choice_test_omr/README.md'),
    description='Making an OMR for a generic multiple choice test, step by step, using OpenCV and Python.',
    og_image='https://ci8.it/images/share/multiple_choice_test_omr.jpg',
    category=python,
    tags=[
        ('python', 'Python'),
        ('omr', 'OMR'),
        ('opencv', 'OpenCV'),
    ]
)
mod_wsgi_error_page = Page(
    title='Apache mod_wsgi/psycopg2 error',
    slug='mod-wsgi-error',
    template='md.html',
    date=date(2020, 1, 29),
    changefreq='monthly',
    priority=0.8,
    md=html_from_markdown_url('src/electronics/teardowns/mod_wsgi_error/README.md'),
    description='mod_wsgi: Truncated or oversized response headers received from daemon process.',
    og_image='https://ci8.it/images/share/mod_wsgi_error.jpg',
    category=system,
    tags=[
        ('python', 'Python'),
        ('apache', 'Apache'),
        ('wsgi', 'WSGI'),
        ('gdb', 'GDB'),
    ]
)

articles = [
    mod_wsgi_error_page,
    multiple_choice_test_omr_page,
    haier_t32x_page,
    digipass_go_6_page,
    intro_to_arduino_page,
]
articles = sorted(articles, reverse=True, key=lambda a: a.date)
last_articles = articles[:2]

series = [
    intro_to_arduino_page,
]
