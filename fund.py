
from jqdatasdk import *
from wxpy import embed


class fund(object):

    def __init__(self):
        self.code = '003095'

    def query(self):
        auth('18827420512', '1397160Zb@@')
        df = finance.run_query(query(finance.FUND_MAIN_INFO).filter(
            finance.FUND_MAIN_INFO.main_code == self.code))
        pro_df = finance.run_query(query(finance.FUND_PORTFOLIO_STOCK)
                                   .filter(finance.FUND_PORTFOLIO_STOCK.code == self.code))
        embed()


if __name__ == "__main__":
    fund = fund()
    fund.query()
