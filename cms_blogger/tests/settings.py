SITE_ID = 1
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'cms',
    'mptt',
    'menus',
    'sekizai',
    'filer',
    'cms.plugins.text',

    'django_select2',
    'cms_layouts',
    'cms_blogger',
]

CMS_TEMPLATES = [('page_template.html', 'page_template.html'),
                 ('404.html', '404.html'),]
CMS_MODERATOR = False
CMS_PERMISSION = True
STATIC_ROOT = ''
STATIC_URL = '/static/'
ROOT_URLCONF = 'cms_blogger.tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

CACHE_BACKEND = 'locmem:///'

CMS_PLUGIN_PROCESSORS = ('cms_layouts.context_processor.add_extra_html', )
SOUTH_TESTS_MIGRATE = False
BLOGGER_ALLOWED_SITES_FOR_USER = 'cms_blogger.tests.utils.get_allowed_sites'
USE_TZ = True
SECRET_KEY = 'secret'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            # 'propagate': True,
        },
    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': (
                "django.contrib.auth.context_processors.auth",
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                'django.template.context_processors.csrf',
                "cms.context_processors.media",
                "sekizai.context_processors.sekizai",
                "django.template.context_processors.static",
            ),
            'loaders': (
                'cms_layouts.tests.utils.MockLoader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ),
        },
    },
]
