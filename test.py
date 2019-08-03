#! /usr/bin/env python2.7
#coding=utf-8

from __future__ import unicode_literals
import logging
from gensim import corpora, models, similarities
#from gensim.scripts.make_wiki import dictionary
import jieba
import pickle  
import cPickle 

import sys
sys.path.append("../")
reload(sys)
sys.setdefaultencoding( "utf-8" )
def similarity(datapath):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    stopList = []
    with open('D:\\eclipse-workspace\\docudeal\\stopwords.txt') as stopfile:
        for words in stopfile:
            words.replace('\n','')
            stopList.append(words)
    trainfile = open(datapath) #不同的documents用换行符隔开
    documents = trainfile.readlines()
    print len(documents)
    texts = [[word for word in line.split() if len(word)>1 and word not in stopList] for line in documents if len(line)>4]
    #texts = [[word for word in document.split()] for document in documents]
    trainfile.close()            
    diction = corpora.Dictionary(texts)
    print type(diction)
    cPickle.dump(diction,open("../dictionary.pkl","wb"))
    #diction.save('../dictionary.data')
    corpus = [diction.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    print type(tfidf)
    #tfidf.save('../tfidf.data')
    cPickle.dump(tfidf,open("../tfidf.pkl","wb"))

    
def cal_similarity(querypath,searchpath):
    print "query start"
    s_file = open(searchpath,'r')
    search = s_file.readline()
    s_file.close()
    
    q_file = open(querypath, 'r')
    query_text = q_file.readlines()
    q_file.close()
#     dFile =file('../dictionary.data','r')
#     tFile = file('../tfidf.data','r')
#     diction = load(dFile)
#     tfidf = load(tFile)
    
    diction = cPickle.load(open("../dictionary.pkl","rb"))
    tfidf = cPickle.load(open("../tfidf.pkl","rb"))
    search = search.decode('gbk')
    search_bow = diction.doc2bow(search.split())
    search_tfidf = tfidf[search_bow]
    print "============"
    result = []
    for query_line in query_text:
        wordList = list(jieba.cut(query_line.decode('gbk').replace('\n',''))) 
        query = ''  
        for word in wordList:   
            print word
            query += str(word)
            query += ' '  
#       query = query.decode('gbk')
        print query
        query_bow = diction.doc2bow(query.split())
        query_tfidf = tfidf[query_bow]
        
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
                normA += idq[1]*idq[1]
            for ids in search_tfidf:
                normB += ids[1]*ids[1]
            if normA == 0.0 or normB==0.0:  
                result.append(0) 
            else:  
                 result.append(dot_product / ((normA*normB)**0.5) )
        else:
            result.append(0)
    return result
#similarity("D:\\eclipse-workspace\\docudeal\\corpus.txt")
ans = []
print "-----------"
ans = cal_similarity("../../search.txt","../../query1.txt")
print ans