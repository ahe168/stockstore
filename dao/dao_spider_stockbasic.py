 

import sys

from sqlalchemy import text

sys.path.append("..")
from   config.config_db import ConfigDb
from   dbutil import DbHandle   as mysqlh
import pandas as pd
from tqdm import tqdm

def stockbasicSave(df,trade_date):
    dbtype,db_info = ConfigDb().getDbInfo()
    if dbtype == 'mysql':
        engine = mysqlh.getEngine(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"]) 
        session = mysqlh.getSession(db_info.loc[0,"user"],db_info.loc[0,"password"],db_info.loc[0,"url"],db_info.loc[0,"port"],db_info.loc[0,"database"])  
    
        if (len(df) > 500):
            
            for index , row  in tqdm(df.iterrows()):
                df2 = pd.read_sql_query(sql=r""" SELECT * FROM runner_stock_basic WHERE symbol ='{symbol}' LIMIT 1 """.format(symbol = row["symbol"]), con=engine)

                # 已经存在则跳过
                if len(df2)>0 :continue  
                
                if row["symbol"][0] == "0": row["ts_code"] =  row["symbol"]+".SZ"
                if row["symbol"][0] == "3": row["ts_code"] =  row["symbol"]+".SZ"
                if row["symbol"][0] == "4": row["ts_code"] =  row["symbol"]+".BJ"
                if row["symbol"][0] == "6": row["ts_code"] =  row["symbol"]+".SH"
                if row["symbol"][0] == "8": row["ts_code"] =  row["symbol"]+".BJ"
                if "area" in row.keys() : area =  row["area"] 
                else : area =  ""
                if "industry" in row.keys() : industry =  row["industry"] 
                else : industry =  ""
                if "fullname" in row.keys() : fullname =  row["fullname"] 
                else : fullname =  ""
                if "enname" in row.keys() : enname =  row["enname"] 
                else : enname =  ""
                if "market" in row.keys() : market =  row["market"] 
                else : market =  ""
                if "exchange" in row.keys() : exchange =  row["exchange"] 
                else : exchange =  ""
                if "curr_type" in row.keys() : curr_type =  row["curr_type"] 
                else : curr_type =  ""
                if "list_status" in row.keys() : list_status =  row["list_status"] 
                else : list_status =  ""
                if "list_date" in row.keys() : list_date =  row["list_date"] 
                else : list_date =  ""
                if "delist_date" in row.keys() : delist_date =  row["delist_date"] 
                else : delist_date =  ""
                if "is_hs" in row.keys() : is_hs =  row["is_hs"] 
                else : is_hs =  "" 

                session.execute( text(""" INSERT INTO runner_stock_basic 
                                    (`symbol`,`name`,`area`,`industry`,`fullname`,`enname`,`market`,`exchange`,
                                    `curr_type`,`list_status`,`list_date`,`delist_date`,`is_hs`,`ts_code`)
                                    values(
                                        :symbol,:name,:area,:industry,:fullname,:enname,:market,:exchange,
                                    :curr_type,:list_status,:list_date,:delist_date,:is_hs,:ts_code 
                                    ) """), params={ "symbol": row["symbol"],"name":row["name"] , "area": area , "industry":industry  , "fullname": fullname,"enname":enname , "market":market  , "exchange":exchange, "curr_type": curr_type,"list_status":list_status ,
                                    "list_date":list_date , "delist_date":delist_date, "is_hs":is_hs , "ts_code":row["ts_code"] })
                session.commit() 
                print("更新股票："+row["ts_code"])


            session.execute(text(""" update  runner_stock_trade_cal t set t.stock_basic_spider = 1   WHERE  cal_date = :cal_date  and ( t.stock_basic_spider != 1  or t.stock_basic_spider is NULL) """),   params={ "cal_date": trade_date})
            session.commit()
            session.remove()
            return 1
 