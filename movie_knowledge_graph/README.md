# 学习从github上的一个知识图谱项目

# 爬虫

## 百度百科爬虫

该爬虫对应与crawl 下的baidu_baike 文件夹。该爬虫基于scrapy框架，爬取电影类数据，包含电影22219部，演员13967人，演员电影间联系1942个，电影与类别间联系23238,其中类别为‘其他’的电影有10个。对应数据集可在[坚果云下载](https://www.jianguoyun.com/p/Dfga9AgQq_6CBxiw8Go)

### mysql建库
* 演员 ：爬取内容为 ID, 简介， 中文名，外文名，国籍，星座，出生地，出生日期，代表作品，主要成就，经纪公司；  
* 电影 ：ID，简介，中文名，外文名，出品时间，出品公司，导演，编剧，类型，主演，片长，上映时间，对白语言，主要成就；  
* 电影类型： 爱情，喜剧，动作，剧情，科幻，恐怖，动画，惊悚，犯罪，冒险，其他； 
* 演员->电影： 演员ID， 电影ID； 
* 电影-> 类型： 电影ID， 类型ID；

与其相对应的建表语句即要求请参考craw_without_spider/mysql/creat_sql.txt文件。 在修改目标库的名称后即可通过
```
mysql -uroot -pnlp < creat_sql.txt
```
创建数据库。

### 运行爬虫
直接运行 scrapy crawl baidu 即可

## 互动百科爬虫 

该爬虫对应与crawl 下的hudong_baike 文件夹。该爬虫基于scrapy框架，爬取电影类数据，包含电影13866部，演员5931人，演员电影间联系800个，电影与类别间联系14558,其中类别为‘其他’的电影有0个。对应数据集可在[坚果云下载](https://www.jianguoyun.com/p/Db3wsKQQq_6CBxi7tGs)

数据库的结构和百度百科的一致，也可通过creat_sql.txt 文件创建。    

通过 scrapy crawl hudong 运行爬虫。

## craw_without_spider

百科数据爬取爬虫，用于提取半结构化实体文本。该爬虫未使用scrapy框架.用于提取目标是百度百科里面的演员和电影。


### 运行爬虫程序
爬虫程序可爬取演员和电影两类，其中：  
* 爬取演员：python craw.py actor 
* 爬取电影：python craw.py movie 
用户应先爬取电影，这样在爬取演员时才可以建立演员->电影表。

## 微信公众号爬虫
微信公众号爬虫对应的文件夹是weixin_spider，该项目采用MYSQL作为存储数据库，pymysql接口。

### 运行程序

* 建立数据库： 建立数据库的命令放在creat_mysql.txt文件内，所以直接运行 mysql -u[username] -p[passwd] < creat_mysql.txt 建立数据库和表; 
* 运行爬虫: 爬虫名字是weixin，因此直接运行scrapy crawl weixin;  

## 虎嗅网爬虫
虎嗅网爬虫放在 news_spider 目录下，采用的是文件存储方式，爬取下来的新闻存放在news 目录下。

### 运行程序

直接运行 scrapy crawl huxiu 即可。

# 结构化数据到 RDF

结构化数据到RDF由两种主要方式，一个是通过[direct mapping](https://www.w3.org/TR/rdb-direct-mapping/)，另一个通过[R2RML](https://www.w3.org/TR/r2rml/#acknowledgements)语言这种，基于R2RML语言的方式更为灵活，定制性强。对于R2RML有一些好用的工具，此处我们使用d2rq工具，它基于R2RML-KIT。

## 基于D2RQ的结构化到RDF
运行struct_to_rdf 下的 get_ttl.sh 脚本生成 mapping 文件和 最终的 RDF 文件。
fuseki_conf.ttl
是启动jena-fuseki服务的配置文件,该文件里面配置了:本体文件的路径ontology.ttl，OWL推理机owl,规则推理机rules.ttl

ontology.owl
通过protege软件构建的本体ontology.owl文件,通过本体进行推理。

rules.ttl
规则文件，用于基于规则的推理。

1. 分步操作如下：
去jena-fuseki官网下载，并进入jena-fuseki服务,并启动数据库时
其中 fuseki_conf.ttl是数据库jena-fuseki server配置文件，配置TDB路径，推理引擎，本体文件路径，规则文件路径，
```bash
cd ~/Public/apache-jena-fuseki-3.9.0/
fuseki-server --config fuseki_conf.ttl
```
登录apache-jena-fuseki
```bash
http://localhost:3030/
```
如果在启动jena-fuseki服务之前没有建立数据库，也就是没有构建fuseki_conf.ttl，可以在manage datasets中添加数据库

2. 生成mapping文件
```bash
./generate-mapping -o movie.ttl -d com.mysql.jdbc.Driver -u root -p 123 jdbc:mysql://localhost:3306/kg_demo_movie
```
通过mapping 文件 和数据库，就可以使用 ./d2r-server movie.ttl开启查询端口进行查询了。

3. 通过mapping文件生成RDF文件movie.nt
```bash
./dump-rdf -o movie.nt movie.ttl
```

## NTriples to TDB
TDB 是Jena 用于存储RDF的组件，是属于存储层面的技术。在单机情况下，它能够提供非常高的RDF存储性能。在下载完apache-jena 后，运行 ./tdbloader --loc="../tdb/" "path/to/NTriples" 把 NTriples 加载到TDB中。

## Apache jena fuseki 的运行

在Apache Jena fuseki 服务器的配置文件中，可以指定本体，从而实现推理机制。该本体文件是从顶向下定义的，采用protege 软件编辑生成，格式为Turtle，放在struct_to_rdf/kg_movie_tultle.owl。该配置文件中另一个需要修改的是TDB 文件夹的路径，改成上面TDB 文件夹路径即可。

需要注意的是，每次运行fuseki服务器后，会在TDB文件夹内生成一些以prefix*开头的文件，重新运行fuseki服务的话不删除它们可能会报错。

## Apache jena SPARQL endpoint

Jena fuseki开启服务后，可以通过网页端和命令行方式进行 SPQRQL查询。接下来我们可以直接进行SPARQL查询，也可以把自然语言转换为 SPARQL 模板后进行查询。


# KBQA
## data文件夹
kg_demo_movie.sql：创建数据库、表，插入所有数据的sql文件。用户可以直接使用sql文件导入数据到mysql中。

### KBQA文件夹
-  "external_dict"包含的是人名和电影名两个外部词典,用于导入jieba进行分词用的。csv文件是从mysql-workbench导出的，按照jieba外部词典的格式，我们将csv转为对应的txt。
-  "word_tagging"，定义Word类的结构（即我们在REfO中使用的对象）；定义"Tagger"类来初始化词典，并实现自然语言到Word对象的方法。
-  "jena\_sparql_endpoint"，用于完成与Fuseki的交互。
-  "question2sparql"，将自然语言转为对应的SPARQL查询。
-  "question_temp"，定义SPARQL模板和匹配规则。
-  "query\_main"，main函数。在运行"query_main"之前，读者需要启动Fuseki服务。


# 非结构化文本的知识抽取
## 基于Deepdive的知识抽取

Deepdive是由斯坦福大学InfoLab实验室开发的一个开源知识抽取系统。它通过弱监督学习，从非结构化的文本中抽取结构化的关系数
据 。本次实战基于OpenKG上的[支持中文的deepdive：斯坦福大学的开源知识抽取工具（三元组抽取）](http://www.openkg.cn/    dataset/cn-deepdive)，我们基于此，抽取电影领域的演员-电影关系。

详细介绍请见[从零开始构建知识图谱（五）Deepdive抽取演员-电影间关系](https://zhuanlan.zhihu.com/p/46560845)


# 语义搜索
## 基于elasticsearch 的简单语义搜索
本项目是对浙大的[ 基于elasticsearch的KBQA实现及示例 ](http://openkg.cn/tool/elasticsearch-kbqa)的简化版本，并在自己的数据库上做了实现。
### 代码结构
文档结构为：    
.:    
data  query.py  utils    
./data:    
actor.json  all_entity.txt  attr_ac.pkl  attr_mapping.txt  baidu_baike.json  __init__.py  movie.json  total_val.txt    
./utils:    
build_dict.py  get_ac_attr.py  get_json.py  get_total_val.py  __init__.py  insert.py  query_cmd.sh  views.py    

其中data/文件夹 下的数据可以在[data数据](https://www.jianguoyun.com/p/DZVXpjwQq_6CBxjN5G0)下载。

utils/ 下为程序核心文件:
* get_ac_attr.py 用来得到属性的AC自动机文件-attr_ac.pkl    
* get_json.py 用来得到actor.json 和 movie.json文件，将二者去重合一后得到baidu_baike.json.    
* insert.py将数据插入到elasticsearch中。    
* build_dict.py 将上面产生的文件加载进来    
* query_cmd.sh 是一个在shell 终端输入的查询样例。我们的目标就是把自然语言转化为这种格式，才能查询得到答案。    
* view.py为核心文件，将输入的自然语言问题转化为逻辑表达式再到查询模板后进行查询得到答案。

### 示例
<p align="center">
<img src="img/example_elastic_ss.png">
<br/> 基于elasticsearch的简单语义搜索
</p> 

# PLAN:
* 增加基于sceapy框架的百度百科、互动百科、豆瓣三个网站的爬虫，获取半结构化信息    
* 根据zhishi.me建立的文章，使用属性传播等算法建立三个独立的知识图谱    
* 使用知识融合技术，对以上三个知识图谱进行内部融合和互相间融合    
* 对微信公众号、虎嗅网新闻的非结构化文本进行知识抽取，并与上面获得的知识图谱进行融合    
* 基于知识图谱建立语义搜索系统   
* 基于知识图谱建立知识问答系统    
* ....
