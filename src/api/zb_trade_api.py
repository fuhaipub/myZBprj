# -*- coding: utf-8 -*-

import json, urllib2, hashlib,struct,sha,time,sys
import yaml
import zb_error

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
        获得委托挂单信息

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
        (新)获取多个委托买单或卖单，每次请求返回pageSize<100条记录

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

    #未测试
    def zb_get_OrdersIgnoreTradeType(self, currency, pageIndex = 1, pageSize=50):
        '''
        与getOrdersNew的区别是取消tradeType字段过滤，可同时获取买单和卖单，每次请求返回pageSize<100条记录

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

    #未测试
    def zb_get_UnfinishedOrdersIgnoreTradeType(self, currency, pageIndex = 1, pageSize =10):
        '''
        获取未成交或部份成交的买单和卖单，每次请求返回pageSize<=10条记录

        :param currency:btc_usdt,bcc_usdt,ubtc_usdt,ltc_usdt,eth_usdt,etc_usdt,bts_usdt,
        :param pageIndex:当前页数
        :param pageSize:每页数量
        :return:
        //# Request
        GET https://trade.zb.com/api/getUnfinishedOrdersIgnoreTradeType?accesskey=youraccesskey
        &currency=ltc_btc&method=getUnfinishedOrdersIgnoreTradeType&pageIndex=1&pageSize=10
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
            "&method=order" +\
            "&pageIndex="+ str(pageIndex)  +\
            "&pageSize="+ str(pageSize)

        return self.__api_call("getUnfinishedOrdersIgnoreTradeType", params=__params)

    #未测试
    def zb_get_UserAddress(self, currency ):
        '''获取用户充值地址

        :param currency:
        :return:
        //# Request
        GET https://trade.zb.com/api/getUserAddress?accesskey=youraccesskey
        &currency=btc&method=getUserAddress
            &sign=请求加密签名串&reqTime=当前时间毫秒数
        //# Response
        {
            "code": 1000,
            "message": {
                "des": "success",
                "isSuc": true,
                "datas": {
                    "key": "0x0af7f36b8f09410f3df62c81e5846da673d4d9a9"
                }
            }
        }
        key : 地址
        '''
        __params =  "accesskey="+self.mykey +\
            "&currency="+ currency +\
            "&method=getUserAddress"

        return self.__api_call("getUserAddress", params=__params)

    #未测试
    def zb_get_UserWithdrawAddress(self,currency):
        '''
        获取用户认证的提现地址

        :param currency:
        :return:
        //# Request
        GET https://trade.zb.com/api/getWithdrawAddress?accesskey=youraccesskey
        &currency=etc&method=getWithdrawAddress
            &sign=请求加密签名串&reqTime=当前时间毫秒数
        //# Response
        {
            "code": 1000,
            "message": {
                "des": "success",
                "isSuc": true,
                "datas": {
                    "key": "0x0af7f36b8f09410f3df62c81e5846da673d4d9a9"
                }
            }
        }
            key : 地址
        '''
        __params =  "accesskey="+self.mykey +\
            "&currency="+ currency +\
            "&method=getWithdrawAddress"

        return self.__api_call("getWithdrawAddress", params=__params)


    #未测试
    def zb_get_WithdrawRecord(self, currency, pageIndex = 1, pageSize =10):
        '''
        获取数字资产提现记录

        :param currency:
        :return:
        //# Request
        GET https://trade.zb.com/api/getWithdrawRecord?accesskey=youraccesskey
        &currency=eth&method=getWithdrawRecord&pageIndex=1&pageSize=10
            &sign=请求加密签名串&reqTime=当前时间毫秒数
        //# Response
        {
            "code": 1000,
            "message": {
                "des": "success",
                "isSuc": true,
                "datas": {
                    "list": [
                        {
                            "amount": 0.01,
                            "fees": 0.001,
                            "id": 2016042556231,
                            "manageTime": 1461579340000,
                            "status": 3,
                            "submitTime": 1461579288000,
                            "toAddress": "14fxEPirL9fyfw1i9EF439Pq6gQ5xijUmp"
                        }...
                    ],
                    "pageIndex": 1,
                    "pageSize": 10,
                    "totalCount": 4,
                    "totalPage": 1
                }
            }
        }
        code : 返回代码
        message : 提示信息
        amount : 提现金额
        fees : 提现手续费
        id : 提现记录id
        manageTime : 提现处理的时间的时间戳
        status :
        submitTime : 提现发起的时间的时间戳
        toAddress : 提现的接收地址
        '''
        __params =  "accesskey="+self.mykey +\
            "&currency="+ currency +\
            "&method=getWithdrawRecord" +\
            "&pageIndex="+ str(pageIndex)  +\
            "&pageSize="+ str(pageSize)

        return self.__api_call("getWithdrawRecord", params=__params)

    #未测试
    def zb_get_ChargeRecord(self, currency, pageIndex = 1, pageSize =10):
        '''
        获取数字资产充值记录

        :param currency:
        :return:
        //# Request
        GET https://trade.zb.com/api/getChargeRecord?accesskey=youraccesskey
        &currency=btc&method=getChargeRecord&pageIndex=1&pageSize=10
            &sign=请求加密签名串&reqTime=当前时间毫秒数
        //# Response
        {
            "code": 1000,
            "message": {
                "des": "success",
                "isSuc": true,
                "datas": {
                    "list": [
                        {
                            "address": "1FKN1DZqCm8HaTujDioRL2Aezdh7Qj7xxx",
                            "amount": "1.00000000",
                            "confirmTimes": 1,
                            "currency": "BTC",
                            "description": "确认成功",
                            "hash": "7ce842de187c379abafadd64a5fe66c5c61c8a21fb04edff9532234a1dae6xxx",
                            "id": 558,
                            "itransfer": 1,
                            "status": 2,
                            "submit_time": "2016-12-07 18:51:57"
                        }...
                    ],
                    "pageIndex": 1,
                    "pageSize": 10,
                    "total": 8
                }
            }
        }
        code : 返回代码
        message : 提示信息
        amount : 充值金额
        confirmTimes : 充值确认次数
        currency : 充值货币类型(大写)
        description : 充值记录状态描述
        hash : 充值交易号
        id : 充值记录id
        itransfer : 是否内部转账，1是0否
        status : 状态(0等待确认，1充值失败，2充值成功)
        submit_time : 充值时间
        address : 充值地址
        '''
        __params =  "accesskey="+self.mykey +\
            "&currency="+ currency +\
            "&method=getChargeRecord" +\
            "&pageIndex="+ str(pageIndex)  +\
            "&pageSize="+ str(pageSize)

        return self.__api_call("getChargeRecord", params=__params)


    #未测试
    def zb_get_withdraw(self, currency, amount, receiveAddr,safePwd, pageIndex = 1, pageSize =10):
        '''
        提现

        :param currency:
        amount:提现金额(最多小数点后8位数)
        receiveAddr:接收地址（必须是认证了的地址，bts的话，以"账户_备注"这样的格式）
        safePwd: 资金安全密码
        :return:
        //# Request
        GET https://trade.zb.com/api/withdraw?accesskey=youraccesskey&amount=0.0004
        &currency=etc&fees=0.0003&itransfer=0&method=withdraw
        &receiveAddr=14fxEPirL9fyfw1i9EF439Pq6gQ5xijUmp&safePwd=资金安全密码
        &sign=请求加密签名串&reqTime=当前时间毫秒数

        //# Response
        {
            "code": 1000,
            "message": "success",
            "id": "提现记录id"
        }

        code : 返回代码
        message : 提示信息
        id : 提现记录id
        '''
        __params =  "accesskey="+self.mykey +\
            "&amount=" + str(amount) + \
            "&currency="+ currency +\
            "&fees=0"  +\
            "&itransfer=0" + \
            "&method=withdraw"   +\
            "&receiveAddr="+ receiveAddr  +\
            "&pageIndex="+ str(pageIndex)  +\
            "&pageSize="+ str(pageSize)  +\
            "&safePwd="+ safePwd

        return self.__api_call("withdraw", params=__params)


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
    print api.zb_get_UnfinishedOrdersIgnoreTradeType("eos_usdt" , pageIndex= 1, pageSize=10 )
