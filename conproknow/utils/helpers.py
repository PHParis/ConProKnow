from re import compile
from time import time


def keep_alphanumeric_only(s: str) -> str:
    """Return the same string but with only its alphanumeric caracters."""
    pattern = compile('[\W_]+')
    return pattern.sub('', s)


def timing(f):
    """Decorator that track time"""
    def wrap(*args):
        time1 = time()
        ret = f(*args)
        time2 = time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap
