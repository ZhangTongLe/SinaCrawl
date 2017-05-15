# -*- coding:utf-8 -*-
import sys, time
import urllib

from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')

"""表单登录到新浪微博"""
class Sina:
    """构造方法，通过driver构造类的对象"""
    def __init__(self, DRIVER, USER_NAME="", PASS_WORD=""):
        self.username = USER_NAME
        self.password = PASS_WORD
        self.driver = DRIVER

    """登录到新浪微博，从手机端入口登录"""
    def login(self, n=3):
        try:
            self.driver.get("https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F")  # 获取url指定的登录页面
            time.sleep(2)

            self.driver.find_element_by_id('loginName').send_keys(self.username)
            self.driver.find_element_by_id('loginPassword').send_keys(self.password)
            self.driver.find_element_by_id('loginAction').click()
            time.sleep(2)
        except Exception as e:
            if n > 0:
                self.login(n-1)
            else:
                print e.message
                raise e #若登录失败，则程序停止
        else:
            print "cookie", self.driver.get_cookies()
            print "login successfully"

    """登录到新浪微博，从通用页面登录，两种方式二选一即可"""
    def login2(self, n=3):
        try:
            self.driver.get("https://login.sina.com.cn/signup/signin.php")
            time.sleep(5)

            userName = self.driver.find_element_by_id("username")
            passWord = self.driver.find_element_by_id("password")
            submit = self.driver.find_element_by_xpath("//*[@id='vForm']/div[2]/div/ul/li[7]/div[1]/input")
            userName.clear()
            userName.send_keys(self.username)
            passWord.clear()
            passWord.send_keys(self.password)
            submit.click()
            time.sleep(2)
        except Exception as e:
            if n > 0:
                self.login2(n-1)
            else:
                print e.message
                raise e
        else:
            print "cookie", self.driver.get_cookies()
            print "login successfully"

    """访问搜索页面，根据关键字获取信息"""
    def search(self, key, n=2):
        self.driver.get("http://s.weibo.com/")      # 跳转到微博搜索页面
        print "正在搜索关键字：", key
        key = urllib.quote(key)                                  # 对字符进行编码

        try:
            self.driver.find_element_by_class_name("searchInp_form").send_keys(key)
            self.driver.find_element_by_class_name("searchBtn").click()
        except Exception as e:
            if n>0:
                self.search(key, n-1)
            else:
                print e.message
                raise e       #若搜索失败，则程序停止
        else:
            time.sleep(5)
            print "search completed"

    """获取当前页面的评论按钮，并依次点击"""
    def commentClick(self, n=2):
        btns = list()
        try:
            btns = self.driver.find_elements_by_xpath("//ul[@class='feed_action_info feed_action_row4']/li[3]/a")
        except Exception as e:
            if n>0:
                self.commentClick(n-1)
            else:   #若评论按钮获取失败，则跳过
                pass
        finally:
            for btn in btns:
                btn.click()

    """提取信息"""
    def extract(self):
        self.commentClick()     #先对评论按钮进行单击

        """获取并遍历每个微博块"""
        block_list=list()
        blocks = self.driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']")
        index = 0
        for block in blocks:
            block_dict = {'name': '', 'content': '', 'point': '', 'comment_list':list()}
            try:
                name = block.find_element_by_xpath(".//a[@class='W_texta W_fb']")
                content = block.find_element_by_xpath(".//p[@class='comment_txt']")
                point = block.find_element_by_xpath(".//div[@class='feed_from W_textb']/a")
            except Exception as e:
                print "-----------content parse error -----------"
                print e.message
            else:
                """对元素内容进行输出"""
                name = name.text.strip()
                content = content.text.strip()  #提取该部分内容时需要进行URL解码，解码方法见quary.py文件
                point = point.text.strip()
                index += 1
                print "+++++++++++++++ block", index
                print "name: ", name
                print "content: ", content
                print "point: ", point
                block_dict['name'] = name                # 博文用户昵称
                block_dict['content'] = content         # 微博正文
                block_dict['point'] = point                  #  脚注信息，包含博文发布日期

            """抓取评论部分"""
            try:
                comments = block.find_elements_by_xpath(".//div[@class='list_ul']/*/dd/div[@class='WB_text']")
            except Exception as e:
                print "-------- comment parse error -----------"
                print e.message
            else:
                comment_list = list()
                for comment in comments:
                    print "comment: ", comment.text
                    comment_list.append(comment.text)
                block_dict['comment_list'] = comment_list

            block_list.append(block_dict)

        return block_list

    """翻页"""
    def nextPage(self, n=4):
        try:
            btn = self.driver.find_element_by_xpath("//div[@class='W_pages']/a[@class='page next S_txt1 S_line1']")
            btn.click()
        except Exception as e:
            if n>0:
                time.sleep(2)
                self.nextPage(n-1)
            else:
                return False
        else:
            time.sleep(5)
            print "翻页一次"
            return True

if __name__ == '__main__':
    driver = webdriver.PhantomJS()
    driver.maximize_window()

    sina = Sina(driver)     # 类的实例化
    sina.login()                  # 登录到微博，两种登录入口二选一
    sina.search("宜信")  # 搜索关键字

    block_list = sina.extract()             # 提取信息，并打印输入到控制台
    sina.nextPage()                            #  翻页一次
    print "---------------------------------------------"
    block_list.extend(sina.extract())  #  提取翻页后的信息