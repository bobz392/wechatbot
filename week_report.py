#! /usr/bin/env python2.7
#coding=utf-8

import logging
from gensim import corpora, models, similarities
import jieba, jieba.analyse
from model import Message

class WeekReport(object):

    def __init__(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
            level=logging.INFO)

    def preview(self, name):
        jieba.analyse.set_stop_words('./stopwords.dat')
        # jieba.cut(note.message)
        tokenized = [jieba.analyse.extract_tags(note.message) for note \
            in Message.query_weekly_message(name)]
        
        print tokenized
        print '---'
        for i in tokenized:
            print(",".join(i))
        print '---'
        # Corp = MyCorpus()
        dictionary = corpora.Dictionary(tokenized)
        token_vectors = [dictionary.doc2bow(tokens) for tokens in tokenized]
        tfidf = models.TfidfModel(token_vectors)
        tfidf_vectors = tfidf[token_vectors]

        # print list(enumerate(tfidf_vectors))
        # for token in tokenized:
        #     query_bow = dictionary.doc2bow(token)
        #     index = similarities.MatrixSimilarity(tfidf_vectors)
        #     sims = index[query_bow]
        #     print list(enumerate(sims))

        lsi = models.LsiModel(tfidf_vectors, id2word=dictionary, num_topics=2)
        lsi_vector = lsi[tfidf_vectors]
        # lsi.print_topics(2)
        for token in tokenized:
            query_bow = dictionary.doc2bow(token)
            query_lsi = lsi[query_bow]
            index = similarities.MatrixSimilarity(lsi_vector)
            sims = index[query_lsi]
            print list(enumerate(sims))

w = WeekReport()
w.preview(u'M_zhou')