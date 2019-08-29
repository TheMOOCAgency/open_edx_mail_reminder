from datetime import timedelta
import logging
import os
import platform
from django.conf.urls import url, include
from django.conf import settings

DATABASES = {
    'default': {
        # Database backend defaults to 'sqlite3', but 'mysql' is also supported.
        'ENGINE': os.getenv('NOTIFIER_DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        # Name should be set to database file path when using sqlite, and database name when using mysql.
        'NAME': os.getenv('NOTIFIER_DATABASE_NAME', os.path.join(os.getenv('NOTIFIER_DB_DIR', '.'), 'notifier.db')),
        # User and password are not used by sqlite, but you will have to set them when using mysql.
        'USER': os.getenv('NOTIFIER_DATABASE_USER', ''),
        'PASSWORD': os.getenv('NOTIFIER_DATABASE_PASSWORD', ''),
        # Host is not used by sqlite. Empty string means localhost when using mysql.
        'HOST': os.getenv('NOTIFIER_DATABASE_HOST', ''),
        # Port is not used by sqlite. Empty string means default port when using mysql.
        'PORT': os.getenv('NOTIFIER_DATABASE_PORT', ''),
    }
}

INSTALLED_APPS = (
    'kombu.transport.django',
    'django_ses',
    'djcelery',
    'notifier',
    'tma_apps',
    # 'edx-ace',
)


FEATURES = {
        "AUTH_USE_OPENID_PROVIDER": "true",
        "AUTOMATIC_AUTH_FOR_TESTING": "false",
        "CUSTOM_COURSES_EDX": "false",
        "ENABLE_COMBINED_LOGIN_REGISTRATION": "true",
        "ENABLE_CORS_HEADERS": "true",
        "ENABLE_COUNTRY_ACCESS": "false",
        "ENABLE_CREDIT_API": "false",
        "ENABLE_CREDIT_ELIGIBILITY": "false",
        "ENABLE_CROSS_DOMAIN_CSRF_COOKIE": "false",
        "ENABLE_CSMH_EXTENDED": "true",
        "ENABLE_DISCUSSION_HOME_PANEL": "true",
        "ENABLE_DISCUSSION_SERVICE": "true",
        "ENABLE_EDXNOTES": "true",
        "ENABLE_GRADE_DOWNLOADS": "true",
        "ENABLE_INSTRUCTOR_ANALYTICS": "true",
        "ENABLE_MKTG_SITE": "false",
        "ENABLE_MOBILE_REST_API": "true",
        "ENABLE_OAUTH2_PROVIDER": "true",
        "ENABLE_ONLOAD_BEACON": "false",
        "ENABLE_READING_FROM_MULTIPLE_HISTORY_TABLES": "true",
        "ENABLE_SPECIAL_EXAMS": "false",
        "ENABLE_SYSADMIN_DASHBOARD": "true",
        "ENABLE_THIRD_PARTY_AUTH": "true",
        "ENABLE_VIDEO_BEACON": "false",
        "ENABLE_VIDEO_UPLOAD_PIPELINE": "false",
        "PREVIEW_LMS_BASE": "preview.surfschool.edu",
        "SHOW_FOOTER_LANGUAGE_SELECTOR": "false",
        "SHOW_HEADER_LANGUAGE_SELECTOR": "false"
    }

SERVICE_NAME = 'notifier'

# Misc. Notifier Formatting

FORUM_DIGEST_EMAIL_SENDER = os.getenv('FORUM_DIGEST_EMAIL_SENDER', 'norep@themoocagency.com')
FORUM_DIGEST_EMAIL_SUBJECT = os.getenv('FORUM_DIGEST_EMAIL_SUBJECT', 'Daily Discussion Digest')
FORUM_DIGEST_EMAIL_TITLE = os.getenv('FORUM_DIGEST_EMAIL_TITLE', 'Forum EDX')
FORUM_DIGEST_EMAIL_DESCRIPTION = os.getenv(
    'FORUM_DIGEST_EMAIL_DESCRIPTION',
    'A digest of unread content from course discussions you are following.'
)
EMAIL_SENDER_POSTAL_ADDRESS = os.getenv('EMAIL_SENDER_POSTAL_ADDRESS','SYSTEME ADMIN')

# Environment-specific settings

# Application Environment
NOTIFIER_ENV = os.getenv('NOTIFIER_ENV', 'Developement')

# email backend  settings
EMAIL_BACKEND = {
        'console': 'django.core.mail.backends.console.EmailBackend',
        'ses': 'django_ses.SESBackend',
        'smtp': 'django.core.mail.backends.smtp.EmailBackend'
        }[os.getenv('EMAIL_BACKEND', 'smtp')]
# The ideal setting for this is 1 / number_of_celery_workers * headroom, 
# where headroom is a multiplier to underrun the send rate limit (e.g.
# 0.9 to keep 10% behind the per-second rate limit at any given moment).
AWS_SES_AUTO_THROTTLE = 0.9




# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ='mail3.themoocagency.com'
EMAIL_USE_TLS = "true"
EMAIL_PORT = 25
EMAIL_HOST_USER = 'contact'
EMAIL_HOST_PASSWORD = 'waSwv6Eqer89'

# email settings independent of backend
EMAIL_REWRITE_RECIPIENT = os.getenv('EMAIL_REWRITE_RECIPIENT')

# LMS links, images, etc
LMS_URL_BASE = os.getenv('LMS_URL_BASE', 'http://localhost:8000')

# Comments Service Endpoint, for digest pulls
CS_URL_BASE = os.getenv('CS_URL_BASE', 'http://localhost:18080')
CS_API_KEY = os.getenv('CS_API_KEY', 'LP5IYLszva4GKdoFL93gpJT3GR3vg67bGEA')

# User Service Endpoint, provides subscriber lists and notification-related user data
US_URL_BASE = os.getenv('US_URL_BASE', 'http://localhost:8000')
US_API_KEY = os.getenv('US_API_KEY', 'PUT_YOUR_API_KEY_HERE')
US_HTTP_AUTH_USER = os.getenv('US_HTTP_AUTH_USER', '')
US_HTTP_AUTH_PASS = os.getenv('US_HTTP_AUTH_PASS', '')
US_RESULT_PAGE_SIZE = int(os.getenv('US_RESULT_PAGE_SIZE', 10))

# Logging
LOG_FILE = os.getenv('LOG_FILE')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')



LOGGING = {
    'version': 1,
    'disable_existing_loggers': "false",
    'filters': {
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] [service_name={}] [%(module)s] %(message)s'.format(SERVICE_NAME)
        },
        'rsyslog': {
            'format': ("[service_variant={service_variant}]"
                       "[%(name)s][env:{logging_env}] %(levelname)s "
                       "[{hostname} %(process)d] [%(filename)s:%(lineno)d] "
                       "- %(message)s").format(
                           service_variant=SERVICE_NAME, 
                           logging_env=NOTIFIER_ENV.lower(), 
                           hostname=platform.node().split(".")[0])
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': LOG_LEVEL.upper(),
            'propagate': "true"
        },
    }
}

CELERYD_HIJACK_ROOT_LOGGER="false"

RSYSLOG_ENABLED = os.getenv('RSYSLOG_ENABLED', '')
if RSYSLOG_ENABLED:
    LOGGING['handlers'].update({
        'rsyslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'formatter': 'rsyslog',
            'facility': logging.handlers.SysLogHandler.LOG_LOCAL0,
        }
    })
    LOGGING['loggers']['']['handlers'].append('rsyslog')

if LOG_FILE:
    LOGGING['handlers'].update({
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': LOG_FILE
        },
    })
    LOGGING['loggers']['']['handlers'].append('file')

TIME_ZONE = 'UTC'  # what task workers see
CELERY_TIMEZONE = 'UTC'  # what the main celery process sees 



# Celery / RabbitMQ fine-tuning
# Don't use a connection pool, since connections are dropped by ELB.
BROKER_POOL_LIMIT = 0
BROKER_CONNECTION_TIMEOUT = 1

# When the broker is behind an ELB, use a heartbeat to refresh the
# connection and to detect if it has been dropped.
BROKER_HEARTBEAT = 10.0
BROKER_HEARTBEAT_CHECKRATE = 2

# Each worker should only fetch one message at a time
CELERYD_PREFETCH_MULTIPLIER = 1

# Maximum number of tasks a pool worker process can execute
# before it's replaced with a new one.
CELERYD_MAX_TASKS_PER_CHILD = int(os.getenv('CELERYD_MAX_TASKS_PER_CHILD', 1))

DEFAULT_PRIORITY_QUEUE = os.getenv('NOTIFIER_CELERY_QUEUE', 'notifier.default')
CELERY_DEFAULT_EXCHANGE = 'notifier'
CELERY_DEFAULT_ROUTING_KEY = 'notifier'
CELERY_DEFAULT_QUEUE = DEFAULT_PRIORITY_QUEUE

LANGUAGE_CODE = os.getenv('NOTIFIER_LANGUAGE', 'en')
LANGUAGES = (
    ("en", "English"),
    ("ar", "Arabic"),
    ("es-419", "Spanish (Latin America)"),
    ("fr", "French"),
    ("he", "Hebrew"),
    ("hi", "Hindi"),
    ("pt-br", "Portuguese (Brazil)"),
    ("ru", "Russian"),
    ("zh-cn", "Chinese (China)"),
)
USE_L10N = "true"
LOCALE_PATHS = (os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locale'),)

# Parameterize digest logo image url
LOGO_IMAGE_URL = os.getenv('LOGO_IMAGE_URL', "{}/static/images/edx-theme/edx-logo-77x36.png".format(LMS_URL_BASE))

DEAD_MANS_SNITCH_URL = os.getenv('DEAD_MANS_SNITCH_URL', '')

# secret key for generating unsub tokens
# this MUST be changed in production envs, and MUST match the LMS' secret key
SECRET_KEY = '3bYYuzq90mbyzrFqgMKZh8su5FSnYVxMfj1m9H7ZnS4UD69Nj0Dvj2Fpii7cuE0UZiU68t5mpbUPigg3Jdb1C8Eq3pUOtskOqfQg'
