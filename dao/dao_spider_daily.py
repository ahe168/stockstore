 

import sys

from sqlalchemy import text

sys.path.append("..")
from   config.config_db import ConfigDb
from   dbutil import DbHandle   as mysqlh
import pandas as pd
 
def DaoSaveStockDailyByDate(df,trade_date):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])

        session.execute(text(""" delete  from  runner_stock_daily     WHERE  trade_date =:trade_date"""),   params={ "trade_date": str(trade_date).replace('-','')})
        session.commit()
        session.remove()

        pd.io.sql.to_sql(df, 'runner_stock_daily', con=engine, index=False, if_exists='append')
        session.execute(text(""" delete FROM  runner_stock_daily_index    WHERE  trade_date =:trade_date  """),    params={ "trade_date": str(trade_date).replace('-','')})
        session.commit()
        session.remove()
        pd.io.sql.to_sql(df[["ts_code","trade_date"]], 'runner_stock_daily_index', con=engine, index=False, if_exists='append')

        return 1
 

def DaoUpdateStockTradeCal4Daily (trade_date,spider_status,daily_cnt):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])  
        try:   

            session.execute(text(""" update    stock_trade_cal   set daily_spider = :daily_spider, daily_cnt = :daily_cnt    WHERE  cal_date =:cal_date    """),   params={ "daily_spider": spider_status,"daily_cnt":daily_cnt , "cal_date": str(trade_date).replace('-','')})
            session.commit()
            session.remove()

            return 1
        except Exception as e:
            print("error:" + str(e))