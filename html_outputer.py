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
            # fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'])
            fout.write("<td>%s</td>" % data['summary'])
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()

    def output_mysql(self):
        #2.插入操作
        db= pymysql.connect(host="localhost",user="root",
                            password="root",db="lucene",port=3306)

        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        sql = 'insert into baike (title, summary) values '
        for data in self.datas:
            # 用空字符替换字符串里面的双引号
            title=re.sub('"','',data['title'])
            summary=re.sub('"','',data['summary'])
            sql += ' ("'+title+'", "'+summary+'"),'
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
