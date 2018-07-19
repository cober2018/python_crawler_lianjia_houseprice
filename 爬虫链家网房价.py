import requests
import time
from bs4 import BeautifulSoup

#设置列表页URL的固定部分
url='https://hz.lianjia.com/zufang/'
#设置页面页的可变部分
page=('pg')
#设置请求头部信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;wd=&amp;amp;eqid=c3435a7d00146bd600000003582bfd1f'}
#r.status_code
#r.encoding
#循环抓取列表页信息
for i in range(1,2):
    if i == 1:
        i=str(i)
        a=(url+page+i+'/')
        r=requests.get(url=a,headers=headers)
        html=r.content
    else:
        i=str(i)
        a=(url+page+i+'/')
        r=requests.get(url=a,headers=headers)
        html2=r.content
        html = html + html2
     #每次间隔1秒
    time.sleep(1)
#解析抓取的页面内容
lj=BeautifulSoup(html,'lxml')
#提取房源总价
price=lj.find_all('div','price')
tp=[]
for a in price:
    totalPrice=a.span.string
    tp.append(totalPrice)
print(tp)
# 提取房源信息
region = lj.find_all('div', 'where')

hi = []
for b in region:
    house = b.get_text()
    hi.append(house)
for item in hi:
    print (item)
# 提取房源关注度
other = lj.find_all('div', 'other')

ot = []
for c in other:
    others = c.get_text()
    ot.append(others)
for item in ot:
    print (item)
followInfo = lj.find_all('div', attrs={'class': 'square'})

fi = []
for d in followInfo:
    follow = d.get_text()
    fi.append(follow)
for item in fi:
    print (item)
#清洗数据并整理到数据表中
#导入pandas库
import pandas as pd
#创建数据表
house=pd.DataFrame({'totalprice':tp,'region':hi,'followinfo':fi,'other':ot})
#查看数据表的内容
print(house.head())
#对房源信息进行分列
region_split = pd.DataFrame((x.split( ) for x in house.region),index=house.index,columns=['xiaoqu','huxing','mianji','chaoxiang','other'])
#查看分列结果
region_split.head()
#将分列结果拼接回原数据表
house=pd.merge(house,region_split,right_index=True, left_index=True)
print(house.head())
#对房源关注度进行分列
followinfo_split = pd.DataFrame((x.split('/') for x in house.other_x),index=house.index,columns=['地址','楼层','建板楼'])
#将分列后的关注度信息拼接回原数据表
house=pd.merge(house,followinfo_split,right_index=True, left_index=True)
print(house.head())
house.drop(['other_x','region'],axis=1)