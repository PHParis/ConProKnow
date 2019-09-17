from typing import List
import torch
from numpy import ndarray
from conproknow.sentence_embedding.encoder import Encoder
from conproknow.sentence_embedding.gensen import GenSen, GenSenSingle


class GenSenEncoder(Encoder):
    def __init__(self, vocab: List[str]):
        self.gensen_1 = GenSenSingle(
            model_folder='./data/models',
            filename_prefix='nli_large_bothskip',
            pretrained_emb='./data/embedding/glove.840B.300d.h5'
        )

    def update_vocab(self, sentences: List[str]):
        raise NotImplementedError
        # self.infersent.update_vocab(sentences)

    def get_embedding(self, sentence: str) -> ndarray:
        '''Return the embedding of the given sentence.'''
        raise NotImplementedError
        # return self.get_embeddings([sentence])[0]

    def get_embeddings(self, sentences: List[str], update_vocab: bool = False) -> ndarray:
        '''Return the embeddings of the given sentences.'''
        reps_h, reps_h_t = self.gensen_1.get_representation(
            sentences, pool='last', return_numpy=True, tokenize=True
        )
        raise NotImplementedError
        # if update_vocab:
        #     self.infersent.update_vocab(sentences)
        # return self.infersent.encode(sentences, tokenize=True)

    def download_files(self):
        # TODO: this fucntion should check presence of necessary files. Download them otherwise.
        raise NotImplementedError


if __name__ == "__main__":
    word = "Elephant"
    sentence = "I am a sentence for which I would like to get its embedding."
    paragraph = (
        "Universal Sentence Encoder embeddings also support short paragraphs. "
        "There is no hard limit on how long the paragraph is. Roughly, the longer "
        "the more 'diluted' the embedding will be.")
    messages = [word, sentence, paragraph]
    encoder = GenSenEncoder(messages)
    print(encoder.get_embedding(sentence))
