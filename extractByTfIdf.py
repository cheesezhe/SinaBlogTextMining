#!/usr/bin/env python
# -*-coding:utf-8-*-
import BlogData
#根据tf-idf抽取出关键词

#src数据集目录：data_noun_TF_relatedInfo
#dst数据集目录：extracted (这个要自己新建一个)

#在json中添加一个字段extractedInfo,对应的值为一个dict,在dict中有一个
#key为tf-idf，对应的值为5根据tf-idf选取的5个词

#新的json数据为：
#{
# 'content':...
# 'seg':...
#   .
#   .
#   .
#  'extractedInfo':{
#        'tf-idf':['word1','word2','word3','word4','word5']
#   }
# }

def extractByTfIdf(data):
    #TODO:ADD code here
    return data

#corpus_size取决于src数据集目录的文件名中最大的那个数字data_{??}.json
corpus_size = 2736
for i in xrange(corpus_size):
    try:
        print 'processing %d/12832...'%i,
        src = 'data_noun_TF_relatedInfo/data_'+str(i)+'.json'
        blogData = BlogData(src)
        blogData.readFromJson()

        blogData.data = extractByTfIdf(blogData.data)

        dst = 'extracted/data_'+str(i)+'.json'
        blogData.saveData(dst)
    except BaseException,e:
            #不存在的文件直接跳过
            continue