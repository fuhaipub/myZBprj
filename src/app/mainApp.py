# -*- coding: utf-8 -*-

from src.workflow.context import WorkflowContext  as wc
from src.app.topSell import *
from src.app.eosTopSendSMS import *

if __name__ == '__main__':


    #创建数据源
    #ds_bts = wc.getDSManager().createDS("DS_BTS","bts_usdt")
    ds_eos = wc.getDSManager().createDS("DS_EOS","eos_usdt")

    #wc.createWorkflow("workflow_BtsTopSell",ds_bts,[DefaultFilter(),TopSellFilter()],TopSellPattern(), TopSellPolicy(), TopSellAction())

    wc.createWorkflow("workflow_EosTopSendSmS",ds_eos,[DefaultFilter(),EosTopFilter()],EosTopPattern(), EosTopPolicy(), EosTopAction())
    wc.start()
    time.sleep(1000)
    wc.stop()
