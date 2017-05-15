# -*- coding:utf-8 -*-
"""基本工具类"""
from ssdb import SSDB

import time
import sys
import re

reload(sys)
sys.setdefaultencoding("utf-8")

"""字符转码"""
def Gbk2Utf8(content):
    try:
        newContent = content.decode("GBK", "ignore").encode("utf-8", "ignore")
    except Exception as e:
        print e.message
        newContent = ""
    finally:
        return newContent

"""文件保存"""
def save(page, des):
    try:
        fo = open(des, 'w')
        fo.write(page)
    except Exception as e:
        print e.message
    finally:
        fo.close()

    print "save successfully"

"""获取当前时间戳"""
def getTimeAsStr():
    curr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return curr

"""从数据库中获取所有可用的代理IP"""
def getIP():
    client = SSDB(host='10.141.5.89', port=8884)
    keyword = "proxy"
    res = client.get(keyword)

    addr_list = list()
    ip_port_list = res.split(",")[0:-2]
    """拆分出IP和Port"""
    for ip_port in ip_port_list:
        ip, port = re.split("\s+", ip_port)
        addr_list.append(ip+":"+port)

    print "addr parse successful"
    return addr_list

"""读取keyword文件"""
def readKeyword(filepath):
    fp = open(filepath)
    lines = list()

    line = fp.readline().strip()
    while line:
        lines.append(line)
        line = fp.readline().strip()

    fp.close()
    return lines

if __name__ == '__main__':
    print getTimeAsStr()
    print getIP()
    print readKeyword("D:\\develop\\pycharm\\workspace\\ProTest\\src1\\keyword.txt")