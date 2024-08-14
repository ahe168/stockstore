# -*- coding:utf-8 -*-
import time
from   dao  import dao_spider_weekly as  weeklyDao
from config.config_stock_src import TushareHelper
from  dao    import  dao_comp_weekly_qfq as qfqDao
import pandas as pd
from util import logUtil
 
"""
采集周线数据
"""
class RunnerSpiderWeekly( ):
    def __init__(self ):
        self.logger = logUtil.Logger('stockstore')
        self.weeklyData = []
        self.stock_num = 0
        self.hist_df = pd.DataFrame() 
    def runByDate(self,trade_date):
                start_time = time.time()
                self.logger.info( "采集周线数据开始")
                try:
                    self.weeklyData = TushareHelper().pro.weekly(trade_date=str(trade_date).replace('-',''))
                    self.weeklyData["p_open"] = self.weeklyData["open"]
                    self.weeklyData["p_close"] = self.weeklyData["close"]
                    self.weeklyData["p_pre_close"] = self.weeklyData["pre_close"]
                    self.weeklyData["p_high"] = self.weeklyData["high"]
                    self.weeklyData["p_low"] = self.weeklyData["low"]
                except Exception as e :
                    print("error：", str(e))
                if (len(self.weeklyData)>0) :
                    weeklyDao.DaoSaveStockWeeklyByDate(self.weeklyData,str(trade_date).replace('-',''))
                    weeklyDao.DaoUpdateStockTradeCal4Weekly(str(trade_date).replace('-',''),1,self.weeklyData.shape[0])
                stop_time = time.time()
                self.logger.info( "采集周线数据结束，耗时："+f'{stop_time - start_time:.4f}s')

                return 1


  

