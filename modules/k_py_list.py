#!/usr/bin/env python
# -*- coding: utf-8 -*-
def list2dict(list1,list2):
    if len(list1)!=len(list2):
        print (f"error in list2dict len(list1)={len(list1)},len(list2)={len(list2)}")
        return False
    dd={x:list2[i] for i,x in enumerate(list1)}
    xxxprint(vars={'dd':str(dd),'list1':str(list1),'list2':str(list2)})
    return dd
def dif_report(list1,list2):
    for i,x in enumerate(list1):
        if x!=list2[i]:
            print (f"dif in pos( {i} ) :  {x} <> {list2[i]}")
class List_tools(object):
    def dif_report(self,list1,list2):
        for i,x in enumerate(list1):
            if x!=list2[i]:
                print (f"dif in pos( {i} ) :  {x} <> {list2[i]}")