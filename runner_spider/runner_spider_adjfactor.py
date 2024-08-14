# -*- coding:utf-8 -*-
import time
from   dao  import dao_adjfactor as  adjfactorDao
from config.config_stock_src import TushareHelper
import pandas as pd
from   dbutil import DbHandle   as mysqlh
from   dao  import dao_spider_trade_cal as  calDao
from util import logUtil
"""
*复权因子数据采集
"""
class RunnerSpiderAdjfactor( ):

    def __init__(self):
        self.adjfactorData = []
        self.daily_df  = pd.DataFrame()
        self.logger = logUtil.Logger('stockstore')

    def runByDate(self, trade_date,daily_spider):

            start_time = time.time()
            self.logger.info( "采集复权因子开始") 

            self.fqyz_df = TushareHelper().pro.adj_factor(trade_date=str(trade_date).replace('-', ''))
            if (len(self.fqyz_df) > 0):
                pre_date = calDao.DaoQuaryPreTradeDate(trade_date=str(trade_date).replace('-', ''))
                if (pre_date != None):
                    fqyz_pre_df = TushareHelper().pro.adj_factor(trade_date=str(pre_date).replace('-', ''))
                    self.fqyz_df["pre_adj_factor"] = self.fqyz_df["adj_factor"]
                    self.fqyz_df.set_index('ts_code', inplace=True)
                    fqyz_pre_df.set_index('ts_code', inplace=True)
                    self.fqyz_df["pre_adj_factor"].update(fqyz_pre_df["adj_factor"])
                    self.fqyz_df.reset_index(inplace=True)
                else:
                    self.fqyz_df["pre_adj_factor"] = self.fqyz_df["adj_factor"]

                self.fqyz_df["symbol"] = self.fqyz_df["ts_code"].replace(".SZ", "", regex=True).replace(".SH", "", regex=True).replace(".BJ", "", regex=True)
                adjfactorDao.DaoSaveAdjfactorByDateWithPreAdjfactor(self.fqyz_df, str(trade_date).replace('-', ''))
                adjfactorDao.DaoUpdateAdjfactorByCalDate(len(self.fqyz_df), str(trade_date).replace('-', ''))
            stop_time = time.time()
            self.logger.info("采集复权因子结束，耗时："+f'{stop_time - start_time:.4f}s')
            return 1
 

 

 