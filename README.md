# 搭建个人的金融系统-----数据自动同步stockstore

一、安装mysql数据库服务器<br>
二、运行 stockstore.sql 脚本，建表<br>
三、运行  pip install -r requirements.txt 安装依赖<br>
四、修改数据库配置config_stock_db.json<br>
五、修改tushare配置config_stock_src.json  申请 tushare地址：https://tushare.pro/register?reg=381844<br>
六、修改定时任务执行脚本config_cron.json<br>
七、运行 runner.py <br>
八、等待数据入库<br>



