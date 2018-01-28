# -*- coding: utf-8 -*-

import sys

from collections import deque
from src.api.zb_data_api import zb_data_api
import time, threading
import sys, os
import processor

reload(sys)
sys.setdefaultencoding('utf-8')

class DSManager(object):
    pass


class Datasource(object):


    def __init__(self, market, filePath = ""):
        self.describers= []
        self.marketType = market
        self.isRun = False
        self.event_storefile = filePath.strip() if filePath.strip() != "" else "history_"+market +".dat"
        self.que = deque()
        self.__reload()

    def __reload(self):
        #从文件读取json加载到队列中
        try:
            if not os.path.exists(self.event_storefile): return

            with open(self.event_storefile) as jsondata:
                self.que.extend([line.strip() for line in jsondata.readlines() if line.strip() != ""])
        except Exception, ex:
            print "Fail to reload even history, excpetion:"+ str(ex)

    def addDescriber(self,collector):
        self.describers.append(collector)

    def __start(self):
        if self.isRun == True:
            return

        self.isRun = True
        zb = zb_data_api()
        try:
            file = open(self.event_storefile, "a+")
        except Exception, ex:
            self.isRun = False
            print ex
            return

        def loop():
            zb = zb_data_api()

            while self.isRun :
                res =  zb.zb_get_ticker(self.marketType)
                self.que.append(res)
                file.writelines(str(res)+"\n")
                file.flush()
                #print res
                time.sleep(1)
        self.t = threading.Thread(target=loop, name='LoopThread'+ self.marketType)
        self.t.setDaemon(True) #保证父进程退出时,子进程能主动退出
        self.t.start()

    def __join(self):
        self.t.join()

    def __stop(self):
        self.isRun = False

    def __pop(self):
        return self.que.popleft() if len(self.que) > 0 else None

    def __getEvent(self):
        return self.__pop()

    def run(self):
            self.__start()
            while True:

                event = self.__getEvent()
                if event is None:
                    time.sleep(0.05) #每50毫秒调度一次
                    continue

                for describer in self.describers:
                    try:
                        describer.do(event)
                    except Exception, ex:
                        print "Datasource market="+self.marketType+". Exception:"+str(ex)
            #self.__join()



if __name__ == '__main__':

    ds_bts = Datasource("eos_usdt")
    print str(len(ds_bts.que))

    a = processor.Processor("a")
    b = processor.Processor("b")
    c = processor.Processor("c")
    ds_bts.addDescriber(a)
    ds_bts.addDescriber(b)
    ds_bts.addDescriber(c)

    ds_bts.run()

    '''
    print str(len(ds.que))
    print ds.event_storefile

    ds.start()
    time.sleep(5)
    ds.stop()
    '''
