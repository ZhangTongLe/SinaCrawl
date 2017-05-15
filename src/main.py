# -*- coding:utf-8 -*-
import tools
import random
import json
import time

from sina import Sina
from ssdb import SSDB
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from threadpool import ThreadPool, makeRequests
"""方法调用入口"""


"""按单个关键字搜索"""
def process(keyword):
    addr_list = tools.getIP()
    addr = addr_list[random.randint(0, len(addr_list)-1)]       # 随机选择一个代理IP
    """代理设置"""
    proxy = Proxy(
        {
            'proxy_type': ProxyType.MANUAL,
            'http_proxy': addr
        }
    )
    desired_capabilities = webdriver.DesiredCapabilities.PHANTOMJS
    proxy.add_to_capabilities(desired_capabilities)

    """1) 构造driver对象，并设置窗口尺寸"""
    driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
    driver.maximize_window()

    """2) 通过driver对象，实例化Sina类"""
    sina = Sina(DRIVER=driver)

    """3) 实现登录，两种登录方式二选一"""
    sina.login2()
    # sina.login()

    """4) 搜索"""
    sina.search(keyword)

    """连接到SSDB数据库"""
    client = SSDB(host='', port=8884)

    """获取结果集"""
    results = list()
    page = 1
    while len(results) < 100:   #至少返回100条数据
        print "+++++++++++++++++++++++++++++++++++++++", "page", page
        block_list = sina.extract()
        results.extend(block_list)

        page += 1

        if sina.nextPage():
            continue
        else:
            break

    key = "weibo_"+keyword+"_"+tools.getTimeAsStr()
    value = json.dumps(results)
    client.set(key, value)

    print "ssdb save", key, len(results)

"""关键字搜索的多线程实现"""
def multiThread(poolSize):
    keyword_list = tools.readKeyword("/home/panshan/keywords.txt")      #  获取关键字
    # keyword_list = tools.readKeyword('D:\develop\pycharm\workspace\ProTest\src1\keyword.txt')
    pool = ThreadPool(poolSize)     #  设置线程池
    requests = makeRequests(process, keyword_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()

if __name__ == '__main__':
    start = time.time()
    multiThread(2)
    end = time.time()
    print "任务完成，耗时：", end - start, "s"