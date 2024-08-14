# -*- coding: utf-8 -*-
# 导入必要模块

import sys
sys.path.append("..")
import akshare as ak
import time
from  config.config_stock_src import TushareHelper
from   dao  import dao_spider_stockbasic as  dao
from dao import dao_spider_trade_cal as calDao
from util import logUtil

class RunerStockBasic():
    def __init__(self  ):
        self.logger = logUtil.Logger('stockstore')

    def run(self,date):
        self.logger.info( "采集基本信息开始")
        try:

            start_time = time.time()
            cal_df  = calDao.DaoQuaryBasicSpideredTradeDate(str(date))
            # 当天采集过了则返回
            if ["stock_basic_spider"][0] == 1: return
            # 没采集过用最近一天采集
            trade_date = cal_df["cal_date"][0]
            df = TushareHelper().pro.stock_basic(exchange='',
                                        fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
            dao.stockbasicSave(df,str(trade_date))
            end_time = time.time()
            self.logger.info(  "采集基本信息结束，耗时："+f'{end_time - start_time:.4f}s')
            return 1 
        except Exception as e :
            pass