'''
Might be used:
We choose simple WORDNET to find synonyms and anyonyms by using NLTK
'''

from gensim import corpora, models, similarities
from util import read_xlsx_xlrd
import logging
from pprint import pprint
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Build_Corpora(object):
    def __init__(self):
        self.documents = list()
        self.texts = list()

    def add(self, source):
        self.documents.append(str(source))
        return self.documents

    # remove common words and tokenize
    def clean(self):
        stop_list = set('for a of the and to in is with'.split())
        self.texts = [[word for word in self.documents.lower().split() if word not in stop_list]
                      for self.documents in self.documents]
        # remove words that appear only once
        return self.texts

    def remove_once_word(self):
        from collections import defaultdict
        frequency = defaultdict(int)
        for text in self.texts:
            for token in text:
                frequency[token] += 1
        self.texts = [[token for token in text if frequency[token] > 1]
                      for text in self.texts]
        return self.texts

    def dictionary(self, path):
        dictionary = corpora.Dictionary(self.texts)
        dictionary.save(path)
        print(dictionary)
        print(dictionary.token2id)
        return dictionary

    def corpus(self, path):
        corpus = [dictionary.doc2bow(text) for text in self.texts]
        corpora.MmCorpus.serialize(path, corpus)  # store to disk, for later use
        print(corpus)
        return corpus

    def save_dictionary(self, path):
        pass


if __name__ == '__main__':
    path = ('Data/Competency model 2 dimensional.xlsx')
    bc_positive = Build_Corpora()
    # build positive competency model corpora
    for i in range(3, 32):
        cell_positive = [i, 1, 2] # col: B
        documents_compe_positive = bc_positive.add(read_xlsx_xlrd(path, cell_positive))
    bc_negative = Build_Corpora()
    # build negative competency model corpora
    for i in range(3, 32):
        cell_negative = [i, 3, 4] # col: D
        documents_compe_negative = bc_negative.add(read_xlsx_xlrd(path, cell_negative))
    # print(bc_negative.clean())
    # print(bc_positive.clean())
    # bc_positive.save_dictionary('configure/positive.dict')
    bc_positive.clean()
    bc_negative.clean()
    dictionary = bc_positive.dictionary('configure/positive.dict')
    new_doc = 'can lead a team to successes'
    vec_bow = dictionary.doc2bow(new_doc.lower().split())
    # print(new_vec)
    corpus = bc_positive.corpus('configure/positive.mm')
    # tfidf = models.TfidfModel(corpus)
    # corpus_tfidf = tfidf[corpus]
    '''Train the model using LDA'''
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=100)
    corpus_lda = lda[corpus]
   # for doc in corpus_lda:
   #     print(doc)

    '''Send similarity queries'''

    #lda.print_topics(100)
    vec_lda = lda[vec_bow]
    index = similarities.MatrixSimilarity(corpus_lda)
    sims = index[vec_lda]
    print(list(enumerate(sims)))
    #print(documents_compe_negative)
