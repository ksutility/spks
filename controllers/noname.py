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
    session['noname_un']=_noname_ip(request.client)
    if session.view_page=='save':
        session.view_page=''
        if 'auto_hide' in request.args:
            return 'j_box_iframe_win_close'
    session.view_page='xform'
    session['update_step']=True
    res=k_form._xform(['body'])
    form_name=('فرم '+ res['c_form_htm'].x_data_s['base']['title']) if res['c_form_htm'] else ''
    finish=(res['htm_form']['form_editable']==False) if ('htm_form' in res) and (res['htm_form']) else False
    return dict(htm=res['htm'],form_name=form_name,finish=finish)
    #cg_link=res['link']
    #k_form._xform())
def xtable_i():
    return dict(htm=DIV(
        H1("با سپاس فراوان از همکاری شما",_class="text-center"),
        DIV("احتمال وجود مشکل در سیستم-شاید همه فیلدها تعریف نشده باشند",_class="text-center")))
def _noname_ip(xip):
    '''1404/03/12
        امکان تکمیل 1 فرم به صورت ناشناس - گام 3 - گمنام سازی اطلاعات ردگیری سیستم
    '''
    import k_date
    today=k_date.ir_date('yy-mm-dd')
    td_s=today.split("-")#td=today
    tdn=sum([int(td_i)*(11**i) for i,td_i in  enumerate(td_s)]) #11 is 1 random number for remaining the processes unknown (hidden)
    
    xip_s=xip.split(":")
    ip_s=xip_s[0].split(".")
    ip_ni=[int(ip_i)*(256**i) for i,ip_i in enumerate(ip_s)]
    ipn=sum(ip_ni) 
    e=xip_s[1] if len(xip_s)>1 else ''
    return str(ipn+tdn)+"-"+e