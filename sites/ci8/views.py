import os
import requests
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render_to_response
from django.template import RequestContext
from staticsites.decorators import staticview
from markdown2 import Markdown


markdowner = Markdown(extras=['tables', 'fenced-code-blocks'])

# Pages
about_me_page = ('About me', 'index.html', '2019-04-11', 'monthly', 1)
haier_t32x_page = ('Haier T32X robot', 'haier-t32x.html', '2019-04-11', 'monthly', 0.8)
digipass_go_6_page = ('DIGIPASS GO 6', 'digipass-go-6.html', '2019-04-11', 'monthly', 0.8)
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

    return render_to_response('ci8/index.html', ctx, context_instance=RequestContext(request))


@staticview(path=haier_t32x_page[1])
def haier_t32x(request):
    ctx = {
        'title': haier_t32x_page[0],
        'md': html_from_markdown_url('https://raw.githubusercontent.com/ciotto/teardown/master/haier-t32x/README.md'),
        'pages': pages,
        'path': '/%s' % haier_t32x_page[1],
        'description': 'Reverse engineering the Haier T325 Cleaning Robot.',
        'og_image': 'http://ci8.it%s' % static('/ci8/images/share/haier_t32x.jpg'),
    }

    return render_to_response('ci8/md.html', ctx, context_instance=RequestContext(request))


@staticview(path=digipass_go_6_page[1])
def digipass_go_6(request):
    ctx = {
        'title': digipass_go_6_page[0],
        'md': html_from_markdown_url(
            'https://raw.githubusercontent.com/ciotto/teardown/master/digipass-go-6/README.md'
        ),
        'pages': pages,
        'path': '/%s' % digipass_go_6_page[1],
        'description': 'Reverse engineering the Vasco DIGIPASS GO 6.',
        'og_image': 'http://ci8.it%s' % static('/ci8/images/share/digipass_go_6.jpg'),
    }

    return render_to_response('ci8/md.html', ctx, context_instance=RequestContext(request))


@staticview(path='sitemap.xml')
def sitemap(request):
    ctx = {
        'pages': pages,
    }

    return render_to_response('ci8/sitemap.xml', ctx, content_type='application/xml')
