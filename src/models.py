from datetime import date

from utilities import lang_to_locale


class Category:
    def __init__(self, **entries):
        self.__dict__.update({
            'parent': None,
            'slug': None,
            'name': None,
            'icon': 'fas fa-quote-right',
            'icon_svg': None,
            'page': None,
        })
        self.__dict__.update(entries)

    @property
    def children(self):
        from categories import category_list

        return [c for c in category_list if c.parent and c.parent.slug == self.slug]

    @property
    def pages(self):
        from articles import articles

        return [a for a in articles if a.category and a.category.slug == self.slug]


class LocalizedPage:
    lang = 'en'

    def __init__(self, **entries):
        self.__dict__.update(entries)


class Page:
    title = None
    description = 'Something about all.'
    lang = 'en'
    date = date(2019, 4, 18)
    lastmod = None
    changefreq = 'monthly'
    priority = 0.8
    author = 'Christian Bianciotto'
    og_image = 'https://ci8.it/images/share/ci8.jpg'
    robots = 'index, follow'

    _localized_pages = None
    _localized_dict = None

    def __init__(self, localized_pages=None, **entries):
        self.__dict__.update(entries)

        self._localized_pages = localized_pages
        self._localized_dict = self._localized_dict or {}

    def __getattribute__(self, item):
        if item not in [
            'localized_pages',
            '_localized_pages',
            'localized_page',
            'localized_dict',
            '_localized_dict',
            'lang',
            '__dict__',
        ] and item in self.localized_dict and self.localized_dict[item]:
            return self.localized_dict[item]
        return super().__getattribute__(item)

    @property
    def localized_dict(self):
        if self.lang not in self._localized_dict:
            localized_dict = dict(self.__dict__)
            localized_page = self.localized_page
            if localized_page:
                localized_dict.update(localized_page.__dict__)
            self._localized_dict[self.lang] = localized_dict
        return self._localized_dict[self.lang]

    @property
    def menu(self):
        from pages import pages
        return pages

    @property
    def languages(self):
        if not self._localized_pages:
            return [self.lang]
        return [l.lang for l in self._localized_pages]

    @property
    def alt_languages(self):
        return [l for l in self.languages if l != self.lang]

    @property
    def locales(self):
        if not self._localized_pages:
            return [self.locale]
        return [l.locale for l in self._localized_pages]

    @property
    def alt_locales(self):
        return [l for l in self.locales if l != self.locale]

    def localize(self, lang):
        self.lang = lang
        return self

    @property
    def localized_pages(self):
        if self._localized_pages:
            lang = self.lang
            for l in self._localized_pages:
                self.localize(l.lang)
                yield self
            self.localize(lang)
        else:
            yield self

    @property
    def alt_localized_pages(self):
        if self._localized_pages:
            lang = self.lang
            for l in self._localized_pages:
                if l.lang != lang:
                    self.localize(l.lang)
                    yield self
            self.localize(lang)

    @property
    def localized_page(self):
        if self._localized_pages:
            for l in self._localized_pages:
                if l.lang == self.lang:
                    return l
        return None

    @property
    def locale(self):
        return lang_to_locale(self.lang)

    @property
    def name(self):
        if 'name' in self.localized_dict:
            return self.localized_dict['name']
        return self.title

    @property
    def path(self):
        if 'path' in self.localized_dict:
            return self.localized_dict['path']
        return '%s.html' % self.slug

    @property
    def template(self):
        if 'template' in self.localized_dict:
            return self.localized_dict['template']
        return '%s.html' % self.slug

    def __str__(self):
        return str(self.title or self.name)

