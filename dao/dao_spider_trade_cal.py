 

import sys


from sqlalchemy import text

sys.path.append("..")
from   config.config_db import ConfigDb
from   dbutil import DbHandle   as mysqlh
import pandas as pd
 
    
def DaoByYearSpiderTradeCalSave(df,startDate,endDate):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        session = mysqlh.getSession(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"],
                                    db_info.loc[0, "port"], db_info.loc[0, "database"])
        if (len(df) > 0):
            for index,row in df.iterrows():
                
                df2 = pd.read_sql_query(sql=r""" SELECT * FROM runner_stock_trade_cal WHERE cal_date ='{cal_date}'  """.format(cal_date = row["cal_date"]), con=engine)
                if len(df2)>0 :continue 
                if "exchange" in row.keys() : exchange =  row["exchange"] 
                else : exchange =  ""
                if "cal_date" in row.keys() : cal_date =  row["cal_date"] 
                else : cal_date =  ""
                if "is_open" in row.keys() : is_open =  row["is_open"] 
                else : is_open =  "" 

                session.execute(text( """ INSERT INTO runner_stock_trade_cal 
                                    (`exchange`,`cal_date`,`is_open` )
                                    values(
                                        :exchange,:cal_date,:is_open  ) """), params={ "exchange": exchange,"cal_date":cal_date , "is_open": is_open  })
                session.commit() 

  
            return 1

 

def DaoQueryCalDateByTradeDate(trade_date):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        try:
            cals = pd.read_sql_query( sql=r"""  SELECT * FROM  runner_stock_trade_cal WHERE   cal_date='{cal_date}'   """.
                                        format(cal_date=str(trade_date)) ,  con=engine)
            return cals

        except Exception as e:
            print("error:" + str(e))

def DaoQueryCalDateByLast4AnyTradeDate():
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        try:
            cals = pd.read_sql_query( sql=r"""  SELECT * FROM  runner_stock_trade_cal WHERE is_open='1' and is_copy='0'  order by cal_date asc     """
                                          ,  con=engine)
            return cals

        except Exception as e:
            print("error:" + str(e))

def DaoQueryCalDateByLastTradeDate(trade_date):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        try:
            cals = pd.read_sql_query( sql=r"""  SELECT * FROM  runner_stock_trade_cal WHERE is_open='1' and     cal_date<='{cal_date}' order by cal_date desc  limit 1   """.
                                        format(cal_date=str(trade_date)) ,  con=engine)
            return cals

        except Exception as e:
            print("error:" + str(e))

def DaoUpdateDailySpiderByCalDate(daily_cnt,trade_date):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        try:

            if (daily_cnt>0) :
                session.execute(text(""" update    runner_stock_trade_cal   set daily_spider = :daily_spider, daily_cnt = :daily_cnt    WHERE  cal_date =:cal_date    """),   params={ "daily_spider": 1,"daily_cnt":daily_cnt , "cal_date": str(trade_date).replace('-','')})
                session.commit()
                session.remove()

        except Exception as e:
            print("error:" + str(e))

def DaoQuaryPreTradeDate(trade_date):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        try:
            df = pd.read_sql_query( sql=r"""  SELECT max(cal_date) as cal_date FROM  runner_stock_trade_cal WHERE   cal_date < '{cal_date}'   """.
                                        format(cal_date=str(trade_date)) ,  con=engine)
            return df["cal_date"][0]

        except Exception as e:
            print("error:" + str(e))



def DaoQuaryBasicSpideredTradeDate(trade_date):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        try:
            df = pd.read_sql_query( sql=r"""  SELECT  cal_date,stock_basic_spider FROM  runner_stock_trade_cal WHERE  is_open='1' and   cal_date <= '{cal_date}' order by cal_date desc   limit 1  """.
                                        format(cal_date=str(trade_date)) ,  con=engine)
            return df

        except Exception as e:
            print("error:" + str(e))

 