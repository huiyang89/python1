# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
class JdbookPipeline(object):
    def __init__(self):
        self.file = codecs.open("jd.json",'w',encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) +'\n'
        self.file.write(line)
        return item
    def spider_closed(self,spider):
        self.file.close()

from twisted.enterprise import adbapi
import pymysql
class JdbookSqlLine(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root123', db='jd',charset='utf8')

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        try:

            self.cursor.executemany(
                'insert into jd_book (book_id,title,url,keywords,description,img,channel,tag,sub_tag,value_str,comments) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                [(item["_id"],item['title'],item['url'],item['keywords'],item['description'],item['img'],item['channel'],item['tag'],item['sub_tag'],item['value'],item['comments'][0]['content'])])
        except Exception as e:
            print(e)
        finally:
            self.conn.commit()
            self.cursor.close()
        return item
    def spider_closed(self,spider):

        self.conn.close()

