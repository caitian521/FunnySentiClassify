# -*- coding: utf-8 -*- 
"""
Created on Sat May 3 16:37:43 2017

@author: ct
将语料分词，按情感类型存储在相应文档中
8个情感类别，不对其进行更细粒度划分
D:\\eclipse-workspace\\docudeal\\deal\\emo_%s.txt
D:\eclipse-workspace\docudeal\\deal\\corpus.txt
"""
from __future__ import unicode_literals
import os
import sys
import jieba
import re
sys.path.append("../")
reload(sys)
sys.setdefaultencoding( "utf-8" )


def emotionget():
    emo_class_file = open("D:\\eclipse-workspace\\docudeal\\big_small.txt",'r')
    '''
            喜,h,e,c,k
            好,r,b,p,l
            怒,i
            哀,s,w,g,m
            惧,u,f,x
            恶,t,a,d,j,y
            惊,q
            平静,o
    '''
    with open(emo_class_file) as f_r:
        i = 0
        for line in f_r:
            temp = line.decode('gbk').split(",")
            data[i] = temp[1:len(temp)-1]
            data[i].append(temp[len(temp)-1][0])
            f = open("D:\\eclipse-workspace\\docudeal\\deal\\emo_%s.txt" %i,'w')
            f.close()
            i = i+1

emotionget()   
dir = "D:\\eclipse-workspace\\docudeal\\oldtag"
data={}
def mergeit(dir):
    cnt = 0 
    for s in os.listdir(dir): 
        newDir=os.path.join(dir,s)
        fin = open(newDir, 'r') 
        #print newDir
        article = {}         
        for eachLine in fin:
            part = eachLine.decode('gbk').split(u'|')
            # 从前 ， 有个 小伙子 叫 阿福 ， 整日 游手好闲 ， 不学无术 。 | d 
            length = len(part)
            for j in range(length-1):
                temp = []
                for emo in range(8):
                    if part[j+1][0] in data[emo]:
                        #print str(emo)+'---'+str(part[j+1][0])
                        ciyu = re.sub("[a-z]","",part[j]).encode('utf-8')
                        if len(ciyu)>0:
                            if emo in article:
                                article[emo].append(ciyu)
                            else:
                                temp.append(ciyu)
                                article.setdefault(emo,temp)
                                break
        for i in range(8):
            if i in article:
                f = open("D:\\eclipse-workspace\\docudeal\\deal\\emo_%s.txt" %i,'a+')  
                for sentence in article[i]:
                    line = sentence.strip().encode('utf-8')
                    wordList = list(jieba.cut(line)) 
                    outStr = ''  
                    for word in wordList:   
                        outStr += str(word)
                        outStr += ' '  
                    f.write( outStr.strip() + ' ') 
                    f.write('\n') 
                f.close()           
        fin.close()
        cnt = cnt+1
        print cnt

      
mergeit(dir)  
outfile = open("D:\eclipse-workspace\docudeal\\deal\\corpus.txt","w")
for i in range(8): 
    with open("D:\\eclipse-workspace\\docudeal\\deal\\emo_%s.txt" %i) as file:
        data = file.read()
    outfile.write(data)
outfile.close()