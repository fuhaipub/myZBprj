# -*- coding: utf-8 -*-
import httplib
import urllib
import json

import time

from subprocess import call






if __name__ == '__main__':
    cmd = 'display notification \"' + \
        "Notificaton memo" + '\" with title \"Titile\"'

    call(["osascript", "-e", cmd])