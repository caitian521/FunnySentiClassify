# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import os
import sys
import jieba
import re
# sys.path.append("../")
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
 
table = {1:['h','e','c','k'],2:['u','f','x'],3:['s','w','g','m'],4:['i']}
print type(table[1][0])

querylines = open("../../oldtag_corpus.txt")
newtxt = open("../../newfour_corpus.txt",'w')
cnt = 0
# four = [1151, 377, 644, 67]

four_type = [0,0,0,0]
for line in querylines:
    try:
#         print "图式查询ing"
        temp = line.decode('gbk','ignore').split('|')
        R_emotion = temp[1].replace(' ','').replace('\n','')
#         print type(str(R_emotion))
        for key in table:
            if str(R_emotion) in table[key]:
#                 print '@@'
                newtxt.write(line)
                four_type[key-1]+=1
                cnt+=1
                break
    except:
        print "failed"+line.decode('gbk','ignore')
        
querylines.close()
newtxt.close()