#! /usr/bin/env python2.7
# coding=utf-8

from jqdatasdk import *
from datetime import datetime, timedelta
import os


class ConbondData(object):

    def __init__(self):
        self.codes = []
        self._all_codes()

    def _all_codes(self):
        with open('jisilu.txt', 'r') as fp:
            line = fp.readline()
            while line:
                code = line.split('	')[0]
                if code:
                    self.codes.append(code)
                line = fp.readline()

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
        # df.rename(columns={"A": "a", "B": "c"})
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

    def basic_info(self, query_code: str):
        """
        CONBOND_BASIC_INFO，可转债基本资料
        """
        info_df = bond.run_query(query(bond.CONBOND_BASIC_INFO)\
            .filter(bond.CONBOND_BASIC_INFO.code == query_code))
        return info_df

    def _30_day_before(self):
        """
        计算当前往前30个交易日的起始时间， 5 * 6 相当于 6 周
        """
        today_30 = datetime.today() - timedelta(weeks=6)
        today_30_str = today_30.strftime("%Y-%m-%d")
        print(today_30_str)
        return today_30_str

    def daily_conbond_df(self, query_code):
        """
        可转债日行情，从2018-09-13开始（CONBOND_DAILY_PRICE）
        """
        today_30_str = conbond_data._30_day_before()
        df = bond.run_query(query(bond.CONBOND_DAILY_PRICE)
                .filter(bond.CONBOND_DAILY_PRICE.code == query_code, \
                    bond.CONBOND_DAILY_PRICE.date > today_30_str))
        if df.empty:
            print(query_code, ' is empty')
            return None
        df.drop(columns='id', inplace=True)
        return df

    def save_df_2_file(self, data_df):
        """
        把 dataframe 写入到本地的 csv file
        """
        path = "./conbond_folder"
        try:
            os.makedirs(path)
        except FileExistsError:
            print('csv folder already exist')
        data_df.to_csv('%s/%s.csv' % (path, datetime.today().strftime("%Y-%m-%d")), encoding='utf-8')


conbond_data = ConbondData()

if __name__ == "__main__":

    
    from wxpy import embed
    import pandas as pd

    conbond_data._login()
    
    data_df = None

    for query_code in conbond_data.codes:
        # 获取时间的数据
        df = conbond_data.daily_conbond_df(query_code)

        # rename 成中文，导出用
        close = '收盘价'
        low = '最低价'
        high = '最高价'
        pre_close = '昨收价'
        change_pct = '日涨幅'
        columns = {'date':'交易日期', 'code':'债券代码', 'name':'债券简称', \
            'exchange_code':'XSHG-上；XSHE-深）', 'pre_close':pre_close, \
                'open':'开盘价', 'high':high, 'low':low, 'close':close, \
                    'volume':'成交量（手）', 'money':'成交额', 'deal_number':'成交笔数', 'change_pct':change_pct}
        df.rename(columns=columns, inplace=True)
        
        # df.to_csv('file_name.csv', encoding='utf-8')
        # print(df.head(), query_code)

        # 溢价率啥的
        # last_third_day_str = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
        # info_df = bond.run_query(query(bond.BOND_BASIC_INFO).filter(bond.BOND_BASIC_INFO.code == query_code))
        # finance_code = info_df['company_code']
    # 1. 转股价值
    # 转股价值 = 100 / 转股价 x 正股现价
    # 2. 溢价率
    # 溢价率 =（转债现价 - 转股价值）/ 转股价值
        # info_df.drop(columns='id', inplace=True)
        # print(info_df)

        # 计算月涨幅和周涨幅
        day_last = df.loc[df.index[-1]]
        day_last_close = day_last[close]
        day_month_close = df.loc[df.index[0]][close]
        day_week_close = df.loc[df.index[-5]][close]
        day_month_raise = (day_last_close - day_month_close) / day_month_close
        day_week_raise = (day_last_close - day_week_close) / day_week_close
        
        # 计算月振幅和周振幅
        # 真实波动频率 https://zh.wikipedia.org/wiki/%E7%9C%9F%E5%AF%A6%E6%B3%A2%E5%8B%95%E5%B9%85%E5%BA%A6%E5%9D%87%E5%80%BC
        # https://www.dailyfxasia.com/cn/feaarticle/20170727-6033.html how to use atr
        # {\displaystyle TR=max(H_{t},C_{t-1})-min(L_{t},C_{t-1})}
        atr = '日波动'
        df[atr] = df.apply(lambda x: max(x[high], x[pre_close]) - min(x[low], x[pre_close]) , axis=1)
        week_atr = df.loc[df.index[-7:]][atr].mean()
        fourteenth_atr = df.loc[df.index[-14:]][atr].mean()
        month_atr = df[atr].mean()
        week_variable = df.loc[df.index[-5:]][change_pct].var()
        month_variable = df[change_pct].var()
        # 合并成一个新的 series
        today_series = df.loc[df.index[-1]]
        basic_info_df = conbond_data.basic_info(query_code)
        data = {
            '月涨幅': day_month_raise,
            '周涨幅': day_week_raise,
            '周波动': week_atr,
            '14天波动': fourteenth_atr,
            '月波动': month_atr,
            '周涨幅方差': week_variable,
            '月涨幅方差': month_variable,
            '剩余规模(万元)': '无' if basic_info_df.empty else basic_info_df['actual_raise_fund'][0]
        }
        today_series = today_series.append(pd.Series(data))

        if data_df is None:
            data_df = pd.DataFrame([today_series])
        else:
            data_df = data_df.append(today_series, ignore_index=True)

    conbond_data.save_df_2_file(data_df=data_df)
    embed()
    
    ####
    # df2 = bond.run_query(query(bond.CONBOND_DAILY_PRICE)).filter(
    #     bond.BOND_BASIC_INFO.code == '113579')
    # print(df2.head())

    ###
    # now = datetime.now() - timedelta(days=int('15'))
    # time = now.strftime("%Y-%m-%d")
    # print("time:", time)
    # print(type(('file', 'asdasdsa')))
    # s = ('file', 'asdasdsa')
    # print(isinstance(s, tuple))
    # print(s[0])

# def request_xueqiu():
#     url = 'https://xueqiu.com/S/list/search'
#     import requests
    
#     jar = requests.cookies.RequestsCookieJar()
#     domain = '.xueqiu.com'
#     jar.set('aliyungf_tc', 'AQAAAJmFoj0ZGQIAbocSG3kopE6N1p0S', domain=domain, path='/')
#     jar.set('s', 'c71av92zd7', domain=domain, path='/')
#     jar.set('u', '691591373767075', domain=domain, path='/')
#     jar.set('cookiesu', '691591373767075', domain=domain, path='/')
#     jar.set('device_id', '5647a3013166061bf3f8a65d86276e06', domain=domain, path='/')
#     jar.set('xq_a_token', 'ea139be840cf88ff8c30e6943cf26aba8ad77358', domain=domain, path='/')
#     jar.set('xq_r_token', '863970f9d67d944596be27965d13c6929b5264fe', domain=domain, path='/')
#     jar.set('xq_id_token', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5NDAwMjgwOCwiY3RtIjoxNTkyNjY2MDc4MDQxLCJjaWQiOiJkOWQwbjRBWnVwIn0.KfkGPus7aAg-VjHCbXQzEfIWi1tn7iwzufHNleApZg8MR0B6RouEAyqquDIveqh-1Tf7IAaRt3HmkVZzocoKN9KyDM5JeMI0SB7lCLqJs3ZGSLl-Jb4s1RDJAXXKG5TFktADV4MiZmTtAbFMaI9wBdqOFsIMLw-I8Lz2uEq3VnAochQc6YJY899Hl-Q4c9X5OuWHUI7vYruwSVIOJs219SXTRH2DxqL6hqX8UoLHaY2kjIJBCPneFh6QQvtthtGLuGCBIAgfK427qX_Xb-hnpYbHbRzlPyXjBcsSpW0mlEyvTGv24c7VOQZ2Vfx9pl3Ql-VSR3UMu6h7Y2gakU73UA', domain=domain, path='/')
#     jar.set('__utmc', '1', domain=domain, path='/')
#     jar.set('acw_tc', '2760823115927419847157228e2ed11d3c19289e11b765df52bfdd7f38c0ae', domain=domain, path='/')
#     jar.set('__utma', '1.1453397645.1592666103.1592666103.1592741990.2', domain=domain, path='/')
#     jar.set('__utmz', '1.1592741990.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)', domain=domain, path='/')
#     jar.set('__utmt', '1', domain=domain, path='/')
#     jar.set('__utmb', '1.3.10.1592741990', domain=domain, path='/')
#     jar.set('Hm_lvt_1db88642e346389874251b5a1eded6e3', '1592666103,1592741986,1592742039,1592742840', domain=domain, path='/')
#     jar.set('Hm_lpvt_1db88642e346389874251b5a1eded6e3', '1592742840', domain=domain, path='/')

#     r = requests.get(url, \
#         params={'ange':'CN', 'industry': '可转债', 'page': 2, 'size': 30, 'order':'desc', 'orderby': 'percent'}, cookies=jar)
#     print('xueqiu send status %s', r)
#     print('content = %s' % r.content)