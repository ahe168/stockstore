
import json
import os
import pandas as pd
file_path = os.path.dirname(os.path.abspath(__file__))
class ConfigCron():
    def __init__(self):
        pass
    def config_db_read(self):
        with open(file_path+"/config_cron.json", "r", encoding="utf-8") as f:
            return  json.load(f)

    def config_db_write(self,data):
        try:
            with open(file_path+"/config_cron.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)
        return 1

    def getDbInfo(self):
        df = pd.read_json(file_path+"/config_cron.json",encoding="utf-8", orient='records')
        return  df.loc[df['status'] == 1].loc[0,"dbtype"], df.loc[df['status'] == 1]

if __name__ == "__main__":
    a,b =ConfigCron().getDbInfo()