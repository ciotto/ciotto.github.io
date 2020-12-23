from django.shortcuts import render_to_response
from staticsites.decorators import staticview

from ci8.articles import *
from ci8.models import Page

# Pages
home_page = Page(
    name='Home',
    path='index.html',
    date=date(2019, 4, 18),
    lastmod=date(2020, 1, 29),
    changefreq='monthly',
    priority=1,
)
about_me_page = Page(
    name='About me',
    title='Christian Bianciotto',
    path='about.html',
    date=date(2019, 4, 18),
    changefreq='monthly',
    priority=0.9,
)

tags_page = Page(
    title='Tags',
    path='tags.html',
    date=date(2019, 4, 26),
    lastmod=date.today(),
    changefreq='monthly',
    priority=0.9,
)
categories_page = Page(
    title='Categories',
    path='categories.html',
    date=date(2020, 12, 22),
    lastmod=date.today(),
    changefreq='monthly',
    priority=0.9,
)
cookies_policy_page = Page(
    path='cookies-policy.html',
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

pages = [
    home_page,
    categories_page,
    about_me_page,
]

base_ctx = {
    'pages': pages,
}


@staticview(path=home_page.path)
def index(request):
    ctx = dict(base_ctx)
    ctx.update(home_page.__dict__)
    ctx.update({
        'series': series,
        'articles': last_articles,
    })

    return render_to_response('ci8/index.html', ctx)


@staticview(path=about_me_page.path)
def about_me(request):
    ctx = dict(base_ctx)
    ctx.update(about_me_page.__dict__)

    return render_to_response('ci8/about.html', ctx)


@staticview(path=haier_t32x_page.path)
def haier_t32x(request):
    ctx = dict(base_ctx)
    ctx.update(haier_t32x_page.__dict__)

    return render_to_response('ci8/md.html', ctx)


@staticview(path=digipass_go_6_page.path)
def digipass_go_6(request):
    ctx = dict(base_ctx)
    ctx.update(digipass_go_6_page.__dict__)

    return render_to_response('ci8/md.html', ctx)


@staticview(path=multiple_choice_test_omr_page.path)
def multiple_choice_test_omr(request):
    ctx = dict(base_ctx)
    ctx.update(multiple_choice_test_omr_page.__dict__)

    return render_to_response('ci8/md.html', ctx)


@staticview(path=mod_wsgi_error_page.path)
def mod_wsgi_error(request):
    ctx = dict(base_ctx)
    ctx.update(mod_wsgi_error_page.__dict__)

    return render_to_response('ci8/md.html', ctx)


@staticview(path=categories_page.path)
def categories(request):
    ctx = dict(base_ctx)
    ctx.update(categories_page.__dict__)
    ctx.update({
        'categories': main_categories,
    })

    return render_to_response('ci8/categories.html', ctx)


@staticview(path=tags_page.path)
def tags(request):
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

    ctx = dict(base_ctx)
    ctx.update(tags_page.__dict__)
    ctx.update({
        'tags': tags,
    })

    return render_to_response('ci8/tags.html', ctx)


@staticview(path=cookies_policy_page.path)
def cookies_policy(request):
    ctx = cookies_policy_page

    return render_to_response('cookies/cookies.html', ctx)


@staticview(path='sitemap.xml')
def sitemap(request):
    ctx = {
        'pages': pages + articles + [tags_page, cookies_policy_page],
    }

    return render_to_response('ci8/sitemap.xml', ctx, content_type='application/xml')
