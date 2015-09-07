from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.template import Library
from dateutil import tz, relativedelta
import json
import calendar
import datetime
import time


register = Library()


@register.filter
def jsonify(obj_to_jsonify):
    if isinstance(obj_to_jsonify, QuerySet):
        return mark_safe(serialize('json', obj_to_jsonify))
    return mark_safe(json.dumps(obj_to_jsonify))

jsonify.is_safe = True


def as_utc(datetime_obj):
    is_aware = (datetime_obj.tzinfo is not None and
                datetime_obj.tzinfo.utcoffset(datetime_obj) is not None)
    if is_aware:
        as_utc = datetime_obj.astimezone(tz.tzutc())
    else:
        as_utc = datetime_obj
    return as_utc.replace(tzinfo=None)


def as_millis(datetime_obj):
    return calendar.timegm(datetime_obj.timetuple()) * 1000


@register.inclusion_tag('cms_blogger/entry_pub_date.html')
def publish_date_box(entry):
    if not hasattr(entry, 'update_date'):
        return {}
    mod_time = as_utc(entry.update_date)
    pub_time = as_utc(entry.publication_date)
    is_updated = mod_time > pub_time

    display_date = mod_time if is_updated else pub_time
    # entry is published for more than 3 months
    is_older = display_date < (datetime.datetime.utcnow() +
                               relativedelta.relativedelta(months=-3))
    var_name = ("entry_pub_%s%s" % (time.time(), entry.id)).replace('.' , '')
    return {
        'date_var': var_name,
        'utc_millis': as_millis(display_date),
        'show_year': is_older
    }


@register.inclusion_tag('cms_blogger/entry_author.html')
def author_row(entry):
    if not hasattr(entry, 'update_date'):
        return {}
    mod_time = as_utc(entry.update_date)
    pub_time = as_utc(entry.publication_date)
    is_updated = mod_time > pub_time
    var_name = ("entry_pub_%s%s" % (time.time(), entry.id)).replace('.' , '')
    return {
        'date_var': var_name,
        'is_updated': is_updated,
        'utc_millis': as_millis(mod_time if is_updated else pub_time),
        'author_names': entry.authors_display_name,
        'entry': entry
    }
