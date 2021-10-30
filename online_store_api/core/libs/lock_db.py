import functools
import logging

from datetime import timedelta
from django.utils import timezone

from django.db import transaction, IntegrityError
from ..structures.store.models import LockDB


class lock_db(object):
    """
    Use lock db as decorator for locking database
    """

    def __init__(self, lock_id):
        self.lock_id = lock_id
        self.lock = None

    def __call__(self, func):
        return self.decorate_callable(func)

    def __enter__(self):
        self.start()

    def __exit__(self, *args):
        self.stop()

    def start(self):
        # max lock 10 minutes 10 * 60
        LockDB.objects.filter(
            creation_time__lte=timezone.now() - timedelta(seconds=600)
        ).delete()
        try:
            with transaction.atomic():
                self.lock = LockDB.objects.create(lock_id=self.lock_id)
        except IntegrityError as e:
            raise e

    def stop(self):
        # check has lock but function end
        if not LockDB.objects.filter(id=self.lock.id).exists():
            raise ValueError("Lock exist when process finished")
        else:
            self.lock.delete()

    def decorate_callable(self, func):
        def wrapper(*args, **kwargs):
            try:
                with self:
                    result = func(*args, **kwargs)
                return result
            except Exception as e:
                logging.error(str(e))
                raise e

        functools.update_wrapper(wrapper, func)
        return wrapper
