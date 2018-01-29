# -*- coding: utf-8 -*-

import time

class Action(object):
    def __init__(self):
        pass

    def do(self, newEvent):
        pass



class Policy(object):

    def __init__(self):
        pass

    def setAction(self,action):
        if action is None: raise Exception("Policy action can not be None.")
        self.action = action

    def rule(self, newEvent):
        return True

    def do(self, newEvent):
        if  self.rule(newEvent) is True:
            try:
                self.action.do(newEvent)
            except Exception, ex:
                print "Date:"+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"Failed in exceuting in "+type(self.action)