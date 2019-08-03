# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import os
import sys
import jieba
import re
# sys.path.append("../")
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
import numpy as np
import gensim
import pickle  
import cPickle 


model = gensim.models.Word2Vec.load("../wordvec200min1.model")
num = 200
stopList = set()
with open('D:\\eclipse-workspace\\docudeal\\stopwords.txt') as stopfile:
    for words in stopfile:
        stopList.add(words.replace('\n','').decode('utf-8'))
table = {1:['h','e','c','k'],2:['u','f','x'],3:['s','w','g','m'],4:['i']}

def readquery(sentence):
    #file = open(sentence,'r').readline()
    wordList = []
    line = sentence.strip().decode('gbk').encode('utf-8')
    wordList = list(jieba.cut(line)) 
    outStr = []
    for word in wordList:   
        outStr.append(word)
    return outStr

def preDeal(sentence):
    newstr = []
    temp = sentence.split(' ')
    for word in temp:
        if word not in stopList:
            newstr.append(word)
    return newstr

def getVector(sentence):
    result = np.zeros( (200L,) )
    for word in sentence:
#         print word
        try:
            vect = model[word]
            for i in range(num):
                result[i]+=vect[i]
        except:
            print '**'+word
    for i in range(num):
        result[i] = result[i]/len(sentence)
    return result

def readSchema(searchpath):
    schema = []
    file = open(searchpath,'r').readlines()
    for sentence in file:
        line = sentence.replace('\n','').strip().decode('gbk').encode('utf-8')
        wordList = list(jieba.cut(line)) 
        outStr = []
        for word in wordList:   
            outStr.append(word)
        schema.append(getVector(outStr))
    cPickle.dump(schema,open("../schema.pkl","wb"))
    return schema

def cosine(newvect,vect):
    dot_product = 0.0;  
    normA = 0.0;  
    normB = 0.0;  
    for a,b in zip(newvect,vect): 
        #print a,b 
        dot_product += a*b  
        normA += a**2  
        normB += b**2  
    if normA == 0.0 or normB==0.0:  
        return None  
    else:  
        return dot_product / ((normA*normB)**0.5)  
            
def calEmotion(id):    
    if id<95:
        return 1
    elif id>=95 and id <206:
        return 2
    elif id>=206 and id<304:
        return 3
    else:
        return 4
    
def rightemotion(haha):
#     print str(haha.replace('\n','').encode('gbk'))
    for key in table:
        if str(haha.replace('\n','').encode('gbk')) in table[key]:
            return key
    return 0

def word2vecCos_main(ans): 
#     querylines = open("../../query.txt")
    # newschema = readSchema("D:\\eclipse-workspace\\docudeal\\tushi\\all.txt")
    newschema = cPickle.load(open("../schema.pkl","rb"))
    # print len(newschema)
#     count_emo = 0
#     for line in querylines:
    try:
        print "图式查询ing"
#         temp = line.decode('gbk','ignore').split('|')
#         R_emotion = temp[1].replace(' ','')
#     #     print temp[0]
#         ans = preDeal(temp[0])
        newvector = getVector(ans)
        #print newvector
        caicai = []
        for node in newschema:
            #print cosine(newvector, node)
            caicai.append(cosine(newvector, node))
        number = caicai.index(max(caicai))
    #     print number
#         emotion = open("D:\\eclipse-workspace\\docudeal\\tushi\\all.txt").readlines()[number]
        print max(caicai)
        if max(caicai)>0.5:
            myEmotion = calEmotion(number)
        else:
            myEmotion = 0
        return myEmotion
    #     print R_emotion
#         right = rightemotion(R_emotion)
#         if right == myEmotion:
#             count_emo+=1
#             print temp[0]
#         print "answer:"
#         print str(right)+" vs "+str(myEmotion)
#         print emotion.decode('gbk')
    except:
        print "failed"
        return 0
#     print "finally:=================="
#     print count_emo

# newschema = readSchema("D:\\eclipse-workspace\\docudeal\\tushi\\all.txt")
# four = [0,0,0,0]
# four_type = [5515, 2008, 2968, 954]
# querylines = open("../../newfour_corpus.txt")
# # newschema = readSchema("D:\\eclipse-workspace\\docudeal\\tushi\\all.txt")
# newschema = cPickle.load(open("../schema.pkl","rb"))
# # print len(newschema)
# count_emo = 0
# for line in querylines:
#     try:
# #         print "图式查询ing"
#         temp = line.decode('gbk','ignore').split('|')
#         R_emotion = temp[1].replace(' ','')
#     #     print temp[0]
#         ans = preDeal(temp[0])
#         newvector = getVector(ans)
#         #print newvector
#         caicai = []
#         for node in newschema:
#             #print cosine(newvector, node)
#             caicai.append(cosine(newvector, node))
#         number = caicai.index(max(caicai))
#     #     print number
#         emotion = open("D:\\eclipse-workspace\\docudeal\\tushi\\all.txt").readlines()[number]
#         myEmotion = calEmotion(number)
#          
#         right = rightemotion(R_emotion)
#         if right == myEmotion and right != 0:
#             count_emo+=1
#             four[right-1] += 1
# #             print temp[0]
# #         print "answer:"
#         print str(right)+" vs "+str(myEmotion)
#         print emotion.decode('gbk')
#     except:
#         print "failed"
#     
# print "finally-----------------"  
# print count_emo
# 
# print count_emo*1.0/11445.0  
# print four
# for i in range(4):
#     print four[i]*1.0/four_type[i]


