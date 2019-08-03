# -*- coding: utf-8 -*- 
"""
Created on Sat May 3 16:37:43 2017

@author: ct
处理二级情感图式 快乐0-95，恐惧95-206，悲伤206-304，愤怒304-393
D:\\eclipse-workspace\\docudeal\\tushi\\all.txt
"""
from __future__ import unicode_literals
import os
import sys
import jieba
import re
sys.path.append("../")
reload(sys)
sys.setdefaultencoding( "utf-8" )

dir = "D:\\eclipse-workspace\\docudeal\\tushi"
def schemadeal():
    cnt = 0
    outfile = open("D:\\eclipse-workspace\\docudeal\\tushi\\all.txt",'w')
    for s in os.listdir(dir): 
        newDir=os.path.join(dir,s)
        print newDir
        fin = open(newDir, 'r') 
        
        for line in fin:
            sentence = line.decode('gbk').encode('utf-8')
            if '[' in sentence:
                pass
            else:
#                 outfile.write(str(cnt)+' ')
                sentence = sentence.split('=')
                outstr = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),sentence[1])
                outfile.write(outstr)
                outfile.write('\n')
                cnt+=1
        fin.close()
        print cnt
    outfile.close()
schemadeal()