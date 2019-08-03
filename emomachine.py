# -*- coding: utf-8 -*- 
"""
Created on Sat May 3 16:37:43 2017

@author: ct
将语料分词，按情感类型存储在相应文档中，不保留标注格式
"""
from __future__ import unicode_literals
from emodocu import machinecal
import os
import sys
import jieba
import re
import emodocu
sys.path.append("../")
reload(sys)
sys.setdefaultencoding( "utf-8" )

stopList = set()
with open('D:\\eclipse-workspace\\docudeal\\stopwords.txt') as stopfile:
    for words in stopfile:
        stopList.add(words.replace('\n','').decode('utf-8'))
table = {1:['h','e','c','k'],2:['u','f','x'],3:['s','w','g','m'],4:['i']}

ontology = {}
transiton = []
negtive = []
def readontology():
    file = open("D:\\eclipse-workspace\\docudeal\\ontology.txt")
    for line in file:#谢忱    PD
        try:
            sentence = line.decode('gbk').encode('utf-8').replace('\n','').strip()
            temp = sentence.split('\t')
            newstr = []
#             print temp[0]+temp[1]
            if temp[1] in ontology:
                ontology[temp[1]].append(temp[0])
            else:
                newstr.append(temp[0])
                ontology.setdefault(temp[1],newstr)
        except:
            print line

def readtransition():
    file = open("D:\\eclipse-workspace\\docudeal\\转折词.txt")
    for line in file:#谢忱    PD
        try:
            word = line.decode('gbk').encode('utf-8').replace('\n','').strip()
            transiton.append(word)
#             print word
        except:
            print line    
            
def readnegtive():
    file = open("D:\\eclipse-workspace\\docudeal\\否定词.txt")
    for line in file:#谢忱    PD
        try:
            word = line.decode('gbk').encode('utf-8').replace('\n','').strip()
            negtive.append(word)
#             print word
        except:
            print line 
            
readontology()     
readtransition()
readnegtive()
emo_table = {}

def readDS():#PA 快乐 h
    file = open("D:\\eclipse-workspace\\docudeal\\double_single.txt")
    for line in file:
        try:
            sentence = line.decode('gbk').encode('utf-8').replace('\n','').strip()
            temp = sentence.split(' ')
            newstr = ontology[temp[0]]
            emo_table.setdefault(temp[2],newstr)
        except:
            print line 
readDS()   
    
def preDeal(sentence):
    newstr = []
    temp = sentence.split(' ')
    for word in temp:
        if word not in stopList:
            newstr.append(word)
    return newstr

def to_emotion(haha):
#     print str(haha.replace('\n','').encode('gbk'))
    for key in table:
        if str(haha.replace('\n','').encode('gbk')) in table[key]:
            return key
    return 0

def searchTable(query):
#     emo_dict = {}
#     for word in query:
#         if word in transiton:
#             emo_dict.clear()
#         else:
#             for key in emo_table:
#                 if word in emo_table[key]:
#                     if key in emo_dict:
#                         emo_dict[key] += 1
#                     else:
#                         emo_dict.setdefault(key,1)
#     num = 0
#     emotion = ''
#     for key in emo_dict:
#         if emo_dict[key]>=num:
#             num = emo_dict[key]
#             emotion = key
#     print emo_dict
#     if emo_dict == {}:
#         cal_emotion = emodocu.word2vecCos.word2vecCos_main(query)
#     else:
#     if emo_dict == {}:
#         print emo_dict
    newstr = ""
    for word in query:
        newstr+=word
        newstr+=' '
#         print type(newstr)
    cal_emotion = emodocu.machinecal.tfidf_similarity(newstr)
#     else:
#         cal_emotion = to_emotion(emotion) 
    return cal_emotion

querylines = open("../../newfour_corpus.txt")                    
# querylines = open("../../oldtag_corpus.txt")
cnt = 0
cnt_emo = 0
four = [0,0,0,0]
four_type = [5515, 2008, 2968, 954]
for line in querylines:
#     print "------"
    try:
        temp = line.decode('gbk','ignore').split('|')
        R_emotion = temp[1].replace(' ','')
    #     print temp[0]
#         print line.decode('gbk','ignore')
        ans = preDeal(temp[0])
        myemotion = searchTable(ans)
        rightEmotion = to_emotion(R_emotion)
        print str(myemotion)+" vs "+str(rightEmotion)
        if myemotion==rightEmotion and rightEmotion!=0:
            cnt_emo += 1
            four[rightEmotion-1] += 1
    except:
        print "--error--"
        print line.decode('gbk','ignore')
    cnt+=1
     
print "finally-----------------"  
print cnt_emo
print cnt
print cnt_emo*1.0/11445.0  
print four
for i in range(4):
    print four[i]*1.0/four_type[i]