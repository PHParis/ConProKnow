from re import compile
from time import time
import numpy as np


def keep_alphanumeric_only(s: str) -> str:
    '''Removes all non alphanumeric caracters from the given string.'''
    pattern = compile('[\W_]+')
    return pattern.sub('', s)


def timing(f):
    '''Decorator that track time.'''
    def wrap(*args):
        time1 = time()
        ret = f(*args)
        time2 = time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap


def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    """Where u and v are pytorch embeddings"""
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)).item()
