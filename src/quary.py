# -*- coding:utf-8 -*-
from ssdb import SSDB
import sys, urllib
import json

reload(sys)
sys.setdefaultencoding('utf-8')

"""url编码解码测试"""
def code():
    origin = "潘珊"
    coded = urllib.quote(origin)
    decoded = urllib.unquote(coded)

    print coded
    print decoded

"""查询数据库"""
def quary():
    keyword = "weibo_拾笔不良_2017-05-08"

    try:
        client = SSDB(host='', port=8884)    #连接到服务器的SSDB数据库
        res = client.get(keyword)
    except Exception as e:
        print e.message
        results = []
    else:
        results = json.loads(res)
    finally:
        print len(results)

    for block in results:
        print "++++++++++++++"
        print "name:", block['name']
        " *** 重要 *** "
        print "content:", urllib.unquote(str(block['content'])) #首先将结果转换为字符串，然后对字符串进行url解码
        print "point:", block['point']

        comment_list = block['comment_list']
        for comment in comment_list:
            print "comment:", comment

if __name__ == '__main__':
    quary()