# -*- coding: utf-8 -*-

import json, urllib2, hashlib,struct,sha,time,sys
import yaml


reload(sys)
sys.setdefaultencoding('utf-8')


class zb_trade_api:

    TradeType_BUY  = 1
    TradeType_SELL = 0

    def __init__(self, mykey, mysecret):
        self.mykey = mykey
        self.mysecret = mysecret

    def __fill(self, value, length, fillByte):
        if len(value) >= length:
            return value
        else:
            fillSize = length - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb   = struct.pack("%ds" % len(aKey), aKey)
        value  = struct.pack("%ds" % len(aValue), aValue)
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()

        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value  = struct.pack("%ds" % len(aValue), aValue)
        #print value
        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params = ""):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time()*1000)
            params+= '&sign=%s&reqTime=%d'%(sign, reqTime)
            url = 'https://trade.zb.com/api/' + path + '?' + params

            request  = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=3)
            result   = yaml.safe_load(response.read())
            return result
        except Exception,ex:
            return {"error": "Request zb_api failed, URL:"+url + " Exception:"+ str(ex) }


    def zb_get_account(self):
        '''
        获取用户信息
        :return:
        //# Response
        {
            "result": {
                "coins": [
                    {
                        "freez": "0.00000000",
                        "enName": "BTC",
                        "unitDecimal": 8,
                        "cnName": "BTC",
                        "unitTag": "฿",
                        "available": "0.00000000",
                        "key": "btc"
                    },
                    {
                        "freez": "0.00000000",
                        "enName": "LTC",
                        "unitDecimal": 8,
                        "cnName": "LTC",
                        "unitTag": "Ł",
                        "available": "0.00000000",
                        "key": "ltc"
                    },
                   ...
                ],
                "base": {
                    "username": "134150***",
                    "trade_password_enabled": true,
                    "auth_google_enabled": false,
                    "auth_mobile_enabled": true
                }
            }
        }
        auth_google_enabled : 是否开通谷歌验证
        auth_mobile_enabled : 是否开通手机验证
        trade_password_enabled : 是否开通交易密码
        username : 用户名
        coins:
              freez：冻结资产
              ename:币种英文名
              unitDecimal：保留小数位
              cnName:币种中文名
              unitTag:币种符号
              available：可用资产
              key:币种

        '''
        __params = "accesskey="+self.mykey+"&method=getAccountInfo"
        return self.__api_call("getAccountInfo", params=__params)



    def zb_get_Order(self, id, currency):
        '''

        :param id:委托挂单号
        :param currency:btc_usdt,bcc_usdt,ubtc_usdt,ltc_usdt,...
        :return:
        //# Response
        [
            {
                "currency": "btc",
                "id": "20150928158614292",
                "price": 1560,
                "status": 3,
                "total_amount": 0.1,
                "trade_amount": 0,
                "trade_price" : 6000,
                "trade_date": 1443410396717,
                "trade_money": 0,
                "type": 0
            }...
        ]
        currency : 交易类型
        id : 委托挂单号
        price : 单价
        status : 挂单状态(0：待成交,1：取消,2：交易完成,3：待成交未交易部份)
        total_amount : 挂单总数量
        trade_amount : 已成交数量
        trade_date : 委托时间
        trade_money : 已成交总金额
        trade_price : 成交均价
        type : 挂单类型 1/0[buy/sell]
        '''
        __params =  "accesskey="+self.mykey +\
                    "&currency="+ currency +\
                    "&id="+ id  +\
                    "&method=getOrder"
        return self.__api_call("getOrder", params=__params)



    def zb_get_Orders(self, currency, tradeType, pageIndex = 1):
        '''
        获取多个委托买单或卖单，每次请求返回10条记录
        :param currency:btc_usdt,bcc_usdt,ubtc_usdt,ltc_usdt,...
        :param tradeType: 交易类型1/0[buy/sell]
        :param pageIndex: 当前页数
        :return:
        //# Response
        [
            {
                "currency": "btc",
                "id": "20150928158614292",
                "price": 1560,
                "status": 3,
                "total_amount": 0.1,
                "trade_amount": 0,
                "trade_price" : 6000,
                "trade_date": 1443410396717,
                "trade_money": 0,
                "type": 0
            }...
        ]
        currency : 交易类型
        id : 委托挂单号
        price : 单价
        status : 挂单状态(0：待成交,1：取消,2：交易完成,3：待成交未交易部份)
        total_amount : 挂单总数量
        trade_amount : 已成交数量
        trade_date : 委托时间
        trade_money : 已成交总金额
        trade_price : 成交均价
        type : 挂单类型 1/0[buy/sell]
        '''
        __params =  "accesskey="+self.mykey +\
                    "&currency="+ currency +\
                    "&method=getOrders" +\
                    "&pageIndex="+ str(pageIndex)  +\
                    "&tradeType="+ str(tradeType)

        return self.__api_call("getOrders", params=__params)



    def zb_get_OrdersNew(self, currency, tradeType, pageIndex = 1, pageSize=50):
        '''
        获取多个委托买单或卖单，每次请求返回10条记录
        :param currency:btc_usdt,bcc_usdt,ubtc_usdt,ltc_usdt,...
        :param tradeType: 交易类型1/0[buy/sell]
        :param pageIndex: 当前页数
        :return:
        //# Response
        [
            {
                "currency": "btc",
                "id": "20150928158614292",
                "price": 1560,
                "status": 3,
                "total_amount": 0.1,
                "trade_amount": 0,
                "trade_price" : 6000,
                "trade_date": 1443410396717,
                "trade_money": 0,
                "type": 0
            }...
        ]
        currency : 交易类型
        id : 委托挂单号
        price : 单价
        status : 挂单状态(0：待成交,1：取消,2：交易完成,3：待成交未交易部份)
        total_amount : 挂单总数量
        trade_amount : 已成交数量
        trade_date : 委托时间
        trade_money : 已成交总金额
        trade_price : 成交均价
        type : 挂单类型 1/0[buy/sell]
        '''
        __params =  "accesskey="+self.mykey +\
                    "&currency="+ currency +\
                    "&method=getOrdersNew" +\
                    "&pageIndex="+ str(pageIndex)  +\
                    "&pageSize="+ str(pageSize) +\
                    "&tradeType="+ str(tradeType)

        return self.__api_call("getOrdersNew", params=__params)


    def zb_get_OrdersIgnoreTradeType(self, currency, pageIndex = 1, pageSize=50):
        '''
        :param currency:btc_usdt,bcc_usdt,ubtc_usdt,ltc_usdt,eth_usdt,etc_usdt,bts_usdt,
        :param pageIndex:当前页数
        :param pageSize:每页数量
        :return:
        //# Request
            GET https://trade.zb.com/api/getOrdersIgnoreTradeType?accesskey=youraccesskey&currency=ltc_btc
            &method=getOrdersIgnoreTradeType&pageIndex=1&pageSize=1
            &sign=请求加密签名串&reqTime=当前时间毫秒数
            //# Response
            [
                {
                    "currency": "btc",
                    "id": "20150928158614292",
                    "price": 1560,
                    "status": 3,
                    "total_amount": 0.1,
                    "trade_amount": 0,
                    "trade_price" : 6000,
                    "trade_date": 1443410396717,
                    "trade_money": 0,
                    "type": 0
                }...
            ]

            currency : 交易类型
            id : 委托挂单号
            price : 单价
            status : 挂单状态(0：待成交,1：取消,2：交易完成,3：待成交未交易部份)
            total_amount : 挂单总数量
            trade_amount : 已成交数量
            trade_date : 委托时间
            trade_money : 已成交总金额
            trade_price : 成交均价
            type : 挂单类型 1/0[buy/sell]
        '''
        __params =  "accesskey="+self.mykey +\
            "&currency="+ currency +\
            "&method=getOrdersIgnoreTradeType" +\
            "&pageIndex="+ str(pageIndex)  +\
            "&pageSize="+ str(pageSize)

        return self.__api_call("getOrdersIgnoreTradeType", params=__params)

if __name__ == '__main__':


    access_key    = 'accesskey'
    access_secret = 'secretkey'

    api = zb_trade_api(access_key, access_secret)

    #print trade_api.zb_get_account()
    #print trade_api.zb_get_Order('12313131', "eos_usdt")
    #print api.zb_get_OrdersNew("eos_usdt", zb_trade_api.TradeType_BUY , pageIndex= 1)
    #print api.zb_get_OrdersNew("eos_usdt", zb_trade_api.TradeType_BUY , pageIndex= 2)
    #print api.zb_get_OrdersNew("eos_usdt", zb_trade_api.TradeType_SELL , pageIndex= 1)
    #print api.zb_get_OrdersNew("eos_usdt", zb_trade_api.TradeType_SELL , pageIndex= 2)

    print api.zb_get_OrdersNew("eos_usdt", zb_trade_api.TradeType_BUY , pageIndex= 1)
    print api.zb_get_OrdersNew("eos_usdt", zb_trade_api.TradeType_SELL , pageIndex= 1)
    print api.zb_get_OrdersIgnoreTradeType("eos_usdt" , pageIndex= 1)
