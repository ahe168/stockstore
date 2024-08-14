 

import sys
import datetime
import os
import time

from sqlalchemy import text

from dao import dao_comp_weekly_qfq

sys.path.append("..")
from   config.config_db import ConfigDb
from   dbutil import DbHandle   as mysqlh
import pandas as pd
import numpy as np

import runner_compute.runner_com_indexs  as idx
 
def runByCode( ts_code):

    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        # print('1、采集日行情数据...')
        begin = datetime.datetime.now()
        df = pd.read_sql_query(sql=r"""  SELECT d.ts_code,d.symbol,d.trade_date,d.`p_close`,d.p_high,d.p_low  
                            FROM runner_stock_weekly d   ,    runner_stock_trade_cal c ,runner_stock_weekly_index i
                             WHERE c.cal_date = d.trade_date and i.trade_date = d.trade_date and i.ts_code = d.ts_code and d.trade_date > '20220101' and 
                               c.weekly_qfq_compute=1 and    d.ts_code='%s'  order by d.trade_date    """ % (ts_code), con=engine)
        
        if (len(df)==0): return  
        df = idx.Qh_Target_MA(df, qh_close="p_close", qh_timeperiod=5)
        df = idx.Qh_Target_EMA(df, qh_close="p_close", qh_timeperiod=20)
        df = idx.Qh_Target_MACD(df, qh_close="p_close", qh_fastperiod=12, qh_slowperiod=26, qh_signalperiod=9)
        df = idx.Qh_Target_BOLL(df, qh_close="p_close", qh_timeperiod=20, qh_nbdev=2)
        # qh_df_stock = Qh_Target_KDJ(qh_df_stock, qh_hig="最高价", qh_low="最低价", qh_close="收盘价", qh_fastk=9, qh_slowk=3, qh_slowd=3)
        df = idx.Qh_Target_KDJ_CN(df, qh_hig="p_high", qh_low="p_low", qh_close="p_close", qh_fastk_period=9,
                                  qh_slowk_period=3, qh_fastd_period=3)

        df['bar'] = df['DIFF_26'] - df['DEA_26']
        df = df.replace(np.nan, -10000)

        runUpdateWeekly(df)
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 信息 正在计算周线" + ts_code + "数据...")

def runByCode2( ts_code):

    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        # print('1、采集日行情数据...')
        start_time = time.time()

        df = pd.read_sql_query(sql=r"""  SELECT w.ts_code,w.symbol,w.trade_date,w.`p_close`,w.p_high,w.p_low 
                                        FROM runner_stock_weekly w   ,    runner_stock_trade_cal c  
        																WHERE c.cal_date = w.trade_date 
        																and  w.`p_close` is not null 
        																and    w.ts_code='%s' order by w.trade_date    """ % (ts_code), con=engine)
        if (len(df)==0): return
        df.sort_values("trade_date", inplace=True, ascending=True)

        df = idx.Qh_Target_MA(df, qh_close="p_close", qh_timeperiod=5)
        df = idx.Qh_Target_EMA(df, qh_close="p_close", qh_timeperiod=20)
        df = idx.Qh_Target_MACD(df, qh_close="p_close", qh_fastperiod=12, qh_slowperiod=26, qh_signalperiod=9)
        df = idx.Qh_Target_BOLL(df, qh_close="p_close", qh_timeperiod=20, qh_nbdev=2)
        # qh_df_stock = Qh_Target_KDJ(qh_df_stock, qh_hig="最高价", qh_low="最低价", qh_close="收盘价", qh_fastk=9, qh_slowk=3, qh_slowd=3)
        df = idx.Qh_Target_KDJ_CN(df, qh_hig="p_high", qh_low="p_low", qh_close="p_close", qh_fastk_period=9,
                                  qh_slowk_period=3, qh_fastd_period=3)

        df['BAR'] = df['DIFF_26'] - df['DEA_26']
        df = df.replace(np.nan, -10000)
        print(df)
        df = df[["ts_code","trade_date","MA_5","EMA_20","DIFF_26","DEA_26","MACD_26","UPPER_20","MID_2","LOWER_2","QH_K_9","QH_D_9","QH_J_9","BAR"]]

        # self.dailyQfqData.rename(columns={"open": "p_open", "close": "p_close", "high": "p_high", "low": "p_low", "pre_close": "p_pre_close"}, inplace=True)

        df.rename(columns={"MA_5": "MA5", "EMA_20": "EMA20", "DIFF_26": "DIFF", "DEA_26": "DEA", "MACD_26": "MACD", "UPPER_20": "UPPER20",
                                "MID_2": "MID2", "LOWER_2": "LOWER2", "QH_K_9": "QHK9", "QH_D_9": "QHD9", "QH_J_9": "QHJ9" }, inplace=True)
        print(df)
        # runUpdateDaily(df)
        runSaveWeekly(df,ts_code)
        stop_time = time.time()
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "采集日线数据结束，耗时："+f'{stop_time - start_time:.4f}s')
def runByByDate( ts_code, trade_date):

    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 信息 正在计算周线"+ts_code+"数据...")
        begin = datetime.datetime.now()
        df = pd.read_sql_query(sql=r"""  SELECT d.ts_code,d.symbol,d.trade_date,d.`p_close`,d.p_high,d.p_low  
                            FROM runner_stock_weekly d   ,    runner_stock_trade_cal c ,runner_stock_weekly_index i
                             WHERE c.cal_date = d.trade_date and i.trade_date = d.trade_date and i.ts_code = d.ts_code and 
                                   d.ts_code='{ts_code}' and d.trade_date <='{trade_date}' order by d.trade_date desc limit 100"""
                               .format(trade_date=str(trade_date).replace('-', ''),ts_code=ts_code), con=engine)
        # print(df)

        df.sort_values("trade_date", inplace=True, ascending=True)


        df = idx.Qh_Target_MA(df, qh_close="p_close", qh_timeperiod=5)
        df = idx.Qh_Target_EMA(df, qh_close="p_close", qh_timeperiod=20)
        df = idx.Qh_Target_MACD(df, qh_close="p_close", qh_fastperiod=12, qh_slowperiod=26, qh_signalperiod=9)
        df = idx.Qh_Target_BOLL(df, qh_close="p_close", qh_timeperiod=20, qh_nbdev=2)
        # qh_df_stock = Qh_Target_KDJ(qh_df_stock, qh_hig="最高价", qh_low="最低价", qh_close="收盘价", qh_fastk=9, qh_slowk=3, qh_slowd=3)
        df = idx.Qh_Target_KDJ_CN(df, qh_hig="p_high", qh_low="p_low", qh_close="p_close", qh_fastk_period=9,
                                  qh_slowk_period=3, qh_fastd_period=3)

        df['bar'] = df['DIFF_26'] - df['DEA_26']

        df = df.where(df['trade_date'] == trade_date)
        df = df[~(df['trade_date'].isnull())]  # 删掉空行
        # print(df)
        df = df.replace(np.nan, -10000)
        # print(df)
        runUpdateWeekly(df)

        end = datetime.datetime.now()
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 信息 正在计算周线" + ts_code + "数据...")

def runUpdateWeekly( df):
    dbtype,db_info = ConfigDb().getDbInfo()
    try:
        if dbtype == 'mysql':
            engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
            session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
            # print(df)
            # try:
            for  index , row  in df.iterrows():

                sql = """ UPDATE runner_stock_weekly_index d  set 
                               ma5=:MA_5,     ema20=:EMA_20,   diff=:DIFF_26,    dea=:DEA_26,   macd=:MACD_26,   upper20=:UPPER_20,   
                                mid2=:MID_2,    lower2=:LOWER_2,      qhk9=:QH_K_9,      qhd9 =:QH_D_9,     qhj9=:QH_J_9,bar=:bar
                                
                               where 2=2 and ts_code=:ts_code and trade_date=:trade_date     """
                session.execute(text(sql), params={"ts_code": row['ts_code'], "trade_date": str( row['trade_date']).replace('-', '')
                    , 'MA_5':  row['MA_5'], 'EMA_20': row['EMA_20'], 'DIFF_26':  row['DIFF_26'], 'DEA_26':  row['DEA_26'], 'MACD_26': row['MACD_26'],'UPPER_20':  row['UPPER_20']
                    , 'MID_2':  row['MID_2'], 'LOWER_2':  row['LOWER_2'], 'QH_K_9':  row['QH_K_9'], 'QH_D_9':  row['QH_D_9'], 'QH_J_9':  row['QH_J_9'],'bar':  row['bar']
                    
                                                }
                                   )
                if index % 500 == 0 :    session.commit()

            session.commit()
            session.remove()

    except Exception as e:
        print("error:" + str(e))



# 104 保存日线计算指标
def runSaveWeekly( df,ts_code):
    dbtype,db_info = ConfigDb().getDbInfo()
    try:
        if dbtype == 'mysql':
            engine = mysqlh.getEngine(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"], db_info.loc[0, "port"], db_info.loc[0, "database"])
            session = mysqlh.getSession(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"], db_info.loc[0, "port"], db_info.loc[0, "database"])

            session.execute(text(""" delete FROM  runner_stock_weekly_index    WHERE  ts_code =:ts_code  """), params={"ts_code": ts_code})
            session.commit()
            pd.io.sql.to_sql(df , 'runner_stock_weekly_index', con=engine, index=False, if_exists='append')
            session.commit()
            session.close()

    except Exception as e:
        print("------------******except————————————————")
        print("error:" + str(e))

 


def runCompWeeklyCommonsByDate(trade_date):
    qh_path = os.path.abspath(os.path.join(os.getcwd(), ".."))  
    sys.path.append(qh_path)   
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor(max_workers=40)   

    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        # 按交易日更新
        df1 = pd.read_sql_query(sql=r""" SELECT cal_date  FROM runner_stock_trade_cal c  WHERE    c.cal_date ='{trade_date}'
                                              ORDER BY  cal_date ASC 
                                      """. format(trade_date=str(trade_date).replace('-', '')), con=engine)

        for index1, row1 in df1.iterrows():
            df2 = pd.read_sql_query(
                sql=r""" SELECT *  FROM  runner_stock_weekly d  WHERE   d.trade_date = '%s'   order by ts_code   """ % (row1['cal_date']),
                con=engine)
            df3 = pd.read_sql_query(
                sql=r""" SELECT DISTINCT trade_date, ts_code FROM runner_stock_adjfactor a,    runner_stock_trade_cal c  
                                    WHERE c.cal_date = a.trade_date and    
                                    a.adj_factor !=a.pre_adj_factor and a.last_adj_factor is not null and a.pre_adj_factor AND
            								(   a.trade_date >=  ( SELECT MAX(trade_date) FROM runner_stock_weekly WHERE   trade_date < '{trade_date}' ))     order by a.ts_code  """.
                    format(trade_date=str(trade_date).replace('-', '')), con=engine)

            tasks = pool.map(runByByDate, df2['ts_code'], df2['trade_date'])
            for data in tasks:
                pass

            tasks = pool.map(runByCode, df3['ts_code'])
            #
            for data in tasks:
                pass


            session.execute(text(
                """ update    runner_stock_trade_cal   set weekly_compute = :weekly_compute      WHERE  cal_date =:cal_date    """),
                params={"weekly_compute": 1,   "cal_date": str(row1['cal_date']).replace('-', '')})
            session.commit()
            session.remove()


            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "---因复权因子发生变化的数据计算结束")

