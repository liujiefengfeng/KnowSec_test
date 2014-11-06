# -*- coding:utf-8 -*-
# !/usr/bin/env python

"""Unit test for nibolan.py"""

import RNP
import unittest

class RNPTest(unittest.TestCase): 
    num = {
        ('0',True),
        ('5',True),
        ('23',True),
        ('88',True),
        ('100',True),
        ('10.0',False),
        ('-2',False) ,   
        }
    OPT = {
        ('+',True),
        ('-',True),
        ('*',True),
        ('(',True),
        ('#',True),
        ('&',False),
        ('$',False),
        }

    Input_example = ['1+ 2','1+2 * 3','1 + 2 * 3 / 5','1+ 2*3/ (5+4)']
    Input_answer = ['1+2','1+2*3','1+2*3/5','1+2*3/(5+4)']
    
    RNP_example = ['1:2','1+2*3','1+2*3/5','1+2*3/(5+4)']
    RNP_answer = [False,'123*+','123*5/+','123*54+/+']

    #def setUp(self);
     #   self.
    def testIsnumberFunc(self):
        for number,flags in self.num:
            result = RNP.isnumber(number)
            self.assertEqual(flags,result)
            
    def testIsoptFunc(self):
        for opt,flags in self.OPT:
            result = RNP.isopt(opt)
            self.assertEqual(flags,result)
            
    def testUserInputFunc(self):
        for i in range(len(self.Input_example)-1):
            result = RNP.deal_user_input(self.Input_example[i])
            self.assertEqual(self.Input_answer[i],result)

    def testMainFunc(self):
        for i in range(len(self.RNP_example)-1):
            result = RNP.RNP_Func(['#'],self.RNP_example[i],self.RNP_example[i])
            self.assertEqual(self.RNP_answer[i],result)

 
if __name__ == "__main__":
    unittest.main()
