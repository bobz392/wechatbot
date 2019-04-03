#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import os
import bs4
from bs4 import BeautifulSoup
from random import randint
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


cached_b_zhan_meizi = []


class BeautyFucker(object):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    mziTu = 'http://www.mzitu.com/'

    bzhan = 'https://api.vc.bilibili.com/link_draw/v2/Photo/list'
    # 'https://api.vc.bilibili.com/link_draw/v2/Doc/index'

    def downloadBeauty(self, page_num):

        res_sub = requests.get(page_num, headers=self.headers)
        soup_sub = BeautifulSoup(res_sub.text, 'html.parser')
        all_post = soup_sub.find('div', class_='postlist') \
            .find_all('a', target='_blank')

        choice_index = randint(0, len(all_post))
        href = all_post[choice_index].attrs['href']
        res_sub_1 = requests.get(href, headers=self.headers)
        soup_sub_1 = BeautifulSoup(res_sub_1.text, 'html.parser')

        try:
            pic_max = soup_sub_1.find('div', class_='pagenavi') \
                .find_all('span')[6].text
            choice_page = randint(1, int(pic_max) + 1)
            href_sub = href + "/" + str(choice_page)
            print('choice sub href %s' % href_sub)
            res_sub_2 = requests.get(href_sub, headers=self.headers)
            soup_sub_2 = BeautifulSoup(res_sub_2.text, "html.parser")
            img = soup_sub_2.find('div', class_='main-image').find('img')

            if isinstance(img, bs4.element.Tag):
                # 提取src
                url = img.attrs['src']
                array = url.split('/')
                # 防盗链加入Referer
                headers = {'Referer': href}
                img = requests.get(url, headers=headers)
                return img.content
        except Exception as e:
            print(e)
            return None

    def prepare_page(self):
        res = requests.get(self.mziTu, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        image_page_count = soup.find('div', class_='nav-links') \
            .find_all('a')[3].text
        choice_page = randint(1, int(image_page_count) + 1)
        if choice_page == 1:
            page = self.mziTu
        else:
            page = self.mziTu + 'page/' + str(image_page_count)

        return self.downloadBeauty(page)

    def get_b_fun_image(self):
        if not cached_b_zhan_meizi:
            self.get_b_fun_list()

        choice_page = randint(0, len(cached_b_zhan_meizi) - 1)
        print(choice_page, len(cached_b_zhan_meizi))
        img = requests.get(
            cached_b_zhan_meizi.pop(choice_page), headers=self.headers)

        return img.content

    def get_b_fun_list(self):
        page_size = 45
        page_num = randint(0, 6)
        params = {
            'category': 'cos',
            'type': 'hot',
            'page_num': page_num,
            'page_size': page_size,
        }
        r = requests.get(url=self.bzhan, params=params, headers=self.headers)
        # print(r, r.text)
        html = r.text
        decodejson = json.loads(html)
        c = decodejson.get("data").get("items")
        i = 0
        while i < len(c):
            item = c[i].get("item")
            # title = item.get("title")
            pictures_url = item.get("pictures")[0].get("img_src")
            cached_b_zhan_meizi.append(pictures_url)
            i += 1
            if i > page_size:
                break


if __name__ == "__main__":
    b = BeautyFucker()
    b.get_b_fun_image()
