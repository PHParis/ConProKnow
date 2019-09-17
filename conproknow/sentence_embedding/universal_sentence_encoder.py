import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

from typing import List
from numpy import ndarray
from conproknow.sentence_embedding.encoder import Encoder
# from encoder import Encoder


class UniversalSentenceEncoder(Encoder):
    def __init__(self, vocab: List[str]):
        # @param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
        module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"

        # Import the Universal Sentence Encoder's TF Hub module
        self.embed = hub.Module(module_url)
        tf.logging.set_verbosity(tf.logging.ERROR)

    def update_vocab(self, sentences: List[str]):
        raise NotImplementedError

    def get_embedding(self, sentence: str) -> ndarray:
        '''Return the embedding of the given sentence.'''
        with tf.Session() as session:
            session.run([tf.global_variables_initializer(),
                         tf.tables_initializer()])
            message_embeddings = session.run(self.embed([sentence]))
            return np.array(message_embeddings)[0]

    def get_embeddings(self, sentences: List[str], update_vocab: bool = False) -> ndarray:
        '''Return the embeddings of the given sentences.'''
        with tf.Session() as session:
            session.run([tf.global_variables_initializer(),
                         tf.tables_initializer()])
            message_embeddings = session.run(self.embed(sentences))
            return np.array(message_embeddings)

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
    encoder = UniversalSentenceEncoder(messages)
    print(encoder.get_embedding(sentence))
