# -*- coding: utf-8 -*-
# ver 1.00 1402/09/12
# -------------------------------------------------------------------------
''' value help
    x_data :# all form "extra data" that read from x_data.py file
        ساختار اطلاعات کل فرمها که از فایل مربوطه خوانده می شود
    x_data_s :# selected x_data = x_data for <select db_file><select table>    
'''
from gluon.custom_import import track_changes; track_changes(True)
from k_sql import DB1
import k_htm
import k_form
from k_err import xxprint,xprint,xalert,xreport_var,xxxprint
from x_data import x_data ,x_data_verify_task
import k_date
import k_tools,k_user
k_user.how_is_connect('form')
from k_time import Cornometer
now = k_date.ir_date('yy/mm/dd-hh:gg:ss')
# import datetime
# now = datetime.datetime.now().strftime("%H:%M:%S")

debug= False #True #False # True: for check error
db_path='applications\\spks\\databases\\'


style1=XML('''
        <style>
            table {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              text-align: center;
              width: 100%;    }

            table td, #customers th {
              border: 1px solid #ddd;
              padding: 8px; }

            table tr:nth-child(even){background-color: #f2f2f2;}

            table tr:hover {background-color: #ffccaa;}

            table th {
              padding: 8px;
              padding-top: 12px;
              padding-bottom: 12px;
              border: 1px solid #ddd;
              
              color: white; }
        </style>
      ''')
def _get_init_data():
    '''
    اطلاعات مورد نیاز را حسب آدرس صفحه از اطلاعات ساختاری جدول مورد نظر استخراج می کند
    output:
    -------
    return down inf according args in 1 url page
        x_data_s :#
        db_name:str
        tb_name:str    
    '''
    #global: x_data
    args=request.args
    if len(args)>0:
        if args[0] not in x_data:
            return False,'','',f'error: >  "{args[0]}" not defined in Fieldes'
        db_name=args[0]
        #print (db_name)
        if len(args)<2:args+=['a']
        tb_name=args[1]# if len(args)>1 else 'a'
        
        if not db_name in x_data:return False,'','','error : "{}" not in ( x_data )'.format(db_name)
        x_data_s1=x_data[db_name]#x_data_select
        
        tb_n1=tb_name if (len(tb_name)<7) or (tb_name[-7:]!='_backup') else tb_name[:-7]
        if (not tb_n1 in x_data_s1):
            return False,'','','error : "{}" not in ( x_data["{}"] )'.format(tb_name,db_name)
        x_data_s=x_data_s1[tb_n1]
        return x_data_s,db_name,tb_name,'ok'
    return False,'','','error : args not set correctly'    
#--------------------------------------------
class C_FILTER():
    """
    old:
        _def get_table_filter(tasks,x_data_s)
    output:
    ------
        select_cols, all_cols
        htm()
    """
    def __init__(self,tasks,x_data_s):
        '''
            use in:2(show_xtable,show_kxtable)
        goal:
        ------
            -show input filter form for customizing filter data
            نمایش فرم فیلتر جهت تنظیم اطلاعات فیلتر ها
            -set new_value of filter data in goal variabl
            
        
        output:
        ------
            select_cols, all_cols,htm_table_filter
        '''
        #share data for class
        self.tasks=tasks
        self.x_data_s=x_data_s
        
        

        cols_filter=x_data_s['cols_filter']
        self.cols_filter_obj={'name':'cols_filter','type':'select','select':cols_filter,'add_empty_first':False}#,$hlp='prop':["can_add"],}
        data_filter=x_data_s['data_filter'] 
        
        data_filter={k_form.template_parser(x):y for x,y in data_filter.items()}
        def_value=k_form.template_parser(x_data_s['base'].get('data_filter',''))
        self.data_filter_obj={'name':'data_filter','type':'select','select':data_filter,'def_value':def_value,'add_empty_first':False}
        
        #import k_err
        #k_err.xreport_var([data_filter,self.data_filter_obj])
        
        all_cols=list(tasks.keys())
        #print(f'all_cols={all_cols}')
        
        flt=request.vars['cols_filter']
        if flt:
            if flt[0]=='#':
                select_cols=cols_filter[int(flt[1:])] 
            else:
                flt_list=flt.split(',')
                if flt_list[0][0] in [0,1,2,3,4,5,6,7,8,9] :
                    select_cols = [all_cols[int(x)] for x in flt_list]
                else:
                    select_cols = flt_list
        else:
            select_cols= all_cols
        self.select_cols=select_cols
        self.all_cols=all_cols
        self.htm=self._htm()
    def set_htm_var(self,caption,obj,width='15vw',_help='',_val='',_meta=''):
        '''
        inputs:
        ------
            obj:str / dict
                str : object name
                dict: object props
        '''
        
        import x_data, k_js,k_htm
        
        if type(obj)==str:
            name=obj
            val=request.vars.get(name,_val)
            xw=f"width={width}" if width else ""
            tt=f'''<input {_meta} name='{name}' id='{name}' value='{val}' class='input-filter' style='width:100%;''>'''
            tjs=''
        else:
            name=obj['name']
            name2=name+'-x'
            obj['onchange']=f"document.getElementById('{name}').value=document.getElementById('{name2}').value;"
            x_data.x_data_verify_task(name2,obj)
            obj['def_value']=request.vars.get(name2,obj['def_value'])
            val=request.vars.get(name,_val) or obj['def_value']
            if width:obj['width']=width
            tt=XML(k_form.obj_set(i_obj=obj,x_dic={},x_data_s=self.x_data_s, need=['input'],request=request)['input'])
            ##import k_err
            ##k_err.xreport_var([tt,XML(tt),obj,self.x_data_s])
            tt+=f'''<input {_meta} name='{name}' id='{name}' value='{val}' class='input-filter' >'''
            tjs=k_js.toggle(clicking_name=name+"_label",hiding_name=name)
            obj['value']=val #===> output
        xcap=f"""<label id='{name}_label'><a title='{_help}'>{caption}</a></label>"""
        tt1=k_htm.xtd([[xcap,4],[tt,8]])
        
        
        return  f'''<td style='width:{width};'>
                            {tt1}
                        </td>
                    ''' +tjs       
    def _htm(self):
        hlp={'cols_filter':'''
                    text    => result
                    ---------------------------------
                            => show all defined cols in data_str
                    #1      => filter by cols_filter[1]
                    1,3,4   => show cols[1],cols[3],cols[4]
                    des,prj => shoe cols['des'],cols['prj']''',
                    
            'data_filter':'''
                   "des" like "%L%"
                   "prj"="29" AND "des" like "%L-%"
                   date_e > "1401/09/01"
                ''',
            'prj':'''
                
            '''
            }
        return XML('<form><table id="table_filter"><tr style="height:10px;padding:0px;margin:0px">'
                    #+set_htm_var(caption='prj',width='20vw',obj=data_filter1,_help=hlp['data_filter'])
                    +self.set_htm_var(caption='فیلتر اطلاعات',width='30vw',obj=self.data_filter_obj,_help=hlp['data_filter'])
                    +self.set_htm_var(caption='فیلتر ستونها',width='30vw',obj=self.cols_filter_obj,_help=hlp['cols_filter'])
                    +self.set_htm_var(caption='حالت نمایش',obj='table_class',width='10vw',_val=2,_meta="type='number' min=-1 max=6",_help='1 to 6')
                    +self.set_htm_var(caption='صفحه',obj='data_page_n',width='10vw',_val=1,_meta="type='number' min=1" ,_help='صفحه شماره')
                    +self.set_htm_var(caption='تعداد',obj='data_page_len',width='10vw',_val=20,_meta="type='number'" ,_help='تعداد ردیف در هر صفحه')
                    +'<td><input type="submit" value="انجام"></td></tr></table></form>')
    #return select_cols, all_cols,htm_table_filter,

#===================================================================================================================
def xform():#view 1 row
    
    if request.vars['text_app']:
        return save()
    session.view_page='xform'
    if not session.username:
        return dict(htm=H1("لطفا اول وارد سیستم بشوید"))
    '''
    goal:
        show / manage a formated & costomize form
        show only cols/fields/task that defied in data_structur and 'hide' str not in its 'prop' attbute
        
    '''
    def show_form(x_data_s,db1,tb_name,xid):#show 1 form 
        x_color={'x':'danger','y':'success','r':'warning','':''}
        def show_step_1_row(x_data_s,xid,form_sabt_data,field_name,mode):
            #mode='output'/'input'
            fd=x_data_s['tasks'][field_name]#fd=field_data
            htm_1=A(fd['title'],_title=field_name)#htm_1=html for 1th_part(=field name) of row
            if 'hide' in fd['prop']:
                return [htm_1,'*','']
            x_obj=k_form.obj_set(i_obj=fd,x_dic=form_sabt_data,x_data_s=x_data_s,xid=xid, need=[mode],request=request)
            
            return [htm_1,x_obj[mode],x_obj['help']]
            #------------------------------------------------- 
        def chidman(hx,x_data_s,step):
            jobs_title=k_user.jobs_title(step['jobs'],x_data_s)
            form_case=int(request.vars['form_case'] or '2')
            if form_case==1:
                return [DIV(DIV(hx['stp'],_class='col text-right'), DIV(jobs_title,_title=step['jobs'],_class='col text-warning',_dir='rtl'),_class='row text-light bg-dark' )]+hx['data']+[
                    DIV(DIV(_class="col"),*[DIV(x,_class=f"col {hx['app-color']}") for x in hx['app']],_class=f"row")
                    ]
                #return DIV(DIV(hx['stp'],_class='col-2 text-right border-left'),DIV(htm_1,_class='col-10'),_class='row border-bottom')
            elif form_case==2:
                htm_1=[DIV(x,_class='row') for x in hx['app']]
                return DIV(
                    DIV(DIV(hx['stp'],_class='row'),DIV(jobs_title,_title=step['jobs'],_class='row text-warning'),_class='col-2 text-right border-left text-light bg-dark'),
                    DIV(hx['data'],_class='col-8'),
                    DIV(htm_1,_class=f"col-2 {hx['app-color']}"),
                    _class="row border-bottom "),
        def show_step_not_cur(x_data_s,xid,form_sabt_data,step,mode): #like=row_view
            '''
                0209012
            INPUT:
            ------
                mode:str ('b'/'a')
                    b=befor of cur
                    a=aftre of cur
            '''
            fsc_mode={"a":"form_step_after","b":"form_step_befor","c":"form_step_cur_unactive"}[mode] #form_step_class
            hx={'data':[],'stp':'','app':[]}
            htm_1=[]
            for field_name in step['tasks'].split(','):
                if field_name in x_data_s['labels']:
                    hx['data']+=[DIV(DIV(x_data_s['labels'][field_name],_class="col text-center bg-info text-light"),_class='row border-top')]
                else:
                    hh=show_step_1_row(x_data_s,xid,form_sabt_data,field_name,mode='output')
                    hx['data']+=[DIV(DIV(hh[0],_class='col-3 text-right'),DIV(hh[1],_class='col-6 text-right'),DIV(hh[2],_class='col-3 text-right'),_class='row border-top')]
            #breakpoint()
            def val_in_dic(x_dict,v_name):
                '''
                    goal:extract item_val(=return) from dict(=x_dict) by its item_name(=v_name)
                '''
                v_name=v_name or '' # NONE => ''
                v_name=v_name.lower()
                return x_dict.get(v_name,v_name)
            #print("step[i]="+str(step["i"]))
            #print("==>"+str(form_sabt_data[f'step_{step["i"]}_un']))   
            hx['app']=[ 
                        (val_in_dic(step['app_kt'],form_sabt_data[f'step_{step["i"]}_ap'])),
                        (" توسط "+val_in_dic(k_user.all_users.inf,form_sabt_data[f'step_{step["i"]}_un']).get('fullname','')),
                        (" در تاریخ "+(form_sabt_data[f'step_{step["i"]}_dt'] or '')),
                        ]
            # breakpoint()
            hx['app-color']="bg-"+val_in_dic(x_color,form_sabt_data[f'step_{step["i"]}_ap'])
            hx['stp']=[str(step['i']+1) +' - '+ step['title']]
            

            return DIV(chidman(hx,x_data_s,step),_class="container-fluid "+fsc_mode)#DIV(,_style="background-color:#555;")
        def show_step_cur(x_data_s,xid,form_sabt_data,step): #like=row_edit
            '''
                0209012 
            '''
            hx={'data':[],'stp':'','app':[]}
            for field_name in x_data_s['steps'][step_n]['tasks'].split(','):
                if field_name in x_data_s['labels']:
                    hx['data']+=[DIV(DIV(x_data_s['labels'][field_name],_class="col text-center bg-info text-light"),_class='row border-top')]
                else:
                    hh=show_step_1_row(x_data_s,xid,form_sabt_data,field_name,mode='input')
                    hx['data']+=[DIV(DIV(hh[0],_class='col-3 text-right'),DIV(hh[1],_class='col-6 text-right'),DIV(hh[2],_class='col-3 text-right'),_class='row border-top')]
            hx['app']=[BUTTON(step['app_kt'][xx],_type='BUTTON',_class=f'w-100 btn btn-{x_color[xx]}',_onclick=f"app_key('{xx}')") for xx in step['app_kt']]
            hx['stp']=[str(step['i']+1) +' - '+ step['title']]
            hx['app-color']=''
            return FORM(DIV(chidman(hx,x_data_s,step),_class="container-fluid form_step_cur"),INPUT(_type='hidden',_id='text_app',_name='text_app',_value='')
                        ,_id="form1") #,_action=URL('save',args=request.args)
        def app_review (): 
            '''
                0209018
            '''
            htm_1=[DIV(
                    DIV('',_class='col-4'),
                    DIV(BUTTON("بازبین مرحله آخر",_type='submit',_class='btn ',_onclick=f"app_key('r')"),_class='col-4'), 
                    DIV('',_class='col-4')
                    ,_class='row')]
            htm_1+=[HR()]
            htm= FORM(DIV(htm_1,_class="container form_step_cur"),INPUT(_type='hidden',_id='text_app',_name='text_app',_value='')
                        ,_action=URL('save_app_review',args=request.args),_id="form1") 
            return XML(k_htm.x_toggle_s(XML(htm),sign='...'))
        #-- def show_form:start ----------------------------------------------
        def inf_g():
            rows,titles,rows_num=db1.select(tb_name,where={'id':xid})
            #xxxprint(msg=[str(xid),'where id='+str(xid),'len rows='+str(len(rows))+'--- (xid==-1) : '+str(xid=='-1')])
            
            if xid=='-1':
                form_sabt_data={x:'' for x in titles}
                f_nxt_s=0
            elif not rows:
                return '',0,''    
            else:
                form_sabt_data=dict(zip(titles,rows[0]))
                f_nxt_s=form_sabt_data['f_nxt_s']
                f_nxt_u=form_sabt_data['f_nxt_u']
                if f_nxt_s:
                    if f_nxt_u=="x":
                        f_nxt_s=-int(f_nxt_s)
                    else:
                        f_nxt_s=int(f_nxt_s)
                else:
                    f_nxt_s=0
            steps=x_data_s['steps']
            return form_sabt_data,f_nxt_s,steps
        form_sabt_data,f_nxt_s,steps=inf_g() #form_sabt_data=all field data that is in form of sabt 
        
        form_case_dic={'1':'عمودی','2':'افقی'}
        htm_form=[ FORM(DIV(
                        DIV(x_data_s['base']['title'],_class='col-8 bg-info text-center text-light h3 border-left'),
                        DIV(' ثبت شماره ' + xid ,_class='col-2 bg-info text-center text-light h6 '),
                        DIV('حالت نمایش',_class='col-1'),
                        DIV(k_htm.select(_options=form_case_dic,_name='form_case',_value=request.vars['form_case'] or '2',_onchange="submit();"),
                            #BUTTON('',_type='submit',_style="display:hidden"),
                            _class='col-1'),
                        _class='row  '))] #align-items-center ,_style="height:50px;  margin: auto;align-items: center;" align-middle vh-100
        
        if form_sabt_data:
            step_befor='' # svae name of before step
            for i,step_n in enumerate(x_data_s['steps']):
                step=x_data_s['steps'][step_n]
                step['i']=i
                if i == f_nxt_s:
                    
                    if k_user.user_in_jobs_can('edit',x_data_s,form_sabt_data,step_index=i):
                        #k_user.can_user_edit_step(step=step,step_index=i,form_sabt_data=form_sabt_data):
                        #k_user.user_in_jobs(step['jobs'],row_data=form_sabt_data):
                        htm_form+=[show_step_cur(x_data_s,xid,form_sabt_data,step)]
                    else :
                        # show revize buttom نشان دادن دکمه بازبینی مرحله آخر
                        if step_befor and k_user.user_in_jobs_can('edit',x_data_s,form_sabt_data,step_index=i-1):
                            #step_befor and k_user.step_changer(i-1,form_sabt_data)==session['username'] :
                            #k_user.user_in_jobs(x_data_s['steps'][step_befor]['jobs'],row_data=form_sabt_data):
                            htm_form+=[app_review()]
                        htm_form+=[DIV(HR(),'   /\   '+'شما اجازه تکمیل این بخش را ندارید'+'   /\   ',_class='form_step_cur_unactive text-center text-light')]
                        #htm_form+=[DIV(DIV(_class='col-1'),DIV([show_step_not_cur(x_data_s,xid,form_sabt_data,step,'c')],_class='col-10'),DIV(_class='col-1'),_class='row')]
                        htm_form+=[DIV([show_step_not_cur(x_data_s,xid,form_sabt_data,step,'c')])]
                        htm_form+=[DIV('   \/   '+'شما اجازه تکمیل این بخش را ندارید'+'   \/   ',HR(),_class='form_step_cur_unactive text-center text-light')]
                else:
                    if 'order' in step and k_user.user_in_jobs_can('edit',x_data_s,form_sabt_data,step_index=i):
                        htm_form+=[show_step_cur(x_data_s,xid,form_sabt_data,step)]
                    else:
                        ab_case="b" if i < f_nxt_s else "a"
                        htm_form+=[show_step_not_cur(x_data_s,xid,form_sabt_data,step,ab_case)]
                step_befor=step_n
            # show revize buttom نشان دادن دکمه بازبینی مرحله آخر
            # if "end_step is field(form is compelete)" and "cur_user is end_step owner"
            if (f_nxt_s >=len(x_data_s['steps']) and k_user.user_in_jobs_can('edit',x_data_s,form_sabt_data,step_index=f_nxt_s-1)):
                #k_user.user_in_jobs(k_tools.nth_item_of_dict(x_data_s['steps'],f_nxt_s-1)['jobs'],row_data=form_sabt_data)):
                # test = form(morakhsi_saat).rec(15 steps=comple) : user(mlk) =>can view (app_review but) ,other users(atl,ks,..) cannot view (app_review but)
                htm_form+=[app_review()]
            # if "previus_step result = x (form is omit)" and "cur_user is previus_step owner"
            elif (f_nxt_s < 0 and k_user.user_in_jobs_can('edit',x_data_s,form_sabt_data,step_index=-f_nxt_s)):
                #k_user.user_in_jobs(k_tools.nth_item_of_dict(x_data_s['steps'],-f_nxt_s)['jobs'],row_data=form_sabt_data):
                # test = 
                htm_form+=[app_review()]
            
        bx=x_data_s['base']
        xlink=URL('sabege',args=(bx['db_name'],bx['tb_name']+"_backup",xid))
        x_arg=request.args[:2]
        xid=int(xid)
        args=request.args
        htm_form+=[XML(k_htm.x_toggle_s(DIV(
                A('T',_title='نمایش جدول مربوطه',_href=URL('data','xtable',args=args[:2]+['edit']+[args[2]]),_class='btn btn-primary'),'-',
                A('تغییرات',_title='تغییرات این ثبت از فرم',_href='javascript:void(0)',_onclick=f'j_box_show("{xlink}")',_class='btn btn-primary'),'-',
                A('+',_title='فرم بعدی',_href=URL('xform',args=x_arg+[str(xid+1)]),_class='btn btn-primary'),'-',  
                A('-',_title='فرم قبلی',_href=URL('xform',args=x_arg+[str(xid-1)]),_class='btn btn-primary')
                ))),
                A('لیست فرم',_href=URL('xtable',args=args),_class='btn btn-primary')]
        return DIV(htm_form,_dir="rtl")
    #-- def xform:start ------------------------------------------------------------
    x_data_s,db_name,tb_name,msg=_get_init_data()
    db1=DB1(db_path+db_name+'.db')
    xid=request.args[2] or 1
    return dict(htm=show_form(x_data_s,db1,tb_name,xid))
# ------------------------------------------------------------------------------------------ 
def _save_out(htm_form,tt,args,err_show=False):
    sec=2500 if err_show or (debug and session["admin"]) else .5
    htm_form+=[DIV(DIV(DIV(A('بازگشت به فرم',_href=URL('xform',args=args),_class="btn h4 btn-primary text-light"),_class="col-7"),
                    DIV("ثانیه تا برگشت اتوماتیک به فرم",_class="col-4 h6 text-right"),
                    DIV("timer",_id="x_time_counter",_class="col-1 bg-info text-light h3 text-center"),
                    _class="row"),
                    _class="container")]
    htm_form+=[tt]
    htm_form+=[XML("""
    <script>
        $( document ).ready(function() {
            $("a.toggle").click();
        });
        var sec=""" + str(sec) + """;
        var redirect_timer = setTimeout(function() {
            window.location='""" + URL('xform',args=args) + """'
        }, sec * 1000);
        setInterval(time_counter, 1000);
        function time_counter() {
            document.getElementById("x_time_counter").innerHTML = sec;
            sec+=-1
        }
    </script>
    """)]
    #return htm_form
def save():
    '''
    GOAL:
        save 1 row
    '''
    
    #چک کردن عدم ذخیره مجدد اطلاعات به دلیل ریلود شدن صفحه 
    if session.view_page!='xform' :
        return 'refer to this page is uncorrect'
    session.view_page='save'
    def save1(text_app,xid):
        def get_vv(f_nxt_s,f_nxt_s_new,reset=False):
            '''
                تهیه یک دیکشنری از اطلاعاتی که قرار است در دیتا بیس به روز رسانی شوند
                reset:
                    True:all field in cur step of form shoud be reset =>(set to '')
                    False:all field in cur step of form shoud be save
            '''
            steps=x_data_s['steps']
            step=steps[list(steps.keys())[f_nxt_s]]
            step_flds=step['tasks'].split(',')
            rv=list(request.vars)
            #breakpoint()
            #vv={t:request.vars[t] for t in rv if t in step_flds }
            #xxxprint(msg=['++',f_nxt_s,step],args=step_flds,vals=request.vars)
            vv={}
            for t in step_flds:#t=field name
                t_req=request.vars[t]
                if t in x_data_s['labels']:
                    continue
                if x_data_s['tasks'][t]['type']=='file':
                    continue
                if 'uniq' in x_data_s['tasks'][t]:
                    url = f"""/spks/km/uniq_inf.json/{x_data_s['base']['db_name']}/{x_data_s['base']['tb_name']}/{t}"""
                    data = {'uniq_value':t_req,'uniq_where':x_data_s['tasks'][t]['uniq']};
                    #xxx->return f"""url={url}<br>data={str(data)}"""
                vv[t]=(lambda x:','.join(x) if type(x)==list else (x or " ").strip())(request.vars[t]) if not reset else ''
            #vv={t:(lambda x:','.join(x) if type(x)==list else (x or " ").strip())(request.vars[t])  for t in step_flds} # multiple select refine output # 021203
            c_form=k_form.C_FORM(x_data_s,xid,vv)
            dict2=c_form.set_step_app(f_nxt_s) 
            dict2.update(c_form.set_form_app(f_nxt_s_new))
            vv.update(dict2)
            return vv
        def update(text_app,xid):
            rr=''
            if text_app=='r': 
                result=db1.row_backup(tb_name,xid)
                f_nxt_s_new = str(f_nxt_s-1)
                rr="backup<br>"+"<br>".join([f'{x}={str(y)}' for x,y in result.items()])
            elif text_app=='x':
                f_nxt_s_new = str(f_nxt_s)#"x-"+
            elif text_app=='y':
                f_nxt_s_new = str(f_nxt_s+1)
            vv=get_vv(f_nxt_s,f_nxt_s_new,reset=(text_app=='x'))    
            #xxx->return "vv=<br>"+str(vv),"update not done"
            xu = db1.update_data(tb_name,vv,{'id':xid})
            
            p1=A("#",_onclick="$(this).next().toggle()",_class='toggle')
            p2=DIV(XML(f"{db1.get_path()}<br> UPDATE: <hr>{rr}<hr>"))
            return DIV(p1,p2,k_htm.val_report(xu)),xu
        def insert():
            vv=get_vv(0,1)
            #xreport_var([vv])
            r1=db1.insert_data(tb_name,vv)#.keys(),vv.values())
            #rr=f"{db1.get_path()}<br> INSERT:result=" + "<br>".join([f'{x}:{r1[x]}' for x in r1])
            
            p1=A("#",_onclick="$(this).next().toggle()",_class='toggle')
            p2=DIV(XML(f"{db1.get_path()}<br> INSERT:<hr>"))
            #rr=f"{db1.get_path()}<br> INSERT:{k_htm.val_report(r1)}"
            return DIV(p1,p2,k_htm.val_report(r1)),r1['id'],r1
        #--------------------------------    
        if xid=='-1':
            r1,xid,r_dic=insert()
        else:
            r1,r_dic=update(text_app,xid)
        return DIV(XML(r1)),xid,r_dic
        #--------------------------------    
    x_data_s,db_name,tb_name,msg=_get_init_data()
    #xxxprint(msg=[db_name,tb_name,msg],vals=x_data_s)
    db1=DB1(db_path+db_name+'.db')
    htm_form=[]
    xid=request.args[2] or 1
    htm_form=[DIV('request.args= '+str(request.args[2]),_class="row")]
    rows,titles,rows_num=db1.select(tb_name,where={'id':xid})
    #xreport_var([rows,titles])
    #form_sabt_data= data of 1 sabt /record of 1 form
    if xid=='-1':
        form_sabt_data={x:'' for x in titles}
        f_nxt_s=0
    else:
        form_sabt_data=dict(zip(titles,rows[0]))
        f_nxt_s=int(form_sabt_data['f_nxt_s'] or '0')
    steps=x_data_s['steps']
    
    #xreport_var([form_sabt_data,f_nxt_s])
    if request.vars['text_app']:# if form is filled and send for save
        text_app=request.vars['text_app'].lower()
        htm_form=[DIV('text_app= '+request.vars['text_app'],_class="row")]
        tt,xid,r_dic=save1(text_app,xid)

        err_show=False#:True
        try:
            if r_dic['exe']['done'] and xid !=0:
                htm_form+=[DIV("ذخیره تغییرات با موفقیت انجام شد",_class="container bg-info text-light h3 text-center")]
                err_show=False
            else:
                htm_form+=[DIV("ذخیره سازی با مشکل مواجه شد به مسئول سیستم اطلاع دهید",_class="container bg-danger text-light h3 text-center")]
                htm_form+=[DIV("xid =" +str(xid) + " | r_dic['exe']= " + str(r_dic['exe']),_class="container bg-warning text-light h3 text-center")]
                htm_form+=[DIV(r_dic)]
        except Exception as err:
            htm_form+=[DIV("err = " +str(err),_class="container bg-danger text-light h3 text-center")]
            htm_form+=[DIV(r_dic)]
    else:
        tt=''
    #xreport_var([text_app,htm_form,tt,xid])
    args=request.args
    args[2]=xid
    _save_out(htm_form,tt,args,err_show)
    try:
        #
        return dict(htm=DIV(htm_form)) #,x=response.toolbar())
    except Exception as err:
        return DIV(htm_form)
def save_app_review():
    '''
        تغییرات لازم در زمان زدن دکمه بازبینی مرحله آخر
    '''
    if session.view_page!='xform' :
        return 'refer to this page is uncorrect'
    args=request.args
    session.view_page='save'
    x_data_s,db_name,tb_name,msg=_get_init_data()
    db1=DB1(db_path+db_name+'.db')
    xid=request.args[2] or 1
    rows,titles,rows_num=db1.select(tb_name,where={'id':xid})
    form_sabt_data=dict(zip(titles,rows[0]))
    f_nxt_s=int(form_sabt_data['f_nxt_s'] )
    f_nxt_s_new=f_nxt_s-1 if form_sabt_data['f_nxt_u']!='x' else f_nxt_s

    c_form=k_form.C_FORM(x_data_s,xid)
    dict2=c_form.set_step_app(f_nxt_s_new,reset=True) 
    dict2.update(c_form.set_form_app(f_nxt_s_new))
    result=db1.row_backup(tb_name,xid)
    xu = db1.update_data(tb_name,dict2,{'id':xid})
    htm_form=['UPDATE:'] 
    try:
        if xu['exe']['done']:
            htm_form+=[DIV("با موفقیت انجام شد",_class="container bg-info h3 text-center")]
    except:
        pass
    htm_form=[f"{db1.get_path()}<br> UPDATE: "+str(xu)+"<hr> backup<br>"+"<br>".join([f'{x}={str(y)}' for x,y in result.items()])]
    htm_form+=[DIV(A('نمایش فرم',_href=URL('xform',args=request.args),_class="btn h4 btn-primary text-light"))]
    htm_form+=[DIV("timer",_id="div_time_counter",_class="bg-primary")]
    htm_form+=[XML("""
    <script>
        $( document ).ready(function() {
            $("a.toggle").click();
        });
        var sec=0.5;
        var redirect_timer = setTimeout(function() {
            window.location='""" + URL('xform',args=args) + """'
        }, sec * 1000);
        setInterval(time_counter, 1000);
        function time_counter() {
            document.getElementById("div_time_counter").innerHTML = sec;
            sec+=-1
        }
    </script>
    """)]
    try:
        return dict(htm=DIV(htm_form)) 
    except Exception as err:
        return DIV(htm_form) #,x=response.toolbar())
#------------------------------------------------------------------------------------------------------------
def list_0():
    from x_data import x_data_cat
    #x_data_cat=x_data.x_data_cat
    trsx={x:[] for x in x_data_cat}
    n=0
    titels=['n','نام فرم','تعداد منتظر اقدام شما','تعداد کل',""]
  
    for db_name,db_obj in x_data.items():
        for tb_name,tb_obj in db_obj.items():
            if tb_obj['base']['mode']=='form':
                n+=1
                db1=DB1(db_path+db_name+'.db')
                total_n=db1.count(tb_name)['count']
                x_where=f'''f_nxt_u = "{session['username']}"'''
                for_me_n=db1.count(tb_name,where=x_where)['count']
                code=tb_obj['base']['code'] if 'code' in tb_obj['base'] else '900'
                xcat=code[0] 
                n1=len(trsx[xcat])+1
                if session["admin"]:
                    _class="btn btn-primary btn-sm"
                    tools=DIV(
                        A("T",_class=_class,_title="جدول",_href=URL('data','xtable',args=[db_name,tb_name])),"-",
                        A("M",_class=_class,_title="ساخت فیلدهاو جدول",_href=URL("data","rc",args=["creat_table_4_form",db_name,tb_name])) ,"-",
                        A("U",_class=_class,_title="بروز رسانی نتیجه فرم",_href=URL("data","rc",args=["update_f_nxt_u",db_name,tb_name,"do-x"])),"-",
                        A("D",_class=_class,_title="نمایش ستونهای اضافه در جدول",_href=URL("data","rc",args=["columns_dif",db_name,tb_name,"do-x"])),"-",
                        A("A",_class=_class,_title="به روز رسانی فیلدهای اتوماتیک",
                            _href=URL("data","rc",args=["update_auto_filed",db_name,tb_name,"do-x"]
                                    ,vars={'select_cols':XML(','.join([x for x in tb_obj['tasks'] if tb_obj['tasks'][x]['type']=='auto']))}
                                    ))
                    )
                else:
                    tools=''
                tx=[A(tb_obj['base']['title'],_href=URL('xtable',args=[db_name,tb_name])),
                    A(for_me_n,_href=URL('xtable',args=[db_name,tb_name],vars={'data_filter':x_where}),_class="btn btn-primary") if for_me_n else '',
                    total_n,
                    tools,
                    ]
                tn= [DIV(n,_title=code)]  
                tn1= [DIV(n1,_title=code)] 
                trsx[xcat]+=[tn1+tx]
                trsx["-"]+=[tn+tx]
 
    from k_table import K_TABLE
    # tt=['<div class="tab-content">']
    # for cat in x_data_cat:
        # tt+=[XML(k_htm.x_toggle_h(x_data_cat[cat], K_TABLE.creat_htm ( trsx[cat],titels,table_class="1"))) ]      
    # tt+=['</div>']
    tt=[DIV(H3("لیست فرمها",_style="text-align:center;"))]
    tbl={}
    for cat in x_data_cat:
        tbl[cat]=XML(K_TABLE.creat_htm ( trsx[cat],titels,table_class="1")) 
    tt+=[XML(k_htm.tabs(cat_dict=x_data_cat,content_dict=tbl,x_active='2'))]
    server_add=k_tools.server_python_add()
    t0=f"""<hr><div class="row">
        <div class="col">
            <a class='btn btn-primary' target='_blank' href='{server_add}/spks/km/aqc_report_daily_pivot/user_day'>نمودار های جادویی از گزارش عملکرد همکاران طراحی </a>
        </div>
        <div class="col">
            <a class='btn btn-primary' target='_blank' href='{server_add}/spks/km/aqc_report_daily_kytable'>گزارش مدیریتی هفته جاری از گزارش عملکرد همکاران طراحی </a> 
        </div>
    </div>"""
    tt+=[XML(t0)]
    return dict(htm=DIV(tt,_dir='rtl'))
#@k_tools.x_cornometer
def xtable():
    from k_tools import X_DICT
    x_dict=X_DICT({'style':'','script':'','table_filter':'','table_head':'','table':'','btm_mnu':''})
    if not session.username:
        msg=H1("لطفا اول وارد سیستم بشوید")
        return x_dict.add({'table':msg})
    cornometer=Cornometer("xtable")
    def xtable_show(rows,titles,tasks,x_data_s):
        ''' func desc
        goal:
        ------
            - show formated & costomize table 
            - link to edit each row for auth users
        input:
        ------
            tasks:dict
                column/field selected {name:{props}}
            x_data_s:dict
                table data structur
                کل ساختار اطلاعاتی مرتبط با جدول مورد نظر 
                base json inf that tasks is 1 part of it
        test:
        ------
            open url:
                /spks/data/xtable/paper/a
        '''
        


        select_cols='form_v_cols_1'#form_v_cols_full  
        ''' form_v_cols_1=form view columns ALT 1 
            form_v_cols_full= form view columns FULL
        '''
        #thead=THEAD(TR(TH('n',_width='30px'),TH('id',_width='30px'),*[TH(A(tasks[x]['title'],_title=f'{i} : {x}')) for i,x in enumerate(select_cols)]))
        app_dic1={'un':'کاربر','ap':'نتیجه','dt':'زمان'}
        #--table head
        new_titles=[{'name':'n','width':'30px'},{'name':'id','width':'30px'}]
        for st_n,step in x_data_s['steps'].items():
            new_titles+=[{'name':tasks[x]['title'],'title':x} for x in step['tasks'].split(',') if x not in x_data_s['labels']]
            if select_cols=='form_v_cols_full':
                new_titles+=[{'name':"^"+str(step['i']+1)+"-"+y,'title':" مرحله "+f"step_{step['i']}_{x}",'class':'bg-info'} for x,y in app_dic1.items()]
            elif select_cols=='form_v_cols_1':
                new_titles+=[{'name':"^"+str(step['i']+1),'title':" مرحله "+",".join([f"step_{step['i']}_{x}" for x in app_dic1]),'class':'bg-info'}]
        new_titles+=[{'name':"S",'title':'f_nxt_s','width':'30px'},{'name':"U",'title':'f_nxt_u','width':'30px'}]
        #thead=THEAD(TR(*tds))
        #---------------        
        trs=[]
        
        ref_i={}
        #xxxprint(msg=['xdic','',''],reset=True)
        for i,row in enumerate(rows):
            #cornometer.print('a')
            x_dic=dict(zip(titles,row))
            #xxxprint(msg=['xdic','',''],vals=x_dic,launch=True)
            ''' '''
            n=str(i+1)
            idx=f"{x_dic['id']}"
            jobs=k_tools.nth_item_of_dict(x_data_s['steps'],0)['jobs']
            form_url=URL('xform',args=(args[0],args[1],idx))
            id_l=A(idx,_title='open form '+idx,_href=form_url,_class="btn btn-primary") #if session["admin"] or k_user.user_in_jobs(jobs) else n
            cls1='app_'+x_dic[f"f_nxt_u"] if x_dic[f"f_nxt_u"] else ''
            tds=[{'value':n,'class':cls1},{'value':id_l}]
            #cornometer.print('b')
            for st_n,step in x_data_s['steps'].items():
                cornometer2=Cornometer("c2","+ - ")
                x_select_cols=[fn for fn in step['tasks'].split(',') if fn not in x_data_s['labels']]
                tds_i=k_form.get_table_row_view(row[0],row,titles,tasks,x_select_cols,x_data_s,request=request)
                tds+=[{'value':x} for x in tds_i]
                #tds+=[TD(k_form.obj_set(i_obj=tasks[fn],x_dic=x_dic,x_data_s=x_data_s,xid=row[0], need=['output'],request=request)['output']) for fn in step['tasks'].split(',') if fn not in x_data_s['labels']]# fn=field name
                #cornometer2.print('a---b')
                if select_cols=='form_v_cols_full':
                    tds+=[{'value':x_dic[f"step_{step['i']}_{x}"]} for x in app_dic1]
                elif select_cols=='form_v_cols_1':  
                    tds+=[{'value':str(x_dic[f"step_{step['i']}_ap"]),'title':",".join([str(x_dic[f"step_{step['i']}_{x}"]) for x in app_dic1])}]
                #cornometer2.print('a---c')
            cornometer.print('c')
            tds+=[{'value':x_dic[f"f_nxt_s"],'class':cls1},{'value':x_dic[f"f_nxt_u"],'class':cls1}]
            ''' '''
            #tds=k_form.get_table_row_view(row[0],row,titles,tasks,select_cols,x_data_s)
            
            trs+=[tds]
        return trs,new_titles,len(rows)
    #----------------------------------------------------------------------------------------
    #tasks,f_views
    script1=XML('''<script>
        $(document).ready(function(){
            $("table td").click(function(){
                $("#viewcell").text($(this).text());
            });
            $("table th").click(function(){
                $("#viewcell").text($(this).text());
            });
        });
    </script>
    ''' )    
 
    args=request.args
    response.title='xtable-'+'-'.join(args)#[x] for x in range(0,len(args),2)])
      
    x_data_s,db_name,tb_name,msg=_get_init_data()#x_data)
    if not x_data_s:
        return x_dict.add({'table':msg})
    else:
        # check access /auth
        if 'auth' in x_data_s['base']:
            if not (session["admin"] or k_user.user_in_jobs_can('view',jobs=x_data_s['base']['auth'])):
                #k_user.user_in_jobs(x_data_s['base']['auth'])):
                msg=H1("شما اجازه دسترسی به این فرم را ندارید")
                return x_dict.add({'table':msg})
               
        db1=DB1(db_path+db_name+'.db')
        tasks=x_data_s['tasks']
        c_filter=C_FILTER(tasks,x_data_s) 
        filter_data=c_filter.data_filter_obj["value"]#k_form.template_parser(request.vars.get('data_filter'),x_dic={})#eval(flt) if flt else ''
        
        rows,titles,rows_num=db1.select(table=tb_name,where=filter_data,page_n=request.vars['data_page_n'],page_len=request.vars['data_page_len'],order=x_data_s['order'])
        #if rows:rows.reverse()
        trs,new_titles,nr=xtable_show(rows,titles,tasks,x_data_s)
        #import k_err
        #k_err.xreport_var([trs,new_titles])
        from k_tools import C_URL
        c_url=C_URL()
        from k_htm import C_TABLE
        c_table=C_TABLE(new_titles,trs)
        
        if c_url.ext=='': #html
  
            table_class=request.vars['table_class'] if request.vars['table_class'] else '0'
            table1=c_table.creat_htm(table_class)   
            
            #print(f'job={job}')
            if session["admin"] or k_user.user_in_jobs_can('creat',x_data_s,step_index=0):
                #jobs=k_tools.nth_item_of_dict(x_data_s['steps'],0)['jobs']
                #k_user.user_in_jobs(jobs):
                new_record_link=A('+',_class='btn btn-primary',_title='NEW RECORD',_href=URL('xform',args=(args[0],args[1],"-1"))) 
            else:
                new_record_link='-'
            htm_head=DIV(TABLE(TR( TD(new_record_link,_width='20px')
                                ,TD( A("S",_title="Smart Select",_class="btn btn-success",_href=URL('data','select',args=args)),_width='30px')
                                ,TD(A("T",_title="Table",_class="btn btn-primary",_href=URL('data','xtable',args=args,vars=request.vars)),_width='30px')
                                ,TD(A(f"{nr}",_title="تعداد نمایش داده شده"),_width='30px')
                                ,TD(A(f"{rows_num}",_title="تعداد کل بر اساس فیلتر جاری"),_width='30px')
                                ,TD(DIV('...',_id='viewcell',_name='viewcell'))
                                ,TD(x_data_s['base']['title'],_width='10%')
                        )),_style='position:sticky;top:0px')
            import k_date,k_icon
            btm_mnu= DIV(A("XLS",XML(k_icon.download(20)),_title="Download XLS",_class="btn btn-success",_href=URL('xtable.xls',args=args+[args[0]+"_form_"+k_date.ir_date('yymmdd-hhggss')],vars=request.vars)),
                         A("CSV",XML(k_icon.download(20)),_title="Download CSV",_class="btn btn-warning",_href=URL('xtable.csv',args=args+[args[0]+"_form_"+k_date.ir_date('yymmdd-hhggss')],vars=request.vars)))
            return dict(style=style1,script=script1,
                table_filter=c_filter.htm,table_head=htm_head,table=table1,btm_mnu=btm_mnu)
        elif c_url.ext=='xls':
            tt="\ufeff" # BOM
            #return tt+'\n'.join([','.join([str(cel) for cel in row]) for row in [new_titles]+trs])
            return c_table.export_csv(request.args[-1])
            #return dict(data=rows)
        elif c_url.ext=='csv':
            return dict(x=c_table.creat_htm())
#--------------------------------------
def _sabege():
    if len(request.args)<3 :
        return "err: arg number send to fun(sabege) is < 3"
    #breakpoint()
    x_data_s,db_name,tb_name,msg=_get_init_data()
    
    db1=DB1(db_path+db_name+'.db')
    xid=request.args[2] 
    rows,titles,rows_num=db1.select(tb_name,where={'xid':str(xid)})
    def simple_table_rows(rows,titles):
        return TABLE(TR(titles),*[TR(row) for row in rows],_class='table table-bordered')
    return simple_table_rows(rows,titles)
def sabege():
    #sample=   spks/form/sabege/test/b_backup/1
    return dict(table=_sabege())

