# Contextual Propagation of Properties for Knowledge Graphs: a Sentence Embedding Based Approach

## Presentation

## Preliminaries
 
 You must ensure the following requirements are met on your test machine: 
 * Python 3.6
 * PyTorch
 * Then install the following pip package *hdt*, *numpy* and *nltk*.
 ```bash
 pip install numpy hdt nltk
 ```

To make InferSent work, make sure you have the NLTK tokenizer by running the following once:
 ```Python
 import nltk
 nltk.download('punkt')
 ```
and
 ```bash
 mkdir GloVe
 curl -Lo GloVe/glove.840B.300d.zip http://nlp.stanford.edu/data/glove.840B.300d.zip
 unzip GloVe/glove.840B.300d.zip -d GloVe/
 mkdir fastText
 curl -Lo fastText/crawl-300d-2M.vec.zip https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip
 unzip fastText/crawl-300d-2M.vec.zip -d fastText/
 ```
 and
 ```bash
 mkdir encoder
 curl -Lo encoder/infersent1.pkl https://dl.fbaipublicfiles.com/infersent/infersent1.pkl
 curl -Lo encoder/infersent2.pkl https://dl.fbaipublicfiles.com/infersent/infersent2.p
 ```
 Finally, from [rdfhdt.org](http://www.rdfhdt.org/datasets/) get Wikidata HDT file:
 ```bash
 curl -Lo encoder/wikidata2018_09_11.hdt.gz http://gaia.infor.uva.es/hdt/wikidata/wikidata2018_09_11.hdt.gz
 gunzip wikidata2018_09_11.hdt.gz
 curl -Lo encoder/wikidata/wikidata2018_09_11.hdt.index.v1-1 http://gaia.infor.uva.es/hdt/wikidata/wikidata2018_09_11.hdt.index.v1-1 
 gunzip wikidata2018_09_11.hdt.index.v1-1.gz
 ```

 ## How to run the program?