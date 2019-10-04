from typing import List
import torch
from numpy import ndarray
from conproknow.sentence_embedding.encoder import Encoder
from conproknow.sentence_embedding.gensen import GenSen, GenSenSingle


class GenSenEncoder(Encoder):
    def __init__(self, vocab: List[str]):
        self.gensen = GenSenSingle(
            model_folder='dataset/gensen/models',
            filename_prefix='nli_large_bothskip_parse',
            pretrained_emb='dataset/gensen/embedding/glove.840B.300d.h5'
        )
        # words = set()
        # for sentence in vocab:
        #     sample = sentence.lower().split()
        #     words.update(sample)
        # self.gensen.vocab_expansion(words)

    def update_vocab(self, sentences: List[str]):
        raise NotImplementedError
        # self.infersent.update_vocab(sentences)

    def get_embedding(self, sentence: str) -> ndarray:
        '''Return the embedding of the given sentence.'''
        _, reps_h_t = self.gensen.get_representation(
            [sentence], pool='last', return_numpy=True
        )
        return reps_h_t[0]
        # return self.get_embeddings([sentence])[0]

    def get_embeddings(self, sentences: List[str], update_vocab: bool = False) -> ndarray:
        '''Return the embeddings of the given sentences.'''
        _, reps_h_t = self.gensen.get_representation(
            sentences, pool='last', return_numpy=True
        )
        return reps_h_t
        # if update_vocab:
        #     self.infersent.update_vocab(sentences)
        # return self.infersent.encode(sentences, tokenize=True)

    def download_files(self):
        # TODO: this fucntion should check presence of necessary files. Download them otherwise.
        raise NotImplementedError

    def close(self):
        pass


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
