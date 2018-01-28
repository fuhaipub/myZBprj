# -*- coding: utf-8 -*-


class Pattern(object):
    def __init__(self,name ):
        self.name  = name
        self.policys = []
        self.result= {}

    def addPolicy(self,policy):
        self.policys.append(policy)

    def matching(self, event):
        print "Enter Pattern ["+self.name+"], event="+ str(event)
        pass

    def run(self,event):
        if self.matching(event) is True:
            for p in self.policys:
                p.do(self.result)