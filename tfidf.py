#!/usr/bin/python  
# -*- coding: utf-8 -*-
import numpy
import os
import string
import sys
import re
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

reload(sys)

def cal_tfidf(num):
    
    trainfile = open("D:\\eclipse-workspace\\docudeal\\deal\\emo_%s.txt" %num,"r") #不同的documents用换行符隔开
    corpus = trainfile.readlines()
    # corpus = corpus + u'心情愉快'
    trainfile.close()
    
    freWord = CountVectorizer()
    #统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    #计算出tf-idf(第一个fit_transform),并将其转换为tf-idf矩阵(第二个fit_transformer)
    tfidf = transformer.fit_transform(freWord.fit_transform(corpus))
    
    #获取词袋模型中的所有词语
    word = freWord.get_feature_names()
    
    weight = tfidf.toarray()
    #每行对应一个文本中的所有词的权重
    tfidfDict = {}
    print num
    for i in range(len(weight)):
        for j in range(len(word)):
            getword = word[j]
            getValue = weight[i][j]
            if getValue != 0:
                if tfidfDict.has_key(getword):
                    tfidfDict[getword] = tfidfDict[getword]+string.atof(getValue)
                else:
                    tfidfDict.update({getword:getValue})
    sorted_tfidf = sorted(tfidfDict.iteritems(),
                          key = lambda d:d[1],reverse = True)
    
    fw = open("D:\\eclipse-workspace\\docudeal\\deal\\tfidf_%s.txt" %num,'w')
    for i in sorted_tfidf:
        fw.write(i[0].encode("utf-8") + '\t' + str(i[1]) +'\n')
    fw.close()

for num in range(8):
    cal_tfidf(num)