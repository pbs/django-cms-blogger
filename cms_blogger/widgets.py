from django import forms
from django.utils.safestring import mark_safe
from django.contrib.admin.templatetags.admin_static import static
from dateutil import tz, parser
from django.template.loader import render_to_string

from . import settings

class ToggleWidget(forms.widgets.CheckboxInput):

    def render(self, name, value, attrs={}):
        attrs.update({'class': 'ace ace-switch ace-switch-4 btn-empty'})
        widget_html = super(ToggleWidget, self).render(
            name, value, attrs=attrs)
        is_disabled = (self.attrs.get('disabled', False) or
                       attrs.get('disabled', False))
        active = 'false' if is_disabled else 'true'
        output = ("<label class='pull-left'>"
                  "%s<span class='lbl'></span></label>" % widget_html)
        return mark_safe(output)


class TagItWidget(forms.widgets.TextInput):

    class Media:
        css = {
            'all': (
                static('cms_blogger/css/redmond-jquery-ui.css'),
                static('cms_blogger/css/jquery.tagit.css'),)
        }
        js = (static('cms_blogger/js/jquery-1.9.1.min.js'),
              static('cms_blogger/js/jquery-ui.min.js'),
              static('cms_blogger/js/tag-it.js'),)

    tagit_script = (
        "<script type='text/javascript'>"
        "jQuery('#id_%s').tagit(%s);"
        "</script>")

    def __init__(self, attrs=None):
        super(TagItWidget, self).__init__(attrs=attrs)
        self.tagit_attrs = attrs.pop('tagit', '{}')

    def render(self, name, value, attrs={}):
        widget_html = super(TagItWidget, self).render(
            name, value, attrs=attrs)
        output = "%s%s" % (
            widget_html, self.tagit_script % (name, self.tagit_attrs))
        return mark_safe(output)


class ButtonWidget(forms.widgets.CheckboxInput):
    # make it a CheckboxInput in order to not show the ':' after the label

    class Media:
        css = {
            'all': (
                static('cms_blogger/css/redmond-jquery-ui.css'),)
        }
        js = (static('cms_blogger/js/jquery-1.9.1.min.js'),
              static('cms_blogger/js/jquery-ui.min.js'), )

    hide_label = (
        '<style type="text/css">label[for="id_%s"]{'
        'display:none !important;}</style>')

    make_js_button = (
        "<script type='text/javascript'>"
        "jQuery('#id_%s').addClass('default btn btn-primary').click("
        "function(event) {event.preventDefault();%s});"
        "</script>")
    submit_on_click_js = (
        "jQuery(this).closest('form').append("
        "jQuery('<input>').attr('type', 'hidden').attr("
        "'name', '_continue').val('Save')"
        ").submit();")

    def __init__(self, attrs=None, check_test=None, link_url='',
                 text=None, submit=False, on_click=''):
        super(ButtonWidget, self).__init__(attrs, check_test)
        self.text = text
        self.link_url = link_url or "#"
        self.submit = submit
        self.on_click = on_click

    def _render_js_on_click(self):
        return "%s%s" % (
            self.on_click, self.submit_on_click_js if self.submit else '')

    def render(self, name, value, attrs=None):
        text = self.text or name.capitalize()
        return mark_safe(
            u"%s<a %s href='%s' id='id_%s'>%s</a>%s" % (
                self.hide_label % name,
                forms.utils.flatatt(self.build_attrs(attrs)),
                self.link_url, name, text,
                self.make_js_button % (name, self._render_js_on_click(), )))

    def value_from_datadict(self, data, files, name):
        return False

    def _has_changed(self, initial, data):
        return False


class DateTimeWidget(forms.widgets.TextInput):

    class Media:
        css = {
            'all': (
                static('cms_blogger/css/redmond-jquery-ui.css'),
                static('cms_blogger/css/datetimepicker-extension.css'),
            )
        }
        js = (static('cms_blogger/js/jquery-1.9.1.min.js'),
              static('cms_blogger/js/jquery-ui.min.js'),
              static('cms_blogger/js/jquery-ui-timepicker-addon.js'),
              static('cms_blogger/js/datetimepicker-field.js'),
              static('cms_blogger/js/moment.min.js')
              )

    def render(self, name, value, attrs={}):
        html = (
            u"<input type='text' size='30' name='{name}' id='id_{name}' "
            u"class='ui-button ui-corner-all ui-state-focus ui-textfield'/>"
            u"<div id='picker_id_{name}'></div>"
            u"<input type='hidden' name='_{name}_tzoffset' "
            u"id='_{name}_tzoffset'/>"
            u"<script type='text/javascript'>"
            u"buildDatetimePickerField("
            u"'#picker_id_{name}', '#id_{name}', '#_{name}_tzoffset', "
            u"'{initial}');"
            u"</script>"
        )
        return mark_safe(html.format(name=name, initial=value or ''))

    def value_from_datadict(self, data, files, name):
        value = super(DateTimeWidget, self).value_from_datadict(
            data, files, name)
        offset_str = data.get('_{name}_tzoffset'.format(name=name))
        # apparently dateutil throws error when it tries to parse something
        #   like ' +0500' but it works when parsing ' -0500' and the date
        #   returned is naive.
        #   Workaround for this: if no date is set, just don't go any further
        if not value:
            return None
        try:
            value_as_date = parser.parse(value + " " + offset_str)
        except:
            return None
        return value_as_date.astimezone(tz.tzutc())


class PosterImage(forms.widgets.CheckboxInput):

    class Media:
        js = (static('filer/js/fileuploader.js'),)

    def render(self, name, value, attrs=None):
        return render_to_string(
            "admin/cms_blogger/blogentrypage/poster_image.html",
            {
                'blog_entry_id': self.blog_entry_id,
                'image_url': self.image_url,
                'size_limit': settings.MAXIMUM_THUMBNAIL_FILE_SIZE,
                'image_types': settings.ALLOWED_THUMBNAIL_IMAGE_TYPES,
                'poster_width': settings.POSTER_IMAGE_WIDTH,
                'poster_height': settings.POSTER_IMAGE_HEIGHT,
            }
        )


class SpinnerWidget(forms.widgets.TextInput):

    class Media:
        js = (static('cms_blogger/js/jquery-1.9.1.min.js'),
              static('cms_blogger/js/ace-extra.min.js'),
              static('cms_blogger/js/ace-elements.min.js'),
              static('cms_blogger/js/fuelux.spinner.min.js'),
              static('cms_blogger/js/ace.min.js'), )

    spinner_script = (
        "<script type='text/javascript'>"
        "jQuery('#id_%s').ace_spinner(%s)"
        "</script>")

    def __init__(self, attrs=None):
        super(SpinnerWidget, self).__init__(attrs=attrs)
        self.spinner_attrs = attrs.pop('spinner', '{}')

    def render(self, name, value, attrs={}):
        widget_html = super(SpinnerWidget, self).render(
            name, value, attrs=attrs)
        output = "%s%s" % (
            widget_html, self.spinner_script % (name, self.spinner_attrs))
        return mark_safe(output)


class BootstrapMultiselect(forms.widgets.SelectMultiple):

    class Media:
        css = {
            'all': (
                static('cms_blogger/css/bootstrap-multiselect.min.css'),
            )
        }
        js = (static('cms_blogger/js/jquery-1.9.1.min.js'),
              static('cms_blogger/js/bootstrap-multiselect.min.js'), )

    multiselect_script = (
        "<script type='text/javascript'>"
        "jQuery('#id_%s').multiselect(%s).next().css('width', 'auto')"
        ".find('.multiselect-search').css('width', 'auto')"
        ".next().find('.multiselect-clear-filter').css('height', '34px');"
        "</script>")

    max_selected_script = (
        "<script type='text/javascript'>"
        "jQuery('#id_%s').on('multiselectclick', function(event, ui) {"
        "var widget = jQuery(this).multiselect('widget');"
        "var selected_items = widget.find('input:checked');"
        "if(ui.checked && selected_items.length > %d){"
        "alert('You can only select %d items.'); "
        "return false;}"
        "});"
        "</script>")

    def __init__(self, attrs=None):
        attrs = attrs or {}
        self.multiselect_attrs = attrs.pop('multiselect', '{}')
        self.max_selected = attrs.pop('max_items_allowed', None)
        super(BootstrapMultiselect, self).__init__(attrs=attrs)

    def render(self, name, value, attrs={}):
        widget_html = super(BootstrapMultiselect, self).render(
            name, value, attrs=attrs)

        widget_html += self.multiselect_script % (
            name, self.multiselect_attrs)

        if self.max_selected:
            widget_html += self.max_selected_script % (
                name, self.max_selected, self.max_selected)
        return mark_safe(widget_html)


class BootstrapSelect(forms.widgets.Select):

    class Media:
        css = {
            'all': (
                static('cms_blogger/css/bootstrap-multiselect.min.css'),
            )
        }
        js = (static('cms_blogger/js/jquery-1.9.1.min.js'),
              static('cms_blogger/js/bootstrap-multiselect.min.js'), )

    multiselect_script = ("""<script type='text/javascript'>
jQuery('#id_%s').multiselect(%s).next().css('width', 'auto')
    .find('.multiselect-search').css('width', 'auto').next()
    .find('.multiselect-clear-filter').css('height', '34px'); </script>""")

    def __init__(self, attrs=None):
        attrs = attrs or {}
        self.multiselect_attrs = attrs.pop('multiselect', '{}')
        self.max_selected = attrs.pop('max_items_allowed', None)
        super(BootstrapSelect, self).__init__(attrs=attrs)

    def render(self, name, value, attrs={}):
        widget_html = super(BootstrapSelect, self).render(
            name, value, attrs=attrs
        )

        widget_html += self.multiselect_script % (
            name, self.multiselect_attrs)

        return mark_safe(widget_html)
