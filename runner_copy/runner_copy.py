# -*- coding:utf-8 -*-

import sys
sys.path.append("..")
from   config.config_db import ConfigDb
from   dbutil import DbHandle   as mysqlh

from sqlalchemy import text
"""
拷贝数据，采集和计算完成后，将数据拷贝到最终成果数据库
"""
class RunnerCopy( ):

    def __init__(self,runner ):
        self.dailyData = []
        print(runner)

    def runCopyByDate(self,trade_date):
        dbtype,db_info = ConfigDb().getDbInfo()
        try:
            if dbtype == 'mysql':
                    session = mysqlh.getSession(db_info.loc[0, "user"], db_info.loc[0, "password"], db_info.loc[0, "url"],
                                                db_info.loc[0, "port"], db_info.loc[0, "database"])
                    
                      
                    session.execute(text(
                        """ update    runner_stock_trade_cal   set is_copy = :is_copy    WHERE  cal_date =:cal_date    """),
                        params={"is_copy": 1,   "cal_date": str(trade_date).replace('-', '')})

                    session.commit()
                    session.remove()
        except Exception as e:
                    print("异常错误:" + str(e))
 

