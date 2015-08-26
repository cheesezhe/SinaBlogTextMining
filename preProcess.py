#!/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = 'ZhangHe'
import json,re,urllib2,urllib,sys,socket,httplib
#preProcess类用于处理从数据库导出的json数据
class preProcess:
    #Initialization
    #file_path is the path of json data file
    def __init__(self,file_path):
        self.data        = {}
        self.file_path   = file_path
        self.data_length = 0

    #read data from original corpus
    def readData(self):
        with open(self.file_path, 'r') as f:
            self.data = json.load(f)
        self.data = self.data['RECORDS']
        self.data_length = len(self.data)

    #print data
    #cnt is the amount of printed data
    def printData(self,cnt=-1):
        if cnt == -1:
            cnt = self.data_length
        for i in xrange(cnt):
            print self.data[i]['content']

    #filter data
    #用于对数据进行过滤，提取content的原文，保存在json的filteredContent字段中
    def filterData(self):
        contentPattern = '转发了 .*? 的微博:(.*?)原图 赞'.decode('utf-8')
        noPrePattern   = '(.*?)原图 赞'.decode('utf-8')
        pattern        = re.compile(contentPattern)
        noPrePattern   = re.compile(noPrePattern)

        cnt = self.data_length
        # cnt = 10
        for i in xrange(cnt):
            print 'preProcessing %d/%d...'%(i,cnt)
            content = self.data[i]['content']
            if content.startswith('转发了'.decode('utf-8')):
                content = re.findall(pattern,content)
            else:
                content = re.findall(noPrePattern,content)
            if len(content)!=0:
                self.data[i]['filteredContent'] = content[0].strip()
            else:
                self.data[i]['filteredContent'] = ''

            d = {}
            d['content']=self.data[i]['content'].encode('utf-8')
            self.data[i]['filteredContent'] = re.sub(r'http://t\.cn/\w{6,7}',"URL",self.data[i]['filteredContent'])

            pp = '（分享自 .*?）|\[组图共\d张\]'.decode('utf-8')
            pp = re.compile(pp)
            self.data[i]['filteredContent'] = re.sub(pp,"",self.data[i]['filteredContent'])

            d['filteredContent']=self.data[i]['filteredContent'].encode('utf-8')
            if hasattr(self.data[i]['seg'],'encode'):
                d['seg'] = self.data[i]['seg'].encode('utf-8')
            else:
                d['seg'] = None
            if hasattr(self.data[i]['relatedInfo'],'encode'):
                d['relatedInfo'] = self.data[i]['relatedInfo'].encode('utf-8')
            else:
                d['relatedInfo'] = None
            self.data[i] = d

    #process data by LTP-cloud
    #使用LTP语言云处理数据，得到每条数据的依存句法分析结果，保存在json的dp字段中
    #因为LTP语言云是通过在线接口调用的，所以会出现各种异常
    #异常的处理方式：发生异常就跳过，把出现问题的数据id保存在error.txt中，当所有数据处理完，再单独处理一下error.txt中的数据。
    def processData(self):
        uri_base = "http://ltpapi.voicecloud.cn/analysis/?"
        api_key  = "7132G4z1HE3SYMFjSAPvDSxtNcmA1jScSE5XumAI"
        format   = "json"
        pattern  = "dp"
        cnt = self.data_length

        for i in xrange(cnt):
            print 'processing %d/%d...'%(i,cnt)
            text     = self.data[i]['filteredContent']
            text     = urllib.quote(text)
            url      = (uri_base
                   + "api_key=" + api_key + "&"
                   + "text="    + text    + "&"
                   + "format="  + format  + "&"
                   + "pattern=" + pattern)
            try:
                response = urllib2.urlopen(url)
                content  = response.read().strip()
                self.data[i]['dp'] = eval(content)[0][0]
                self.saveOneData(self.data[i],i)
            except urllib2.HTTPError, e:
                with open('error.txt','a+') as f:
                    f.write(str(i)+'\n')
            except urllib2.URLError, e:
                with open('error.txt','a+') as f:
                    f.write(str(i)+'\n')
            except socket.timeout,e :
                with open('error.txt','a+') as f:
                    f.write(str(i)+'\n')
            except httplib.BadStatusLine,e:
                with open('error.txt','a+') as f:
                    f.write(str(i)+'\n')
            except httplib.IncompleteRead,e:
                with open('error.txt','a+') as f:
                    f.write(str(i)+'\n')
            except BaseException,e:
                with open('error.txt','a+') as f:
                    f.write(str(i)+'\n')

    #save all data in data.json file
    #保存全部的数据（把所有数据保存在一个json文件中）
    def saveData(self):
        with open('data.json', 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    #save one data
    #保存单个数据（把每一条数据单独保存在一个json文件中）
    def saveOneData(self,data,idx):
        with open('data/data_'+str(idx)+'.json','w') as f:
            json.dump(data,f,indent=2,ensure_ascii=False)

pre = preProcess('t_mweibo.json')
pre.readData()
pre.filterData()
pre.processData()
pre.saveData()
print 'Done'