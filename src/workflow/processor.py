# -*- coding: utf-8 -*-
import pattern

class Processor(object):
    def __init__(self, name):
        self.name = name
        self.filterChain = []
        self.patterns = []

    def addFilter(self,filter):
        self.filterChain.append(filter)

    def clearFilter(self):
        self.filterChain=[]

    def addPattern(self, p):
        self.patterns.append(p)

    def clearPattern(self):
        self.patterns = []

    def do(self, event):
        print "entter processor["+self.name+"] do()"+ str(event)

        flag = True
        for filter in self.filterChain:
            if filter.filter(event) is False:
                flag = False
                continue

        if flag is True :
            for p in self.patterns:
                p.run(event)



if __name__ == '__main__':

    pass

