# Contextual Propagation of Properties for Knowledge Graphs: a Sentence Embedding Based Approach

## Presentation

As the number of open knowledge graphs (KGs) growths, the complexity for users to find their way with data increases.
Thus, it is important to provide to users approaches that help them handling KGs while writing queries.
Several works demonstrated the importance to consider identity links (_owl:sameAs_) between entities as context-dependant identity links.
W.r.t. an identity context, some properties might be propagated and some don't.
In this work, we propose an approach based on sentence embedding to find those propagable properties 
for a given context.

Currently, only Wikipedia is supported due to specifities of its data model.

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
and in `dataset` directory
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
 curl -Lo encoder/infersent1.pkl https://dl.fbaipublicfiles.com/infersent/infersent1.pkl
 curl -Lo encoder/infersent2.pkl https://dl.fbaipublicfiles.com/infersent/infersent2.p
 ```
 Finally, from [rdfhdt.org](http://www.rdfhdt.org/datasets/) get Wikidata HDT file:
 ```bash
 curl -Lo dataset/wikidata2018_09_11.hdt.gz http://gaia.infor.uva.es/hdt/wikidata/wikidata2018_09_11.hdt.gz
 gunzip dataset/wikidata2018_09_11.hdt.gz
 curl -Lo dataset/wikidata/wikidata2018_09_11.hdt.index.v1-1 http://gaia.infor.uva.es/hdt/wikidata/wikidata2018_09_11.hdt.index.v1-1 
 gunzip dataset/wikidata2018_09_11.hdt.index.v1-1.gz
 ```

 ## How to run the program?

To create an identity lattice:
 ```bash
 python3 -m conproknow lattice --resource "http://www.wikidata.org/entity/Q90" --output /output_dir/  --hdt /path/to/wikidata2018_09_11.hdt
 ```

 To check the gold standard results:
 ```bash
 python3 -m conproknow gold --hdt /path/to/wikidata2018_09_11.hdt
 ```