# -*- coding: utf-8 -*-
"""
Created on 1402/12/17 
    @author: ks
    last update 1402/12/17
"""
#k_form
def var_compare(x1,x2,None_to_str=True):
    '''
    goal:
    ------
        compare 2 str (supposed) var
    '''
    if None_to_str:
        if x1==None:x1=''
        if x2==None:x2=''
    if x1==x2:
        return {'ok':True,'msg':' = : ' + str(x1)}
    else:
        y1=var_inf(x1)
        y2=var_inf(x2)
        return {'ok':False,'msg':f" ! : {y1['type']}({y1['len']}),{y2['type']}({y2['len']}) -- {y1['str']},{y2['str']}"}
def var_inf(x):
    l=''
    s=''
    if x:
        try:
            l=str(len(x))
            s=str(x)
        except:
            pass
    return {'type':type(x),'len':l,'str':s}