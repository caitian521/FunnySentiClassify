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

outfile = open("D:\\eclipse-workspace\\docudeal\\deal\\corpus.txt")
for i in range(8):
    dir = "D:\\eclipse-workspace\\docudeal\\deal\\emo_%s.txt" %i
    with open(dir,'r') as file:
        
                