from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.template.defaultfilters import slugify
from cms.plugin_pool import plugin_pool
from cms.plugins.text.settings import USE_TINYMCE
from cms.plugins.text.widgets.wymeditor_widget import WYMEditor
from cms_layouts.models import Layout
from .models import Blog, BlogEntry


class BlogLayoutForm(forms.ModelForm):
    layout_type = forms.ChoiceField(
        label='Layout Type', choices=Blog.LAYOUTS_CHOICES.items())

    class Meta:
        model = Layout
        fields = ('layout_type', 'from_page')


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog

    def clean_slug(self):
        return slugify(self.cleaned_data.get('slug', ''))

    def clean_site(self):
        site = self.cleaned_data.get('site')
        if not site:
            return site
        from cms.models import Page
        try:
            cms_home_page = Page.objects.get_home(site)
        except Exception as e:
            raise ValidationError("%s" % e)
        return site


class BlogAddForm(BlogForm):

    def __init__(self, *args, **kwargs):
        self.base_fields.pop('categories', None)
        self.base_fields.pop('entries_slugs_with_date', None)
        super(BlogAddForm, self).__init__(*args, **kwargs)


class BlogEntryAddForm(forms.ModelForm):

    class Meta:
        model = BlogEntry
        fields = ('blog', )


def _get_text_editor_widget():
    installed_plugins = plugin_pool.get_all_plugins()
    plugins = [plugin for plugin in installed_plugins if plugin.text_enabled]

    if USE_TINYMCE and "tinymce" in settings.INSTALLED_APPS:
        from cms.plugins.text.widgets.tinymce_widget import TinyMCEEditor
        return TinyMCEEditor(installed_plugins=plugins)
    else:
        return WYMEditor(installed_plugins=plugins)


class BlogEntryChangeForm(forms.ModelForm):
    body = forms.CharField(
        label='Blog Entry', required=True,
        widget=_get_text_editor_widget())

    class Media:
        js = ("cms_blogger/js/jQuery-patch.js",)
        css = {"all": ("cms_blogger/css/entry-change-form.css", )}

    class Meta:
        model = BlogEntry
        exclude = ('content', )

    def __init__(self, *args, **kwargs):
        super(BlogEntryChangeForm, self).__init__(*args, **kwargs)
        self.fields['body'].initial = self.instance.body
        # prepare for save
        self.instance.draft_id = None

    def clean_body(self):
        body = self.cleaned_data.get('body')
        self.instance.body = body
        return body

    def clean_slug(self):
        slug = slugify(self.cleaned_data.get('slug', ''))
        blog_id = self.instance.blog_id
        try:
            BlogEntry.objects.exclude(pk=self.instance.pk).get(
                slug=slug, blog=blog_id, draft_id=None)
        except BlogEntry.DoesNotExist:
            pass
        else:
            raise ValidationError("Entry with the same slug already exists.")
        return slug
