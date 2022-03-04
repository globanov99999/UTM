import csv
import datetime
import logging
import time

from acq.acqcore.acq_logger import ACQLogger

logger = ACQLogger().get_logger()


def timeit(method):
    def timed(*a, **kw):
        ts = time.time()
        result = method(*a, **kw)
        te = time.time()
        logging.info('{} : {:.2f} s'.format(method.__name__, (te - ts)))
        return result

    return timed


def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate
