# -*- coding: utf-8 -*-
import re
import urllib2
import ConfigParser
import mysql.connector


conf = ConfigParser.ConfigParser()
conf.read("config/config.ini")
stockId = conf.get("stock", "stock_code")

#数据请求方法
def data_api(id):
    strHtml = urllib2.urlopen('http://hq.sinajs.cn/list=' + id).read()
    return strHtml
def request(stockId):
    #query
    conn = mysql.connector.connect(host='60.205.207.56',port='3306',user='rht102',password='rht102',database='stock',use_unicode=True);
    cursor = conn.cursor();
    #原始数据
    sorce_data = data_api(stockId)
    #print re.split(';|,|"',sorce_data)

    #正则处理过的数据（数组）
    processed_data = re.split(';|,|"',sorce_data)

    #涨跌幅
    float_persent = (float(processed_data[4]) - float(processed_data[3]))/float(processed_data[3])*100
    #print float_persent
    
    #股票名称
    #print processed_data[1]
    
    #昨日收盘价
    #print processed_data[3]
    
    #今日开盘价
    #print processed_data[2]
    
    #当前价
    #print processed_data[4]
    
    #当前时刻
    #print processed_data[-4]
    
    #成交量
    #print processed_data[9]
    
    #成交额
    #print processed_data[10]
    
    #股票代码
    #print processed_data[0]
    
    #sql update
    sql = """UPDATE stocks_data
        SET price_yesterday = %s,price_open = %s,price = %s,count_time = %s,turnover_volume = %s,turnover_amount = %s,float_persent = %s
        WHERE stock_code = %s """
    data = (processed_data[3],processed_data[2],processed_data[4],processed_data[-4],processed_data[9],processed_data[10],float_persent,stockId)
    cursor = conn.cursor();
    cursor.execute(sql,data)
    conn.commit()
    #close db sorce
    cursor.close()
    conn.close()

request(stockId)
