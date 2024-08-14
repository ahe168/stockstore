from fastapi import FastAPI
import  sys
sys.path.append("../")
from dbutil import DBHandle2
import  pandas as pd
app = FastAPI()

@app.get("/")
async def root():
    df = pd.DataFrame()
    stock_hfq_df = DBHandle2.getDataService('get_daily_starttrade_endtrade_code', {'ts_code': '000001.SZ', 'startDate': '20230930', 'endDate': '20231231'})
    print(stock_hfq_df)
    res = stock_hfq_df.to_dict('records')
    return res
