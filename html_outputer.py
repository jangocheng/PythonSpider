import pymysql
import re
import datetime
class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = open('output.html', 'w', encoding="utf-8")

        fout.write("<html>")
        fout.write("<head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"></head>")
        fout.write("<body>")
        fout.write("<table>")

        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['title'])
            fout.write("<td>%s</td>" % data['summary'])
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()

    # 爬取的记录插入到mysql中
    def output_mysql(self):
        db= pymysql.connect(host="localhost",user="root",
                            password="root",db="lucene",port=3306)

        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        sql = 'insert into baike (title, summary) values '
        #拼接sql，批量插入，提高访问数据库效率
        for data in self.datas:
            # 用空字符替换字符串里面的双引号，解决拼接插入sql语句“出错的问题
            title=re.sub('"','',data['title'])
            summary=re.sub('"','',data['summary'])
            sql += ' ("'+title+'", "'+summary+'"),'
        #去除sql尾部的,
        sql = sql[:-1]
        print(sql)
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
            endTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(nowTime)
            print(endTime)
