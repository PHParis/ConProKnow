from typing import Dict
from numpy import ndarray


class Containers(object):
    """Utility class to avoid unecessary repeated access to HDT file or computation of embeddings"""
    # key = property, value = description
    prop_desc: Dict[str, str] = dict()

    # key = encoder type, value = (key = description, value = ndarray)
    encoder_desc_ndarray: Dict[str, ndarray] = dict()
