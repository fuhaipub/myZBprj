# -*- coding: utf-8 -*-
import sys
import Queue
import datasource as ds
import processor as  processor
import time
import pattern
import filter
reload(sys)
sys.setdefaultencoding('utf-8')

class WorkflowContext(object):
    __processorMap = {}

    @staticmethod
    def getDSManager():
        return ds.DSManager

    @classmethod
    def createProcessor(cls, name):
        p = processor.Processor(name)
        cls.__processorMap[name] = p
        return cls.__processorMap[name]

    @classmethod
    def getProcessor(cls):
        return cls.__processorMap

    @classmethod
    def start(cls):
        cls.getDSManager().startWork()

    @classmethod
    def stop(cls):
        cls.getDSManager().stopWork()

    @classmethod
    def createWorkflow(cls, name, datasource, filterChain, pattern, policy, action  ):

        if name.strip() == "" : raise Exception("Workflow name can not be empty string.")
        if datasource is None : raise Exception("Workflow Datasource can not be None.")
        if pattern  is  None  : raise Exception("Workflow pattern can not be None.")
        if policy is None     : raise Exception("Workflow policy can not be None.")
        if action is None     : raise Exception("Workflow action can not be None.")

        proc = cls.createProcessor(name)

        proc.clearFilter()
        if filterChain is not None:
            for f in filterChain:
                proc.addFilter(f)

        proc.addPattern(pattern)

        policy.setAction(action)

        pattern.clearPolicy()
        pattern.addPolicy(policy)

        cls.getDSManager().subscribe(datasource.name , proc)



if __name__ == '__main__':

    wc = WorkflowContext
    wc.getDSManager().createDS("DS_EOS","eos_usdt")
    wc.getDSManager().createDS("DS_BTS","bts_usdt")


    for i in range(1):
        p = wc.createProcessor("Processor_"+str(i))
        pme = pattern.Pattern("Pattern_test")
        filter = filter.DefaultFilter()
        p.addFilter(filter)
        p.addPattern(pattern.Pattern("Pattern_test"))

        wc.getDSManager().subscribe("DS_EOS", p)
        wc.getDSManager().subscribe("DS_BTS", p)

    print wc.getDSManager().getDS()
    print wc.getProcessor()

    wc.start()
    time.sleep(36000)
    wc.stop()







