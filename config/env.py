import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()


BASE_DIR = environ.Path(__file__) - 2
APPS_DIR = BASE_DIR.path("technews")


def env_to_enum(enum_cls, value):
    for x in enum_cls:
        if x.value == value:
            return x

    raise ImproperlyConfigured(f"Env value {repr(value)} could not be found in {repr(enum_cls)}")
