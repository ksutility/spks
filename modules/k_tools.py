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
    #print(f"*** x= {x}")
    #print(str(xdic[x]))
    return xdic[x]
#class X_DIC():
def server_is_test():
    from gluon import current
    srv_port=current.request.env.SERVER_PORT 
    return (srv_port == '50' or srv_port == '150')
def server_is_python():
    from gluon import current
    srv_port=current.request.env.SERVER_PORT 
    return srv_port == '100' or srv_port == '150'
def server_python_add():
    from gluon import current
    ip='http://192.168.88.179'
    ip="""http://"""+ current.request.env.HTTP_HOST.partition(":")[0]
    if server_is_test():
        return ip+":150"
    else:
        return ip+":100"
def access_from_internet():
    from gluon import current
    u_ip=str(current.request.client)
    return True if u_ip[:11]!='192.168.88.' else False
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
        self.refer=current.request.env.HTTP_REFERER
    def check_refer(self,ref_f,cur_f):
        from gluon import current
        '''
        
        refer=current.request.env.HTTP_REFERER
        if not refer or (not url in refer):
            response.redirect(url)
        print('refer='+ refer)
        print("---=="+request.env.HTTP_REFERER)
        '''
        rf=current.session.view_page
        if rf !=ref_f :
            if rf == cur_f:
                msg= """شما دوبار متوالی این صفحه را اجرا کردید 
                        برای جلوگیری از خطا های ممکن در اثر 2 باره نویسی اطلاعات 
                        این فرایند متوقف شد
                       """
            else:
                msg= """ارجای شما به این صفحه به صورت نا مناسب بوده است
                       """
            from gluon.html import URL 
            from gluon.http import redirect
            redirect(URL('spks','form','msg',vars={'msg':msg}))     
        current.session.view_page=cur_f
    def set_refer(self,cur_f): 
        from gluon import current
        current.session.view_page=cur_f
def int_force(x,n):
    try:
        return int(x)
    except:
        return n
def list_list__2__list_list(in_rows,in_titels,out_titles):
    '''
    inputs:
    ------
        in_rows=list of row =list of list
    '''
    out_rows=[]
    for row in in_rows:
        out_row=[row[in_titels.index(out_title)] for out_title in out_titles]
        out_rows+=[out_row]
    return out_rows        
def list_dict__2__list_list(in_list_dict,out_titles):
    '''
    inputs:
    ------
        in_list_dict= rows = list of row =list of dict
    '''
    out_rows=[]
    for x_dic in in_list_dict:
        out_row=[x_dic[out_title] for out_title in out_titles]
        out_rows+=[out_row]
    return out_rows        