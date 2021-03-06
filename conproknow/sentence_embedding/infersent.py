from typing import List
import torch
from numpy import ndarray
from conproknow.sentence_embedding.encoder import Encoder
from conproknow.sentence_embedding.models import InferSent


class InfersentEncoder(Encoder):
    def __init__(self, vocab: List[str]):
        V = 2
        MODEL_PATH = 'dataset/infersent%s.pkl' % V
        params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                        'pool_type': 'max', 'dpout_model': 0.0, 'version': V}
        self.infersent = InferSent(params_model)
        self.infersent.load_state_dict(torch.load(MODEL_PATH))

        W2V_PATH = 'dataset/GloVe/glove.840B.300d.txt' if V == 1 else 'dataset/fastText/crawl-300d-2M-subword.vec'
        self.infersent.set_w2v_path(W2V_PATH)
        if vocab is not None:
            self.infersent.build_vocab(vocab)

    def update_vocab(self, sentences: List[str]):
        self.infersent.update_vocab(sentences)

    def get_embedding(self, sentence: str) -> ndarray:
        '''Return the embedding of the given sentence.'''
        return self.get_embeddings([sentence])[0]

    def get_embeddings(self, sentences: List[str], update_vocab: bool = False) -> ndarray:
        '''Return the embeddings of the given sentences.'''
        if update_vocab:
            if "word_vec" not in self.infersent.__dict__:
                self.infersent.build_vocab(sentences)
            else:
                self.infersent.update_vocab(sentences)
        return self.infersent.encode(sentences, tokenize=True)

    def download_files(self):
        # TODO: this fucntion should check presence of necessary files. Download them otherwise.
        raise NotImplementedError

    def close(self):
        pass
