from gensim import corpora, models, similarities
from util import read_xlsx_xlrd
import logging
from pprint import pprint
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Build_Corpora(object):
    def __init__(self):
        self.documents = list()

    def add(self, source):
        self.documents.append(str(source))
        return self.documents

    # remove common words and tokenize
    def clean(self):
        stop_list = set('for a of the and to in is'.split())
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

    def dictionary(self):
        dictionary = corpora.Dictionary(self.texts)
       # dictionary.save(path)
        return dictionary
       # print(dictionary)
       # print(dictionary.token2id)


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
    print(bc_negative.clean())
    print(bc_positive.clean())
   # bc_positive.save_dictionary('configure/positive.dict')
    dictionary = bc_positive.dictionary()
    new_doc = 'Flexibility Dealing with paradox'
    new_vec = dictionary.doc2bow(new_doc.lower().split())
    print(new_vec)




    #print(documents_compe_negative)
