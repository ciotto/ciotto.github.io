from articles import *
from articles.electronics import glossary_page as electronics_glossary_page
from models import Page

# Pages
home_page = Page(
    name='Home',
    slug='index',
    date=date(2019, 4, 18),
    lastmod=date(2020, 1, 29),
    changefreq='monthly',
    priority=1,
    series=series,
    articles=last_articles,
)
about_me_page = Page(
    name='About me',
    title='Christian Bianciotto',
    slug='about',
    desc='I am Christian an italian Software Engineer and I live near Turin. I love computers and technologies and '
         'I like to work in different sectors, jumping from frontend to backend using always new tools.',
    date=date(2019, 4, 18),
    changefreq='monthly',
    priority=0.9,
)

tags = {}
for page in articles:
    if page.tags:
        for tag_slug, tag_name in page.tags:
            if tag_slug not in tags:
                tags[tag_slug] = {
                    'slug': tag_slug,
                    'name': tag_name,
                    'pages': []
                }
            tags[tag_slug]['pages'].append(page)

tags_page = Page(
    title='Tags',
    slug='tags',
    date=date(2019, 4, 26),
    lastmod=date.today(),
    changefreq='monthly',
    priority=0.9,
    tags=tags,
)
categories_page = Page(
    title='Categories',
    name='Articles',
    slug='categories',
    date=date(2020, 12, 22),
    lastmod=date.today(),
    changefreq='monthly',
    priority=0.9,
    categories=main_categories,
)
cookies_policy_page = Page(
    slug='cookies-policy',
    template='cookies/cookies.html',
    date=date(2020, 1, 17),
    changefreq='yearly',
    priority=0.7,
    cookies={
        'needed': [
            {

                'name': 'EU_COOKIE_LAW_CONSENT',
                'provider': '.ci8.it',
                'purpose': 'Stores the consent status of the user\'s cookies for the current domain.',
                'expiration': '1 year',
            },
        ],
        'preferences': [
        ],
        'statistics': [
            {
                'name': '_ga',
                'provider': '.ci8.it',
                'purpose': 'Register a unique ID used to generate statistical data on how the visitor uses the website.',
                'expiration': '2 years',
            },
            {
                'name': '_gat',
                'provider': '.ci8.it',
                'purpose': 'Used by Google Analytics to limit the frequency of requests.',
                'expiration': '1 day',
            },
            {
                'name': '_gid',
                'provider': '.ci8.it',
                'purpose': 'Register a unique ID used to generate statistical data on how the visitor uses the website.',
                'expiration': '1 day',
            },
        ],
        'marketing': [
        ],
    }
)
codicini_page = Page(
    slug='codicini',
    template='codicini.html',
    date=date(2021, 1, 11),
    changefreq='yearly',
    priority=0.8,
)

pages = [
    home_page,
    categories_page,
    about_me_page,
]

all_pages = pages + articles + [tags_page, cookies_policy_page, electronics_glossary_page, codicini_page]

sitemap_page = Page(
    slug='sitemap',
    path='sitemap.xml',
    changefreq='monthly',
    priority=0.9,
    pages=all_pages,
    template='sitemap.xml',
)
