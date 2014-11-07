# -*- coding:utf-8 -*-
#!/usr/bin/env python

import threading

class MyThread(threading.Thread):
    def __init__(self, func, args, name = ''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        print self.name, 'start...'
        self.res = apply(self.func, self.args)
        print self.name, 'end...'

    def getResult(self):
        return self.res
