# -*- coding: utf-8 -*- 
"""
Created on Sat May 3 16:37:43 2017

@author: ct
查情感表，否定词表，转折词表，得到情感标签，并计算准确率，召回率
"""
from __future__ import unicode_literals
from emodocu import word2vecCos
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




def readontology():
    ontology = {}
    file = open("D:\\eclipse-workspace\\docudeal\\ontology.txt")
    for line in file:#谢忱    PD
        try:
            sentence = line.decode('gbk').encode('utf-8').replace('\n','').strip()
            temp = sentence.split('\t')
            newstr = []
            if temp[1] in ontology:
                ontology[temp[1]].append(temp[0])
            else:
                newstr.append(temp[0])
                ontology.setdefault(temp[1],newstr)
        except:
            print line
    return ontology

def readtransition():
    transiton = []
    file = open("D:\\eclipse-workspace\\docudeal\\转折词.txt")
    for line in file:#谢忱    PD
        try:
            word = line.decode('gbk').encode('utf-8').replace('\n','').strip()
            transiton.append(word)
        except:
            print line    
    return transiton
            
def readnegtive():
    negtive = []
    file = open("D:\\eclipse-workspace\\docudeal\\否定词.txt")
    for line in file:#谢忱    PD
        try:
            word = line.decode('gbk').encode('utf-8').replace('\n','').strip()
            negtive.append(word)
#             print word
        except:
            print line 
    return negtive        
    
def readDS():#PA 快乐 h
    emo_table = {}
    file = open("D:\\eclipse-workspace\\docudeal\\double_single.txt")
    for line in file:
        try:
            sentence = line.decode('gbk').encode('utf-8').replace('\n','').strip()
            temp = sentence.split(' ')
            newstr = emo_table_fine[temp[0]]
            emo_table.setdefault(temp[2],newstr)
        except:
            print line 
    return emo_table        

    
emo_table_fine = readontology()    
transiton = readtransition()
negtive = readnegtive()
emo_table = readDS()
 
def to_emotion(haha):
#     print str(haha.replace('\n','').encode('gbk'))
    for key in table:
        if str(haha.replace('\n','').encode('gbk')) in table[key]:
            return key
    return 0
        
       
def readlibrary():
    emo_library = {}
    file = open("D:\\eclipse-workspace\\docudeal\\library.txt")
    for line in file:
        try:
            sentence = line.decode('gbk').encode('utf-8').replace('\n','').strip()
            temp = sentence.split('\t')
            key = to_emotion(temp[1])
            if key in emo_library:
                emo_library[key].append(temp[0])
            else:
                templist = []
                templist.append(temp[0])
                emo_library.setdefault(key,templist)
        except:
            print line 
 
  
emo_library = readlibrary()

      
def preDeal(sentence):
    newstr = []
    temp = sentence.split(' ')
    for word in temp:
        if word not in stopList:
            newstr.append(word)
    return newstr



def searchTable(query):
    emo_dict = {}
    front = ""
    flag = 0
    for word in query:
        flag = 0
        if word in transiton:
            emo_dict.clear()
        else:
            if front in negtive:
                flag = 1
            for key in emo_library:
                if word in emo_library[key]:
                    if flag == 0:
                        if key in emo_dict:
                            emo_dict[key] += 2
                        else:
                            emo_dict.setdefault(key,2)
                    else:
                        if key == 1:
                            if key in emo_dict:
                                emo_dict[3] += 2
                            else:
                                emo_dict.setdefault(3,2)
                        else:
                            if key in emo_dict:
                                emo_dict[1] += 2
                            else:
                                emo_dict.setdefault(1,2)                        
            for key in emo_table:
                if word in emo_table[key]:
                    if flag == 0:
                        if key in emo_dict:
                            emo_dict[key] += 1
                        else:
                            emo_dict.setdefault(key,1)
                    else:
                        if key == 1:
                            if key in emo_dict:
                                emo_dict[3] += 1
                            else:
                                emo_dict.setdefault(3,1)
                        else:
                            if key in emo_dict:
                                emo_dict[1] += 1
                            else:
                                emo_dict.setdefault(1,1)
        front = word
    num = 0
    cal_emotion = 0
    for key in emo_dict:
        if emo_dict[key]>=num:
            num = emo_dict[key]
            cal_emotion = key
#     print emo_dict
    if emo_dict == {}:
        cal_emotion = emodocu.word2vecCos.word2vecCos_main(query)
#         newstr = ""
#         for word in query:
#             newstr+=word
#             newstr+=' '
#     #         print type(newstr)
#         cal_emotion = emodocu.machinecal.tfidf_similarity(newstr)

    return cal_emotion
                  
querylines = open("../../newfour_corpus.txt")
cnt = 0
cnt_emo = 0
four = [0,0,0,0]
four_type = [5515, 2008, 2968, 954]
for line in querylines:
#     print "------"
    try:
        temp = line.decode('gbk','ignore').split('|')
        R_emotion = temp[1].replace(' ','')
        ans = preDeal(temp[0])
        myemotion = searchTable(ans)
        rightEmotion = to_emotion(R_emotion)
        print str(myemotion)+" vs "+str(rightEmotion)
        if myemotion==rightEmotion and myemotion != 0:
            cnt_emo += 1
            four[rightEmotion-1] += 1
    except:
        print line.decode('gbk','ignore')
    cnt+=1
    
print "finally-----------------"  
print cnt_emo
print cnt
print cnt_emo*1.0/11445.0  
print four
for i in range(4):
    print "p:" + str(four[i]*1.0/four_type[i])

    