# -*- coding: utf-8 -*- 
"""
Created on Sat May 3 16:37:43 2017

@author: ct
将语料分词，按情感类型存储在相应文档中，保留标注格式
"""
from __future__ import unicode_literals
import os
import sys
import jieba
import re
sys.path.append("../")
reload(sys)
sys.setdefaultencoding( "utf-8" )

dir = "D:\\eclipse-workspace\\docudeal\\oldtag"


def mergeit(dir):
    cnt = 0 
    f = open("D:\\eclipse-workspace\\docudeal\\biaozhu\\oldtag_corpus.txt",'w')
    for s in os.listdir(dir): 
        newDir=os.path.join(dir,s)
        fin = open(newDir, 'r') 
        #print newDir
        article = {}         
        for eachLine in fin:
            line = eachLine.decode('gbk').split()
            for sentence in line:
                #print sentence
                new_sentence = sentence.strip().encode('utf-8')
                wordList = list(jieba.cut(new_sentence)) 
                outStr = ''  
                for word in wordList:   
                    outStr += str(word)
                    outStr += ' '  
                f.write( outStr.strip() + ' ') 
                f.write('\n') 
        fin.close()
#         cnt = cnt+1
#         if cnt>1:
#             break
    f.close()
       
mergeit(dir)  