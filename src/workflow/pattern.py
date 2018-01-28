# -*- coding: utf-8 -*-


class Pattern(object):
    def __init__(self ):
        self.policies = []
        self.result= {}

    def addPolicy(self,policy):
        self.policies.append(policy)

    def clearPolicy(self):
        self.policies= []

    def matching(self, event):
        return True

    def run(self,event):
        if self.matching(event) == True:
            for p in self.policies:
                p.do(self.result)