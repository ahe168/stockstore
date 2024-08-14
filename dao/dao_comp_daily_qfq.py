 

import sys

from sqlalchemy import text

sys.path.append("..")
from   config.config_db import ConfigDb
from   dbutil import DbHandle   as mysqlh
import pandas as pd

import time
 
 

# 对复权因子发生变化的重新计算
def reCompQfqByDF( df):
    # print("前复权计算")
    dbtype, db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"],db_info.loc[0, "port"], db_info.loc[0, "database"])
        session = mysqlh.getSession(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"],db_info.loc[0, "port"], db_info.loc[0, "database"])
 
    if (df==None or len(df) )== 0:
        return

    for index , row  in df.iterrows():
        sql = text(""" UPDATE runner_stock_daily d  
                        SET
                        p_high = :p_high ,
                        p_low =:p_low  ,
                        p_close = :p_close  ,
                        p_open =  :p_open  ,
                        p_pre_close =  :p_pre_close 
                        where     d.ts_code =:ts_code  and  d.trade_date =:trade_date    """)
        
        session.execute(sql,   params={ "p_high":row["high"], "p_low":row["low"],
                                        "p_close":row["close"], "p_open":row["open"], "p_pre_close":row["pre_close"],
                                         "ts_code":row["ts_code"], "trade_date":row["trade_date"]})
        session.commit()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 信息 重新计算日线前复权"+row["ts_code"]+"数据...")

 
 


# 对复权因子发生变化的重新计算
def reCompQfqByDate( trade_date):
    # print("前复权计算")
    dbtype, db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"],db_info.loc[0, "port"], db_info.loc[0, "database"])
        session = mysqlh.getSession(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"],db_info.loc[0, "port"], db_info.loc[0, "database"])
    df = pd.read_sql_query(
        sql=r""" SELECT distinct ts_code FROM runner_stock_adjfactor a WHERE  a.adj_factor !=a.pre_adj_factor and a.last_adj_factor is not null and a.pre_adj_factor AND a.trade_date ={trade_date} """.
        format(trade_date=str(trade_date).replace('-', '')),con=engine)
    if len(df) == 0:
        return 

    for tup in zip(df['ts_code']):
        ts_codes = tup[0]
        sql = text(""" UPDATE runner_stock_daily d ,runner_stock_adjfactor a 
                        SET
                        p_high = (d.high * a.adj_factor) /a.last_adj_factor ,
                        p_low = (d.low * a.adj_factor) /a.last_adj_factor ,
                        p_close = (d.close * a.adj_factor) /a.last_adj_factor ,
                        p_open =   (d.open * a.adj_factor) /a.last_adj_factor ,
                        p_pre_close =   (d.pre_close * a.adj_factor) /a.last_adj_factor 
                        where     d.ts_code=a.ts_code and d.trade_date = a.trade_date 
                        AND      d.ts_code =:ts_code  and a.last_adj_factor !=0   """)
                       
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
            text(""" update    runner_stock_trade_cal   set daily_qfq_compute = 1    WHERE  cal_date =:cal_date    """),
            params={"daily_qfq_compute": 1, "cal_date": str(trade_date).replace('-', '')})
        session.commit()
        session.remove()



 
