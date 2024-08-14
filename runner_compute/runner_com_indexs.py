# encoding:utf-8
import os
import sys
import pandas as qh_pd
import talib

if __name__ == "__main__":
    qh_path = os.path.abspath(os.path.join(os.getcwd(), ".."))    
    sys.path.append(qh_path)  
else:
    qh_path = os.path.abspath(os.path.join(os.getcwd(), ".."))   
    sys.path.append(qh_path)   

qh_pd.set_option('display.max_columns', None)
qh_pd.set_option('display.width', 1000)


def Qh_Target_MA(qh_df, qh_close="收盘价", qh_timeperiod=5):
    """
    计算MA指标，  
    :param qh_df:
    :param qh_close:
    :param qh_timeperiod:
    :return:
    """
    qh_cloumn = "MA_{}".format(qh_timeperiod)
    qh_df[qh_cloumn] = talib.MA(qh_df[qh_close], timeperiod=qh_timeperiod, matype=0)
    return qh_df


def Qh_Target_EMA(qh_df, qh_close="收盘价", qh_timeperiod=5):
    """
    计算EMA指标，  
    :param qh_df:
    :param qh_close:
    :param qh_timeperiod:
    :return:
    """
    qh_cloumn = "EMA_{}".format(qh_timeperiod)
    qh_df[qh_cloumn] = talib.EMA(qh_df[qh_close], timeperiod=qh_timeperiod)
    return qh_df


def Qh_Target_MACD(qh_df, qh_close="收盘价", qh_fastperiod=12, qh_slowperiod=26, qh_signalperiod=9):
    """
    计算MACD指标， 
    :param qh_df:
    :param qh_close:
    :param qh_fastperiod:
    :param qh_slowperiod:
    :param qh_signalperiod:
    :return:
    """
    qh_diff = "DIFF_{}".format(qh_slowperiod)
    qh_dea = "DEA_{}".format(qh_slowperiod)
    qh_macd = "MACD_{}".format(qh_slowperiod)
    qh_df[qh_diff], qh_df[qh_dea], qh_df[qh_macd] = talib.MACD(qh_df[qh_close], fastperiod=qh_fastperiod,
                                                               slowperiod=qh_slowperiod, signalperiod=qh_signalperiod)
    qh_df[qh_macd] = qh_df[qh_macd] * 2  # 修正macd
    return qh_df


def Qh_Target_BOLL(qh_df, qh_close="收盘价", qh_timeperiod=20, qh_nbdev=2):
    """
    计算BOLL指标，  
    :param qh_df:
    :param qh_close:
    :param qh_timeperiod:
    :param qh_nbdev:
    :return:
    """
    qh_uuper = "UPPER_{}".format(qh_timeperiod)
    qh_mid = "MID_{}".format(qh_nbdev)
    qh_lower = "LOWER_{}".format(qh_nbdev)
    qh_df[qh_uuper], qh_df[qh_mid], qh_df[qh_lower] = talib.BBANDS(qh_df[qh_close], timeperiod=qh_timeperiod,
                                                                   nbdevup=qh_nbdev, nbdevdn=qh_nbdev, matype=0)
    return qh_df


def Qh_Target_KDJ(qh_df, qh_hig="最高价", qh_low="最低价", qh_close="收盘价", qh_fastk=9, qh_slowk=3, qh_slowd=3):
    """
    计算KDJ指标，  
    :param qh_df:
    :param qh_hig:
    :param qh_low:
    :param qh_close:
    :param qh_fastk:
    :param qh_slowk:
    :param qh_slowd:
    :return:
    """
    qh_K = "K_{}".format(qh_fastk)
    qh_D = "D_{}".format(qh_fastk)
    qh_J = "J_{}".format(qh_fastk)
    qh_df[qh_K], qh_df[qh_D] = talib.STOCH(qh_df[qh_hig], qh_df[qh_low], qh_df[qh_close],
                                           fastk_period=qh_fastk, slowk_period=qh_slowk,
                                           slowk_matype=1, slowd_period=qh_slowd, slowd_matype=1)
    qh_df[qh_J] = 3 * qh_df[qh_K] - 2 * qh_df[qh_D]
    return qh_df


def Qh_Target_KDJ_CN(qh_df, qh_hig="最高价", qh_low="最低价", qh_close="收盘价", qh_fastk_period=9, qh_slowk_period=3,
                     qh_fastd_period=3):
    """
    计算KDJ指标                 
    :param qh_higt:
    :param qh_low:
    :param qh_close:
    :param qh_fastk_period:
    :param qh_slowk_period:
    :param qh_fastd_period:
    :return:
    """
    QH_K = "QH_K_{}".format(qh_fastk_period)
    QH_D = "QH_D_{}".format(qh_fastk_period)
    QH_J = "QH_J_{}".format(qh_fastk_period)

    qh_df[qh_low] = qh_df[qh_low].astype("float64")
    qh_df[qh_low] = qh_df[qh_low].fillna(0)
    QH_MinLow = qh_df[qh_low].rolling(qh_fastk_period, min_periods=qh_fastk_period).min()  # 最低价
    QH_MinLow.fillna(value=qh_df[qh_low].expanding().min(), inplace=True)  # 填充空值 NaN

    qh_df[qh_hig] = qh_df[qh_hig].astype("float64")
    qh_df[qh_hig] = qh_df[qh_hig].fillna(0)
    QH_MaxHigh = qh_df[qh_hig].rolling(qh_fastk_period, min_periods=qh_fastk_period).max()  # 最高价
    QH_MaxHigh.fillna(value=qh_df[qh_hig].expanding().max(), inplace=True)  # 填充空值 NaN

    qh_df[qh_close] = qh_df[qh_close].astype("float64")
    qh_df[qh_close] = qh_df[qh_close].fillna(0)
    # RSV  公式：RSV = (收盘价 - 最低价）/（最高价 - 最低价） * 100 n日RSV=（Cn－Ln）÷（Hn－Ln）×100
    QH_RSV = (qh_df[qh_close] - QH_MinLow) / (QH_MaxHigh - QH_MinLow) * 100
    QH_RSV = QH_RSV.fillna(0)

    # 当日K值=2/3×前一日K值＋1/3×当日RSV
    qh_df[QH_K] = QH_RSV.ewm(adjust=False, alpha=1 / qh_slowk_period).mean()
    # 当日D值=2/3×前一日D值＋1/3×当日K值
    qh_df[QH_D] = qh_df[QH_K].ewm(adjust=False, alpha=1 / qh_fastd_period).mean()
    # J=3D—2K
    qh_df[QH_J] = 3 * qh_df[QH_K] - 2 * qh_df[QH_D]

    return qh_df

