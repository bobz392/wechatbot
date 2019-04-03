#! /usr/bin/env python2.7
#coding=utf-8

from selenium import webdriver
import time

class Kr:
    def __init__(self):
        self.dr = webdriver.Chrome()
        
        self.dr.get('http://36kr.com/')
        self.dr.add_cookie(cookie_dict={'name': 'new_user_guidance', 'value': True})#, 'domain': '.36kr.com', 'path': '/', 'secure': False})
        # time.sleep(1.5)
        self.dr.refresh()
        # self.dr.get('http://36kr.com/')

        # cookie = self.dr.get_cookies()
        # self.skip_guide()

    def skip_guide(self):
        # xpath_next = "/html/body/div[@class='kr-portal']/div/div[@class='page-first-wrapper']/div[@class='page-first-content']/div[@class='next']/span"
        # span_next = self.dr.find_element_by_xpath(xpath_next)
        # print(span_next)
        # span_next.click()
        self.dr.find_element_by_class_name('next').click()
        # print(guide_div)


    def loadData(self):
        feed_ul = self.dr.find_element_by_class_name('feed_ul')
        msg = u''
        i = 1
        add_count = 0
        while  i <= 30 and add_count < 10:
            try:
                xpath_head = "/html/body/div[@id='app']/div/div[@class='index_36kr']/div[@class='pagewrap']/div[@class='mainlib_flex_wapper']/div[@class=' mainlib']/div[@class='center_content']/div[@class='content-wrapper']/div[@class='list_con']/div[2]/div/div/div[@class='kr_article_list']/div/ul[@class='feed_ul']/li[" + str(i) + "]/div[@class='am-cf inner_li']/a/div[@class='intro']/h3"
                xpath_detail = "/html/body/div[@id='app']/div/div[@class='index_36kr']/div[@class='pagewrap']/div[@class='mainlib_flex_wapper']/div[@class=' mainlib']/div[@class='center_content']/div[@class='content-wrapper']/div[@class='list_con']/div[2]/div/div/div[@class='kr_article_list']/div/ul[@class='feed_ul']/li[" + str(i) + "]/div[@class='am-cf inner_li']/a/div[@class='intro']/div[@class='abstract']"
                xpath_href = "/html/body/div[@id='app']/div/div[@class='index_36kr']/div[@class='pagewrap']/div[@class='mainlib_flex_wapper']/div[@class=' mainlib']/div[@class='center_content']/div[@class='content-wrapper']/div[@class='list_con']/div[2]/div/div/div[@class='kr_article_list']/div/ul[@class='feed_ul']/li[" + str(i) + "]/div[@class='am-cf inner_li']/a"
                # xpath_img  = "//li[" + str(i) + "]/div[@class='am-cf inner_li inner_li_abtest']/a/div[@class='img_box']/div/img"
# "//li[" + str(i) + "]/div[@class='am-cf inner_li inner_li_abtest']/a/div[@class='img_box']/div"
                head  = feed_ul.find_element_by_xpath(xpath_head)
                title = head.text
                detail  = feed_ul.find_element_by_xpath(xpath_detail)

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