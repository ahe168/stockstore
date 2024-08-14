# -*- coding:utf-8 -*-
import time
from   dao  import dao_spider_daily as  dailyDao
from   dao  import dao_spider_trade_cal as  calDao
from config.config_stock_src import TushareHelper
import pandas as pd
from   dao  import dao_adjfactor as  adjfactorDao
from   dao  import dao_comp_daily_qfq as  qfqDao


from util import logUtil

"""
采集日数据
"""
class RunnerSpiderDaily( ):

    def __init__(self ):
        self.dailyData = []
        self.hist_df = pd.DataFrame()
        self.logger = logUtil.Logger('stockstore')
 
    def runByDate(self,trade_date):
                start_time = time.time()
                self.logger.info( "采集日线数据开始")
                self.dailyData = TushareHelper().pro.daily(trade_date=str(trade_date).replace('-',''))
                if (len(self.dailyData) > 0):

                    self.dailyData["p_open"] = self.dailyData["open"]
                    self.dailyData["p_close"] = self.dailyData["close"]
                    self.dailyData["p_pre_close"] = self.dailyData["pre_close"]
                    self.dailyData["p_high"] = self.dailyData["high"]
                    self.dailyData["p_low"] = self.dailyData["low"]

                    dailyDao.DaoSaveStockDailyByDate(self.dailyData, str(trade_date).replace('-', ''))
                    calDao.DaoUpdateDailySpiderByCalDate(len(self.dailyData), str(trade_date).replace('-', ''))

                stop_time = time.time()
                self.logger.info(  "采集日线数据结束，耗时："+f'{stop_time - start_time:.4f}s')
                return 1


 
    def runAdjfactoryByDate(self,trade_date):
                start_time = time.time()
                self.logger.info(  "采集前复权日线数据开始")
                df =  adjfactorDao.DaoQueryAllAdjFactorByDailyDate(trade_date,trade_date)
                for index , row  in df.iterrows():
                        if (row["pre_adj_factor"] == row["adj_factor"]):
                            continue
                        try:
                            import tushare as ts
                            self.dailyData  = ts.pro_bar(ts_code=row["ts_code"], adj='qfq' )
                            if (len(self.dailyData) > 0):
                                qfqDao.reCompQfqByDF(self.dailyData )
                                qfqDao.runComp(trade_date )
 
                        except Exception as e:
                            self.logger.error("出现如下异常%s"%e)
                            pass
                stop_time = time.time()
                self.logger.info( "采集日线数据结束，耗时："+f'{stop_time - start_time:.4f}s')
                return 1


 

