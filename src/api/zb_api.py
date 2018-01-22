# -*- coding: utf-8 -*-

import httplib
import json
import yaml
import sys
import urllib2
import zb_error
import utils

reload(sys)
sys.setdefaultencoding('utf-8')


class zb_api:
    def __init__(self):
        pass

    def __api_call(self, path, params = ""):
        try:
            url = 'http://api.zb.com/data/v1/' + path
            if params != "" : url += '?' + params

            request  = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=3)
            result   = yaml.safe_load(response.read())
            return result
        except Exception,ex:
            return {"error": "Request zb_api failed, URL:"+url + " Exception:"+ str(ex) }


    def zb_get_market(self):
        '''
        获取已开启的市场信息，包括价格、数量小数点位数

        #http://api.zb.com/data/v1/markets  获取已开启的市场信息，包括价格、数量小数点位数
        # Response
        {
            "btc_usdt": {
                "amountScale": 4,
                "priceScale": 2
            },
            "ltc_usdt": {
                "amountScale": 3,
                "priceScale": 2
            }
            ...
        }

        priceScale : 价格小数位数
        amountScale : 数量小数位数

        '''
        return self.__api_call(path="markets")


    def zb_get_ticker(self, marketType ):
        """
        返回一种币种的行情

        http://api.zb.com/data/v1/ticker?market=btc_usdt
        market范围:
        btc_usdt,bcc_usdt,ubtc_usdt,ltc_usdt,eth_usdt,etc_usdt,bts_usdt,eos_usdt,qtum_usdt,hsr_usdt,xrp_usdt
        ,bcd_usdt,dash_usdt,btc_qc,bcc_qc,ubtc_qc,ltc_qc,eth_qc,etc_qc,bts_qc,eos_qc,qtum_qc,hsr_qc,xrp_qc,b
        cd_qc,dash_qc,bcc_btc,ubtc_btc,ltc_btc,eth_btc,etc_btc,bts_btc,eos_btc,qtum_btc,hsr_btc,xrp_btc,bcd_
        btc,dash_btc,sbtc_usdt,sbtc_qc,sbtc_btc,ink_usdt,ink_qc,ink_btc,tv_usdt,tv_qc,tv_btc,bcx_usdt,bcx_qc
        ,bcx_btc,bth_usdt,bth_qc,bth_btc,lbtc_usdt,lbtc_qc,lbtc_btc,chat_usdt,chat_qc,chat_btc,hlc_usdt,hlc_
        qc,hlc_btc,bcw_usdt,bcw_qc,bcw_btc,btp_usdt,btp_qc,btp_btc,bitcny_qc,topc_usdt,topc_qc,topc_btc,ent_
        usdt,ent_qc,ent_btc,bat_usdt,bat_qc,bat_btc,1st_usdt,1st_qc,1st_btc,safe_usdt,safe_qc,safe_btc,qun_u
        sdt,qun_qc,qun_btc,btn_usdt,btn_qc,btn_btc,true_usdt,true_qc,true_btc,cdc_usdt,cdc_qc,cdc_btc,ddm_us
        dt,ddm_qc,ddm_btc,bite_btc

        //# Response
        {
            "ticker": {
                "vol": "40.463",
                "last": "0.899999",
                "sell": "0.5",
                "buy": "0.225",
                "high": "0.899999",
                "low": "0.081"
            },
            "date": "1507875747359"
        }

        出错返回200 OK,json中key=error:
        (200, 'OK', {u'error': u'\u5e02\u573a\u9519\u8bef'})

        high : 最高价
        low : 最低价
        buy : 买一价
        sell : 卖一价
        last : 最新成交价
        vol : 成交量(最近的24小时)
        """
        __params = "market=" + marketType
        return  self.__api_call(path="ticker", params = __params)


    def zb_get_depth(self, marketType , size= 50):
        """
        市场深度,参数:币种,竞卖asks和竞买bids的个数,最多是50个

        http://api.zb.com/data/v1/depth?market=btc_usdt&size=3   市场深度,参数:币种,竞卖asks和竞买bids的个数,最多是50个
        //# Response
        {
            "asks": [
                [
                    83.28,
                    11.8
                ]...
            ],
            "bids": [
                [
                    81.91,
                    3.65
                ]...
            ],
            "timestamp" : 时间戳
        }

        asks : 卖方深度
        bids : 买方深度
        timestamp : 此次深度的产生时间戳

        返回:
        ask:    竞卖价格(udst为美元), 竟卖个数
        bids:   竞买价格(udst为美元), 竟卖个数
        {"timestamp":1516526083,
        "asks":[
                [14.087,45.6],
                14.086,246.0],
                [14.084,357.0]
               ],
        "bids":[
                 [13.91,92.0],
                 [13.907,2.8],
                 [13.906,105.0]
               ]
        }
        出错返回200 OK,json中key=error:
        (200, 'OK', {u'error': u'\u5e02\u573a\u9519\u8bef'})
        """
        __params = "market="+marketType+"&"+"size=" + str(size)
        return self.__api_call(path="depth", params=__params)


    def zb_get_trades(self, marketType):
        """
        历史成交

        http://api.zb.com/data/v1/trades?market=btc_usdt

        //# Response
        [
            {
                "amount": 0.541,
                "date": 1472711925,
                "price": 81.87,
                "tid": 16497097,
                "trade_type": "ask",
                "type": "sell"
            }...
        ]
        date : 交易时间(时间戳)
        price : 交易价格
        amount : 交易数量
        tid : 交易生成ID
        type : 交易类型，buy(买)/sell(卖)
        trade_type : 委托类型，ask(卖)/bid(买)

        since   从指定交易ID后50条数据

        出错返回200 OK,json中key=error:
        (200, 'OK', {u'error': u'\u5e02\u573a\u9519\u8bef'})
        """
        __params = "market=" + marketType
        return self.__api_call(path="trades", params=__params)



if __name__ == '__main__':

    zbapi = zb_api()
    #print zbapi.zb_get_market()
    #print zbapi.zb_get_ticker("eos_usdt")
    #print zbapi.zb_get_depth("eos_usdt",3)
    #print zbapi.zb_get_trades("eos_usdt")
    while True:

        eos = zbapi.zb_get_ticker("eos_usdt")
        import time
        print eos
        if eos.has_key("ticker") == False : continue
        print "Date:%s   买:%.4f  卖:%.4f    最新成交:%.4f     最高位:%.4f      最低位:%.4f    成交量:%.1f " % (

                      time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                      float(eos["ticker"]["buy"]) * 6.7,
                      float(eos["ticker"]["sell"]) * 6.7,
                      float(eos["ticker"]["last"]) * 6.7,
                      float(eos["ticker"]["high"]) * 6.7,
                      float(eos["ticker"]["low"]) * 6.7,
                      float(eos["ticker"]["vol"]) * 6.7
        )

        if float(eos["ticker"]["last"]) * 6.7 < 95 : utils.mac_notify("Eos 交易价格已经小于 95元")

        time.sleep (2)


    """
    >>> import json
    >>> js = json.loads('{"haha": "哈哈"}')
    >>> print json.dumps(js)
    {"haha": "\u54c8\u54c8"}

    解决办法很简单:

    >>> print json.dumps(js, ensure_ascii=False)
    {"haha": "哈哈"}



      eos["ticker"]["buy"] * 6.7,
      eos["ticker"]["sell"] * 6.7,
      eos["ticker"]["last"] * 6.7,
      eos["ticker"]["high"] * 6.7,
      eos["ticker"]["low"] * 6.7,
      eos["ticker"]["vol"] * 6.7
    """