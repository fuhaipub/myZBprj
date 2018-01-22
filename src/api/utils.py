# -*- coding: utf-8 -*-
import httplib
import urllib
import json

import time

from subprocess import call

def mac_notify( message, title = "ZB实时交易通知" ):
    cmd = 'display notification \" ' + message  + '\" with title \"' +title +'\"'
    call(["osascript", "-e", cmd])






if __name__ == '__main__':

    mac_notify("EOS开始大涨,请注意行情")