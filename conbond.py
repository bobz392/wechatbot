#! /usr/bin/env python2.7
# coding=utf-8

from jqdatasdk import *
from datetime import datetime, timedelta
import os


class ConbondData(object):

    def _login(self):
        auth('18827420512', '1397160Zb@@')

    def daily_price(self, code, start_date):
        """
        code: 代表查询可转债的内容
        start date: 格式是 YYYY-MM-dd
        """
        self._login()
        df = bond.run_query(query(bond.CONBOND_DAILY_PRICE)
                            .filter(bond.CONBOND_DAILY_PRICE.code == code)
                            .filter(bond.CONBOND_DAILY_PRICE.date > start_date))
        file_path = '%s/csv/%s_%s.csv' % (os.getcwd(), code, start_date)
        if os.path.exists(file_path):
            os.remove(file_path)
        print(file_path)
        df.to_csv(file_path, encoding='utf-8')
        logout()
        return file_path

    def _date_before(self, days):
        """
        day：计算多少天之前的日期 string
        return: YYYY-mm-dd 格式的 string
        """
        now = datetime.now() - timedelta(days=days)
        print(now, now.strftime("%Y-%m-%d"))
        return now.strftime("%Y-%m-%d")

    def daily_before_price(self, code, days_before):
        """
        计算几天之前的日期的数据
        """
        date = self._date_before(days=int(days_before))
        print('out daily_before_price: %s' % date)
        return self.daily_price(code, date)


conbond_data = ConbondData()

if __name__ == "__main__":

    # auth('18827420512', '1397160Zb@@')

    # df = bond.run_query(query(bond.CONBOND_DAILY_PRICE).filter(
    #     bond.CONBOND_DAILY_PRICE.code == '128086')
    #     .filter(bond.CONBOND_DAILY_PRICE.date > '2020-03-01'))
    # df.to_csv('file_name.csv', encoding='utf-8')
    # print(df)

    ####
    # df2 = bond.run_query(query(bond.CONBOND_DAILY_PRICE)).filter(
    #     bond.BOND_BASIC_INFO.code == '113579')
    # print(df2.head())

    ###
    now = datetime.now() - timedelta(days=int('15'))
    time = now.strftime("%Y-%m-%d")
    print("time:", time)
    print(type(('file', 'asdasdsa')))
    s = ('file', 'asdasdsa')
    print(isinstance(s, tuple))
    print(s[0])
