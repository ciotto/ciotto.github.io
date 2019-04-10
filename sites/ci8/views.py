import os
import requests
from django.shortcuts import render_to_response
from staticsites.decorators import staticview
from markdown2 import Markdown


markdowner = Markdown(extras=['tables', 'fenced-code-blocks'])

# Pages
about_me_page = ('About me', 'index.html')
haier_t32x_page = ('Reverse the Haier T32X robot', 'haier-t32x.html')
digipass_go_6_page = ('DIGIPASS GO 6', 'digipass-go-6.html')
pages = [
    about_me_page,
    haier_t32x_page,
    digipass_go_6_page,
]


def html_from_markdown_url(url):
    base_url = os.path.dirname(url)

    response = requests.get(url)
    content = response.content.replace('](images', '](%s/images' % base_url)
    return markdowner.convert(content)


@staticview
def index(request):
    ctx = {
        'title': 'Christian Bianciotto',
        'pages': pages,
    }

    return render_to_response('ci8/index.html', ctx)


@staticview(path=haier_t32x_page[1])
def haier_t32x(request):
    ctx = {
        'title': haier_t32x_page[0],
        'md': html_from_markdown_url('https://raw.githubusercontent.com/ciotto/teardown/master/haier-t32x/README.md'),
        'pages': pages,
    }

    return render_to_response('ci8/md.html', ctx)


@staticview(path=digipass_go_6_page[1])
def digipass_go_6(request):
    ctx = {
        'title': digipass_go_6_page[0],
        'md': html_from_markdown_url(
            'https://raw.githubusercontent.com/ciotto/teardown/master/digipass-go-6/README.md'
        ),
        'pages': pages,
    }

    return render_to_response('ci8/md.html', ctx)
