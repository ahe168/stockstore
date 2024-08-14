 
import sys
import threading
from sqlalchemy import text

sys.path.append("..")
from   config.config_db import ConfigDb
from   dbutil import DbHandle   as mysqlh
import pandas as pd


lock = threading.Lock()
 

# 按日期采集前复权数据
def DaoSaveAdjfactorByDate(df,trade_date):
    lock.acquire()  # 线程锁定
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        try:
            print("1003.复权因子，删除"+trade_date+"数据")
            session.execute(text(""" delete  from  runner_stock_adjfactor     WHERE  trade_date =:trade_date"""),   params={ "trade_date": str(trade_date).replace('-','')})
            session.commit()
            session.remove()
            
            pd.io.sql.to_sql(df, 'runner_stock_adjfactor', con=engine, index=False, if_exists='append')
            print("1003.复权因子，入库"+trade_date+"数据")
            session.execute(text(
                """ UPDATE    runner_stock_adjfactor a ,  
        (select ts_code,max(trade_date) as max_trade_date FROM  runner_stock_adjfactor   GROUP BY ts_code   ) as b1,
        runner_stock_adjfactor b2
                             SET  a.last_adj_factor = b2.adj_factor		
                            WHERE   b1.ts_code = b2.ts_code
                            AND b1.max_trade_date =  b2.trade_date 
                            AND  b2.ts_code = a.ts_code 
                            and (a.last_adj_factor != b2.adj_factor   OR a.last_adj_factor is NULL )    """))
            session.commit()

            session.execute(text(
                """ UPDATE    runner_stock_adjfactor a ,  
        (select d.ts_code,max(d.trade_date) as pre_trade_date FROM  runner_stock_adjfactor d where d.trade_date<:trade_date    GROUP BY d.ts_code   ) as b1,
        runner_stock_adjfactor b2
                             SET  a.pre_adj_factor = b2.adj_factor		
                            WHERE   b1.ts_code = b2.ts_code
                            AND b1.pre_trade_date =  b2.trade_date 
                            AND  b2.ts_code = a.ts_code and a.trade_date=:trade_date   """),   params={ "trade_date": str(trade_date).replace('-','')})
            session.commit()
            session.remove()

            print("1003.复权因子，设置最新复权因子数据")

        except Exception as e:
            print( e)
    lock.release() # 线程解锁
    return 1

# 按日期采集前复权数据
def DaoSaveAdjfactorByDateWithPreAdjfactor(df, trade_date):
    lock.acquire() # 线程锁定
    dbtype, db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"], db_info.loc[0, "port"], db_info.loc[0, "database"])
        session = mysqlh.getSession(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"], db_info.loc[0, "port"], db_info.loc[0, "database"])
        try:
            print("1003.复权因子，删除" + trade_date + "数据")
            session.execute(text(""" delete  from  runner_stock_adjfactor     WHERE  trade_date =:trade_date"""), params={"trade_date": str(trade_date).replace('-', '')})
            session.commit()

            pd.io.sql.to_sql(df, 'runner_stock_adjfactor', con=engine, index=False, if_exists='append')
            print("1003.复权因子，入库" + trade_date + "数据")
            session.execute(text(
                """ UPDATE    runner_stock_adjfactor a ,  
        (select ts_code,max(trade_date) as max_trade_date FROM  runner_stock_adjfactor   GROUP BY ts_code   ) as b1,
        runner_stock_adjfactor b2
                             SET  a.last_adj_factor = b2.adj_factor		
                            WHERE   b1.ts_code = b2.ts_code
                            AND b1.max_trade_date =  b2.trade_date 
                            AND  b2.ts_code = a.ts_code 
                            and (a.last_adj_factor != b2.adj_factor   OR a.last_adj_factor is NULL )    """))
            session.commit()
            session.remove()

            print("1003.复权因子，设置最新复权因子数据")
        except Exception as e:
            print("error:" + str(e))
    lock.release() # 线程解锁
    return 1


# 采集完成修改日历表状态
def DaoUpdateAdjfactorByCalDate(adj_factor_cnt,trade_date):
    lock.acquire()  # 线程锁定
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        try:

            if (adj_factor_cnt>0) :
                session.execute(text(""" update    runner_stock_trade_cal   set adj_factor_spider = :adj_factor_spider, 
                                    adj_factor_cnt = :adj_factor_cnt    WHERE  cal_date =:cal_date    """),
                                params={ "adj_factor_spider": 1,"adj_factor_cnt":adj_factor_cnt , "cal_date": str(trade_date).replace('-','')})
                session.commit()
                session.remove()

        except Exception as e:
            print("error:" + str(e))
    lock.release() # 线程解锁
 
 

# 查询复权因子,用于检查是否股票因子发生变化
def DaoQueryAllAdjFactorByDailyDate(start_trade_date,end_trade_date):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        df = pd.read_sql_query( sql=r"""  SELECT  *  FROM  runner_stock_adjfactor  a  where a.trade_date>='{start_trade_date}' and  a.trade_date<='{end_trade_date}'  order by a.ts_code """
                                    .format(start_trade_date=start_trade_date,end_trade_date=end_trade_date ) , con=engine)

        return df