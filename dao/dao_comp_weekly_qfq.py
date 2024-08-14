 

import sys
import time
from sqlalchemy import text

sys.path.append("..")
from   config.config_db import ConfigDb
from   dbutil import DbHandle   as mysqlh
import pandas as pd

 

 
# 对复权因子发生变化的重新计算
def reCompQfqByDate( trade_date):
    # print("前复权计算")
    dbtype, db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"],db_info.loc[0, "port"], db_info.loc[0, "database"])
        session = mysqlh.getSession(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"],db_info.loc[0, "port"], db_info.loc[0, "database"])
    df = pd.read_sql_query(
        sql=r""" SELECT distinct ts_code FROM runner_stock_adjfactor a
                 WHERE  a.adj_factor !=a.pre_adj_factor and a.last_adj_factor is not null 
                 and a.pre_adj_factor is not null  AND ( a.trade_date > (SELECT max(cal_date) ts_code FROM runner_stock_trade_cal  where weekly_spider = 1 and cal_date <{trade_date})
                   and  a.trade_date <={trade_date} ) """.
        format(trade_date=str(trade_date).replace('-', '')),con=engine)
    if len(df) == 0:
        return

    for tup in zip(df['ts_code']):
        ts_codes = tup[0]
        sql = text(""" UPDATE runner_stock_weekly w ,runner_stock_adjfactor a 
                        SET
                        p_high = (w.high * a.adj_factor) /a.last_adj_factor ,
                        p_low = (w.low * a.adj_factor) /a.last_adj_factor ,
                        p_close = (w.close * a.adj_factor) /a.last_adj_factor ,
                        p_open =   (w.open * a.adj_factor) /a.last_adj_factor ,
                        p_pre_close =   (w.pre_close * a.adj_factor) /a.last_adj_factor 
                        where     w.ts_code=a.ts_code and w.trade_date = a.trade_date 
                        AND      w.ts_code =:ts_code  and a.last_adj_factor !=0   """)
                       
        session.execute(sql,   params={ "ts_code":ts_codes})
        session.commit()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 信息 重新计算日线前复权"+ts_codes+"数据...")






# 计算日线前复权数据
def runComp( trade_date):
    dbtype, db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        session = mysqlh.getSession(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"], db_info.loc[0, "port"], db_info.loc[0, "database"])
        # 计算当天前复权
        # # 对复权因子发生变化的重新计算 

        session.execute(
            text(""" update    runner_stock_trade_cal   set weekly_qfq_compute = 1    WHERE  cal_date =:cal_date    """),
            params={"cal_date": str(trade_date).replace('-', '')})
        session.commit()
        session.remove()

