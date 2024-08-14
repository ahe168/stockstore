 

import sys
sys.path.append("..")
from   config.config_db import ConfigDb
from   dbutil import DbHandle   as mysqlh
import pandas as pd


 

def DaoUpdateStockTradeCal4DailyBasic (trade_date,spider_status,dailybasic_cnt):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])  
        try:   

            session.execute(text(""" update    stock_trade_cal   set daily_basic_spider = :daily_basic_spider, daily_basic_cnt = :daily_basic_cnt    WHERE  cal_date =:cal_date    """), 
                              params={ "daily_basic_spider": spider_status,"daily_basic_cnt":dailybasic_cnt , "cal_date": str(trade_date).replace('-','')})
            session.commit()
            session.remove()

            return 1
        except Exception as e:
            print("------------******except————————————————")
            print("error:" + str(e))