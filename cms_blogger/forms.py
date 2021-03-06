from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.contrib.sites.models import Site
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.auth.models import User
from django.utils.translation import get_language, ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.forms.utils import ErrorList
from django.conf import settings
from django.db import router
from django import forms

from cms.plugin_pool import plugin_pool
from cms.plugins.text.settings import USE_TINYMCE
from cms.plugins.text.widgets.wymeditor_widget import WYMEditor
from cms.utils.plugins import get_placeholders
from cms.models import Page, Title
from cms.exceptions import NoHomeFound
from cms_layouts.models import Layout
from cms_layouts import slot_finder
from cms.templatetags.cms_admin import admin_static_url

from django_select2 import fields as f

from . import models as m
from . import widgets as w
from . import slug as slug_utils
from . import utils
from . import settings as blog_settings

import json


class BlogLayoutInlineFormSet(BaseGenericInlineFormSet):

    def clean(self):
        if any(self.errors):
            return
        data = filter(lambda x: not x.get('DELETE', False), self.cleaned_data)

        if len(data) < 1:
            raise ValidationError('At least one layout is required!')

        if len(data) > len(m.Blog.LAYOUTS_CHOICES):
            layout_types_count = len(m.Blog.LAYOUTS_CHOICES)
            raise ValidationError(
                'There can be a maximum of %d layouts.' % layout_types_count)

        submitted_layout_types = [layout.get('layout_type')
                                  for layout in data]

        if len(submitted_layout_types) != len(set(submitted_layout_types)):
            raise ValidationError(
                "You can have only one layout for each layout type.")

        specific_layout_types = [
            layout_type
            for layout_type in m.Blog.LAYOUTS_CHOICES.keys()
            if layout_type != m.Blog.ALL]

        # if the default blog layout type is not submitted check if there
        #   are layouts for all of the rest types
        if m.Blog.ALL not in submitted_layout_types:
            if not all([specific_layout_type in submitted_layout_types
                        for specific_layout_type in specific_layout_types]):
                pretty_specific_layout_types = (
                    m.Blog.LAYOUTS_CHOICES[layout_type]
                    for layout_type in specific_layout_types)
                raise ValidationError(
                    "If you do not have a layout for %s you need to specify "
                    "a layout for all the rest layout types: %s" % (
                        m.Blog.LAYOUTS_CHOICES[m.Blog.ALL],
                        ', '.join(pretty_specific_layout_types)))
        return self.cleaned_data


class HomeBlogLayoutInlineFormSet(BaseGenericInlineFormSet):

    def clean(self):
        if any(self.errors):
            return
        data = filter(lambda x: not x.get('DELETE', False), self.cleaned_data)
        if len(data) != 1:
            raise ValidationError('One layout is required.')
        return self.cleaned_data


def get_page_choices(blog):
    if not blog:
        return []
    available_choices = Title.objects.filter(
        page__site=blog.site,
        language=get_language()).values_list(
            'page', 'page__level', 'title').order_by(
                'page__tree_id', 'page__lft')
    return [
        (page, mark_safe('%s%s' % (2 * level * '&nbsp;', title)))
        for page, level, title in available_choices]


def is_valid_for_layout(page, raise_errors=True):
    """
    Checks if a page can be used for a layout
    """
    try:
        slots = get_placeholders(page.get_template())
        slot_finder.get_fixed_section_slots(slots)
    except slot_finder.MissingRequiredPlaceholder as e:
        if not raise_errors:
            return False
        raise ValidationError(
            "Page %s is missing a required placeholder named %s. Add this "
            "placeholder in the page template." % (page, e.slot, ))
    except Exception as page_exception:
        if not raise_errors:
            return False
        raise ValidationError(
            "Error found while scanning template from page %s: %s. "
            "You need to fix this manually." % (page, page_exception))
    return True


def validate_for_layout(page_id):
    if not page_id:
        raise ValidationError('Select a page for this layout.')
    try:
        page = Page.objects.get(id=page_id)
    except Page.DoesNotExist:
        raise ValidationError(
            'This page does not exist. Refresh this form and select an '
            'existing page.')
    is_valid_for_layout(page)
    return page


class LayoutForm(forms.ModelForm):
    from_page = forms.IntegerField(
        label='Inheriting layout from page', widget=forms.Select())

    def clean_from_page(self):
        from_page_id = self.cleaned_data.get('from_page', None)
        return validate_for_layout(from_page_id)

    class Meta:
        model = Layout
        fields = ('from_page', )


class BlogLayoutForm(LayoutForm):
    layout_type = forms.IntegerField(
        label='Layout Type',
        widget=forms.Select(choices=m.Blog.LAYOUTS_CHOICES.items()))

    class Meta:
        fields = ('layout_type', 'from_page', )

    def clean_layout_type(self):
        layout_type = self.cleaned_data.get('layout_type', None)
        if layout_type is None:
            raise ValidationError("Layout Type required")
        if layout_type not in m.Blog.LAYOUTS_CHOICES.keys():
            raise ValidationError(
                "Not a valid Layout Type. Valid choices are: %s" % (
                    ', '.join(m.Blog.LAYOUTS_CHOICES.values())))
        return layout_type


class MultipleUserField(f.AutoModelSelect2MultipleField):
    search_fields = ['first_name__icontains', 'last_name__icontains',
                     'email__icontains', 'username__icontains']
    queryset = User.objects.all()
    empty_values = [None, '', 0]

    def label_from_instance(self, obj):
        return utils.user_display_name(obj)


def _save_related(form, commit, model_obj, *form_functions):
    """
    Allowes 'form_functions' to be called just after the form saved the
        model instance. Useful in cases where m2m objects are saved from form
        and not from inlines.
    """
    def call_post_save():
        for post_save_func in form_functions:
            post_save_func(model_obj)

    if commit:
        call_post_save()
        return
    original_save_m2m = form.save_m2m
    if hasattr(original_save_m2m, '_save_related_attached'):
        return

    def _extra_save_m2m():
        call_post_save()
        original_save_m2m()
    form.save_m2m = _extra_save_m2m
    setattr(form.save_m2m, '_save_related_attached', True)


class AbstractBlogForm(forms.ModelForm):
    requires_request = True
    help_text = {}

    def __init__(self, *args, **kwargs):
        for field_name, text in self.help_text.items():
            if field_name in self.base_fields:
                self.base_fields[field_name].help_text = text
        if not hasattr(self, 'request'):
            self.request = kwargs.pop('request', None)
        super(AbstractBlogForm, self).__init__(*args, **kwargs)
        self._has_valid_root = False

    def set_site(self, site):

        @utils.set_cms_site
        def change_session_site(request):
            return site

        change_session_site(self.request)

    def _get_default_layout_page(self, site):
        page = Page.objects.on_site(site).all_root().order_by("tree_id")[:1]
        if page:
            return page[0]
        return None

    def _clean_home_page(self, site):
        first_root = self._get_default_layout_page(site)
        if not first_root:
            raise ValidationError(
                "The site you are working on does not have a valid layout "
                "page. You need to have at least a root page before you can"
                " add a blog.")
        if is_valid_for_layout(first_root, raise_errors=False):
            self._has_valid_root = True

    def _add_default_layout(self, blog):
        if blog.layouts.count() == 0:
            from_page = self.cleaned_data.get(
                'layout_page', self._get_default_layout_page(blog.site))
            article_layout = Layout()
            article_layout.from_page = from_page
            article_layout.content_object = blog
            article_layout.save()

    def clean_in_navigation(self):
        in_navigation = self.cleaned_data.get('in_navigation', False)
        if in_navigation:
            if not self.instance.navigation_node:
                raise ValidationError(
                    "Choose a location in the navigation menu")
        return in_navigation


class BlogForm(AbstractBlogForm):
    categories = forms.CharField(help_text=_('Categories help text'))
    allowed_users = MultipleUserField(label="Add Users")

    class Media:
        css = {
            'all': (
                static('cms_blogger/css/redmond-jquery-ui.css'),
                static('cms_blogger/css/jquery.tagit.css'),)
        }
        js = (static('cms_blogger/js/jquery-1.9.1.min.js'),
              static('cms_blogger/js/jquery-ui.min.js'),
              static('cms_blogger/js/tag-it.js'),
              static('cms_blogger/js/categories-widget.js'),)

    class Meta:
        model = m.Blog
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self._init_categories_field(self.instance)
        if (not self.is_bound and self.instance.layouts.count() == 0):
            self.missing_layouts = ErrorList([
                "This blog is missing a layout. "
                "Add one in the Layouts section."])
        else:
            self.missing_layouts = False
        self.set_site(self.instance.site)

    def _init_categories_field(self, blog):
        categories_field = self.fields.get('categories', None)
        if blog and blog.pk and not categories_field.initial:
            names = blog.categories.order_by('name').values_list(
                'name', flat=True)
            categories_field.initial = ', '.join(names)

    def clean_categories(self):
        categories = self.cleaned_data.get('categories', '')
        if not categories:
            raise ValidationError("Add at least one category.")

        categories_names = [name.strip().lower()
                            for name in categories.split(',')]
        invalid = [name
                   for name in categories_names
                   if not 3 <= len(name) <= 30]
        if invalid:
            invalid_names = ', '.join(invalid)
            raise ValidationError(
                "Following categories have invalid length: %s. Category names"
                " must have between 3 and 30 characters." % invalid_names)
        return categories_names

    def clean_slug(self):
        slug = slugify(self.cleaned_data.get('slug', '').strip())
        if not slug:
            raise ValidationError('Slug required.')
        if m.Blog.objects.exclude(pk=self.instance.pk).filter(
                site=self.instance.site, slug=slug).exists():
            raise ValidationError("Blog with this slug already exists.")
        return slug

    def clean_disqus_shortname(self):
        disqus_enabled = self.cleaned_data.get('enable_disqus', None)
        disqus_shortname = self.cleaned_data.get('disqus_shortname', None)
        if disqus_enabled and not disqus_shortname:
            raise ValidationError('Disqus shortname required.')
        return disqus_shortname

    def _save_categories(self, saved_blog):
        names = set(self.cleaned_data.get('categories', []))
        existing_names = set(saved_blog.categories.values_list(
            'name', flat=True))
        removed_categories = existing_names - names
        new_category_names = names - existing_names

        for name in new_category_names:
            m.BlogCategory.objects.create(name=name, blog=saved_blog)

        for category in m.BlogCategory.objects.filter(
                name__in=removed_categories, blog=saved_blog):
            category.delete()

    def save(self, commit=True):
        saved_instance = super(BlogForm, self).save(commit=commit)
        _save_related(self, commit, saved_instance, self._save_categories)
        return saved_instance


class HomeBlogForm(AbstractBlogForm):
    help_text = {
        'title': _('Super Landing Page title'),
        'tagline': _('Super Landing Page tagline'),
        'branding_image': _('Super Landing Page branding image'),
        'in_navigation': _('Super Landing Page in navigation'),
        'site': _('Super Landing Page site')
    }
    labels = {'in_navigation': _('Super Landing Page label in navigation')}

    def __init__(self, *args, **kwargs):
        self.base_fields['in_navigation'].label = self.labels['in_navigation']
        super(HomeBlogForm, self).__init__(*args, **kwargs)
        self.set_site(self.instance.site)
        if 'title' not in self.initial:
            self.initial['title'] = 'Latest blog posts'

    class Meta:
        model = m.HomeBlog
        exclude = ()


class BlogLayoutMissingForm(AbstractBlogForm):

    layout_page = forms.IntegerField(
        label='Inheriting layout from page', widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(BlogLayoutMissingForm, self).__init__(*args, **kwargs)
        choices = get_page_choices(self.instance)
        self.fields['layout_page'].widget.choices = choices
        if not self.errors:
            self.missing_layouts = ErrorList([_('Blog Form Missing Layout')])
        else:
            self.missing_layouts = False

    def clean_layout_page(self):
        layout_page_id = self.cleaned_data.get('layout_page', None)
        return validate_for_layout(layout_page_id)

    def save(self, commit=True):
        saved = super(BlogLayoutMissingForm, self).save(commit=commit)
        _save_related(self, commit, saved, self._add_default_layout)
        return saved

    class Meta:
        model = m.Blog
        fields = ('layout_page', )


class BlogAddForm(AbstractBlogForm):

    def clean(self):
        site = Site.objects.get_current()
        self.instance.site = site
        slug = self.cleaned_data.get('slug', None)
        if m.Blog.objects.filter(site=self.instance.site, slug=slug).exists():
            raise ValidationError("Blog with this slug already exists.")
        self._clean_home_page(site)
        return self.cleaned_data

    def _allow_current_user(self, blog):
        if (blog.allowed_users.count() == 0 and
                self.request and self.request.user):
            blog.allowed_users.add(self.request.user)

    def save(self, commit=True):
        saved = super(BlogAddForm, self).save(commit=commit)
        _call = [self._allow_current_user]
        if self._has_valid_root:
            _call.append(self._add_default_layout)
        _save_related(self, commit, saved, *_call)
        return saved

    class Meta:
        model = m.Blog
        fields = ('title', 'slug',)


class HomeBlogAddForm(AbstractBlogForm):
    help_text = {
        'title': _('Super Landing Page title'),
        'site': _('Super Landing Page site')
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        if self.request and not self.request.user.is_superuser:
            allowed_sites = utils.get_allowed_sites(self.request, m.HomeBlog)
        else:
            allowed_sites = Site.objects.all()
        site_field = self.base_fields['site']
        site_field.queryset = allowed_sites.filter(homeblog=None)
        site_field.widget.can_add_related = False
        super(HomeBlogAddForm, self).__init__(*args, **kwargs)
        if 'title' not in self.initial:
            self.initial['title'] = 'Latest blog posts'
        current_site = utils.get_current_site(self.request, m.HomeBlog)
        if ('site' not in self.initial and
                current_site in site_field.queryset):
            self.initial['site'] = current_site

    def clean_site(self):
        site = self.cleaned_data.get('site')
        if not site:
            raise ValidationError("Site is required.")
        if site not in utils.get_allowed_sites(self.request, m.HomeBlog):
            raise ValidationError("You do not have permissions on this site.")
        if m.HomeBlog.objects.filter(site=site).exists():
            raise ValidationError(
                "This site already has a %s. You may only have one %s per"
                " site. You may change it from the list view." % (
                    (m.HomeBlog._meta.verbose_name.lower(), ) * 2))
        return site

    def clean(self):
        self._clean_home_page(self.cleaned_data.get('site'))
        return self.cleaned_data

    def save(self, commit=True):
        saved = super(HomeBlogAddForm, self).save(commit=commit)
        if self._has_valid_root:
            _save_related(self, commit, saved, self._add_default_layout)
        # current site is required in the navigation tool from the change form
        self.set_site(self.instance.site)
        return saved

    class Meta:
        model = m.HomeBlog
        fields = ('site', 'title')


_ADD_HIDDEN_VAR_TO_FORM = (
    "jQuery(this).closest('form').append("
    "jQuery('<input>').attr('type', 'hidden').attr('name', '%s').val(%s))%s;")


class EntryChangelistForm(forms.ModelForm):

    is_published = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={
            'onclick': _ADD_HIDDEN_VAR_TO_FORM % (
                '_save', '"Save"', ".submit()")}))

    def __init__(self, *args, **kwargs):
        entry = kwargs.get('instance', None)
        pub_field = self.base_fields['is_published']
        if entry and entry.is_draft:
            pub_field.widget.attrs['disabled'] = 'disabled'
        else:
            pub_field.widget.attrs.pop('disabled', None)
        super(EntryChangelistForm, self).__init__(*args, **kwargs)

    def clean_is_published(self):
        is_published = self.cleaned_data.get('is_published')
        if not self.instance:
            return is_published

        if is_published != self.instance.is_published:
            if not is_published:
                self.instance.start_publication = None
                self.instance.end_publication = None

            self.instance.publication_date = timezone.now()

        self.instance.update_date = timezone.now()
        return is_published

    class Meta:
        model = m.BlogEntryPage
        exclude = ()


class BlogEntryPageAddForm(forms.ModelForm):
    requires_request = True

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        # filter available blog choices
        site = Site.objects.get_current()
        blog_field = self.base_fields['blog']
        allowed_blogs = blog_field.queryset.filter(site=site)
        if request and not request.user.is_superuser:
            allowed_blogs = allowed_blogs.filter(
                allowed_users=request.user)
        blog_field.queryset = allowed_blogs
        blog_field.widget.can_add_related = False
        super(BlogEntryPageAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = m.BlogEntryPage
        fields = ('blog', )


def _get_text_editor_widget():
    installed_plugins = plugin_pool.get_all_plugins()
    plugins = [plugin for plugin in installed_plugins if plugin.text_enabled]

    try:
        from cms.plugins.text.widgets.ckeditor_widget import CKEditor
        return CKEditor(installed_plugins=plugins)
    except ImportError:
        pass

    if USE_TINYMCE and "tinymce" in settings.INSTALLED_APPS:
        from cms.plugins.text.widgets.tinymce_widget import TinyMCEEditor
        return TinyMCEEditor(installed_plugins=plugins, mce_attrs={
            'theme_advanced_buttons1': (
                'forecolor, bold, italic, underline, link, unlink, numlist, '
                'bullist, outdent, indent, formatselect, image, code'),
            'theme_advanced_buttons2_add': (
                'justifyleft, justifycenter, justifyright, justifyfull,'
                'fontselect, fontsizeselect'),
            'theme_advanced_buttons3_add': (
                'strikethrough, sub, sup, fullscreen'),
            'theme_advanced_toolbar_location': 'top',
            'theme_advanced_toolbar_align': 'left',
            'setup': 'tinyMCESetup'
        })
    else:
        return WYMEditor(installed_plugins=plugins)


class ButtonField(forms.Field):

    def __init__(self, *args, **kwargs):
        kwargs["label"] = ""
        kwargs["required"] = False
        super(ButtonField, self).__init__(*args, **kwargs)


class AuthorsField(f.AutoModelSelect2TagField):
    queryset = m.Author.objects.db_manager(router.db_for_write(m.Author))
    empty_values = [None, '', 0]
    search_fields = ['name__icontains', 'user__first_name__icontains',
                     'user__last_name__icontains', 'user__email__icontains',
                     'user__username__icontains']

    def get_model_field_values(self, value):
        if not value:
            raise ValidationError("This field is required.")
        return {'name': value}

    def make_authors(self):
        # since this might be a GET request and it does a db updates,
        #   ensure it uses the 'write' db for reads also
        author_mgr = m.Author.objects.db_manager(router.db_for_write(m.Author))
        user_mgr = User.objects.db_manager(router.db_for_write(User))
        users_used = author_mgr.filter(
            user__isnull=False).values_list('user', flat=True)
        candidates_for_author = user_mgr.exclude(id__in=users_used)
        for user in candidates_for_author:
            author_mgr.get_or_create(name='', user=user)
        return author_mgr.all()


class BlogEntryPageChangeForm(forms.ModelForm):
    requires_request = True

    body = forms.CharField(
        label='Blog Entry', required=True)
    authors = AuthorsField()
    poster_image_uploader = forms.CharField(label="", widget=w.PosterImage())
    categories = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        help_text=_("Check all the categories to apply to this "
                    "post. Uncheck to remove."),
        queryset=m.BlogCategory.objects.none(), required=False)

    publish = ButtonField(widget=w.ButtonWidget(
        submit=True,
        on_click=_ADD_HIDDEN_VAR_TO_FORM % ('_pub_pressed', 'true', "")))

    schedule_publish = ButtonField(widget=w.ButtonWidget(
        attrs={'class': 'pull-right'},
        submit=True, text='Schedule Publish',
        on_click=_ADD_HIDDEN_VAR_TO_FORM % (
            '_schedule_pub_pressed', 'true', "")))

    schedule_unpublish = ButtonField(widget=w.ButtonWidget(
        attrs={'style': 'float: right'},
        submit=True, text='Schedule Unpublish',
        on_click=_ADD_HIDDEN_VAR_TO_FORM % (
            '_schedule_unpub_pressed', 'true', "")))

    start_publication = forms.Field(
        required=False, widget=w.DateTimeWidget())
    end_publication = forms.Field(
        required=False, widget=w.DateTimeWidget())

    save_button = ButtonField(widget=w.ButtonWidget(submit=True, text='Save'))
    preview_on_top = ButtonField(widget=w.ButtonWidget(text='Preview'))

    class Media:
        css = {"all": ("cms_blogger/css/entry-change-form.css",
                       "cms_blogger/css/jquery.custom-scrollbar.css")}
        js = ('cms_blogger/js/tinymce-extend.js',
              'cms_blogger/js/entry-admin.js',
              'cms_blogger/js/jquery.custom-scrollbar.min.js',
              'cms_blogger/js/admin-collapse.js',
              'cms_blogger/js/entry-preview.js', )

    class Meta:
        model = m.BlogEntryPage
        exclude = ('content', 'blog', 'slug', 'publication_date')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        instance = kwargs.get('instance')
        self._init_categ_field(instance) if instance else ''
        super(BlogEntryPageChangeForm, self).__init__(*args, **kwargs)
        self._init_preview_buttons()
        self._init_poster_image_widget()
        self._init_publish_button()
        self._init_save_button()
        self._init_authors_field(request)
        self.fields['body'].widget = _get_text_editor_widget()
        if 'body' not in self.initial:
            self.initial['body'] = self.instance.content_body

    def _init_authors_field(self, request):
        self.fields['authors'].widget.options['tokenSeparators'] = [',']
        self.fields['authors'].make_authors()
        if (request and not self.initial.get('authors', None) and
                self.instance.authors.count() == 0):
            self.initial['authors'] = m.Author.objects.filter(
                name='', user=request.user.pk)[:1]

    def _init_categ_field(self, entry):
        categories_field = self.base_fields.get('categories')
        if categories_field and entry.blog:
            categories_field.queryset = entry.blog.categories.order_by('name')
            categories_field.initial = entry.categories.filter(
                blog=entry.blog)

    def _init_publish_button(self):
        pub_button = self.fields['publish'].widget
        if self.instance.is_published:
            pub_button.text = 'Unpublish'
        else:
            pub_button.text = 'Publish Now'

    def _init_save_button(self):
        pub_button = self.fields['save_button'].widget
        if self.instance.is_published:
            pub_button.text = 'Update'
        else:
            pub_button.text = 'Save and Continue'

    def _init_preview_buttons(self):
        preview = self.fields['preview_on_top'].widget
        preview.link_url = reverse(
            'admin:cms_blogger-entry-preview', args=[self.instance.id])
        preview.on_click = "return showEntryPreviewPopup(this,'%s');" % (
            admin_static_url(), )

    def _init_poster_image_widget(self):
        poster_widget = self.fields['poster_image_uploader'].widget
        poster_widget.blog_entry_id = self.instance.pk
        poster_widget.image_url = None
        if self.instance.poster_image and self.instance.poster_image.name:
            poster_widget.image_url = self.instance.poster_image.url

    def clean_body(self):
        body = self.cleaned_data.get('body')
        self.instance.content_body = body
        return body

    def clean_title(self):
        title = self.cleaned_data.get('title').strip()
        empty_qs = m.BlogEntryPage.objects.none()
        # slug is generated only the first time
        if not self.instance.slug:
            slug = slug_utils.get_unique_slug(self.instance, title, empty_qs)
            if not slug:
                raise ValidationError(
                    "Cannot generate slug from this title. Enter a valid"
                    " title consisting of letters, numbers or underscores.")
            if slug in blog_settings.DISALLOWED_ENTRIES_SLUGS:
                raise ValidationError(
                    "Cannot use slug generated from this title %s. This is a "
                    "system reserved slug. Change the title so that it can "
                    "generate a different slug." % slug)
        return title

    def _set_publication_date(self):
        was_published = self.instance.is_published
        publish_toggle = bool(self.data.get('_pub_pressed'))
        if publish_toggle:
            self.instance.is_published = not self.instance.is_published
        elif (bool(self.data.get('_schedule_pub_pressed')) or
                bool(self.data.get('_schedule_unpub_pressed'))):
            self.instance.is_published = True

        now = timezone.now()
        if not self.instance.is_published:
            # entry got unpublished
            self.cleaned_data['start_publication'] = None
            self.cleaned_data['end_publication'] = None
            self.instance.publication_date = now
            return

        start_date = self.cleaned_data.get('start_publication')
        if start_date != self.instance.start_publication or not was_published:
            self.instance.publication_date = start_date or now
        self.instance.update_date = timezone.now()

    def clean(self):
        start_date = self.cleaned_data.get('start_publication')
        end_date = self.cleaned_data.get('end_publication')
        if (start_date and end_date and not start_date < end_date):
            raise ValidationError("Incorrect publication dates interval.")
        self._set_publication_date()
        return self.cleaned_data

    def _save_categories(self, saved_entry):
        submitted_categories = self.cleaned_data.get('categories', [])
        blog = saved_entry.blog
        saved_entry.categories.clear()
        if blog and submitted_categories:
            saved_entry.categories = submitted_categories.filter(blog=blog)

    def _remove_unused_authors(self, saved_entry):
        submitted = [ath.pk for ath in self.cleaned_data.get('authors', [])]
        # exclude sumbitted authors + authors generated from users
        check_for_complete_removal = saved_entry.authors.exclude(
            id__in=submitted).filter(user__isnull=True)
        rest_of_entries = m.BlogEntryPage.objects.exclude(pk=saved_entry.pk)
        for author in check_for_complete_removal:
            entries_for_author = rest_of_entries.filter(authors=author.pk)
            if not entries_for_author.exists():
                author.delete()

    def save(self, commit=True):
        saved_instance = super(BlogEntryPageChangeForm, self).save(
            commit=commit)
        _save_related(self, commit, saved_instance,
                      self._save_categories, self._remove_unused_authors)
        return saved_instance


class BlogRiverForm(forms.ModelForm):
    requires_request = True
    cancel_filter_btn_html = (
        '<span class="input-group-btn">'
        '<button class="btn btn-white multiselect-clear-filter" type="button">'
        '<i class="fa fa-times-circle red2"></i></button></span>')
    entries_ordering = forms.ChoiceField(
        widget=w.BootstrapSelect(
            attrs={
                'multiselect': json.dumps({
                    "selectedList": 1,
                    "header": "Choose categories below",
                    "buttonClass": "btn btn-white btn-primary",
                    "enableFiltering": False,
                    "templates": {
                        "filterClearBtn": cancel_filter_btn_html,
                    }
                }),
                "max_items_allowed": 1,
            }),
        choices=m.OrderEntriesMixin.ordering_choices,
    )
    categories = forms.MultipleChoiceField(
        widget=w.BootstrapMultiselect(
            attrs={
                'multiselect': json.dumps({
                    "selectedList": m.MAX_CATEGORIES_IN_PLUGIN,
                    "header": "Choose categories below",
                    "buttonClass": "btn btn-white btn-primary",
                    "enableFiltering": True,
                    "templates": {
                        "filterClearBtn": cancel_filter_btn_html,
                    }
                }),
                "max_items_allowed": m.MAX_CATEGORIES_IN_PLUGIN,
            }))
    spinner_opts = ('{min: 3, max: 10,'
                    'btn_up_class: "btn-info", btn_down_class: "btn-info"}')
    number_of_entries = forms.CharField(
        widget=w.SpinnerWidget(attrs={'spinner': spinner_opts}))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        plugin_page = getattr(request, 'current_page', None)
        categories_field = self.base_fields.get('categories')
        if plugin_page and plugin_page.site and categories_field:
            categories_field.choices = [
                (name, name)
                for name in m.BlogCategory.objects.filter(
                        blog__site=plugin_page.site
                ).order_by('name').values_list('name', flat=True).distinct()]

        super(BlogRiverForm, self).__init__(*args, **kwargs)
        self._init_categories()
        self._init_number_of_entries_field()

    def _init_categories(self):
        if (self.instance and self.instance.categories):
            names = self.instance.categories.split(',')
            self.initial['categories'] = names

    def _init_number_of_entries_field(self):
        if not self.initial.get('number_of_entries'):
            self.initial['number_of_entries'] = "%d" % (
                self.instance.number_of_entries, )

    def clean_categories(self):
        categories = set(self.cleaned_data.get('categories'))
        if len(categories) > m.MAX_CATEGORIES_IN_PLUGIN:
            raise ValidationError(
                'You can add only %d categories.' % m.MAX_CATEGORIES_IN_PLUGIN)
        return ','.join(list(categories))

    def clean_number_of_entries(self):
        no_entries = self.cleaned_data.get('number_of_entries', None)
        try:
            no_entries = int(no_entries)
        except:
            no_entries = None
        if not no_entries or no_entries < 3 or no_entries > 10:
            raise ValidationError('Choose a number from 3 to 10.')
        return no_entries

    class Meta:
        model = m.RiverPlugin
        exclude = ()


class MoveEntriesForm(forms.Form):
    mirror_categories = forms.BooleanField(
        label="Create missing categories in destination blog",
        help_text="<p>(Categories from source blogs will be deleted if they "
                  "have no entries left after the move operation.)</p>",
        initial=True,
        required=False)
    entries = forms.ModelMultipleChoiceField(
        queryset=m.BlogEntryPage.objects.none(),
        initial=m.BlogEntryPage.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        label="The following blog entries will be "
              "moved to the destination blog",
        required=False)

    def __init__(self, *args, **kwargs):
        entries = kwargs.pop('entries', m.BlogEntryPage.objects.none())
        checked = kwargs.pop('checked', m.BlogEntryPage.objects.none())
        destination_blog = kwargs.pop('destination_blog', None)
        super(MoveEntriesForm, self).__init__(*args, **kwargs)
        self.fields['destination_blog'] = forms.ModelChoiceField(
            m.Blog.objects.filter(
                site=Site.objects.get_current()),
            required=True)
        self.fields['destination_blog'].initial = destination_blog

        self.fields['entries'].queryset = entries
        self.fields['entries'].initial = checked
