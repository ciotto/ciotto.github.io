import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

import settings
from pages import all_pages, sitemap_page


def render_page(page):
    file_loader = FileSystemLoader(os.path.join(settings.BASE_DIR, 'templates'))
    env = Environment(loader=file_loader, extensions=['jinja2.ext.i18n'])

    template = env.get_template(page.template)

    output = template.render(page=page)

    dirname = os.path.dirname(os.path.abspath(page.path))
    if not os.path.isdir(dirname):
        Path(dirname).mkdir(parents=True, exist_ok=True)

    with open(os.path.join('docs', page.path), 'w') as f:
        f.write(output)


def main():
    for page in all_pages + [sitemap_page]:
        for language in page.languages:
            page.localize(language)
            render_page(page)


if __name__ == '__main__':
    main()
