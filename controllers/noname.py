# -*- coding: utf-8 -*-
# ver 1.00 1404/03/01 - kurosh saadati
'''
noname کاربر ناشناس
        فرم برای کاربرانی که تمایل دارند ناشناس بمانند
        Form for users who wish or need to remain anonymous
'''
import k_form
def xform():
    '''
        nn=noname کاربر ناشناس
        فرم برای کاربرانی که تمایل دارند ناشناس بمانند
        Form for users who wish or need to remain anonymous
    '''
    session['noname_un']=request.client
    if session.view_page=='save':
        session.view_page=''
        if 'auto_hide' in request.args:
            return 'j_box_iframe_win_close'
    session.view_page='xform'
    session['update_step']=True
    res=k_form._xform(['body'])
    return dict(htm=res['htm'],form_name="فرم")
    #cg_link=res['link']
    #k_form._xform())
def xtable_i():
    return dict(htm=H1("با سپاس فراوان از همکاری شما",_class="text-center"))