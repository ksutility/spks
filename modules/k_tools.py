# -*- coding: utf-8 -*-
"""
Created on 1402/12/17 
    @author: ks
    last update 1402/12/17
"""
debug=False
from functools import wraps
import time
import k_err
    
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
def x_cornometer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1=time.time()
        xxx=func(*args, **kwargs)
        if debug:
            t2=time.time()
            try:
                tt1=nth_item_of_dict(nth_item_of_dict(kwargs,0),0)
            except:
                tt1='*err* => nth_item_of_dict'
            try:
                tt2=",".join([kwargs[x] for x in kwargs if type(kwargs[x])==str])
            except:
                tt2='*err* '    
                
            dtm1="{:.4f}".format(t2-t1) #delta time 1
            tm1='{:.4f}'.format(t1 % 1000) #time 1
            tm2='{:.4f}'.format(t2 % 1000) #time 2
            #k_err.xxxprint(msg=[dtm1,tm1,tm2],vals=kwargs)
            t3=time.time()
            tm3='{:.4f}'.format(t3 % 1000) #time 3
            dtm2='{:.4f}'.format(t3-t2) #delta time 2
            print('--------{} , {} : {} - {} , func = {} , {} , args = {}'.format(dtm1,dtm2,tm1,tm3,func.__name__,tt1,tt2))
        return xxx
    return wrapper
def nth_item_of_dict(xdic,n,up_result=''):
    '''
    inputs:
    -------
        up_result:value for return if n > xdic.len
            > is used becuse index is start from 0
    '''
    if n>=len(xdic):return up_result
    x=list(xdic)[n]
    return xdic[x]