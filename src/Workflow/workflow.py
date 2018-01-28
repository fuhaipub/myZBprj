# -*- coding: utf-8 -*-
import sys
import Queue


reload(sys)
sys.setdefaultencoding('utf-8')


class Workflow:
    def __init__(self, datasource, collector, streaming, policy, action):
        self.datasource = datasource
        self.collector = collector
        self.streaming = streaming
        self.policy = policy
        self.action = action

    def run(self):
        if  self.datasource is None or \
            self.collector is None or \
            self.streaming is None or \
            self.policy is None or    \
            self.action is None:
            print "Failed: workflow can not work!"
            return

        while True:
            if self.policy.do(self.streaming.do(self.collector.do(self.datasource))) is True:
                if self.action.isSure():
                    self.action.do()






