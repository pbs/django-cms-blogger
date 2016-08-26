import pytest

import cms_blogger.models as m


def make_entry(**options):
    object_dict = dict(
        title=options.get('title', 'title'),
        blog=options.get('blog'),
        short_description=options.get('short_description', 'description'),
        is_published=options.get('is_published', True),
    )
    entry = m.BlogEntryPage.objects.create(**object_dict)
    return entry


@pytest.fixture
def blog_entries(request):
    def fn(self, blog, how_many=4, **qs_options):
        entries = [make_entry(title=str(i), blog=blog)
                   for i in xrange(how_many)]
        if qs_options:
            m.BlogEntryPage.objects.update(**qs_options)
        fixture = {int(entry.title): entry
                   for entry in m.BlogEntryPage.objects.all()}
        return fixture
    request.cls.make_blog_entries = fn

