# SinaBlogTextMining
新浪微博文本图像相关性研究

**t_mweibo.json**

从数据库导出的原始数据

**data.json**

对t_mweibo.json进行预处理，增加了dp和filteredContent两个字段

**data目录**

把data.json中的每条数据单独保存在该目录一个json文件中

**data_noun_relatedInfo目录**

从data目录中抽取出relatedInfo含有名词成分的数据

**data_noun_TF_relatedInfo目录**

根据data_noun_relatedInfo目录中的数据，计算每个词的TF-IDF数据，增加了tf，idf，tf-idf三个字段

**error.txt**

存储preProcess.py中使用LTP-cloud遇到异常的数据id

**pos_tags_and_dp_tags.txt**

存储BlogData.py中统计的relatedInfo中名词成分可能出现的POS和DP标签，有了这些标签，可以在特征向量中添加一系列ont-hot值

**preProcess.py**

数据预处理（除杂/依存句法分析）

**BlogData.py**

对预处理后的数据进行进一步处理（统计/提取特征等）

**README.md**

说明文档