from datetime import date


class Category:
    def __init__(self, **entries):
        self.__dict__.update({
            'parent': None,
            'slug': None,
            'name': None,
            'icon': 'fas fa-quote-right',
            'page': None,
        })
        self.__dict__.update(entries)

    @property
    def children(self):
        from ci8.categories import category_list

        return [c for c in category_list if c.parent and c.parent.slug == self.slug]

    @property
    def pages(self):
        from ci8.articles import articles

        return [a for a in articles if a.category and a.category.slug == self.slug]


class Page:
    def __init__(self, **entries):
        self.__dict__.update({
            'title': None,
            'path': None,
            'date': date(2019, 4, 18),
            'lastmod': None,
            'changefreq': 'monthly',
            'priority': 0.8,
            'author': 'Christian Bianciotto',
        })
        self.__dict__.update(entries)

    @property
    def name(self):
        if 'name' in self.__dict__:
            return self.__dict__['name']
        return self.title

