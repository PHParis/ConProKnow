from typing import List
from numpy import ndarray


class Encoder(object):
    '''Abstract class for sentence embedding encoder. This class allows to get
    representational vectors of sentences.'''

    def get_embedding(self, sentence: str) -> ndarray:
        '''Return the embedding of the given sentence.'''
        raise NotImplementedError

    def get_embeddings(self, sentences: List[str]) -> ndarray:
        '''Return the embeddings of the given sentences.'''
        raise NotImplementedError

    def close(self):
        '''Clean the resources used by the encoder'''
        raise NotImplementedError
