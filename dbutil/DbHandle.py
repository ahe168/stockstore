import os
import sys

os.chdir(sys.path[0])
sys.path.append("../")
# print(sys.path)
# print(sys.path[0])

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session
from   config.config_db import ConfigDb
import pandas as pd
# # 初始化数据库连接，使用pymysql模块

def getEngine(user = None, password=None, host= None,port=3306,database=None):
    db_info = {'user': user, 'password': password, 'host': host,  'port': int(port), 'database': database}
    engine = create_engine(
            "mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8"% db_info,
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=500,  # 连接池大小
            pool_timeout=50,  # 池中没有线程最多等待的时间，否则报错
            pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
            echo=True# True 输出sql到控制台
        )
    return engine

def getSession(user = None, password=None, host= None,port=3306,database=None):
    engine = getEngine(user, password, host,port,database)
    SessionFactory = sessionmaker(bind=engine)
    session = scoped_session(SessionFactory)
    return session
 
def getDataService(serviceName=None,params: dict=None ):
    try:
        dbtype,db_info = ConfigDb().getDbInfo()
        # print(db_info)
        if dbtype != 'mysql': 
            print('不是mysql') 
            return
        engine = getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        # session = getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])
        # 获取SQL语句
        df = pd.read_sql_query(
                    sql=r""" SELECT SQL_BODY FROM  conf_sql s where s.valid_flag = 1 and sql_code='{sql_code}' limit 1 """.
                        format(sql_code=serviceName), con=engine)
        if len(df)==0: 
            print('没有配置此服务') 
            return
        sql = df['SQL_BODY'][0]
        sql = sql.format(**params)
        df = pd.read_sql_query(  sql=text(sql), con=engine)
        return df 
    except Exception as e:
        print(e)
    return None
 
if __name__ == '__main__':
   df =  getDataService('get_daily_starttrade_endtrade_code',{'ts_code':'000001.SZ'})
   print(df)