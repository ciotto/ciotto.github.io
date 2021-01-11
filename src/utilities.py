import os
import re
import requests

from markdown2 import Markdown

import settings

markdowner = Markdown(extras=['tables', 'fenced-code-blocks', 'code-friendly'])


def html_from_markdown_url(url, skip_title=1):

    if url.startswith('http://') or url.startswith('https://'):
        base_url = os.path.dirname(url)
        base_image_url = base_url

        response = requests.get(url)
        content = response.content
    else:
        base_url = settings.BASE_REPO_URL + os.path.dirname(url)
        base_image_url = settings.BASE_REPO_IMAGE_URL + os.path.dirname(url)

        with open(url, 'rb') as f:
            content = f.read()

    content = content.decode('utf-8')
    content = '\n'.join(content.split('\n', skip_title)[skip_title:])
    content = re.sub(re.compile(r'!\[(.+)\]\((?!http)(.+)\)', re.MULTILINE), r'![\1](' + base_image_url + r'/\2)', content)
    content = re.sub(re.compile(r'\[(.+)\]\((?!http)(.+)\)', re.MULTILINE), r'[\1](' + base_url + r'/\2)', content)
    content = markdowner.convert(content)
    content = content.replace('<table>', '<div class="table-responsive"><table>')
    content = content.replace('</table>', '</table></div>')
    return content


def lang_to_locale(lang):
    if lang.lower() == 'en':
        return 'en_GB'
    return '%s_%s' % (lang.lower(), lang.upper())
