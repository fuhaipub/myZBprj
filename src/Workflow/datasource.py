# -*- coding: utf-8 -*-

import sys

from collections import deque
from src.api.zb_data_api import zb_data_api
import time, threading
import sys, os
import processor
import yaml

reload(sys)
sys.setdefaultencoding('utf-8')

class DSManager(object):
    __DSmap = {}
    __threads ={}

    @classmethod
    def createDS(cls, dsname, market,filepath=""):
        ds = Datasource(dsname, market, filepath)
        cls.__DSmap[dsname] = ds
        return cls.__DSmap[dsname]

    @classmethod
    def removeDS(cls,dsname):
        if cls.__DSmap.has_key(dsname) :
            del cls.__DSmap[dsname]

    @classmethod
    def subscribe(cls,dsname, sub_processor):
        cls.__DSmap[dsname].addSubscriber(sub_processor)

    @classmethod
    def getDS(cls):
        return cls.__DSmap

    @classmethod
    def startWork(cls):
        for (k, ds) in cls.__DSmap.items() :
            cls.__threads[k] = threading.Thread(target=ds.run, name='DSThread'+ k)
            cls.__threads[k].setDaemon(True) #保证父线程退出时,子线程能主动退出
            cls.__threads[k].start()
            print "Datasource ["+k+"] start work..."

    @classmethod
    def stopWork(cls):
        for (k, ds) in cls.__DSmap.items() :
            ds.stop()
            cls.__threads[k].join()
            print "Datasource ["+k+"] stop work."
        cls.__threads = []




class Datasource(object):


    def __init__(self, name, market, filePath = ""):
        self.name = name
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

    def addSubscriber(self, processor):
        self.describers.append(processor)

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
                time.sleep(1)
        self.t = threading.Thread(target=loop, name='LoopThread'+ self.marketType)
        self.t.setDaemon(True) #保证父进程退出时,子进程能主动退出
        self.t.start()

    def __pop(self):
        return yaml.safe_load(str(self.que.popleft()).strip()) if len(self.que) > 0 else None

    def __getEvent(self):
        return self.__pop()

    def __join(self):
        self.t.join()

    def __stop(self):
        self.isRun = False

    def run(self):
            self.__start()
            self.runflag= True
            while self.runflag :

                event = self.__getEvent()
                if event is None or event == "":
                    time.sleep(0.05) #每50毫秒调度一次
                    continue

                for p in self.describers:
                    try:
                        p.do(event)
                    except Exception, ex:
                        print "Datasource market="+self.marketType+". Exception:"+str(ex)

    def stop(self):
        self.runflag = False
        self.__stop()
        self.__join()



if __name__ == '__main__':
    pass