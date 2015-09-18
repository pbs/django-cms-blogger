from django.contrib.admin.views.main import ChangeList
from .utils import get_current_site, get_allowed_sites


class BlogChangeList(ChangeList):
    """
    Follows the CMSChangeList logic for setting the current working site.
    """

    def __init__(self, request, model, *args, **kwargs):
        # set site choices for the site chooser widget
        self.sites = get_allowed_sites(request, model).order_by('name')
        self.has_access_to_multiple_sites = len(self.sites) > 1
        self.site_lookup = model.site_lookup
        self.current_site = get_current_site(request, model)
        super(BlogChangeList, self).__init__(request, model, *args, **kwargs)

    def get_queryset(self, request):
        qs = super(BlogChangeList, self).get_queryset(request)
        return qs.filter(**{self.site_lookup: self.current_site})

    def get_results(self, request):
        self.root_queryset = self.root_queryset.filter(
            **{self.site_lookup: self.current_site})
        super(BlogChangeList, self).get_results(request)


class BlogEntryChangeList(BlogChangeList):
    pass
