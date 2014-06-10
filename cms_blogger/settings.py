from django.conf import settings
from filer import settings as filer_settings
import copy


UPLOAD_TO_PREFIX = getattr(
    settings, 'BLOGGER_UPLOAD_TO_PREFIX', "blog")

USE_FILER_STORAGE = getattr(
    settings, 'BLOGGER_USE_FILER_STORAGE', False)


def _get_image_storage():
    if USE_FILER_STORAGE:
        storage = copy.deepcopy(
            filer_settings.FILER_PUBLICMEDIA_STORAGE)
        cdn_domain = getattr(filer_settings, 'CDN_DOMAIN', None)
        if not cdn_domain:
            return storage
        # for s3 storage
        if hasattr(storage, 'custom_domain'):
            setattr(storage, 'custom_domain', cdn_domain)
        return storage
    return None


POSTER_IMAGE_STORAGE = _get_image_storage()

ALLOWED_THUMBNAIL_IMAGE_TYPES = getattr(
    settings, 'BLOGGER_ALLOWED_THUMBNAIL_IMAGE_TYPES',
    ['jpg', 'jpeg', 'png', 'gif'])

MAXIMUM_THUMBNAIL_FILE_SIZE = getattr(
    settings, 'BLOGGER_MAXIMUM_THUMBNAIL_FILE_SIZE', 1 * 1024 * 1024)

POSTER_IMAGE_WIDTH = getattr(
    settings, 'BLOGGER_POSTER_IMAGE_WIDTH', 640)

POSTER_IMAGE_ASPECT_RATIO = getattr(
    settings, 'BLOGGER_POSTER_IMAGE_ASPECT_RATIO', 16.0 / 9.0)

POSTS_ON_LANDING_PAGE = getattr(
    settings, 'BLOGGER_POSTS_ON_LANDING_PAGE', 15)

ALLOWED_SITES_FOR_USER = getattr(
    settings, 'BLOGGER_ALLOWED_SITES_FOR_USER', None)
