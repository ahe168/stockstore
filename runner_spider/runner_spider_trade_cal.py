# -*- coding:utf-8 -*- 

import sys
sys.path.append("..")
from   dao  import dao_spider_trade_cal as  dao
from  config.config_stock_src import TushareHelper
import pandas as pd
"""
采集日历数据
"""
class RunnerTradeCal( ):

    def __init__(self ):
        self.dailyData = []
        self.dfTradeCal = pd.DataFrame()

    def run(self,start_date,end_date):
        try:
            self.dfTradeCal = TushareHelper().pro.trade_cal(exchange='',is_open='1', start_date=start_date, end_date=end_date)
            if (len(self.dfTradeCal)>0) :
                dao.DaoByYearSpiderTradeCalSave(self.dfTradeCal,start_date, end_date)
                self.is_spider = True
                return


        except Exception as e:
            print(e)
 