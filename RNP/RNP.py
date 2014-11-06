# -*- coding:utf-8 -*-
# !/usr/bin/env python

import re

OPT = {}
OPT['#'] = 0
OPT['('] = 1
OPT['+'] = 2
OPT['-'] = 2
OPT['*'] = 4
OPT['/'] = 4
OPT['//'] = 4
OPT['%'] = 4
OPT['**'] = 6
OPT[')'] = 8

    
def addSpace(matched): #为数字前后插入空格
    num = matched.group("number")
    addedspace = ' ' + num + ' '
    return addedspace

def deal_SourceStr(inputStr): #正则，找出数字，插入空格
    '''make num and opt split with space'''
    #pattern = re.compile('(?P<number>\d+)')
    Replaced_space_Str = re.sub("(?P<number>\d+)", addSpace, inputStr)
    ReplacedStr = Replaced_space_Str.split(' ')[1:]
    return deal_con_opt(ReplacedStr)

def deal_con_opt(ReplacedStr): #处理连在一起的操作符
    '''deal  the opt once connected'''
    Result_String = []
    for each in ReplacedStr:
        if isnumber(each):
            Result_String.append(each)
        else:
            opt = list(each)
            for i in opt:
                Result_String.append(i)
    return Result_String

def isopt(opt):
    '''returns True if opt is in OPT'''
    return opt in OPT 

def isnumber(opt): #判断是否为数字
    '''returns True if opt is a number'''
    return all(c in '0123456789' for c in opt)

def deal_user_input(user_input):
    '''make user input to the same format''' 
    deal_space = user_input.split(' ')
    source = ''.join(deal_space)
    return source

def RNP_Func(OpStack,SourceList,SourceStr):
    DesList = []
    for opt in SourceList:
        if isnumber(opt):    #若当前操作符为数字。进队列。
            DesList.append(opt)
        elif isopt(opt):         #若当前操作符为运算符
            top_stack = OpStack[len(OpStack)-1] #取得栈顶元素
            if opt == '(':     #若当前运算符为'(',直接压栈
                OpStack.append(opt)
                OPT[opt] = OPT[opt]+1
            elif opt == ')':   #若当前操作符为')',取出OpStack中的元素，直到遇到'('
                while top_stack != '(':
                    top_stack = OpStack.pop()
                    DesList.append(top_stack)
                    top_stack = OpStack[len(OpStack)-1]
                else:
                    OpStack.pop()
            elif OPT[opt]<OPT[top_stack]: #当前运算符优先级小于栈顶运算符
                flags = True              #栈顶运算符出栈，并且入队列DesList，当前运算符入栈
                while flags:              #直到遇到当前运算符大于栈顶运算符，停止
                    top_stack = OpStack.pop()
                    DesList.append(top_stack)
                    top_stack = OpStack[len(OpStack)-1]
                    flags = OPT[opt]<OPT[top_stack]
                OpStack.append(opt)
                OPT[opt] = OPT[opt]+1
            else:# OPT[opt]>=OPT[top_stack]: #当前运算符优先级高于栈顶运算符，当前运算符压栈
                OpStack.append(opt)
                OPT[opt] = OPT[opt]+1 
        else :
            DesList[:] = []
            break
    if len(DesList)!= 0:
        while len(OpStack)>0:
            each = OpStack.pop()
            DesList.append(each)
        return ''.join(DesList[:-1])
    else:
        print 'invalid input : ' +SourceStr
        return False
    
def main():
    user_input = raw_input('Please input your formula: \n')
    SourceStr = deal_user_input(user_input)
    SourceList = deal_SourceStr(SourceStr)
    OpStack.append('#')
    result = RNP_Func(OpStack,SourceList,SourceStr)
    print result

    

if __name__ == "__main__":
    main()
