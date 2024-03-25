# -*- coding: utf-8 -*-
"""
Created on 1400/11/20
@author: ks
update1: 1400/11/20
"""
xx=1
def var_report(var_names_str,var_val,spl=','):
    '''
    var_val:list
    '''
    return spl.join(f'{v}={var_val[i]}' for i,v in enumerate(var_names_str.split(',')))
def alert(msg):
    import tk_ui as ui
    ui.msg(msg)
def input(msg):
    if xx==1:
        print('-'*20+'\n')
        x=input(msg)
        return x
    else:
        import tk_ui as ui
        x=ui.input([['x','','',msg]])['x']
        print ('test1='+x)
        return x
