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
from k_tools import C_URL
c_url=C_URL()
now = k_date.ir_date('yy/mm/dd-hh:gg:ss')
# import datetime
# now = datetime.datetime.now().strftime("%H:%M:%S")
if not session['username']:redirect(URL('spks','user','login',args=['go']))
debug= False #False # True: for check error
db_path='applications\\spks\\databases\\'
x_color={'x':'danger','y':'success','r':'warning','':''}
scripts={'table cell display':
        XML('''<script>
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
        }

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
        
        data_sort_items={'id':'id'}
        data_sort_items.update({x:y['title'] for x,y in x_data_s['tasks'].items()})
        self.data_sort={'name':'data_sort','type':'select','select':data_sort_items,'add_empty_first':False}
        
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
            'data_sort':'''
                
            ''',  
            'prj':'''
                
            '''
            }
        return XML('<form><table id="table_filter"><tr style="height:10px;padding:0px;margin:0px">'
                    #+set_htm_var(caption='prj',width='20vw',obj=data_filter1,_help=hlp['data_filter'])
                    +self.set_htm_var(caption='فیلتر اطلاعات',width='30vw',obj=self.data_filter_obj,_help=hlp['data_filter'])
                    +self.set_htm_var(caption='روش مرتب سازی',width='15vw',obj=self.data_sort,_help=hlp['data_sort'])
                    +self.set_htm_var(caption='فیلتر ستونها',width='30vw',obj=self.cols_filter_obj,_help=hlp['cols_filter'])
                    +self.set_htm_var(caption='حالت نمایش',obj='table_class',width='10vw',_val=2,_meta="type='number' min=-1 max=6",_help='1 to 6')
                    +self.set_htm_var(caption='صفحه',obj='data_page_n',width='10vw',_val=1,_meta="type='number' min=1" ,_help='صفحه شماره')
                    +self.set_htm_var(caption='تعداد',obj='data_page_len',width='10vw',_val=20,_meta="type='number'" ,_help='تعداد ردیف در هر صفحه')
                    +'<td><input type="submit" value="انجام"></td></tr></table></form>'
                    +"""
                        <script>
                            $(document).ready(function() {
                                $("#table_class").change(function() {
                                    var selectedStyle = "w-auto table"+$(this).val();
                                    $("#table_f").removeClass().addClass(selectedStyle);
                                });
                            });
                        </script>
                    """)
    #return select_cols, all_cols,htm_table_filter,

#===================================================================================================================
def xform_sd():
    return dict(htm=_xform(out_items=['body']))#_xform())
def xform():
    return dict(htm=_xform())#_xform())

def _xform(out_items=['head','body','tools']):
    #show all section
    #response.show_toolbar=True #error check
    
    if request.vars['text_app']:
        #print("text_app="+str(request.vars['text_app']))
        if request.vars['text_app'] in ['ir','IR']:
            return XML(save_app_review())
        else:
            return XML(save())
    session.view_page='xform'
    
    '''
    goal:
        show / manage a formated & costomize form
        show only cols/fields/task that defied in data_structur and 'hide' str not in its 'prop' attbute
        
    '''
    #------------------------------------------
    x_data_s,db_name,tb_name,msg=_get_init_data()
    if not x_data_s:
        return dict(htm=msg)
    
    # check access /auth
    auth= k_user.C_AUTH_FORM(x_data_s)
    if not auth.ok:return dict(htm=H1(auth.msg))
    
    #db1=DB1(db_path+db_name+'.db')
    
    xid=request.args[2] or 1
    htm_form=C_FORM_HTM(x_data_s,xid).show_form()
    htm_x=[y for x in out_items for y in htm_form[x]]
    return DIV(FORM(*htm_x,
        INPUT(_type='hidden',_id='text_app',_name='text_app',_value=''),_id="form1")
        ,_dir="rtl")
class C_FORM_HTM():
    #:#view 1 row
    def __init__(self,x_data_s,xid):
        self.x_data_s=x_data_s
        self.xid=xid
        self.c_form=k_form.C_FORM(x_data_s,xid)
        
        if xid=='-1':
            f_nxt_s=0
        #elif not rows:
        #    return c_form,'',0,''    
        else:
            f_nxt_s=self.c_form.form_sabt_data['f_nxt_s']
            f_nxt_u=self.c_form.form_sabt_data['f_nxt_u']
            if f_nxt_s:
                if f_nxt_u=="x":
                    f_nxt_s=-int(f_nxt_s)
                else:
                    f_nxt_s=int(f_nxt_s)
            else:
                f_nxt_s=0
        steps=x_data_s['steps']
        self.f_nxt_s=f_nxt_s
    def show_form(self):#show 1 form 
        x_data_s=self.x_data_s
        xid=self.xid

        def show_step_not_cur(x_data_s,xid,c_form,step,mode): #like=row_view
            '''
                0209012
            INPUT:
            ------
                mode:str ('b'/'a')
                    b=befor of cur
                    a=aftre of cur
            '''
            fsc_mode={"a":"form_step_after","b":"form_step_befor","c":"form_step_cur_unactive"}[mode] #fsc_mode=form_step_class
            hx={'data':[],'stp':'','app':[]}
            
            for field_name in step['tasks'].split(','):
                if field_name in x_data_s['labels']:
                    hx['data']+=[DIV(DIV(x_data_s['labels'][field_name],_class="col text-center bg-info text-light"),_class='row border-top')]
                else:
                    #hh=show_step_1_row(x_data_s,xid,form_sabt_data,field_name,mode='output')
                    hh=c_form.show_step_1_row(field_name,request,mode='output')
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
            form_sabt_data=c_form.form_sabt_data
            hx['app']=[ 
                        (val_in_dic(step['app_kt'],form_sabt_data[f'step_{step["i"]}_ap'])),
                        (" توسط "+val_in_dic(k_user.all_users.inf,form_sabt_data[f'step_{step["i"]}_un']).get('fullname','')),
                        (" در تاریخ "+(form_sabt_data[f'step_{step["i"]}_dt'] or '')),
                        ]
            # breakpoint()
            hx['app-color']="bg-"+val_in_dic(x_color,form_sabt_data[f'step_{step["i"]}_ap'])
            hx['stp']=[str(step['i']+1) +' - '+ step['title']]
            

            return DIV(k_form.chidman(hx,x_data_s,step,request=request),_class="container-fluid "+fsc_mode) #DIV(,_style="background-color:#555;")
        def show_step_cur(x_data_s,xid,c_form,step): #like=row_edit
            '''
                0209012 
                step=x_data_s['steps'][step_n]
            '''
            hx={'data':[],'stp':'','app':[]}
            for field_name in step['tasks'].split(','):
                if field_name in x_data_s['labels']:
                    hx['data']+=[DIV(DIV(x_data_s['labels'][field_name],_class="col text-center bg-info text-light"),_class='row border-top')]
                else:
                    #hh=show_step_1_row(x_data_s,xid,form_sabt_data,field_name,mode='input')
                    hh=c_form.show_step_1_row(field_name,request,mode='input')
                    hx['data']+=[DIV(DIV(hh[0],_class='col-3 text-right'),DIV(hh[1],_class='col-6 text-right'),DIV(hh[2],_class='col-3 text-right'),_class='row border-top')]
            hx['app']=[BUTTON(step['app_kt'][xx],_type='BUTTON',_class=f'w-100 btn btn-{x_color[xx]}',_onclick=f"app_key('{xx}')") for xx in step['app_kt']]
            hx['stp']=[str(step['i']+1) +' - '+ step['title']]
            hx['app-color']=''
            return DIV(k_form.chidman(hx,x_data_s,step,request=request),_class="container-fluid form_step_cur")
                         #,_action=URL('save',args=request.args)
        def app_review (): 
            '''
                0209018
            '''
            htm_1=[DIV(
                    DIV('',_class='col-4'),
                    DIV(BUTTON("بازبین مرحله آخر",_type='submit',_class='btn ',_onclick=f"app_key('ir')"),_class='col-4'), 
                    DIV('',_class='col-4')
                    ,_class='row')]
            #htm_1+=[HR()]
            htm=DIV(htm_1)# FORM(DIV(htm_1,_class="container form_step_cur"),_action=URL('save_app_review',args=request.args),_id="form1") 
            return XML(k_htm.x_toggle_s(XML(htm),sign='اصلاح'))
        #-- def show_form:start ----------------------------------------------
          
        c_form,form_sabt_data,f_nxt_s=self.c_form,self.c_form.form_sabt_data,self.f_nxt_s #,steps=inf_g() #form_sabt_data=all field data that is in form of sabt 
        
        form_case_dic={'1':'عمودی','2':'افقی'}
        htm_form={'body':[]}
        htm_form['head']=[ DIV(
                        DIV(x_data_s['base']['title'],_class='col-8 bg-info text-center text-light h3 border-left'),
                        DIV(' ثبت شماره ' + xid ,_class='col-2 bg-info text-center text-light h6 '),
                        DIV('حالت نمایش',_class='col-1'),
                        DIV(k_htm.select(_options=form_case_dic,_name='form_case',_value='2',_onchange="submit();"), #request.vars['form_case'] or 
                            #BUTTON('',_type='submit',_style="display:hidden"),
                            _class='col-1'),
                        _class='row  ')] #align-items-center ,_style="height:50px;  margin: auto;align-items: center;" align-middle vh-100
        
        if form_sabt_data:
            step_befor='' # svae name of before step
            for i,step_n in enumerate(x_data_s['steps']):
                step=x_data_s['steps'][step_n]
                step['i']=i
                if i == f_nxt_s:
                    
                    if k_user.user_in_jobs_can('edit',x_data_s,form_sabt_data,step_index=i):
                        #k_user.can_user_edit_step(step=step,step_index=i,form_sabt_data=form_sabt_data):
                        #k_user.user_in_jobs(step['jobs'],row_data=form_sabt_data):
                        htm_form['body']+=[show_step_cur(x_data_s,xid,c_form,step)]
                    else :
                        # show revize buttom نشان دادن دکمه بازبینی مرحله آخر
                        if step_befor and k_user.user_in_jobs_can('edit',x_data_s,form_sabt_data,step_index=i-1):
                            #step_befor and k_user.step_changer(i-1,form_sabt_data)==session['username'] :
                            #k_user.user_in_jobs(x_data_s['steps'][step_befor]['jobs'],row_data=form_sabt_data):
                            htm_form['body']+=[app_review()]
                        htm_form['body']+=[DIV(HR(),'   /\   '+'شما اجازه تکمیل این بخش را ندارید'+'   /\   ',_class='form_step_cur_unactive text-center text-light')]
                        
                        htm_form['body']+=[DIV([show_step_not_cur(x_data_s,xid,c_form,step,'c')])]
                        htm_form['body']+=[DIV('   \/   '+'شما اجازه تکمیل این بخش را ندارید'+'   \/   ',HR(),_class='form_step_cur_unactive text-center text-light')]
                else:
                    if 'order' in step and k_user.user_in_jobs_can('edit',x_data_s,form_sabt_data,step_index=i):
                        htm_form['body']+=[show_step_cur(x_data_s,xid,c_form,step)]
                    else:
                        ab_case="b" if i < f_nxt_s else "a"
                        htm_form['body']+=[show_step_not_cur(x_data_s,xid,c_form,step,ab_case)]
                step_befor=step_n
            # show revize buttom نشان دادن دکمه بازبینی مرحله آخر
            # if "end_step is field(form is compelete)" and "cur_user is end_step owner"
            if (f_nxt_s >=len(x_data_s['steps']) and k_user.user_in_jobs_can('edit',x_data_s,form_sabt_data,step_index=f_nxt_s-1)):
                #k_user.user_in_jobs(k_tools.nth_item_of_dict(x_data_s['steps'],f_nxt_s-1)['jobs'],row_data=form_sabt_data)):
                # test = form(morakhsi_saat).rec(15 steps=comple) : user(mlk) =>can view (app_review but) ,other users(atl,ks,..) cannot view (app_review but)
                htm_form['body']+=[app_review()]
            # if "previus_step result = x (form is omit)" and "cur_user is previus_step owner"
            elif (f_nxt_s < 0 and k_user.user_in_jobs_can('edit',x_data_s,form_sabt_data,step_index=-f_nxt_s)):
                #k_user.user_in_jobs(k_tools.nth_item_of_dict(x_data_s['steps'],-f_nxt_s)['jobs'],row_data=form_sabt_data):
                # test = 
                htm_form['body']+=[app_review()]
            
        bx=x_data_s['base']
        xlink=URL('sabege',args=(bx['db_name'],bx['tb_name']+"_backup",xid))
        x_arg=request.args[:2]
        xid=int(xid)
        args=request.args
        htm_form['tools']=[XML(k_htm.x_toggle_s(DIV(
                A('T',_title='نمایش جدول مربوطه',_href=URL('data','xtable',args=args[:2]+['edit']+[args[2]]),_class='btn btn-primary'),'-',
                A('تغییرات',_title='تغییرات این ثبت از فرم',_href='javascript:void(0)',_onclick=f'j_box_show("{xlink}")',_class='btn btn-primary'),'-',
                A('+',_title='فرم بعدی',_href=URL('xform',args=x_arg+[str(xid+1)]),_class='btn btn-primary'),'-',  
                A('-',_title='فرم قبلی',_href=URL('xform',args=x_arg+[str(xid-1)]),_class='btn btn-primary')
                ),'ابزار',color='info')),
                A('لیست فرم',_href=URL('xtable',args=args),_class='btn btn-primary')]
        return htm_form

    #-- def xform:start ------------------------------------------------------------
    
# ------------------------------------------------------------------------------------------ 
def _save_out(xid,err_show=False):
    args=request.args
    if xid:#
        args[2]=xid
        link=URL('xform',args=args)
    else:#call from x_table_i
        link=URL('xtable_i',args=request.args,vars={x:request.vars[x] for x in ['data_filter','data_sort','cols_filter','paper_num','table_class','data_page_n','data_page_len']})
    return _auto_redirect(link,delay=.5,err_show=err_show)+[DIV('request.args= '+str(request.args[2]),_class="row")] 
    
def _auto_redirect(link,delay=.5,err_show=False,title="بازگشت به فرم"):
    sec=2500 if err_show or (debug and session["admin"]) else delay
    htm_form=[DIV(HR(),
                DIV(
                    DIV("timer",_id="x_time_counter",_class="col-2 bg-info text-light h3 text-center"),
                    DIV("ثانیه تا اقدام اتوماتیک :",_class="col-6 h3 text-right"),
                    DIV(A(title,_href=link,_class="btn h4 btn-primary text-light w-100"),_class="col-4"),
                    _class="row"),
                HR(),
                _class="container"),
                ]        
    htm_form+=[XML("""
    <script>
        $( document ).ready(function() {
            $("a.toggle").click();
        });
        var sec=""" + str(sec) + """;
        var redirect_timer = setTimeout(function() {
            window.location='""" + link  + """'
        }, sec * 1000);
        setInterval(time_counter, 1000);
        function time_counter() {
            document.getElementById("x_time_counter").innerHTML = sec;
            sec+=-1
        }
    </script>
    """)]
    return htm_form
def save():
    '''
    GOAL:
        save 1 row
    '''
    #چک کردن عدم ذخیره مجدد اطلاعات به دلیل ریلود شدن صفحه 
    if session.view_page!='xform':
        redirect(URL('xform')) #return 'refer to this page is uncorrect'
    session.view_page='save'
      
    x_data_s,db_name,tb_name,msg=_get_init_data()
    #xxxprint(msg=[db_name,tb_name,msg],vals=x_data_s)
    
    htm_form=[]
    xid=request.args[2] or 1
    
    #xreport_var([form_sabt_data,f_nxt_s])
    if request.vars['text_app']:# if form is filled and send for save
        text_app=request.vars['text_app'].lower()
        htm_form=[DIV('text_app= '+request.vars['text_app'],_class="row")]
        #x_r,xid,r_dic=save1(text_app,xid)
        x_r=k_form.C_FORM(x_data_s,xid).save(new_data=request.post_vars)
        tt,xid,r_dic=x_r['html_report'],x_r['id'],x_r['db_report']
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

    htm_form+=_save_out(xid)
    htm_form+=[tt]
    return DIV(htm_form)
    #try:
    return dict(htm=DIV(htm_form)) #,x=response.toolbar())
    #except Exception as err:
    #   return DIV(htm_form)
def save_app_review():
    '''
        تغییرات لازم در زمان زدن دکمه بازبینی مرحله آخر
    '''
    if session.view_page!='xform' :
        return 'refer to this page is uncorrect'
    session.view_page='save'
    
    x_data_s,db_name,tb_name,msg=_get_init_data()
    xid=request.args[2] or 1
    tt=k_form.C_FORM(x_data_s,xid).save_app_review(request_data=request.vars)
    
    htm_form=_save_out(xid)
    htm_form+=[tt]
    return DIV(htm_form)
    try:
        return dict(htm=DIV(htm_form)) 
    except Exception as err:
        return DIV("*****",htm_form) #,x=response.toolbar())
#------------------------------------------------------------------------------------------------------------
def list_0():
    import k_icon,k_htm
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
                for_me_n_link=A(for_me_n,_href=URL('xtable',args=[db_name,tb_name],vars={'data_filter':x_where}),_class="btn btn-primary") if for_me_n else ''
                
                multi_app=[]
                if for_me_n and 'multi_app' in tb_obj['base']:
                    #print("multi_app="+str(multi_app))
                    for m_a_step,m_a_users in tb_obj['base']['multi_app'].items():
                        if session['username'] in m_a_users:
                            multi_app+=[A(XML(k_icon.auto_app(24)),_href=URL('xtable_i',args=[db_name,tb_name,m_a_step]))]
                if multi_app:
                    for_me_n_link=XML(k_htm.xtd(multi_app+[for_me_n_link]))    
                    
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
                    for_me_n_link,
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
            <h3> گزارش عملکرد همکاران طراحی </h3>
        </div>
        <div class="col">
            <a class='btn btn-primary' target='_blank' href='{server_add}/spks/km/aqc_report_daily_pivot/user_day'>نمودار های جادویی </a>
        </div>
        <div class="col">
            <a class='btn btn-primary' target='_blank' href='{server_add}/spks/km/aqc_report_daily_kytable'>گزارش مدیریتی هفته جاری </a> 
        </div>
        <div class="col">
            <a class='btn btn-primary' target='_blank' href='{server_add}/spks/km/test_ipgrid'>ورود اطلاعات</a> 
        </div>
        <div class="col">
            <a class='btn' target='_blank' href='{URL('km','user_timesheet')}'><img src="{URL('static','icon/3d/timesheet.gif')}" title="تایم شیت" width="40" height="40"></a> 
        </div>
    </div>"""
    tt+=[XML(t0)]
    return dict(htm=DIV(tt,_dir='rtl'))
#@k_tools.x_cornometer
def xtable():
    from k_tools import X_DICT
    x_dict=X_DICT({'style':'','script':'','table_filter':'','table_head':'','table':'','btm_mnu':''})

    #cornometer=Cornometer("xtable")
    
    #----------------------------------------------------------------------------------------
    #tasks,f_views
 
    args=request.args
    response.title='xtable-'+'-'.join(args)#[x] for x in range(0,len(args),2)])
      
    x_data_s,db_name,tb_name,msg=_get_init_data()
    if not x_data_s: return x_dict.add({'table':msg})
    
    # check access /auth
    auth= k_user.C_AUTH_FORM(x_data_s)
    if not auth.ok:return x_dict.add({'table':H1(auth.msg)})
  
    db1=DB1(db_path+db_name+'.db')
    tasks=x_data_s['tasks']
    
    c_filter=C_FILTER(tasks,x_data_s) 
    filter_data=c_filter.data_filter_obj["value"]#k_form.template_parser(request.vars.get('data_filter'),x_dic={})#eval(flt) if flt else ''
    
    if auth.where:
        filter_data=["AND",filter_data,auth.where]#__where__list__
    order=c_filter.data_sort["value"] or x_data_s['order']
    x_select=db1.select(table=tb_name,where=filter_data,result='dict_x',page_n=request.vars['data_page_n'],page_len=request.vars['data_page_len'],order=order)
    # xxxprint(out_case=3, msg=["filter_data",filter_data,""],vals={'filter_data':filter_data,"session['auth_prj']":session['auth_prj'],'sql':x_select["sql"]})
    #if rows:rows.reverse()
    trs,new_titles,nr=_xtable_show(x_select["rows"],x_select['titles'],tasks,x_data_s,c_filter)
    #import k_err
    #k_err.xreport_var([trs,new_titles])
    from k_tools import C_URL
    c_url=C_URL()
    from k_htm import C_TABLE
    c_table=C_TABLE(new_titles,trs)
    
    if c_url.ext=='': #html

        table_class=request.vars['table_class'] if request.vars['table_class'] else '0'
        table1=c_table.creat_htm(table_class,_id="table_f")   
        
        #print(f'job={job}')
        if session["admin"] or k_user.user_in_jobs_can('creat',x_data_s,step_index=0):
            #jobs=k_tools.nth_item_of_dict(x_data_s['steps'],0)['jobs']
            #k_user.user_in_jobs(jobs):
            new_record_link=A('+',_class='btn btn-primary',_title='NEW RECORD',_href=URL('xform',args=(args[0],args[1],"-1"))) 
        else:
            new_record_link='-'
        import k_date,k_icon
        btm_mnu= DIV(A("XLS",XML(k_icon.download(20)),_title="Download XLS",_class="btn btn-success",_href=URL('xtable.xls',args=args+[args[0]+"_form_"+k_date.ir_date('yymmdd-hhggss')],vars=request.vars)),
                     A("CSV",XML(k_icon.download(20)),_title="Download CSV",_class="btn btn-warning",_href=URL('xtable.csv',args=args+[args[0]+"_form_"+k_date.ir_date('yymmdd-hhggss')],vars=request.vars)))
        return dict(style=style1,script=scripts['table cell display'],
            table_filter=c_filter.htm,
            table_head=_xtable_head(x_data_s,x_select,nr,new_record_link),
            table=table1,btm_mnu=btm_mnu)
    elif c_url.ext=='xls':
        tt="\ufeff" # BOM
        #return tt+'\n'.join([','.join([str(cel) for cel in row]) for row in [new_titles]+trs])
        return c_table.export_csv(request.args[-1])
        #return dict(data=rows)
    elif c_url.ext=='csv':
        return dict(x=c_table.creat_htm())
#--------------------------------------
def xtable_i():
    """
        نشان  دادن لسیت فرمهای قابل تغییر توسط من برای تایید دسته جمعی
    """
    if request.vars['text_app']:
        return xtable_i_save()
    session.view_page='xtable_i'
    
    def show_step_cur(x_data_s,step): #like=row_edit
        '''
            0209012 
            step=x_data_s['steps'][step_n]
        '''
        c_form=k_form.C_FORM(x_data_s,-1)
        hx={'data':[],'stp':'','app':[]}
        for field_name in step['tasks'].split(','):
            if field_name in x_data_s['labels']:
                hx['data']+=[DIV(DIV(x_data_s['labels'][field_name],_class="col text-center bg-info text-light"),_class='row border-top')]
            else:
                hh=c_form.show_step_1_row(field_name,request,mode='input')
                hx['data']+=[DIV(DIV(hh[0],_class='col-3 text-right'),DIV(hh[1],_class='col-6 text-right'),DIV(hh[2],_class='col-3 text-right'),_class='row border-top')]
        hx['app']=[BUTTON(step['app_kt'][xx],_type='BUTTON',_class=f'w-100 btn btn-{x_color[xx]}',_onclick=f"app_key('{xx}')") for xx in step['app_kt']]
        hx['stp']=[str(step['i']+1) +' - '+ step['title']]
        hx['app-color']=''
        return hx
    
    from k_tools import X_DICT
    x_dict=X_DICT({'style':'','script':'','table_filter':'','table_head':'','table':'','btm_mnu':DIV([BR()]*5+[HR()]+_auto_redirect(URL('list_0'),delay=10,title='برگشت'))})
                        
    c_url.set_refer(cur_f='xtable_i')
    if len(request.args)<3:return x_dict.add({'table':"اشتباه در ورود اطلاعات مورد نیاز"})
    #x_dict.add({'style':'','table':"اشتباه در ورود اطلاعات مورد نیاز"}) 
    f_nxt_s=request.args[2]
    
    show_filter=True if len(request.args)>3 and request.args[3]=='f' else False
    
    

    response.title='xtable-'+'-'.join(request.args)
      
    x_data_s,db_name,tb_name,msg=_get_init_data()
    if not x_data_s: return x_dict.add({'table':msg})
    
    # check access /auth
    auth= k_user.C_AUTH_FORM(x_data_s)
    if not auth.ok:return x_dict.add({'table':H1(auth.msg)})
  
    db1=DB1(db_path+db_name+'.db')
    tasks=x_data_s['tasks']
    
    c_filter=C_FILTER(tasks,x_data_s) 
    filter_data1=c_filter.data_filter_obj["value"] if show_filter else ''

    filter_data={'f_nxt_u':session["username"],
                    'f_nxt_s':f_nxt_s}
    
    if auth.where or filter_data1:
        filter_data=["AND",filter_data,filter_data1,auth.where]#__where__list__
    order=c_filter.data_sort["value"] or x_data_s['order'] or 'id'
    if order=='None':order='id'
    x_select=db1.select(table=tb_name,where=filter_data,result='dict_x',page_n=request.vars['data_page_n'],page_len=request.vars['data_page_len'],order=order)
    #print(f"filter_data={filter_data}")#x_select['sql']
    trs,new_titles,nr=_xtable_show(x_select["rows"],x_select['titles'],tasks,x_data_s,c_filter)
    if not trs:return x_dict.add({'table':H2(f"هیچ فرمی در مرحله { f_nxt_s } منتظر شما نیست")})
    from k_htm import C_TABLE
    
    #output
    i_x=x_select['titles'].index('id')
    trs1=[[k_htm.checkbox(name="checkbox_"+str(x_select["rows"][i][i_x]))]+tr for i,tr in enumerate(trs)]
    c_table=C_TABLE(['X']+new_titles,trs1)
    table_class=request.vars['table_class'] if request.vars['table_class'] else '0'
    table1=c_table.creat_htm(table_class,_id="table_f")  
    #import k_err
    #k_err.xreport_var([f_nxt_s,x_data_s])
    step=k_tools.nth_item_of_dict(x_data_s['steps'],int(f_nxt_s))
    hx=show_step_cur(x_data_s,step)
    table2=FORM(
            DIV(table1),
            DIV(k_form.chidman(hx,x_data_s,step),_class="container-fluid form_step_cur"),
            INPUT(_type='hidden',_id='text_app',_name='text_app',_value=''),
            _id="form1" #_action=URL('xtable_i_save',args=request.args)
            ) #,_action=URL('save',args=request.args)
    table1=k_htm.form(inner_html=table1,action=URL('xtable_i_save',args=request.args))    
    return dict(
        style=style1,
        script=scripts['table cell display'],
        table_filter=c_filter.htm if show_filter else '***',
        table_head=_xtable_head(x_data_s,x_select,nr,''),
        table=table2,btm_mnu="")
def xtable_i_save():

    if session.view_page!='xtable_i':
        redirect(URL('xtable_i',args=request.args,vars=request.vars)) #return 'refer to this page is uncorrect'
    session.view_page='xtable_i_save'
    
    #چک کردن عدم ذخیره مجدد اطلاعات به دلیل ریلود شدن صفحه 
    #c_url.check_refer(ref_f='xtable_i',cur_f='xtable_i_save')

    tt=""
    xid_list=[]
    if request.vars:
        for x in request.vars:
            if "checkbox_" in x:
                n=x[9:]
                xid_list+=[n]
                tt+="<br>" + str(n) + ":" + str(request.vars[x])
    x_data_s,db_name,tb_name,msg=_get_init_data()
    #{'des_modir':'','text_app':'y'}
    htm_form=_save_out(xid=0)
    htm_form+=[tt]
    htm_form+=[k_form.C_FORM(x_data_s,xid).save(new_data=request.vars)['html_report'] for xid in xid_list]
    
    
    try:
        return dict(table=DIV(htm_form),script='',table_filter='',table_head='',style='',btm_mnu='') 
    except Exception as err:
        return DIV("*****",htm_form) #,x=response.toolbar())
    #return(DIV(k_htm.val_report(htm_form)))  
def _xtable_show(rows,titles,tasks,x_data_s,c_filter):
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
    

    args=request.args
    cols_filter=c_filter.cols_filter_obj['value'].replace('None','')
    if cols_filter:
        cf_list=cols_filter.split(',')
        if cf_list[0][0] in [0,1,2,3,4,5,6,7,8,9] :
            select_cols=[all_cols[int(x)] for x in cf_list]
        else:
            select_cols=cf_list or 'id'
            #if select_cols=='None':select_cols='id'
         
        print('select_cols='+str(select_cols))
        #--table head
        new_titles=[{'name':'n','width':'30px'},{'name':'id','width':'30px'}]
        x_tasks=tasks.copy()
        x_tasks.update({'id':{'title':'id'}})
        new_titles+=[{'name':x_tasks[x]['title'],'title':x} for x in select_cols]
        #---------------        
        trs=[]
        

        for i,row in enumerate(rows):

            x_dic=dict(zip(titles,row))

            n=str(i+1)
            idx=f"{x_dic['id']}"
            jobs=k_tools.nth_item_of_dict(x_data_s['steps'],0)['jobs']
            form_url=URL('xform',args=(args[0],args[1],idx))
            id_l=A(idx,_title='open form '+idx,_href=form_url,_class="btn btn-primary") #if session["admin"] or k_user.user_in_jobs(jobs) else n
            cls1='app_'+x_dic["f_nxt_u"] if x_dic["f_nxt_u"] else ''
            tds=[{'value':n,'class':cls1},{'value':id_l}]
            
            #---------------
            x_select_cols=[fn for fn in select_cols]
            tds_i=k_form.get_table_row_view(row[0],row,titles,tasks,x_select_cols,x_data_s,request=request)
            tds+=[{'value':x} for x in tds_i]           
            trs+=[tds]
        return trs,new_titles,len(rows)  
    else:        
        select_cols='form_view_cols_1' #form_view_cols_full  
        ''' form_view_cols_1=form view columns ALT 1 
            form_view_cols_full= form view columns FULL
        '''
        
        app_dic1={'un':'کاربر','ap':'نتیجه','dt':'زمان'}
        #--table head
        new_titles=[{'name':'n','width':'30px'},{'name':'id','width':'30px'}]
        for st_n,step in x_data_s['steps'].items():
            new_titles+=[{'name':tasks[x]['title'],'title':x} for x in step['tasks'].split(',') if x not in x_data_s['labels']]
            if select_cols=='form_view_cols_full':
                new_titles+=[{'name':"^"+str(step['i']+1)+"-"+y,'title':" مرحله "+f"step_{step['i']}_{x}",'class':'bg-info'} for x,y in app_dic1.items()]
            elif select_cols=='form_view_cols_1':
                new_titles+=[{'name':"^"+str(step['i']+1),'title':" مرحله "+",".join([f"step_{step['i']}_{x}" for x in app_dic1]),'class':'bg-info'}]
        new_titles+=[{'name':"S",'title':'f_nxt_s','width':'30px'},{'name':"U",'title':'f_nxt_u','width':'30px'}]
        #thead=THEAD(TR(*tds))
        #---------------        
        trs=[]
        

        for i,row in enumerate(rows):

            x_dic=dict(zip(titles,row))

            n=str(i+1)
            idx=f"{x_dic['id']}"
            jobs=k_tools.nth_item_of_dict(x_data_s['steps'],0)['jobs']
            form_url=URL('xform',args=(args[0],args[1],idx))
            id_l=A(idx,_title='open form '+idx,_href=form_url,_class="btn btn-primary") #if session["admin"] or k_user.user_in_jobs(jobs) else n
            cls1='app_'+x_dic["f_nxt_u"] if x_dic["f_nxt_u"] else ''
            tds=[{'value':n,'class':cls1},{'value':id_l}]
            
            for st_n,step in x_data_s['steps'].items():
                
                x_select_cols=[fn for fn in step['tasks'].split(',') if fn not in x_data_s['labels']]
                tds_i=k_form.get_table_row_view(row[0],row,titles,tasks,x_select_cols,x_data_s,request=request)
                tds+=[{'value':x} for x in tds_i]           

                if select_cols=='form_view_cols_full':
                    tds+=[{'value':x_dic[f"step_{step['i']}_{x}"]} for x in app_dic1]
                elif select_cols=='form_view_cols_1':  
                    tds+=[{'value':str(x_dic[f"step_{step['i']}_ap"]),'title':",".join([str(x_dic[f"step_{step['i']}_{x}"]) for x in app_dic1])}]

            tds+=[{'value':x_dic["f_nxt_s"],'class':cls1},{'value':x_dic["f_nxt_u"],'class':cls1}]
       
            trs+=[tds]
        return trs,new_titles,len(rows)    
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
def msg():
    msg='<br>'.join(request.vars['msg'].split('\n'))
    return dict(msg=DIV(H1(XML(msg)),_dir="rtl"))
def _xtable_head(x_data_s,x_select,nr,new_record_link):
    return DIV(TABLE(TR( 
                TD(new_record_link,_width='20px')
                ,TD(A("S",_title="Smart Select",_class="btn btn-success",_href=URL('data','select',args=request.args)),_width='30px')
                ,TD(A("T",_title="Table",_class="btn btn-primary",_href=URL('data','xtable',args=request.args,vars=request.vars)),_width='30px')
                ,TD(A(f"{nr}",_title="تعداد نمایش داده شده"),_width='30px')
                ,TD(A(f"{x_select['rows_num']}",_title="تعداد کل بر اساس فیلتر جاری"),_width='30px')
                ,TD(DIV('...',_id='viewcell',_name='viewcell'))
                ,TD(x_data_s['base']['title'],_width='10%')
            )),_style='position:sticky;top:0px')

def search():
    '''
    030728
    goal:
    ------
        URL_base search:
            جستجو ساده مبنتی بر URL
            ------
            - search in 1 field or in all field
                - search in 1 field : 4_ args => db/tb/search_text/field_name
                - search in all field : 3_ args => db/tb/search_text
                    عدم نوشتن نام فیلد جستجو
                - search in n fields : vars => s_cols=field_name_1,field_name_2,...,field_name_n
                    s_cols = search_colomns
                    exam => db/tb/search_text?s_cols=field_name_1,field_name_2,...,field_name_n
            - define out_colomns
                -in url : vars => o_cols=field_name_1,field_name_2,...,field_name_n
                    o_cols=output_colomns
        search by form:
            جستجو بر اساس اطلاعات پر شده در یک فرم
            -------
            - 2_ args => db/tb
            

    exam :
        http://192.168.88.179/spks/data/search/paper/a/gate?s_cols=sbj&o_cols=sbj,id
    '''
    out=[]
    x_data_s,db_name,tb_name,msg=_get_init_data()
    if not x_data_s : return msg
    if len(request.args)<2: return "len(request.args)<3"
    args=request.args+['','','']
    search_text=args[2] or request.vars['search_text']
    
    from k_sql import DB1,C_SQL
    import k_htm
    db1=DB1(db_path+db_name+'.db')
    if args[2]=="":
        val_dic={x:x for x in db1.columns_list(tb_name)}
        out+=[FORM(DIV(
                INPUT(_name='search_text',_value=request.vars['search_text']),
                k_htm.select(_options=val_dic,_name='o_cols',_multiple=True),
                INPUT(_value='جستجو',_type='submit')))]
        #,DIV())]
    if search_text:
        
        s_cols=request.vars['s_cols'].split(',') if request.vars['s_cols'] else ''
        fields=s_cols or args[3] or db1.columns_list(tb_name) 
        where=' OR '.join([C_SQL().where_cell(field_name,f'%{search_text}%','like') for field_name in fields])
        rows,titles,rows_num=db1.select(tb_name,where=where,limit=0)
        tasks=x_data_s['tasks']
        c_filter=C_FILTER(tasks,x_data_s) 
        rows,titles,nr=_xtable_show(rows,titles,tasks,x_data_s,c_filter)
        table=k_htm.C_TABLE(titles,rows).creat_htm(titels=request.vars['o_cols'])
        out+=["search_text => "+search_text]
        out+=[table]
        out+=[f"where={where}"]
    return dict(x=DIV(*out))