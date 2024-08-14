# -*- coding:utf-8 -*-
from   dao  import dao_spider_dailybasic as  dailyBasicDao
from config.config_stock_src import TushareHelper
import pandas as pd
"""
采集每日指标数据
"""
class RunnerSpiderDailyBasic( ):

    def __init__(self ):
        self.dailyData = []
    def runByDate(self,trade_date):
            try:
                self.dailyBasicData = TushareHelper().pro.daily_basic(trade_date=str(trade_date) )
                if (len(self.dailyData)>0) :
                    dailyBasicDao.DaoSaveStockDailyBasicByDate(self.dailyBasicData,str(trade_date) )
                    dailyBasicDao.DaoUpdateStockTradeCal4DailyBasic(str(trade_date),1,len(self.dailyBasicData) )
            except Exception as e:
                print("error:" + str(e))

 



