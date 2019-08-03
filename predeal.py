# -*- coding: utf-8 -*- 
"""
Created on Sat May 3 16:37:43 2017

@author: ct
将语料分词，按情感类型存储在相应文档中，不保留标注格式
"""
from __future__ import unicode_literals
from cloudmusic import simiword2vec
import os
import sys
import jieba
import re
import cloudmusic
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

def readDS():#h---xiedan,xiexie……
    file = open("D:\\eclipse-workspace\\docudeal\\double_single.txt")#PA 快乐 h
    for line in file:
        try:
            sentence = line.decode('gbk').encode('utf-8').replace('\n','').strip()
            temp = sentence.split(' ')
            newstr = ontology[temp[0]]
            key = to_emotion(temp[2])
            if key in emo_table:
                emo_table[key] += newstr
            else:
                emo_table.setdefault(key,newstr)
        except:
            print line 
            
def readlibrary():
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


def searchTable(query):
    emo_dict = {}
    for word in query:
        if word in transiton:
            emo_dict.clear()
        else:
            for key in emo_library:
                if word in emo_library[key]:
                    if key in emo_dict:
                        emo_dict[key] += 2
                    else:
                        emo_dict.setdefault(key,2)
            for key in emo_table:
                if word in emo_table[key]:
                    if key in emo_dict:
                        emo_dict[key] += 1
                    else:
                        emo_dict.setdefault(key,1)
    num = 0
    cal_emotion = 0
    for key in emo_dict:
        if emo_dict[key]>=num:
            num = emo_dict[key]
            cal_emotion = key
#     print emo_dict
#     if emo_dict == {}:
# #         print emo_dict
#         newstr = ""
#         for word in query:
#             newstr+=word
#             newstr+=' '
# #         print type(newstr)
#         cal_emotion = emodocu.machinecal.tfidf_similarity(newstr)

    return cal_emotion
                 
def readquery(sentence):
    #file = open(sentence,'r').readline()
    wordList = []
    
    line = sentence.strip().replace('\n','')
    newline = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）\[\]]+".decode("utf8"), "".decode("utf8"),line)
    wordList = list(jieba.cut(newline)) 
    outStr = []
    for word in wordList:  
        if word not in stopList: 
            outStr.append(word.decode('utf-8','ignore'))
    return outStr
    
def sum_text(querypath):
    text_emo = {}
    file = open(querypath).readlines()
    for sentence in file:
        temp_query = readquery(sentence)
        temp_emotion = searchTable(temp_query)
        if temp_emotion in text_emo:
            text_emo[temp_emotion] += 1
        else:
            if temp_emotion!=0:
                text_emo.setdefault(temp_emotion,1)
    return text_emo

readontology()     
readtransition()
readnegtive()
emo_table = {}
readDS() 
emo_library = {}  
readlibrary()

dir = "D:\\eclipse-workspace\\musicanaly\\jay"
happy = open("D:\\eclipse-workspace\\musicanaly\\ccjay_1.txt",'w')
sad = open("D:\\eclipse-workspace\\musicanaly\\ccjay_3.txt",'w')
angry = open("D:\\eclipse-workspace\\musicanaly\\ccjay_2.txt",'w')
cnt = 0
for s in os.listdir(dir): 
    cnt +=1
    newDir=os.path.join(dir,s)         
    text_emotion = sum_text(newDir)
    print s.split('.')[0]
    print text_emotion
    try:
        num = 0
        emo = 0
        text_emotion[1] /=2
        for key in text_emotion:
            if text_emotion[key]>=num:
                num = text_emotion[key]
                emo = key
        print emo
        if emo == 1:
            happy.write(s.split('.')[0])
            happy.write('\n')
        elif emo== 2:
            angry.write(s.split('.')[0])
            angry.write('\n')
            
        else:
            sad.write(s.split('.')[0])
            sad.write('\n')
    except:
        print "is empty!"
#     if cnt >30:
#         break
happy.close()
sad.close()
angry.close()