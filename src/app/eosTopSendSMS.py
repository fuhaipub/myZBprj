# -*- coding: utf-8 -*-

from src.workflow.filter import Filter, DefaultFilter
from src.workflow.pattern import Pattern
from src.workflow.policy import Policy, Action
from src.workflow.context import WorkflowContext  as wc
import src.api.zb_data_api as dapi
import src.api.zb_trade_api as tapi
from src.api.utils import *
import time



class EosTopFilter(Filter):
    def __init__(self):
        super(EosTopFilter, self).__init__()
        pass

    def filter(self,event):
        #todo 过滤一些时间上过于老旧的数据

        #print "EosTopFilter: 过滤一些时间上过于老旧的数据"

        evttime = event["date"]

        if time.time() - float(evttime)/1000  > 60 :
            print "Filter("+ self.__class__.__name__+"): Time is too old. discard Event=" + str(event)
            return False  #一分钟之前的老数据过滤掉

        return True



class EosTopPattern(Pattern):
    def __init__(self):
        super(EosTopPattern, self).__init__()
        pass

    def matching(self, event):  #通过重载一个matching来判断是否符合模式;如果符合模式,讲想要输出的结果放到result中,传递给Policy和Action,并返回True
        #todo 匹配上涨的顶峰区间


        self.result = {}
        alarmPrice_high = 98.0
        alarmPrice_low  = 91.0
        rate = 6.7
        lastPrice = float(event["ticker"]["last"]) * 6.7

        if lastPrice >= alarmPrice_high:
            self.result={"date": event["date"], "alarmtype": "high", "lastprice_rmb":lastPrice }
            print "Pattern("+ self.__class__.__name__+"):  matching 匹配高位价格,result="+ str(self.result)
            return True
        elif lastPrice <= alarmPrice_low:
            self.result={"date": event["date"], "alarmtype": "low", "lastprice_rmb":lastPrice }
            print "Pattern("+ self.__class__.__name__+"):  matching 匹配低位价格,result="+ str(self.result)
            return True

        print "Pattern("+ self.__class__.__name__+"): EOS价格"+str(lastPrice)+"在["+str(alarmPrice_low)+","+str(alarmPrice_high)+\
              "]之间, unmatched event=" + str(event)
        return False


class EosTopAction(Action):
    def __init__(self):
        super(EosTopAction, self).__init__()

    def do(self, newEvent):  #实现真正要做的事情

        alarmtype = newEvent["alarmtype"]
        lastprice = float(newEvent["lastprice_rmb"])

        tip = "上涨" if alarmtype == "high" else "下跌"

        message = "Eos 价格(人民币)"+tip+"超过"+ str(lastprice)+"元."
        mac_notify(message)
        self.isSend = True
        print "Mac OS Notify:"+message


class EosTopPolicy(Policy):
    def __init__(self):
        super(EosTopPolicy, self).__init__()
        self.lasttime = 0

    def isDone(self, newtime):
        if newtime - self.lasttime < 60 * 1000:
            return True
        else:
            self.lasttime = newtime
            return False

    def rule(self, newEvent):  # 增加规律判断代码,如果通过,返回True, 不满足返回False

        if  self.isDone(float(newEvent["date"])):
            return False

        return True
