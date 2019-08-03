#!/usr/bin/python  
# -*- coding: utf-8 -*-

import numpy
import os
import string
import sys
import re
import xlwt
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
size = 4
vol_set = set()
dictionary = {}
def read_word(num):
    file_path = "D:\\eclipse-workspace\\docudeal\\deal\\four\\tfidf_%s.txt" %num
    dictionary[num] = {}
    with open(file_path) as f:
        for line in f:
            temp = line.split('\t')
            temp1 = temp[1][0:-1]
            vol_set.add(temp[0])
            dictionary[num].setdefault(temp[0],float(temp1))

result = {}
result1={}
def writeExcel(num,word,data):
    sheet1.write(num,0,word,style)
    #向sheet页中写入数据
    for i in range(4):
        sheet1.write(num,i+1,data[i],style)

def cal_fangcha():
    for word in vol_set:
        sum_2 = 0.0
        sum = 0.0
        all = []
        for i in range(size):
            if word in dictionary[i]:
                sum += dictionary[i][word]
        ave = sum/size*1.0
        for i in range(size):
            if word in dictionary[i]:
                sum_2 += (dictionary[i][word]-ave)*(dictionary[i][word]-ave)
        dx = (sum_2/size*1.0)** 0.5

        result.setdefault(word,dx)

    sorted_result = sorted(result.iteritems(),key = lambda d:d[1],reverse = True)
    fw = open("D:\\eclipse-workspace\\docudeal\\deal\\result.txt",'w')
    word_cnt = 0
    for vol in sorted_result[0:300]:
        fw.write(vol[0] + '\t' + str(vol[1]) +'\n')
        data = []
        for i in range(size):
            if vol[0] in dictionary[i]:
                data.append(dictionary[i][vol[0]])
            else:
                data.append(0)
        writeExcel(word_cnt,vol[0],data)
        word_cnt+=1
    fw.close()    
    

#创建workbook和sheet对象
workbook = xlwt.Workbook(encoding='utf-8')  
sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'SimSun'    # 指定“宋体”
style.font = font       
              
for i in range(size):
    read_word(i)
print len(vol_set)
cal_fangcha()       

workbook.save('D:\\eclipse-workspace\\docudeal\\DifferWordwuwu.xls')
print '创建excel文件完成！'        
        