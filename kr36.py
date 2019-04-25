#! /usr/bin/env python2.7
# coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


class Kr:
    def __init__(self):
        print('init')
        # chrome_options.add_argument("user-data-dir=selenium")
        self.dr = webdriver.Chrome()
        print(self.dr)
        self.dr.get('http://36kr.com/')

        # self.dr.get('http://36kr.com/')

        # cookie = self.dr.get_cookies()
        # print(cookie)

        # self.dr.add_cookie(
        #     cookie_dict={'name': 'new_user_guidance', 'value': True,
        #                  'domain': '.36kr.com', 'path': '/'})

        # time.sleep(1.5)
        # self.dr.refresh()
        WebDriverWait(self.dr, 15)
        self.skip_guide()

    def skip_guide(self):
        xpath_next = "/html/body/div[@class='kr-portal']/div/div[@class='page-first-wrapper']/div[@class='page-first-content']/div[@class='next']/span"
        span_next = self.dr.find_element_by_xpath(xpath_next)
        span_next.click()

        xpath_close = "/html/body/div[@class='kr-portal']/div/div[@class='page-second-wrapper']/div[@class='page-second-content']/div[@class='close']/span"
        span_close = self.dr.find_element_by_xpath(xpath_close)
        span_close.click()
        print('close guide')

    def loadData(self):
        print('start load data')
        feed_ul = self.dr.find_element_by_class_name('kr-home-flow-list')
        msg = u''
        i = 1
        add_count = 0
        while i <= 30 and add_count < 10:
            try:
                xpath_head = "/html/body/div[@id='app']/div[@class='kr-layout']/div[@class='kr-layout-main clearfloat']/div[@class='main-right']/div[@class='kr-layout-content']/div[@class='kr-home']/div[@class='kr-home-main clearfloat']/div[@class='kr-home-flow']/div[@class='kr-home-flow-list']/div[@class='kr-home-flow-item'][" + str(
                    i) + "]/div[@class='kr-flow-article-item']/div[@class='kr-shadow-wrapper']/div[@class='kr-shadow-content']/div[@class='article-item-info clearfloat']/p[@class='feed-title-wrapper ellipsis-2']/a[@class='article-item-title weight-bold']"

                xpath_detail = "/html/body/div[@id='app']/div[@class='kr-layout']/div[@class='kr-layout-main clearfloat']/div[@class='main-right']/div[@class='kr-layout-content']/div[@class='kr-home']/div[@class='kr-home-main clearfloat']/div[@class='kr-home-flow']/div[@class='kr-home-flow-list']/div[@class='kr-home-flow-item'][ " + str(
                    + i) + "]/div[@class='kr-flow-article-item']/div[@class='kr-shadow-wrapper']/div[@class='kr-shadow-content']/div[@class='article-item-info clearfloat']/a[@class='article-item-description ellipsis-2']"

                xpath_href = "/html/body/div[@id='app']/div[@class='kr-layout']/div[@class='kr-layout-main clearfloat']/div[@class='main-right']/div[@class='kr-layout-content']/div[@class='kr-home']/div[@class='kr-home-main clearfloat']/div[@class='kr-home-flow']/div[@class='kr-home-flow-list']/div[@class='kr-home-flow-item'][" + str(
                    i) + "]/div[@class='kr-flow-article-item']/div[@class='kr-shadow-wrapper']/div[@class='kr-shadow-content']/a[@class='article-item-pic']"

                # xpath_img  = "//li[" + str(i) + "]/div[@class='am-cf inner_li inner_li_abtest']/a/div[@class='img_box']/div/img"
# "//li[" + str(i) + "]/div[@class='am-cf inner_li inner_li_abtest']/a/div[@class='img_box']/div"
                head = feed_ul.find_element_by_xpath(xpath_head)
                title = head.text
                detail = feed_ul.find_element_by_xpath(xpath_detail)

                href = feed_ul.find_element_by_xpath(xpath_href)
                href_link = href.get_attribute('href')
                # print("herf %s" % href.get_attribute('href'))
                # url   = 'http://36kr.com' + href.get_attribute('href')

                # img   = feed_ul.find_element_by_xpath(xpath_img)
                # src   = img.get_attribute('src')

                # t = 1
                # while t <= 3:
                #     if src == None:
                #         self.dr.execute_script('window.scrollBy(0,200)')
                #         time.sleep(3)
                #         src = img.get_attribute('src')
                #         t += 1
                #     else:
                #         break

            except Exception as e:
                print('error:%s' % e)
            else:
                add_count += 1
                msg += self.saveData(add_count, title, detail.text, href_link)

            i += 1
        self.quit()
        return msg

    def saveData(self, index, title, detail=None, src=None):
        return u'%d、%s\n%s\n%s \n\n' % (index, title, detail, src)

    def quit(self):
        self.dr.quit()
