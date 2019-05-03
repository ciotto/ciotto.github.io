import os
import re
import requests
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render_to_response
from django.template import RequestContext
from staticsites.decorators import staticview
from markdown2 import Markdown


markdowner = Markdown(extras=['tables', 'fenced-code-blocks'])


def html_from_markdown_url(url, skip_title=1):
    if url.startswith('http://') or url.startswith('https://'):
        base_url = os.path.dirname(url)
        base_image_url = base_url

        response = requests.get(url)
        content = response.content
    else:
        base_url = settings.BASE_REPO_URL + os.path.dirname(url)
        base_image_url = settings.BASE_REPO_IMAGE_URL + os.path.dirname(url)

        with open(url, 'r') as f:
            content = f.read()
    content = '\n'.join(content.split('\n', skip_title)[skip_title:])
    content = re.sub(re.compile(r'!\[(.+)\]\((?!http)(.+)\)', re.MULTILINE), r'![\1](%(path)s/\2)', content) % {
        'path': base_image_url
    }
    content = re.sub(re.compile(r'\[(.+)\]\((?!http)(.+)\)', re.MULTILINE), r'[\1](%(path)s/\2)', content) % {
        'path': base_url
    }
    content = markdowner.convert(content)
    content = content.replace('<table>', '<div class="table-responsive"><table>')
    content = content.replace('</table>', '</table></div>')
    return content


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
    'tags': [
        ('reversing', 'Reversing'),
        ('stm32', 'STM32'),
        ('swd', 'SWD'),
        ('uart', 'UART'),
        ('st-link', 'ST-Link'),
        ('openocd', 'OpenOCD'),
        ('hardware-security', 'Hardware Security'),
    ]
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
    'tags': [
        ('reversing', 'Reversing'),
    ]
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




@staticview(path='tags.html')
def tags(request):
    tags = {}
    for page in pages:
        if 'tags' in page:
            for tag_slug, tag_name in page['tags']:
                if tag_slug not in tags:
                    tags[tag_slug] = {
                        'slug': tag_slug,
                        'name': tag_name,
                        'pages': []
                    }
                tags[tag_slug]['pages'].append(page)
    ctx = {
        'tags': tags,
    }

    return render_to_response('ci8/tags.html', ctx, context_instance=RequestContext(request))
@staticview(path='sitemap.xml')
def sitemap(request):
    ctx = {
        'pages': pages,
    }

    return render_to_response('ci8/sitemap.xml', ctx, content_type='application/xml')
