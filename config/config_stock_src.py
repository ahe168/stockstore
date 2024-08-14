
import json
import os
import pandas as pd
file_path = os.path.dirname(os.path.abspath(__file__))
class ConfigStockSrc():
    def __init__(self):
        pass
    def config_db_read(self):
        with open(file_path+"/config_stock_src.json", "r", encoding="utf-8") as f:
            return  json.load(f)

    def config_db_write(self,data):
        try:
            with open(file_path+"/config_stock_src.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)
        return 1


    def getSrcInfo(self):
        try:
            df = pd.read_json(file_path+"/config_stock_src.json",encoding="utf-8", orient='records')
            return  df.loc[df['status'] == 1][["src","password"]]
        except Exception as e:
            print(e)
        return 1

import tushare as ts
class TushareHelper():

    def __init__(self):

        self.pro = None
        self.df  = ConfigStockSrc().getSrcInfo()
        for index , row  in self.df.iterrows():
            if row["src"] == "tushare":
                self.pro = ts.pro_api(row["password"])

if __name__ == '__main__':
    if TushareHelper().pro != None :
        df = TushareHelper().pro.daily(trade_date='20210602' )
        print(df)


