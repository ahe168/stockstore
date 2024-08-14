 

import sys

from sqlalchemy import text

sys.path.append("..")
from   config.config_db import ConfigDb
from   dbutil import DbHandle   as mysqlh
import pandas as pd
 
def DaoSaveStockDailyBasicByDate(df,trade_date):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        # try:
        session.execute(""" delete FROM  runner_stock_daily_basic    WHERE  trade_date =:trade_date  """,   params={ "trade_date": trade_date})
        session.commit()
        session.remove()
        pd.io.sql.to_sql(df, 'runner_stock_daily_basic', con=engine, index=False, if_exists='append')

        return 1