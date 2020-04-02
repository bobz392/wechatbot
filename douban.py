#! /usr/bin/env python2.7
# coding=utf-8

import csv
import re
import time
import os, sys
import requests
from lxml import etree

headers = {'User-Agent': 'Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/567.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/527.36'}


def index_pages(number):
    url = 'https://movie.douban.com/top250?start=%s&filter=' % number
    index_response = requests.get(url=url, headers=headers)
    tree = etree.HTML(index_response.text)
    m_urls = tree.xpath("//li/div/div/a/@href")
    return m_urls


def parse_pages(url):
    movie_pages = requests.get(url=url, headers=headers)
    parse_movie = etree.HTML(movie_pages.text)
    print(parse_movie)
    # 排名
    ranking = parse_movie.xpath("//span[@class='top250-no']/text()")

    # 电影名
    name = parse_movie.xpath("//h1/span[1]/text()")

    # 评分
    score = parse_movie.xpath("//div[@class='rating_self clearfix']/strong/text()")

    # 参评人数
    value = parse_movie.xpath("//span[@property='v:votes']/text()")
    number = [" ".join(['number:'] + value)]

    # 类型
    value = parse_movie.xpath("//span[@property='v:genre']/text()")
    types = [' '.join(['type:'] + value)]

    # 制片国家/地区
    value = re.findall('<span class="pl">制片国家/地区:</span>(.*?)<br>', movie_pages.text)
    print(value)
    country = [" ".join(['country:'] + value)]

    # 语言
    value = re.findall('<span class="pl">语言:</span>(.*?)<br>', movie_pages.text)
    # print(movie_pages.text)
    print('yuyan')
    print(value)
    language = [" ".join(['lang:'] + value)]

    # 上映时期
    value = parse_movie.xpath("//span[@property='v:initialReleaseDate']/text()")
    date = [" ".join(['date:'] + value)]

    # 片长
    value = parse_movie.xpath("//span[@property='v:runtime']/text()")
    durtaion = [" ".join(['duration:'] + value)]

    # 导演
    value = parse_movie.xpath("//div[@id='info']/span[1]/span[@class='attrs']/a/text()")
    director = [" ".join(['director:'] + value)]

    # 编剧
    value = parse_movie.xpath("//div[@id='info']/span[2]/span[@class='attrs']/a/text()")
    screenwriter = [" ".join(['screenwriter:'] + value)]

    # 主演
    value = parse_movie.xpath("//div[@id='info']/span[3]")
    performer = [value[0].xpath('string(.)')]

    # URL
    m_url = ['link:' + movie_url]

    # IMDb链接
    value = parse_movie.xpath("//div[@id='info']/a/@href")
    imdb_url = [" ".join(['IMDB link:'] + value)]

    # 保存电影海报
    # poster = parse_movie.xpath("//div[@id='mainpic']/a/img/@src")
    # response = requests.get(poster[0])
    # name2 = re.sub(r'[A-Za-z\:\s]', '', name[0])
    # poster_name = str(ranking[0]) + ' - ' + name2 + '.jpg'
    # dir_name = 'douban_poster'
    # if not os.path.exists(dir_name):
    #     os.mkdir(dir_name)
    # poster_path = dir_name + '/' + poster_name
    # with open(poster_path, "wb")as f:
    #     f.write(response.content)

    return zip(ranking, name, score, number, types, country, language, date, durtaion, director, screenwriter, performer, m_url, imdb_url)


def save_results(data):
    with open('douban.csv', 'a') as fp:
        print(data)
        writer = csv.writer(fp)
        # writer.writerow(data)
        writer.writerow([s.encode("utf-8") for s in data])


if __name__ == '__main__':
    num = 0
    for i in range(0, 250, 25):
        movie_urls = index_pages(i)
        for movie_url in movie_urls:
            results = parse_pages(movie_url)
            for result in results:
                num += 1
                save_results(result)
                print('第' + str(num) + '条电影信息保存完毕！')
                time.sleep(4)
