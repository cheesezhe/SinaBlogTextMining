#!/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = 'ZhangHe'
import json,sys,math
#BlogData类，一个BlogData对象对应一个JSON文件中的数据
class BlogData:
    #初始化BlogData对象
    #file_path: JSON数据的目录
    def __init__(self,file_path = None):
        self.file_path = file_path
        self.data = {}

    #从file_path中读取JSON数据并保存在self.data中
    def readFromJson(self):
        with open(self.file_path,'r') as f:
            self.data = json.load(f,encoding='utf-8')

    #判断BlogData数据的relatedInfo中是否有名词成分，返回True or False
    #名词成分包括：名词，命名实体，文字，动词，心情，人称代词，场景
    def hasNounRelatedInfoData(self):
        ret = False
        if self.data['relatedInfo'] == None:
            return False
        relatedInfo = self.data['relatedInfo'].split('|')
        self.data['relatedInfo'] = []
        for info in relatedInfo:
            type = info.split(':')[0]
            value = info.split(':')[1]
            if type == "名词".decode('utf-8') \
                    or type == "命名实体".decode('utf-8') \
                    or type == "人称代词".decode('utf-8') \
                    or type == "场景".decode('utf-8'):
                ret = True
                data = {}
                data['type'] = type.encode('utf-8')
                data['value'] = value.encode('utf-8')
                self.data['relatedInfo'].append(data)
        # print self.data['relatedInfo']
        return ret

    #把BlogData数据按照约定的格式(查看数据目录下的json文件)保存到file_path中
    def saveData(self,file_path = None):
        if file_path == None:
            file_path = self.file_path
        self.data['content'] = self.data['content'].encode('utf-8')
        self.data['seg'] = self.data['seg'].encode('utf-8')
        self.data['filteredContent'] = self.data['filteredContent'].encode('utf-8')
        for idx in xrange(len(self.data['dp'])):
            self.data['dp'][idx]['cont'] = self.data['dp'][idx]['cont'].encode('utf-8')
        for idx in xrange(len(self.data['relatedInfo'])):
            self.data['relatedInfo'][idx]['type'] = self.data['relatedInfo'][idx]['type'].encode('utf-8')
            self.data['relatedInfo'][idx]['value'] = self.data['relatedInfo'][idx]['value'].encode('utf-8')
        with open(file_path,'w') as f:
            json.dump(self.data,f,indent=2,ensure_ascii=False)

#统计语料集中所有词语的tf-idf信息
def calcTF(self):
    idf = {}
    totoal_doc_number = 4067.0
    corpus_size = 12833
    for i in xrange(corpus_size):
        try:
            src = 'data_noun_relatedInfo/data_'+str(i)+'.json'
            blogData = BlogData(src)
            blogData.readFromJson()

            dst = 'data_noun_TF_relatedInfo/data_'+str(i)+'.json'

            total_term_number = len(blogData.data['dp'])

            for j in range(total_term_number):
                term = blogData.data['dp'][j]['cont']
                #term-frequency
                term_number = 0.0
                for k in range(total_term_number):
                    if term == blogData.data['dp'][k]['cont']:
                        term_number = term_number + 1
                term_frequency = term_number/total_term_number

                #inverse document frequency
                term_doc_number = 0.0
                if  not idf.has_key(term):
                    for k in xrange(corpus_size):
                        try:
                            src = 'data_noun_relatedInfo/data_'+str(k)+'.json'
                            tmpBlogData = BlogData(src)
                            tmpBlogData.readFromJson()

                            for l in range(len(tmpBlogData.data['dp'])):
                                tmpTerm = tmpBlogData.data['dp'][l]['cont']
                                if term.encode('utf8') == tmpTerm.encode('utf8') :
                                    term_doc_number = term_doc_number + 1.0
                                    break
                        except BaseException,e:
                            continue
                    inverse_document_frequency = math.log(totoal_doc_number/term_doc_number)
                    idf[term] = inverse_document_frequency
                #tf-idf
                blogData.data['dp'][j]['tf'] = term_frequency
                blogData.data['dp'][j]['idf'] = idf[term]
                blogData.data['dp'][j]['tf-idf'] = term_frequency * idf[term]
            blogData.saveData(dst)
            print 'processing %d/12832 successfully...'%i
        except BaseException,e:
            print  'processing %d/12832 fail...'%i
            continue

#从src目录下的数据中分离出relatedInfo含有名词成分的数据，并保存到dst目录
def extractNounRelatedInfoData():
    for i in xrange(12833):
        try:
            print 'processing %d/12832...'%i,
            src = 'data/data_'+str(i)+'.json'
            blogData = BlogData(src)
            blogData.readFromJson()
            dst = 'data_noun_relatedInfo/data_'+str(i)+'.json'
            if blogData.hasNounRelatedInfoData() == True:
                blogData.saveData(dst)
                print 'successfully...'
        except BaseException,e:
            print 'fail...'
            continue

#统计relatedInfo中出现的词的POS标签和DP标签的集合（标签-次数）
#用于设置POS和DP的one hot vector
def extractPOSTagAndDPTagOfRelatedInfo():
    POSTag = {}
    DPTag = {}
    for i in xrange(12833):
        try:
            if i%100 == 0 and i!=0:
                print '%d-%d have been processed'%(i-100,i-1)
            src = 'data_noun_relatedInfo/data_'+str(i)+'.json'
            blogData = BlogData(src)
            blogData.readFromJson()
            relatedInfos = blogData.data['relatedInfo']
            dps = blogData.data['dp']
            for relatedInfo in relatedInfos:
                value = relatedInfo['value']
                for dp in dps:
                    if dp['cont'] == value:
                         if POSTag.has_key(dp['pos']):
                            POSTag[dp['pos']] = POSTag[dp['pos']]+1
                         else:
                            POSTag[dp['pos']] = 1
                         if DPTag.has_key(dp['relate']):
                            DPTag[dp['relate']] = DPTag[dp['relate']] + 1
                         else:
                            DPTag[dp['relate']] = 1
            sys.stdout.write('.')
        except BaseException,e:
            sys.stdout.write('*')
            continue
    print '\nPOS Tags'
    for k in POSTag.keys():
        print k+' '+str(POSTag[k])
    print 'DP Tags'
    for k in DPTag.keys():
        print k+' '+str(DPTag[k])

#提取微博数据的特征向量
#针对每一个词的特征向量：POS特征向量+RELATE特征向量+PARENT特征向量+IDX特征+TF特征+IDF特征+TF_IDF特征+是否是关键词
#在json数据中添加一项feature
#新的json数据为：
#{
# 'content':...
# 'seg':...
#   .
#   .
#   .
#  "dp": [
#     {
#       "cont": "....",
#       "parent": 3,
#       "relate": "ATT",
#       "tf-idf": 2.0776652264768063,
#       "pos": "nt",
#       "idf": 8.310660905907225,
#       "tf": 0.25,
#       "id": 0,
#       "feature": '0 1 0 1 0 1 0 0 0 ....'
#     }
#   ]
# }
POS_vector = {
    'n':'1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ' ,
    'nh':'0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ' ,
    'ns':'0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ' ,
    'v':'0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ' ,
    'r':'0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ' ,
    'ws':'0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 ' ,
    'nz':'0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 ' ,
    'j':'0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 ' ,
    'a':'0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 ' ,
    'nt':'0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 ' ,
    'i':'0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 ' ,
    'd':'0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 ' ,
    'nl':'0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 ' ,
    'q':'0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 ' ,
    'o':'0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 ' ,
    'ni':'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 ' ,
    'b':'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 ' ,
    'e':'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 ' ,
    'c':'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 '
}
RELATE_vector = {
    'SBV':'1 0 0 0 0 0 0 0 0 ' ,
    'ATT':'0 1 0 0 0 0 0 0 0 ' ,
    'VOB':'0 0 1 0 0 0 0 0 0 ' ,
    'POB':'0 0 0 1 0 0 0 0 0 ' ,
    'COO':'0 0 0 0 1 0 0 0 0 ' ,
    'HED':'0 0 0 0 0 1 0 0 0 ' ,
    'FOB':'0 0 0 0 0 0 1 0 0 ' ,
    'ADV':'0 0 0 0 0 0 0 1 0 ' ,
    'DBL':'0 0 0 0 0 0 0 0 1 '
}
def getFeature(data):
    dp_len = len(data['dp'])
    for i in xrange(dp_len):
        features_vector = ""
        meta_data = data['dp'][i]
        #get POS feature vector
        if POS_vector.has_key(meta_data['pos']):
            features_vector += POS_vector[meta_data['pos']]
        else:
            features_vector += POS_vector[len(POS_vector) - 1]
        #get dp relate feature vector
        if RELATE_vector.has_key(meta_data['relate']):
            features_vector += RELATE_vector[meta_data['relate']]
        else:
            features_vector += RELATE_vector[len(RELATE_vector) - 1]
        #get blog length feature
        features_vector += str(dp_len)+" "
        #get idx feature
        features_vector += str(meta_data['id'])+" "
        #get position feature
        features_vector += str((meta_data['id']+1)*1.0/dp_len*1.0)+" "
        #get parent feature
        features_vector += str(meta_data['parent'])+" "
        #get parent position feature
        features_vector += str((meta_data['parent']+1)*1.0/dp_len*1.0)+" "
        #get tf,idf,tf-idf feature
        features_vector += str(meta_data['tf']) + " "
        features_vector += str(meta_data['idf']) + " "
        features_vector += str(meta_data['tf-idf'])
        data['dp'][i]['features_vector'] = features_vector

        is_keyword = 0
        for j in xrange(len(meta_data['relatedInfo'])):
            if meta_data['cont'].encode('utf-8') == meta_data['relatedInfo'][j]['value'].encode('utf-8'):
                is_keyword = 1
                break
        data['dp'][i]['is_keyword'] = is_keyword
    return data

    return data
def extractFeature():
    corpus_size = 20
    for i in xrange(corpus_size):
        try:
            src = 'data_noun_TF_relatedInfo/data_'+str(i)+'.json'
            blogData = BlogData(src)
            blogData.readFromJson()
            blogData.data = getFeature(BlogData.data)
            dst = 'data_noun_TF_relatedInfo/data_'+str(i)+'.json'
            blogData.saveData(dst)
            print 'processing %d/12832 successfully...'%i
        except BaseException,e:
            print  'processing %d/12832 fail...'%i
            continue
    return 1
