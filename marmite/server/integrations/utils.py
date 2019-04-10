import time
import functools


def throttle(_func=None, *, seconds=0.1):
    """ Decorator to slow down function calls by a given time. """

    def proxy(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            val = func(*args, **kwargs)
            return val

        return wrapper

    if _func is None:
        return proxy
    else:
        return proxy(_func)