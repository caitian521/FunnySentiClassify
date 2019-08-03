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
import pickle  
import cPickle 
import jieba
#from cPickle import load,save
reload(sys)

def cal_tfidf():
    trainfile = open("D:\\eclipse-workspace\\docudeal\\tfidf-use\\test.txt","r")
#     trainfile = open("D:\\eclipse-workspace\\docudeal\\corpus.txt","r") #不同的documents用换行符隔开
    corpus = trainfile.readlines()
    # corpus = corpus + u'心情愉快'
    trainfile.close()
    
    freWord = CountVectorizer()
    #统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    #计算出tf-idf(第一个fit_transform),并将其转换为tf-idf矩阵(第二个fit_transformer)
    tfidf = transformer.fit_transform(freWord.fit_transform(corpus))
    weight=tfidf.toarray()
    cPickle.dump(weight,open("../tfidf.pkl","wb"))
    #获取词袋模型中的所有词语
    print type(weight)
    for name in weight:
        print name
    #print tfidf[0]
    print "========"
    word = freWord.get_feature_names()
    print type(word)
#     for name in word:
#         print name
    cPickle.dump(word,open("../dictionary.pkl","wb"))
    
def cal_similarity(querypath):
    print "query start"
    q_file = open(querypath, 'r')
    query = q_file.readline()
    search = q_file.readline()
    q_file.close()
    diction = cPickle.load(open("../dictionary.pkl","rb"))
    tfidf = cPickle.load(open("../tfidf.pkl","rb"))
    query_bow = diction.doc2bow(query.split())
    query_tfidf = tfidf[query_bow]
    search_bow = diction.doc2bow(search.split())
    search_tfidf = tfidf[search_bow]
    print "vec_tfidf:"
    num =0.0
    dot_product = 0.0;  
    normA = 0.0;  
    normB = 0.0; 
    print query_tfidf
    for idq in query_tfidf:
        for ids in search_tfidf:
            if idq[0] == ids[0]:
                dot_product += idq[1]*ids[1]
    if dot_product>0:
        for idq in query_tfidf:
            print idq[1]
            normA += idq[1]*idq[1]
        for ids in search_tfidf:
            normB += ids[1]*ids[1]
        print 'haha'
        if normA == 0.0 or normB==0.0:  
            return None  
        else:  
            return dot_product / ((normA*normB)**0.5)  
    else:
        return 0
    

tushi = []
def tushi_simi():
    diction = cPickle.load(open("../dictionary.pkl","rb"))
    tfidf = cPickle.load(open("../tfidf.pkl","rb"))
    s_file = open("D:\\eclipse-workspace\\docudeal\\tushi\\all.txt")
    for search in s_file:
#         line = search.replace('\n','').strip().decode('gbk').encode('utf-8')
#         wordList = list(jieba.cut(line)) 
#         outStr = ""
#         for word in wordList:   
#             outStr+=word
#             outStr+=' '
        search_bow = diction.doc2bow(search.split())
        search_tfidf = tfidf[search_bow]
        tushi.append(search_tfidf)
    cPickle.dump(tushi,open("../tushi.pkl","wb"))
    
cal_tfidf()
print cal_similarity('D:\\eclipse-workspace\\docudeal\\search.txt')
# tushi_simi() 
# print tushi[1]  

def tfidf_similarity(query):
    diction = cPickle.load(open("../dictionary.pkl","rb"))
    tfidf = cPickle.load(open("../tfidf.pkl","rb"))
    
    query_bow = diction.doc2bow(query.split())
    query_tfidf = tfidf[query_bow]
    
    num =0.0
    dot_product = 0.0;  
    normA = 0.0;  
    normB = 0.0; 
    for tag in tushi:
        for idq in query_tfidf:
            for ids in tushi[tag]:
                if idq[0] == ids[0]:
                    dot_product += idq[1]*ids[1]
        if dot_product>0:
            for idq in query_tfidf:
                normA += idq[1]*idq[1]
            for ids in tushi[tag]:
                normB += ids[1]*ids[1]
            if normA == 0.0 or normB==0.0:  
                return 0  
            else:  
                return dot_product / ((normA*normB)**0.5)  
        else:
            return 0