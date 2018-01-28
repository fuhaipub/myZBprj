# -*- coding: utf-8 -*-
import pattern

class Processor(object):
    def __init__(self, name):
        self.name = name
        self.filters = []
        self.patterns = []

    def addFilter(self,filter):
        self.filters.append(filter)

    def clearFilter(self):
        self.filters=[]

    def addPattern(self, p):
        self.patterns.append(p)

    def clearPattern(self):
        self.patterns = []

    def do(self, event):

        flag = True
        for filter in self.filters:
            if filter.filter(event) is False:
                flag = False
                continue

        if flag is True :
            for p in self.patterns:
                p.run(event)



if __name__ == '__main__':

    pass

