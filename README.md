### 数据来源

豆瓣用户会对“读过”的书进行“很差”到“力荐”的评价，豆瓣根据每本书读过的人数以及该书所得的评价等综合数据，通过算法分析产生了豆瓣图书 Top 250。

##### 技术与工具

数据分析部分以 Python 编程语言为主，使用pandas作为数据处理和统计分析的工具，matplotlib制作图形。

##### 加载数据

df = pd.read_excel("/Users/fountain/Desktop/spider/doubanTOP250.xlsx")
df.head(）
此数据集包含的字段有name（书名）、url（书籍链接）、author（作者）、publisher（出版社）、date（出版日期）、price（价格）、rate（评分）、commentnum（评分人数）、comment（评论）。

![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/1.png)

### 数据清理

commentnum需要处理一下，剩下数字即可。
```
df["commentnum"] = df["commentnum"].str[22:-21]
```
将date字段分离，筛选出年份，以year作为一列。
```
df['year'] = df.date.str[:5]
```

![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/2.png)

查看下这些字段的基本信息：

![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/3.png)

```

# 将rate的类型转换为float64
df_clean.loc[:,'rate'] = df_clean.loc[:,'rate'].astype('float64')
df_clean
```

检查下是否已经转换成功了呢？

![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/4.png)


至此，数据清理基本完成，切选出我们需要的部分数据即可。
```
df_clean = df[['name','author','publisher','price','year','rate','comment','commentnum']]
```

![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/5.png)

### 对数据进行描述性统计

```
# 对于书籍的价格和评分，用describe函数可以快速生成各类统计指标，如平均数
# 标准差、中位数、最大值等
df_clean.describe()
```
![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/6.png)


按照publisher进行分组，求出price和rate的平均值。
```
df_clean.groupby('publisher').mean()
```
![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/7.png)

### 对数据进行探索性分析

```
df_clean.rate.hist(bins=12)
# bins参数是为了更细的粒度，将直方图的宽距缩小点
```

#### 书籍评分分布
可以看出评分在8.0-9.0之间，不愧为排名豆瓣前250的优秀书

![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/8.png)


筛选出评分在9分以上的书籍，并按评分作降序排序。
```
df_clean[df_clean.rate>=9.0].sort_values(by='rate',ascending=False)[:10]
```
![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/9.png)

#### 出版社排名

在这个TOP250中，出版的书籍数量排名前10的出版社，按从多到少排序，并计算出其评分的平均数
```
df_clean.groupby('publisher').rate.agg(['count','mean']).sort_values(by='count',ascending=False)[:10]
```
人民文学出版社位列第一，共有29本！

![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/10.png)

```
publisher_df = df_clean.groupby('publisher').rate.count().sort_values(ascending=False).head(20)
```
![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/11.png)

#### 高产作家排名
类似地，书籍数量排名前10的作者，按从多到少排序
```
author_df = df_clean.groupby('author').name.count().sort_values(ascending=False).head(20)
```
![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/12.png)

从结果看，日本作家村上春树的作品整体上很受读者的欢迎，安妮宝贝位居第二，当年明月排第三，而对于80后，90后熟知的作家韩寒、郭敬明紧随其后


#### 书籍年份分析
```
data = pd.DataFrame(df_clean.groupby(['year']).agg({'rate':'mean','name':'count'}))
```
![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/13.png)


由上图可以分析发现，TOP250豆瓣书籍中，书籍数量排名前六的年份依次为2007，2009，2006，2010，2003，2008，年份都比较集中，说明进入21世纪以来的前几年是作家们创作的好时期。

### 书籍引述词云

```
import jieba.analyse
from wordcloud import WordCloud

g = lambda x,y:x+y
m = reduce(g,df_clean['comment'])
result = jieba.analyse.textrank(m, topK=50,withWeight=True)
keywords = dict()
for i in result:
    keywords[i[0]] = i[1]
...
wc.generate_from_frequencies(keywords)
show_img(wc)
```
![image](https://github.com/Hefountain/Analysis-Project/raw/master/img/ciyun.jpg)

生活、爱情、青春、中国等几个关键词是文学创作离不开的主旋律，比如关于“生活”的就有《平凡的世界》，《老人与海》，关于“爱情”的《飘》，《霍乱时期的爱情》，《茶花女》等，关于“青春”的《致我们终将逝去的青春》，《挪威的森林》以及《麦田里的守望者》等都是我们比较熟悉的作品。
