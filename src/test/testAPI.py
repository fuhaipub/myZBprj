# -*- coding: utf-8 -*-
import httplib
import urllib
import json

import time

from subprocess import call


class Employee:
   '所有员工的基类'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1

   def __del__(self):
       class_name = self.__class__.__name__
       print "class is deleted,name = " + class_name

   def displayCount(self):
     print "Total Employee %d" % Employee.empCount

   def displayEmployee(self):
      print "Name : ", self.name,  ", Salary: ", self.salary



if __name__ == '__main__':

    e = Employee("ding",800);
    d = Employee("ding",800);
    print "Employee.__doc__:", Employee.__doc__
    print "Employee.__name__:", Employee.__name__
    print "Employee.__module__:", Employee.__module__
    print "Employee.__bases__:", Employee.__bases__
    print "Employee.__dict__:", Employee.__dict__

