# -*- coding: utf-8 -*-

from src.workflow.filter import Filter, DefaultFilter
from src.workflow.pattern import Pattern
from src.workflow.policy import Policy, Action
from src.workflow.context import WorkflowContext  as wc
import src.api.zb_data_api as dapi
import src.api.zb_trade_api as tapi
import time



class TopSellFilter(Filter):
    def __init__(self):
        super(TopSellFilter, self).__init__()
        pass

    def filter(self,event):
        #todo 过滤一些时间上过于老旧的数据
        print "TopSellFilter: 过滤一些时间上过于老旧的数据"
        return True



class TopSellPattern(Pattern):
    def __init__(self):
        super(TopSellPattern, self).__init__()
        pass

    def matching(self, event):
        #todo 匹配上涨的顶峰区间
        print "TopSellPattern: matching 匹配上涨的顶峰区间"
        self.result={"action":"buy"}
        return True


class TopSellAction(Action):
    def __init__(self):
        super(TopSellAction, self).__init__()

    def do(self, newEvent):
        print "TopSellAction: newEvent="+ str(newEvent)


class TopSellPolicy(Policy):
    def __init__(self):
        super(TopSellPolicy, self).__init__()

    def rule(self, newEvent):
        print "TopSellPolicy: newEvent="+ str(newEvent)
        return True



if __name__ == '__main__':


    #创建数据源
    ds = wc.getDSManager().createDS("DS_BTS","bts_usdt")

    wc.createWorkflow("workflow_topsell",ds,[DefaultFilter(),TopSellFilter()],TopSellPattern(), TopSellPolicy(), TopSellAction())

    wc.start()
    time.sleep(10)
    wc.stop()
