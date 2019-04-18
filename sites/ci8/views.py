import os
import requests
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render_to_response
from django.template import RequestContext
from staticsites.decorators import staticview
from markdown2 import Markdown


markdowner = Markdown(extras=['tables', 'fenced-code-blocks'])


def html_from_markdown_url(url):
    base_url = os.path.dirname(url)

    response = requests.get(url)
    content = response.content.replace('](images', '](%s/images' % base_url)
    return markdowner.convert(content)


# Pages
home_page = {
    'title': 'Home',
    'path': 'index.html',
    'lastmod': '2019-04-18',
    'changefreq': 'monthly',
    'priority': 1,
}
about_me_page = {
    'title': 'About me',
    'path': 'about.html',
    'lastmod': '2019-04-18',
    'changefreq': 'monthly',
    'priority': 0.9,
}
haier_t32x_page = {
    'title': 'Haier T32X robot',
    'path': 'haier-t32x.html',
    'lastmod': '2019-04-18',
    'changefreq': 'monthly',
    'priority': 0.8,
    'md': html_from_markdown_url('https://raw.githubusercontent.com/ciotto/teardown/master/haier-t32x/README.md'),
    'description': 'Reverse engineering the Haier T325 Cleaning Robot.',
    'og_image': 'http://ci8.it%s' % static('/ci8/images/share/haier_t32x.jpg'),
}
digipass_go_6_page = {
    'title': 'DIGIPASS GO 6',
    'path': 'digipass-go-6.html',
    'lastmod': '2019-04-18',
    'changefreq': 'monthly',
    'priority': 0.8,
    'md': html_from_markdown_url('https://raw.githubusercontent.com/ciotto/teardown/master/digipass-go-6/README.md'),
    'description': 'Reverse engineering the Vasco DIGIPASS GO 6.',
    'og_image': 'http://ci8.it%s' % static('/ci8/images/share/digipass_go_6.jpg'),
}
pages = [
    home_page,
    about_me_page,
    haier_t32x_page,
    digipass_go_6_page,
]


@staticview(path=home_page['path'])
def index(request):
    ctx = dict(home_page)
    ctx.update({
        'title': None,
        'pages': pages,
        'articles': [
            haier_t32x_page,
            digipass_go_6_page,
        ]
    })

    return render_to_response('ci8/index.html', ctx, context_instance=RequestContext(request))


@staticview(path=about_me_page['path'])
def about_me(request):
    ctx = dict(about_me_page)
    ctx.update({
        'title': 'Christian Bianciotto',
        'pages': pages,
    })

    return render_to_response('ci8/about.html', ctx, context_instance=RequestContext(request))


@staticview(path=haier_t32x_page['path'])
def haier_t32x(request):
    ctx = dict(haier_t32x_page)
    ctx.update({
        'pages': pages,
    })

    return render_to_response('ci8/md.html', ctx, context_instance=RequestContext(request))


@staticview(path=digipass_go_6_page['path'])
def digipass_go_6(request):
    ctx = dict(digipass_go_6_page)
    ctx.update({
        'pages': pages,
    })

    return render_to_response('ci8/md.html', ctx, context_instance=RequestContext(request))


@staticview(path='sitemap.xml')
def sitemap(request):
    ctx = {
        'pages': pages,
    }

    return render_to_response('ci8/sitemap.xml', ctx, content_type='application/xml')
