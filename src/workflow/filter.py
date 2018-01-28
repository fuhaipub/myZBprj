# -*- coding: utf-8 -*-
import datasource
import src.api


class Filter(object):
    def __init__(self):
        pass

    def filter(self, event):
        pass


class DefaultFilter(Filter):
    def __init__(self):
        super(DefaultFilter, self).__init__()
        pass

    def filter(self, event):
        print "DefaultFilter: 过滤结果中包含 error的事件"
        if  event.has_key("error") :
            return False
        return True





