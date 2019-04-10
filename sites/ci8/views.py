import os
import requests
from django.shortcuts import render_to_response
from staticsites.decorators import staticview
from markdown2 import Markdown


markdowner = Markdown(extras=['tables', 'fenced-code-blocks'])


def html_from_markdown_url(url):
    base_url = os.path.dirname(url)

    response = requests.get(url)
    content = response.content.replace('](images', '](%s/images' % base_url)
    return markdowner.convert(content)


@staticview
def index(request):
    ctx = {'title': 'Christian Bianciotto'}

    return render_to_response('ci8/index.html', ctx)


@staticview
def haier_t32x(request):
    ctx = {
        'title': 'Reverse the Haier T32X robot',
        'md': html_from_markdown_url('https://raw.githubusercontent.com/ciotto/teardown/master/haier-t32x/README.md'),
    }

    return render_to_response('ci8/md.html', ctx)
