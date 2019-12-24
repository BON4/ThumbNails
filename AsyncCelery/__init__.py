# I need to ensure that the previously created and configured
# celery application gets injected into the Django application when it is ran.
from .celery import celery_app

__all__ = ('celery_app', )
