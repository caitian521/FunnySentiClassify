# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 16:37:43 2017

@author: caitian
训练word2vec词向量
"""

from gensim.models import word2vec
import logging
import gensim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus("D:\eclipse-workspace\docudeal\\deal\\corpus.txt")
wordvecmodel = word2vec.Word2Vec(sentences, size=200,min_count=1)# 训练skip-gram模型; 默认window=5
wordvecmodel.save("../wordvec200min1.model")


