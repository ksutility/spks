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
    y1=var_inf(x1)
    y2=var_inf(x2)    
    if x1==x2:
        return {'ok':True,'msg': f"({y1['str']} = {y2['str']})"}
    else:
        return {'ok':False,'msg':f"({y1['str']} != {y2['str']}) : {y1['type']}({y1['len']}) != {y2['type']}({y2['len']}) "}
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
#class X_DIC():
def server_is_test():
    from gluon import current
    srv_port=current.request.env.SERVER_PORT 
    #print (f"srv_port == {srv_port} , srv_port == '50' :{srv_port == '50'}")
    return (srv_port == '50' or srv_port == '150')
def server_is_python():
    from gluon import current
    srv_port=current.request.env.SERVER_PORT 
    #print (f"srv_port == {srv_port} , srv_port == '50' :{srv_port == '50'}")
    return srv_port == '100' or srv_port == '150'
def server_python_add():
    ip='http://192.168.88.179'
    if server_is_test():
        return ip+":150"
    else:
        return ip+":100"
class X_DICT():
    def __init__(self,in_dic):
        self.x_dic=in_dic.copy()
    def add(self,in_dic):
        self.x_dic.update(in_dic)
        return self.x_dic
class C_URL():
    def __init__(self):
        from gluon import current
        url_f=current.request.url.split("/")[3]
        uri=url_f.split(".")
        self.ext=uri[1] if len(uri)>1 else ''
        self.port=current.request.env.SERVER_PORT 

    