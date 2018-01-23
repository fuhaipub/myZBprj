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


        """
    >>> import json
    >>> js = json.loads('{"haha": "哈哈"}')
    >>> print json.dumps(js)
    {"haha": "\u54c8\u54c8"}

    解决办法很简单:

    >>> print json.dumps(js, ensure_ascii=False)
    {"haha": "哈哈"}



      eos["ticker"]["buy"] * 6.7,
      eos["ticker"]["sell"] * 6.7,
      eos["ticker"]["last"] * 6.7,
      eos["ticker"]["high"] * 6.7,
      eos["ticker"]["low"] * 6.7,
      eos["ticker"]["vol"] * 6.7
    """