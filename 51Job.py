# -*- coding:utf-8 -*-
import urllib.request
import pymysql
import re

#获取原码
def get_content(page):
    # 爬取51job北京本科生学历要求java岗位招聘的公司名称，岗位名称，薪资待遇等数据
    url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,java,2,'+ str(page)+'.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=04&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=7&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    a = urllib.request.urlopen(url)#打开网址
    html = a.read().decode('gbk')#读取源代码并转为unicode
    return html

def get(html):
    reg = re.compile(r'class="t1 ">.*? <a target="_blank" title="(.*?)".*? <span class="t2"><a target="_blank" title="(.*?)".*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>.*? <span class="t5">(.*?)</span>',re.S)#匹配换行符
    items=re.findall(reg,html)
    return items

db= pymysql.connect(host="localhost",user="root",
                    password="root",db="lucene",port=3306)

# 使用cursor()方法获取操作游标
cur = db.cursor()
sql = 'insert into 51java (job,company,area,money,low,hign) values '
#多页处理，保存到数据库
for  j in range(1,40):
    print("正在爬取第"+str(j)+"页数据...")
    html=get_content(j)#调用获取网页原码
    for i in get(html):
        #print(i[0],i[1],i[2],i[3],i[4])
        with open ('51job.txt','a',encoding='utf-8') as f:
            # java开发工程师20180402	北京华宇泰聚科技有限公司	北京-海淀区	1-1.5万/月
            job = i[0]
            company = i[1]
            area = i[2]
            money = i[3]
            # 根据不同的薪资构成转化成月薪,单位为元
            if '万/月' in money:
                submoney = re.sub('万/月','',money)
                moneyArray = submoney.split('-')
                low = str(int(float(moneyArray[0])*10000))
                hign = str(int(float(moneyArray[1])*10000))
                sql += ' ("'+job+'", "'+company+'", "'+area+'", "'+money+'", "'+low+'", "'+hign+'"),'
            elif '万/年' in money:
                submoney = re.sub('万/年','',money)
                moneyArray = submoney.split('-')
                low = str(int((float(moneyArray[0])*10000)/12))
                hign = str(int((float(moneyArray[1])*10000)/12))
                sql += ' ("'+job+'", "'+company+'", "'+area+'", "'+money+'", "'+low+'", "'+hign+'"),'
            elif '千/月' in money:
                submoney = re.sub('千/月','',money)
                moneyArray = submoney.split('-')
                low = str(int(float(moneyArray[0])*1000))
                hign = str(int(float(moneyArray[1])*1000))
                sql += ' ("'+job+'", "'+company+'", "'+area+'", "'+money+'", "'+low+'", "'+hign+'"),'
            else:
                print(money)
#去除sql尾部的,
sql = sql[:-1]
print(sql)
try:
    cur.execute(sql)
    #提交
    db.commit()
except Exception as e:
    #错误回滚
    db.rollback()
    print(e)
finally:
    db.close()
