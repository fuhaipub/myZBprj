# -*- coding: utf-8 -*-


import time

from subprocess import call

def mac_notify( message, title = "ZB实时交易通知" ):
    cmd = 'display notification \" ' + message  + '\" with title \"' +title +'\"'
    call(["osascript", "-e", cmd])



if __name__ == '__main__':

    mac_notify("行情开始大涨,请注意")