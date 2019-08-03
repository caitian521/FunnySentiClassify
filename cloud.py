# -*- coding:utf-8 -*- 
import requests
import urllib
from bs4 import BeautifulSoup
#from bsddb.test.test_associate import musicdata
import os
import time
import commentGet
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

headers = {'Referer':'http://music.163.com/',
           'Host':'music.163.com',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

# file = open("D:\\eclipse-workspace\\Spider1\\src\\cloudurl.txt")
# url = file.readline()
# while url:

url = 'http://music.163.com/playlist?id=743929495'
s = requests.session()
s = BeautifulSoup(s.get(url,headers=headers).content)
music_id_list = s.find('ul', {'class':'f-hide'})
out_dir = 'D:\\eclipse-workspace\\musicanaly\\jay63\\'
i= 0
for music in music_id_list.find_all('a'):
    i = i+1
    try:
        id = music['href'].split('=')[1]
        name = music.text.decode('utf-8').encode('gb2312')
        target = out_dir+str(name)+'+'+str(id)+".txt"
        print target
        f = open(target,'w')
        url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=" %id
        data = []
        try:
            data = commentGet.get_Comment(url)
            cnt = len(data)
            for num in range(cnt):
                f.write(str(num+1)+': '+data[num]+'\n')
        except:
            print data
        f.close()
    except:
        print music.text+'  歌曲不符合规范'
    time.sleep(3)
    print i
