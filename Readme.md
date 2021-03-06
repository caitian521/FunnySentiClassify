# FunnySentiClassify

## 背景  

爬取网易云音乐评论，分析评论的情感类型，从而确定歌曲的情感类型。  

这是本人本科毕业的工作，当时还没有bert，也不太会面向对象，所以技术层面可能还登不上台面。不过整个项目的构思完全出自于自己，兴趣驱动。周董的歌类型特别丰富，周杰伦的歌一路伴着成长，欢快的、悲伤的我都喜欢。但是有些冷门歌曲只看我就不知道它是哪一种，心情很丧的时候就是想听一些欢快的歌曲啊！！我不会音频分析，可是我会文本挖掘啊，于是乎拍脑袋想出来通过分析评论的情感确定歌曲的情感。感谢网易云音乐，营造了一个很好的社区氛围，再次致敬周董(●'◡'●)  

## 实现

### 数据准备  

2017年网易云音乐还有周杰伦的版权，不过虽然现在版权没有了，但是评论还能爬（突然发现这是珍贵资源啊，毕竟别的平台评论简直没法看，希望猪厂不要删掉这些数据。这里我提供了一份我爬的结果，50首周杰伦热门歌曲10w+条评论，[网盘地址](https://pan.baidu.com/s/1wzsa_xv6Gc8nEpSHpoIn6A)。

首先得有歌曲目录“https:\/\/music.163.com\/#/playlist?id=743929495”，此url便是50首周杰伦热门歌曲歌单。  
怎么获取歌曲id？  
解析html可以发现歌曲id详见代码cloud.py 20-35行  
评论就在这个api：url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=" % id  
这个api被加密了，但是一个优秀的爬虫不在怕的，commentGet.py对网易云音乐api进行了解析，我参考了这个[reference](https://www.zhihu.com/search?type=content&q=%E7%BD%91%E6%98%93%E4%BA%91%E9%9F%B3%E4%B9%90%E8%AF%84%E8%AE%BA%E7%88%AC%E8%99%AB)。  



这个api不光提供了评论数据的接口，还有用户的昵称、头像、是否会员，广大文本挖掘机可以充分发挥想象力，这里略去1万字。  


### 情感分析   

下面就是文本挖掘的范畴了。这里探讨三种简单的方式  

1、基于查情感词表的方式。  
大连理工大学信息检索实验室提供了一个情感本体库，林老师团队花费了很多精力，深度学习还没火的时候，情感本体库解救了很多搞情感分析的人，宣传一波~  

2、基于情感图式的方法，通过计算文本与情感图式节点的相似度，判断情感类别。  

再次背景介绍：当年模型还不够强，通过人工构造知识是一个很好的方式。情感图式就是一个类似于知识图谱的情感图谱，我用的情感图式是基于人工和hownet构建的，每个情感类别扩展出了很多场景，大概长这个样子，想进一步了解情感图式的朋友也可以联系 [大连理工大学IR实验室](http://ir.dlut.edu.cn).  

<img src="https://github.com/caitian521/FunnySentiClassify/blob/master/pic/schema.png" width = "300" height = "260" alt="欢快" align=center>  



有了情感图式，分析文本情感类别就可以转化成计算文本和情感图式每个节点距离的问题了。我用的是余弦相似度，将文本表示成向量我用了两个方式  
1）基于tf-idf向量空间，词袋模型  
2）基于分布式词向量，语言模型word2vec  
NLP发展到现在回头看看这些方法，令人咂舌啊！  

虽然技术略low但是作为一个学位论文还是要有创新点，以下假装高亮   
1、基于查情感词表的方式，考虑了否定词、转折词因素，具体可看search_table.py    
2、基于tf-idf向量空间，词袋模型，对于词表进行了特殊的处理。由于是对文本的情感分类，所以很多词对于情感是是没有意义的。为了给词袋模型降维，我计算了每个词在不同类别情感语料中的tfidf值及其方差。方差大的很明显会是和情感有关的词，方差小的说明这个词各个情感写出现的频率差不多，可以不考虑。  
3、实验说明：情感图式我只使用了二级节点，由于网易云音乐评论是没有标签的，因此实验阶段使用的公开的中文情感语料库。结果当然证明还是word2vec好（捂脸


## 代码说明：

	cloud.py	按照歌单爬取网易云音乐评论
	commentGet.py	网易云音乐api加密解析

	commentGet.py	网易云音乐api加密解析
 	SchemaDeal.py 	处理二级情感图式 快乐0-95，恐惧95-206，悲伤206-304，愤怒304-393
	emomachine.py 	计算文本与情感图式节点相似度，根据情感图式类别判断文本情感类型
	fangcha.py 	计算词表在每个情感类别的tf-idf及方差，目的是过滤掉大众词
	filter.py 	切词
	machinecal.py 	计算向量空间模型两个文本的相似度
	search_table.py 	查情感词表，考虑否定词和转折词
	splitclass_cut.py 	将语料分词，按情感类型存储在相应文档中，8个情感类别，不对其进行更细粒度划分
	sum_sentence.py 	统计每个类别文本个数，计算准确率
	tfidf.py 	向量空间模型
	trainwordvec.py 	训练skip-gram语言模型，获得word2vec词向量
	word2vecCos.py 	用分布式词向量计算文本与情感图式的相似度

	predeal.py 	分析每个歌曲对应的每条评论情感类型，确定歌曲的情感  


做了一个可视化展示

<img src="https://github.com/caitian521/FunnySentiClassify/blob/master/pic/happy_jay.jpg" width = "400" height = "520" alt="欢快" align=left>
<img src="https://github.com/caitian521/FunnySentiClassify/blob/master/pic/sad_jay.jpg" width = "400" height = "520" alt="欢快" align=right>  



