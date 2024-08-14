/*
 Navicat Premium Data Transfer

 Source Server         : 138.2.3.126
 Source Server Type    : MySQL
 Source Server Version : 50744
 Source Host           : 138.2.3.126:3306
 Source Schema         : stock2

 Target Server Type    : MySQL
 Target Server Version : 50744
 File Encoding         : 65001

 Date: 14/08/2024 22:48:43
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for runner_stock_adjfactor
-- ----------------------------
DROP TABLE IF EXISTS `runner_stock_adjfactor`;
CREATE TABLE `runner_stock_adjfactor` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `ts_code` varchar(10) DEFAULT NULL,
  `symbol` varchar(11) DEFAULT NULL COMMENT '股票代码',
  `trade_date` date DEFAULT NULL,
  `adj_factor` float(10,4) DEFAULT NULL,
  `last_adj_factor` float(10,4) DEFAULT NULL COMMENT '最新复权因子',
  `pre_adj_factor` float(10,4) DEFAULT NULL COMMENT '前复权因子',
  `create_datetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '采集时间',
  PRIMARY KEY (`aid`) USING BTREE,
  UNIQUE KEY `i_code_date` (`ts_code`,`trade_date`) USING BTREE,
  KEY `i_ts_code` (`ts_code`) USING BTREE,
  KEY `i_trade__date` (`trade_date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=44561938 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for runner_stock_basic
-- ----------------------------
DROP TABLE IF EXISTS `runner_stock_basic`;
CREATE TABLE `runner_stock_basic` (
  `symbol` varchar(11) CHARACTER SET utf8 NOT NULL COMMENT '股票代码',
  `name` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '股票名称',
  `area` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '所在地域',
  `industry` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '所属行业',
  `fullname` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '股票全称',
  `enname` varchar(100) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '英文全称',
  `market` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '市场类型 （主板/中小板/创业板/科创板）',
  `exchange` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '交易所代码',
  `curr_type` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '交易货币',
  `list_status` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '上市状态： L上市 D退市 P暂停上市',
  `list_date` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '上市日期',
  `delist_date` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '退市日期',
  `is_hs` varchar(50) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT '是否沪深港通标的，N否 H沪股通 S深股通',
  `ts_code` varchar(20) CHARACTER SET utf8 DEFAULT NULL COMMENT '股票代码（支持多个股票同时提取，逗号分隔）',
  `adj_factor` double(10,4) DEFAULT NULL COMMENT '最新复权因子',
  `create_datetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '采集时间',
  PRIMARY KEY (`symbol`) USING BTREE,
  UNIQUE KEY `U_SYMBOL` (`symbol`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci ROW_FORMAT=DYNAMIC COMMENT='股票列表';

-- ----------------------------
-- Table structure for runner_stock_daily
-- ----------------------------
DROP TABLE IF EXISTS `runner_stock_daily`;
CREATE TABLE `runner_stock_daily` (
  `did` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ts_code` varchar(20) NOT NULL COMMENT '股票代码(采集）',
  `name` varchar(40) DEFAULT NULL,
  `trade_date` date NOT NULL COMMENT '交易日期',
  `open` float(20,4) DEFAULT '0.0000' COMMENT '开盘价',
  `p_open` float(20,4) DEFAULT '0.0000' COMMENT '开盘价（前复权)',
  `high` float(20,4) DEFAULT '0.0000' COMMENT '最高价',
  `p_high` float(20,4) DEFAULT '0.0000' COMMENT '最高价（前复权)',
  `low` float(20,4) DEFAULT '0.0000' COMMENT '最低价',
  `p_low` float(20,4) DEFAULT '0.0000' COMMENT '最低价（前复权)',
  `close` float(20,4) DEFAULT '0.0000' COMMENT '收盘价',
  `p_close` float(20,4) DEFAULT '0.0000' COMMENT '收盘价（前复权)',
  `pre_close` float(20,4) DEFAULT '0.0000' COMMENT '昨收价',
  `p_pre_close` float(20,4) DEFAULT '0.0000' COMMENT '昨收价（前复权)',
  `change` float(20,4) DEFAULT '0.0000' COMMENT '涨跌额',
  `pct_chg` float(20,4) DEFAULT '0.0000' COMMENT '涨跌幅 （未复权，如果是复权请用 通用行情接口 ）',
  `vol` float(20,4) DEFAULT '0.0000' COMMENT '成交量 （手）',
  `amount` float(20,4) DEFAULT '0.0000' COMMENT '成交额 （千元）',
  `symbol` varchar(11) DEFAULT '0' COMMENT '股票代码',
  `create_datetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '采集时间',
  PRIMARY KEY (`did`,`trade_date`) USING BTREE,
  UNIQUE KEY `U_STOCK_DATE` (`ts_code`,`trade_date`) USING BTREE,
  KEY `I_TRADE_DATE` (`trade_date`) USING BTREE,
  KEY `I_TS_CODE` (`ts_code`) USING BTREE,
  KEY `i_symbol` (`symbol`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=63949310 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='日线行情';

-- ----------------------------
-- Table structure for runner_stock_daily_basic
-- ----------------------------
DROP TABLE IF EXISTS `runner_stock_daily_basic`;
CREATE TABLE `runner_stock_daily_basic` (
  `ts_code` varchar(20) COLLATE utf8_croatian_ci DEFAULT NULL COMMENT 'TS股票代码',
  `trade_date` date DEFAULT NULL COMMENT '交易日期（采集）',
  `close` float(20,4) DEFAULT NULL COMMENT '当日收盘价',
  `turnover_rate` float(20,4) DEFAULT NULL COMMENT '换手率（%）',
  `turnover_rate_f` float(20,4) DEFAULT NULL COMMENT '换手率（自由流通股）',
  `volume_ratio` float(20,4) DEFAULT NULL COMMENT '量比',
  `pe` float(20,4) DEFAULT NULL COMMENT '市盈率（总市值/净利润， 亏损的PE为空）',
  `pe_ttm` float(20,4) DEFAULT NULL COMMENT '市盈率（TTM，亏损的PE为空）',
  `pb` float(20,4) DEFAULT NULL COMMENT '市净率（总市值/净资产）',
  `ps` float(20,4) DEFAULT NULL COMMENT '市销率',
  `ps_ttm` float(20,4) DEFAULT NULL COMMENT '市销率（TTM）',
  `dv_ratio` float(20,4) DEFAULT NULL COMMENT '股息率 （%）',
  `dv_ttm` float(20,4) DEFAULT NULL COMMENT '股息率（TTM）（%）',
  `total_share` float(20,4) DEFAULT NULL COMMENT '总股本 （万股）',
  `float_share` float(20,4) DEFAULT NULL COMMENT '流通股本 （万股）',
  `free_share` float(20,4) DEFAULT NULL COMMENT '自由流通股本 （万）',
  `total_mv` float(20,4) DEFAULT NULL COMMENT '总市值 （万元）',
  `circ_mv` float(20,4) DEFAULT NULL COMMENT '流通市值（万元）',
  `did` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `create_datetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '采集时间',
  `symbol` varchar(10) CHARACTER SET utf8 DEFAULT NULL COMMENT '交易代码',
  PRIMARY KEY (`did`) USING BTREE,
  UNIQUE KEY `U_STOCK_DATE` (`ts_code`,`trade_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci ROW_FORMAT=DYNAMIC COMMENT='每日指标\n';

-- ----------------------------
-- Table structure for runner_stock_daily_index
-- ----------------------------
DROP TABLE IF EXISTS `runner_stock_daily_index`;
CREATE TABLE `runner_stock_daily_index` (
  `did` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ts_code` varchar(20) NOT NULL COMMENT '股票代码(采集）',
  `trade_date` date NOT NULL COMMENT '交易日期',
  `macd` float(20,6) DEFAULT '0.000000' COMMENT 'macd指标',
  `diff` float(20,6) DEFAULT '0.000000' COMMENT 'dif指标',
  `ema12` float(20,6) DEFAULT '0.000000' COMMENT 'ema12指标',
  `ema26` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `dea` float(20,6) DEFAULT '0.000000' COMMENT 'DEA指标',
  `bar` float(20,6) DEFAULT '0.000000' COMMENT 'BAR 指标',
  `createtime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
  `ma5` float(20,6) DEFAULT '0.000000' COMMENT 'ema5指标',
  `ma10` float(20,6) DEFAULT '0.000000' COMMENT 'ema10指标',
  `ma20` float(20,6) DEFAULT '0.000000' COMMENT 'ema20指标',
  `ma60` float(20,6) DEFAULT '0.000000' COMMENT 'ema60指标',
  `ema20` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `upper20` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `mid2` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `qhd9` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `qhj9` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `lower2` float(20,6) DEFAULT NULL,
  `qhk9` float(20,6) DEFAULT NULL,
  PRIMARY KEY (`did`,`trade_date`) USING BTREE,
  UNIQUE KEY `U_STOCK_DATE` (`ts_code`,`trade_date`) USING BTREE,
  KEY `I_TRADE_DATE` (`trade_date`) USING BTREE,
  KEY `I_TS_CODE` (`ts_code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=78987912 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='日线行情';

-- ----------------------------
-- Table structure for runner_stock_trade_cal
-- ----------------------------
DROP TABLE IF EXISTS `runner_stock_trade_cal`;
CREATE TABLE `runner_stock_trade_cal` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `exchange` varchar(5) DEFAULT NULL COMMENT '交易所 SSE上交所,SZSE深交所,CFFEX 中金所,SHFE 上期所,CZCE 郑商所,DCE 大商所,INE 上能源,IB 银行间,XHKG 港交所;;交易所 SSE上交所 SZSE深交所',
  `cal_date` date DEFAULT NULL COMMENT '日历日期',
  `is_open` varchar(12) DEFAULT NULL COMMENT '是否交易 0休市 1交易',
  `pretrade_date` date DEFAULT NULL COMMENT '上一个交易日',
  `stock_basic_spider` int(11) DEFAULT NULL COMMENT '0:进行中；-1：失败；1已完成（股票基本信息）',
  `daily_spider` int(11) DEFAULT NULL COMMENT '0:进行中；-1：失败；1已完成',
  `weekly_spider` int(11) DEFAULT NULL COMMENT '0:进行中；-1：失败；1已完成',
  `adj_factor_spider` int(11) DEFAULT NULL COMMENT '采集复权因子',
  `daily_qfq_compute` int(11) DEFAULT NULL COMMENT '0:进行中；-1：失败；1已完成',
  `weekly_qfq_compute` int(11) DEFAULT NULL COMMENT '0:进行中；-1：失败；1已完成',
  `daily_compute` int(11) DEFAULT NULL COMMENT '0:进行中；-1：失败；1已完成',
  `weekly_compute` int(11) DEFAULT NULL COMMENT '0:进行中；-1：失败；1已完成',
  `adj_factor_cnt` int(11) DEFAULT NULL COMMENT '当日采集的复权因子数量',
  `daily_cnt` int(11) DEFAULT NULL COMMENT '当日采集的日线数据数量',
  `weekly_cnt` int(11) DEFAULT NULL COMMENT '周采集的指标数量',
  `dailybasic_cnt` int(11) DEFAULT NULL COMMENT '当日采集的每日指标数量',
  `weeklybasic_cnt` int(11) DEFAULT NULL COMMENT '当日采集的每日指标数量',
  `is_copy` int(11) DEFAULT '0' COMMENT '是否拷贝数据',
  `create_datetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '采集时间',
  `daily_basic_cnt` int(11) DEFAULT NULL COMMENT '当日采集的每日指标数量',
  `daily_basic_spider` int(11) DEFAULT NULL COMMENT '0:进行中；-1：失败；1已完成',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `u_cal_date` (`cal_date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=43000 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='交易日历\r\n描述：获取各大交易所交易日历数据,默认提取的是上交所';

-- ----------------------------
-- Table structure for runner_stock_weekly
-- ----------------------------
DROP TABLE IF EXISTS `runner_stock_weekly`;
CREATE TABLE `runner_stock_weekly` (
  `did` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ts_code` varchar(20) NOT NULL COMMENT '股票代码(采集）',
  `name` varchar(40) DEFAULT NULL,
  `trade_date` date NOT NULL COMMENT '交易日期',
  `open` float(20,4) DEFAULT '0.0000' COMMENT '开盘价',
  `p_open` float(20,4) DEFAULT '0.0000' COMMENT '开盘价（前复权)',
  `high` float(20,4) DEFAULT '0.0000' COMMENT '最高价',
  `p_high` float(20,4) DEFAULT '0.0000' COMMENT '最高价（前复权)',
  `low` float(20,4) DEFAULT '0.0000' COMMENT '最低价',
  `p_low` float(20,4) DEFAULT '0.0000' COMMENT '最低价（前复权)',
  `close` float(20,4) DEFAULT '0.0000' COMMENT '收盘价',
  `p_close` float(20,4) DEFAULT '0.0000' COMMENT '收盘价（前复权)',
  `pre_close` float(20,4) DEFAULT '0.0000' COMMENT '昨收价',
  `p_pre_close` float(20,4) DEFAULT '0.0000' COMMENT '昨收价（前复权)',
  `change` float(20,4) DEFAULT '0.0000' COMMENT '涨跌额',
  `pct_chg` float(20,4) DEFAULT '0.0000' COMMENT '涨跌幅 （未复权，如果是复权请用 通用行情接口 ）',
  `vol` float(20,4) DEFAULT '0.0000' COMMENT '成交量 （手）',
  `amount` float(20,4) DEFAULT '0.0000' COMMENT '成交额 （千元）',
  `symbol` varchar(11) DEFAULT '0' COMMENT '股票代码',
  `create_datetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '采集时间',
  PRIMARY KEY (`did`,`trade_date`) USING BTREE,
  UNIQUE KEY `U_STOCK_DATE` (`ts_code`,`trade_date`) USING BTREE,
  KEY `I_TRADE_DATE` (`trade_date`) USING BTREE,
  KEY `I_TS_CODE` (`ts_code`) USING BTREE,
  KEY `i_symbol` (`symbol`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=30438986 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='日线行情';

-- ----------------------------
-- Table structure for runner_stock_weekly_index
-- ----------------------------
DROP TABLE IF EXISTS `runner_stock_weekly_index`;
CREATE TABLE `runner_stock_weekly_index` (
  `did` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ts_code` varchar(20) NOT NULL COMMENT '股票代码(采集）',
  `trade_date` date NOT NULL COMMENT '交易日期',
  `macd` float(20,6) DEFAULT '0.000000' COMMENT 'macd指标',
  `diff` float(20,6) DEFAULT '0.000000' COMMENT 'dif指标',
  `ema12` float(20,6) DEFAULT '0.000000' COMMENT 'ema12指标',
  `ema26` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `dea` float(20,6) DEFAULT '0.000000' COMMENT 'DEA指标',
  `bar` float(20,6) DEFAULT '0.000000' COMMENT 'BAR 指标',
  `createtime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
  `ma5` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `ma10` float(20,6) DEFAULT '0.000000' COMMENT 'ema10指标',
  `ma20` float(20,6) DEFAULT '0.000000' COMMENT 'ema20指标',
  `ma60` float(20,6) DEFAULT '0.000000' COMMENT 'ema60指标',
  `ema20` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `upper20` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `mid2` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `qhd9` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `qhj9` float(20,6) DEFAULT '0.000000' COMMENT 'ema26指标',
  `lower2` float(20,6) DEFAULT NULL,
  `qhk9` float(20,6) DEFAULT NULL,
  PRIMARY KEY (`did`,`trade_date`) USING BTREE,
  UNIQUE KEY `U_STOCK_DATE` (`ts_code`,`trade_date`) USING BTREE,
  KEY `I_TRADE_DATE` (`trade_date`) USING BTREE,
  KEY `I_TS_CODE` (`ts_code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=33203868 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='日线行情';

-- ----------------------------
-- Table structure for stock_conf_sql
-- ----------------------------
DROP TABLE IF EXISTS `stock_conf_sql`;
CREATE TABLE `stock_conf_sql` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `sql_code` varchar(255) NOT NULL COMMENT '代码',
  `sql_body` text COMMENT 'SQL内容',
  `sql_des` varchar(255) DEFAULT NULL COMMENT '描述',
  `valid_flag` int(11) DEFAULT NULL COMMENT '0无效1有效',
  PRIMARY KEY (`sid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
