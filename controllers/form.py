# -*- coding: utf-8 -*-
# ver 1.00 1402/09/12
# -------------------------------------------------------------------------
''' value help
    x_data :# all form "extra data" that read from x_data.py file
        ساختار اطلاعات کل فرمها که از فایل مربوطه خوانده می شود
    x_data_s :# selected x_data = x_data for <select db_file><select table>    
    
    -----------------------------------------------------
    
    بخش های مهم در فایل هایپر تکست فرم
    importat part in HTML of FORM:
        1- text_app
            goal : save result of app_keys ('x'/ 'y' / 'r') or review_step_name ('ir_<step_name>')
            HTML : INPUT(_type='hidden',_id='text_app',_name='text_app',_value='')
        2- cur_step_name
            goal : show curren step name
            HTML : INPUT(_type='hidden',_id='cur_step_name',_name='cur_step_name',_value=step['name'])
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
cornometer=Cornometer("form")
from k_tools import C_URL
c_url=C_URL()
now = k_date.ir_date('yy/mm/dd-hh:gg:ss')

# import datetime
# now = datetime.datetime.now().strftime("%H:%M:%S")

debug=False # True: for check error
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
        self.cols_filter_obj={'name':'cols_filter','type':'select','select':cols_filter,'def_value':x_data_s['base'].get('cols_filter','')
            ,'add_empty_first':False}#,$hlp='prop':["can_add"],}
        
        data_filter=x_data_s['data_filter'] 
        data_filter={k_form.template_parser(x):y for x,y in data_filter.items()}
        def_value=k_form.template_parser(x_data_s['base'].get('data_filter',''))
        self.data_filter_obj={'name':'data_filter','type':'select','select':data_filter,'def_value':def_value,'add_empty_first':False}
        
        data_sort_items={'id':'id'}
        data_sort_items.update({x:y['title'] for x,y in x_data_s['tasks'].items()})
        self.data_sort={'name':'data_sort','type':'select','select':data_sort_items,'add_empty_first':False}
        
        self.data_page_len={'name':'data_page_len','type':'select','select':['20','50','100','200','500'],'add_empty_first':False}
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
    def set_htm_var(self,caption,obj,width='15%',_help='',_val='',_meta=''):
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
            x_data.x_data_verify_task(name2,obj,'','')
            obj['def_value']=request.vars.get(name2,obj['def_value'])
            val=request.vars.get(name,_val) or obj['def_value']
            if width:obj['width']=width
            tt=XML(k_form.obj_set(i_obj=obj,x_dic={},x_data_s=self.x_data_s, need=['input'],request=request)['input'])
            ##import k_err
            ##k_err.xreport_var([tt,XML(tt),obj,self.x_data_s])
            tt+=f'''<input {_meta} name='{name}' id='{name}' value='{val}' class='input-filter filter_menu' >'''
            #tjs=k_js.j_toggle(clicking_name=name+"_label",hiding_css_selector="#"+name)
            obj['value']=val #===> output
        xcap=f"""<label id='{name}_label'><a title='{_help}'>{caption}</a></label>"""
        tt1=k_htm.xtd([[xcap,3],[tt,9]],_calss="table_filter_in")
        
        
        return  f'''<td style='width:{width};'>
                            {tt1}
                        </td>
                    ''' #+tjs       
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
        import k_js
        """
                    + str(TR(
                        TD(ss_input_htm(dbn,tbn,'data_filter_1')),
                        TD(ss_input_htm(dbn,tbn,'data_filter_2')),
                        _class="filter_menu"))
        """
        tjs=k_js.j_toggle(clicking_name="filter_menu_label",hiding_css_selector=".filter_menu")
        dbn,tbn=self.x_data_s['base']['db_name'],self.x_data_s['base']['tb_name']
        obj_name_x=f'{dbn}_{tbn}_data_filter_'
        self.data_filter_x=[session[obj_name_x+'1_val'],session[obj_name_x+'2_val']]
        #print("self.data_filter_x="+str(self.data_filter_x))
        #print(obj_name_x)
        import k_icon
        icon_house=k_icon.chevron_down(24)
        return XML('<form><table class="table_filter"><tr style="height:10px;padding:0px;margin:0px">'
                    #+set_htm_var(caption='prj',width='20vw',obj=data_filter1,_help=hlp['data_filter'])
                    +f'''<td style='width:2%;'><a id='filter_menu_label' class='btn' title='جزئیات'>{icon_house}</a></td>'''

                    +self.set_htm_var(caption='d',width='15%',obj=self.data_filter_obj,_help='فیلتر اطلاعات' + hlp['data_filter'])
                    + str(TD(ss_input_htm(dbn,tbn,'data_filter_1'),_style='width:15%;'))
                    + str(TD(ss_input_htm(dbn,tbn,'data_filter_2'),_style='width:15%;'))
                    +self.set_htm_var(caption='s',width='10%',obj=self.data_sort,_help='ترتیب' + hlp['data_sort'])
                    +self.set_htm_var(caption='c',width='15%',obj=self.cols_filter_obj,_help='فیلتر ستونها' + hlp['cols_filter'])
                    +self.set_htm_var(caption='f',obj='table_class',width='8%',_val=2,_meta="type='number' min=-1 max=6",_help='حالت نمایش - 0 تا 6')
                    +self.set_htm_var(caption='p',obj='data_page_n',width='8%',_val=1,_meta="type='number' min=1" ,_help='صفحه شماره')
                    #+self.set_htm_var(caption='n',obj='data_page_len',width='8%',_val=20,_meta="type='number'" ,_help='تعداد ردیف در هر صفحه')
                    +self.set_htm_var(caption='n',width='8%',obj=self.data_page_len,_help='تعداد ردیف در هر صفحه')
                    +'<td style="width:4%"><input type="submit" value="انجام"></td></tr></table>'
                    +'<table class="table_filter">'
                    +'</table>'
                    +'</table></form>'
                    +tjs
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
def xform_section():
    if session.view_page=='save':
        session.view_page=''
        return 'j_box_iframe_win_close'
    session.view_page='xform_section'
    session['update_step']=False
    htm=_xform(section=0)['htm']
    #xreport_var([{'htm':htm}])
    return dict(htm=htm)
def xform_sd():
    if session.view_page=='save':
        session.view_page=''
        if 'auto_hide' in request.args:
            return 'j_box_iframe_win_close'
    session.view_page='xform_sd'
    session['update_step']=True
    res=_xform(out_items=['body'])
    #xreport_var([{'htm':htm}])
    return dict(htm=res['htm'],link=res['link'])#_xform())
def xform_info():
    x_data_s,db_name,tb_name,msg=_get_init_data()
    style="""
    <style>
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }

    th:nth-child(even),td:nth-child(even) {
      background-color: #D6EEEE;
    }
    </style>
    """
    return style+str(BEAUTIFY(x_data_s))
    return dict(htm=DIV(style,BEAUTIFY(x_data_s)))
def xform():
    session.view_page='xform'
    session['update_step']=True
    x_data_s,db_name,tb_name,msg=_get_init_data()
    res=_xform() 
    return dict(htm=res['htm'],link=res['link'])#_xform())
def xform_cg():
    import k_file,json
    session.view_page='xform_cg'
    session['update_step']=True
    x_data_s,db_name,tb_name,msg=_get_init_data()
    tmplt_fname=x_data_s['base']['xform_cg_file']
    x_file=k_file.read('text',r"D:\ks\I\web2py-test\applications\spks\static\xform_cg"+"\\"+ tmplt_fname)
    
    #return x_file
    json_data=_xform()['json']
    json_data1={x:y['value'] for x,y in json_data.items() if 'value' in y}#str(XML(y['value']
    json_data1['_']={x:y for x,y in json_data.items()} #__inf__
    json_data1['_labels']={x:y for x,y in x_data_s['labels'].items()}
    x_file1=x_file.replace('link_url',str(URL('static','xform_cg/link_url')))
    
    url1=str(URL('xform',args=request.args,vars=request.vars))
    x_file1=x_file1.replace('link_server',url1) 
    if tmplt_fname[-8:]!='-st.html':
        json_txt=json.dumps(json_data1,indent=4,ensure_ascii=False)
    
        #xreport_var([{'json_data':json_data,'json_data1':json_data1,'json_txt':json_txt}])
        #'json_txt':json.dumps(htm_form['body_json'],indent=4,ensure_ascii=False) }#,TABLE([str(y) for x,y in htm_form['body_json'].items()])
        
        #return x_file1
        
        #print(url1)
        
        x_file2=x_file1.replace("{'date':'0000/00/00','time':'00:00',}",json_txt)
        script2=""" 
        document.getElementById('help_div').style.display = "none"
        document.getElementById('bt_writetext').style.display = "none"
        """
        x_file2=x_file2.replace("//script2_inject",script2)
        #return x_file2
        return XML(x_file2)
    else:
        import k_tools,k_str
        #--------------------
        x_dic=k_tools.dict2obj(json_data1)
        #return json.dumps(x_dic,indent=4,ensure_ascii=False)
        x_file1=k_str.template_parser(x_file1,x_dic,do_format=False)
        return XML(x_file1)
def _xform(out_items=['head','body','tools'],section=-1):
    #show all section
    #response.show_toolbar=True #error check
    #print('?save')
    if request.vars['text_app']:
        #print("text_app="+str(request.vars['text_app']))
        text_app=request.vars['text_app'].lower()
        if 'ir' in text_app:
            return {'htm':XML(save_app_review()),'json':'','link':''}
        else:
            
            return {'htm':XML(save()),'json':'','link':''}
    #session.view_page='xform'
    
    '''
    goal:
        show / manage a formated & costomize form
        show only cols/fields/task that defied in data_structur and 'hide' str not in its 'prop' attbute
    
    if section!=0 
        show 1 section else show entire of form
    '''
    #------------------------------------------
    x_data_s,db_name,tb_name,msg=_get_init_data()
    if not x_data_s:
        return {'htm':msg,'json':''}
    
    # check access /auth
    auth= k_user.C_AUTH_FORM(x_data_s)
    if not auth.ok:return {'htm':H1(auth.msg),'json':''}
    #print("test")
   
    xid=request.args[2] or 1
    
    if section>-1:
        
        json_data,htm_x=C_FORM_HTM(x_data_s,xid).show_step_cur(step_n=section)
    else: #entire of form
        htm_form=C_FORM_HTM(x_data_s,xid).show_form()
        #xreport_var([{'htm_form':htm_form}])
        htm_x=[y for x in out_items for y in htm_form[x]]
        json_data=htm_form['body_json']
    htm=DIV(FORM(*htm_x,_id="form1"),_dir="rtl")
    #k_htm.a('+upload File',_target="box"
    link=k_htm.a('نمایش فرم با فرمت استاندارد',_target="blank",_title='فرم استاندارد',_href=URL('xform_cg',args=request.args)
        ,_class='btn btn-primary') if 'xform_cg_file' in x_data_s['base'] else ''
    #xreport_var([{'htm':htm}])
    return {'htm':htm,'json':json_data,'link':link}
class C_FORM_HTM():
    #:#view 1 row
    def __init__(self,x_data_s,xid):
        self.x_data_s=x_data_s
        self.xid=xid
        self.c_form=k_form.C_FORM(x_data_s,xid)
        self.f_nxt_s=self.c_form.f_nxt_s
    def show_form(self):#show 1 form 
        x_data_s=self.x_data_s
        xid=self.xid
        #xxxprint(3,msg=['show_form','',''])
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
            htm_form.update(self.show_form_body(x_data_s,c_form,xid))
            
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

    def show_form_body(self,x_data_s,c_form,xid):   
        #out_mode='json'
        htm_form={'body':[],'body_json':{}}
        text_app_added=False
        #step_befor='' # svae name of before step
        #xxxprint(3,msg=['form_sabt_data','',''])
        for i,step_name in enumerate(x_data_s['steps']):
            step=x_data_s['steps'][step_name]
            step['i']=i
            uwc=c_form.un_what_can_do_4_step(step_name=step_name)#,x_un
            #xxxprint(3,msg=[uwc,i,step_name])
            fsc_mode=self.c_form.step_state(step_name)[0]#['b','c','c','a'][
            #htm_form['body']+=[self.c_form.step_state(step_name)[2]]
            if uwc=='edit':
                
                #xxxprint(3,msg=['edit',i,step_name])
                if self.c_form.cur_step:
                    json,body=self.show_step_not_cur(x_data_s,xid,c_form,step,'2')
                    htm_form['body']+=[body] 
                    htm_form['body_json'].update(json)
                else:
                    self.c_form.cur_step=step_name
                    json,body=self.show_step_cur(step=step)
                    htm_form['body']+=[body]
                    htm_form['body_json'].update(json)
                    text_app_added=True
                    
            elif uwc=='ret_edit':
                json,body=self.show_step_not_cur(x_data_s,xid,c_form,step,'1')
                htm_form['body']+=[body,self.app_review(step_name)]
                htm_form['body_json'].update(json)
            elif uwc=='view':
                json,body=self.show_step_not_cur(x_data_s,xid,c_form,step, fsc_mode )
                htm_form['body']+=[body]
                htm_form['body_json'].update(json) 
            #htm_form['body_json'].update({})   
            htm_form['body']+=[DIV('',_class="text-center",_style="height:5px;background-color:#888")]
            '''        
            if i == f_nxt_s:
                
                if k_user.user_in_xjobs_can('edit',x_data_s,form_sabt_data,step_index=i):
                    #k_user.can_user_edit_step(step=step,step_index=i,form_sabt_data=form_sabt_data):
                    #k_user.user_in_jobs(step['jobs'],row_data=form_sabt_data):
                    htm_form['body']+=[self.show_step_cur(step=step)]
                else :
                    # show revize buttom نشان دادن دکمه بازبینی مرحله آخر
                    if step_befor and k_user.user_in_xjobs_can('edit',x_data_s,form_sabt_data,step_index=i-1):
                        #step_befor and k_user.step_changer(i-1,form_sabt_data)==session['username'] :
                        #k_user.user_in_jobs(x_data_s['steps'][step_befor]['jobs'],row_data=form_sabt_data):
                        htm_form['body']+=[self.app_review()]
                    htm_form['body']+=[DIV(HR(),'   /\   '+'شما اجازه تکمیل این بخش را ندارید'+'   /\   ',_class='form_step_cur_unactive text-center text-light')]
                    
                    htm_form['body']+=[DIV([self.show_step_not_cur(x_data_s,xid,c_form,step,'c')])]
                    htm_form['body']+=[DIV('   \/   '+'شما اجازه تکمیل این بخش را ندارید'+'   \/   ',HR(),_class='form_step_cur_unactive text-center text-light')]
            else:
                if 'sp_order' in step and k_user.user_in_xjobs_can('edit',x_data_s,form_sabt_data,step_index=i):
                    htm_form['body']+=[self.show_step_cur(step=step)]
                else:
                    ab_case="b" if i < f_nxt_s else "a"
                    htm_form['body']+=[self.show_step_not_cur(x_data_s,xid,c_form,step,ab_case)]
            step_befor=step_n
            '''
        # show revize buttom نشان دادن دکمه بازبینی مرحله آخر
        # if "end_step is field(form is compelete)" and "cur_user is end_step owner"
        '''
        if (f_nxt_s >=len(x_data_s['steps']) and k_user.user_in_xjobs_can('edit',x_data_s,form_sabt_data,step_index=f_nxt_s-1)):
            #k_user.user_in_jobs(k_tools.nth_item_of_dict(x_data_s['steps'],f_nxt_s-1)['jobs'],row_data=form_sabt_data)):
            # test = form(morakhsi_saat).rec(15 steps=comple) : user(mlk) =>can view (app_review but) ,other users(atl,ks,..) cannot view (app_review but)
            htm_form['body']+=[self.app_review()]
        '''
        # if "previus_step result = x (form is omit)" and "cur_user is previus_step owner"
        '''
        if (f_nxt_s < 0 and k_user.user_in_xjobs_can('edit',x_data_s,form_sabt_data,step_index=-f_nxt_s)):
            #k_user.user_in_jobs(k_tools.nth_item_of_dict(x_data_s['steps'],-f_nxt_s)['jobs'],row_data=form_sabt_data):
            # test = 
            htm_form['body']+=[self.app_review()]
        '''
        if not text_app_added:
            htm_form['body']+=[INPUT(_type='hidden',_id='text_app',_name='text_app',_value='')]
        htm_form['body']+=['cur_step = '+str(self.c_form.cur_step)]
        htm_form['body']+=[' | f_nxt_u = '+str(self.c_form.form_sabt_data['f_nxt_u'])]
        htm_form['body']+=[' | f_nxt_s = '+str(self.c_form.form_sabt_data['f_nxt_s'])]
        return htm_form #['body']
    def show_step_not_cur(self,x_data_s,xid,c_form,step,fsc_mode,out_mode=''): #like=row_view
        '''
            0209012
        INPUT:
        ------
            fsc_mode:str ('b'/'a')
                1,2=cur
                0=befor of cur - approved
                3=aftre of cur - empty or review
        '''
        #print (step)
        fsc_class=f"form_step_c{fsc_mode}" #fsc_mode=form_step_class
        hx={'data':[],'stp':'','app':[],'data_json':{}}#fsc_mode
        
        for field_name in step['tasks'].split(','):
            if field_name in x_data_s['labels']:
                hx['data']+=[DIV(DIV(x_data_s['labels'][field_name],_class="col text-center bg-info text-light"),_class='row border-top')]
            else:
                hh=self.c_form.show_step_1_row(field_name,request,mode='output')#output_text')
                hx['data']+=[self._show_row(hh,step)]
                #[DIV(DIV(hh[0],_class='col-3 text-right'),DIV(hh[1],_class='col-6 text-right'),DIV(hh[2],_class='col-3 text-right'),_class='row border-top')]
                hx['data_json'][field_name]={'name':str(hh[4]),'value':hh[5],'help':str(hh[2]),'title':str(hh[3])}#(hh[1] if type(hh[1])==str else '')
                #hx['data_json'][field_name]={'name':str(hh[4]),'value':str(hh[1]),'help':str(hh[2]),'title':str(hh[3])}
        #breakpoint() f_nxt_s
        def val_in_dic(x_dict,v_name):
            '''
                goal:extract item_val(=return) from dict(=x_dict) by its item_name(=v_name)
            '''
            v_name=v_name or '' # NONE => ''
            v_name=v_name.lower()
            return x_dict.get(v_name,v_name)
        #print("step[i]="+str(step["i"]))
        #print("==>"+str(form_sabt_data[f'step_{step["i"]}_un']))
        form_sabt_data=self.c_form.form_sabt_data
        un=form_sabt_data[f'step_{step["name"]}_un']
        
        xap={'ap':{'value':val_in_dic(step['app_kt'],form_sabt_data[f'step_{step["name"]}_ap']),'title':"نتیجه : "},
            'un':{'value':(val_in_dic(k_user.ALL_USERS().inf,un).get('fullname','') if un else ''),'title':"توسط : "},
            'dt':{'value':form_sabt_data[f'step_{step["name"]}_dt'] or '','title':"مورخ : "}}
        hx['app']=[xap[x]['title']+xap[x]['value'] for x in ['ap','un','dt']]
        """
                    (xap['ap']['title']+xap['ap']['value']), #val_in_dic(step['app_kt'],form_sabt_data[f'step_{step["name"]}_ap'])),
                    ("توسط : "+hx['app_un']), #(val_in_dic(k_user.ALL_USERS().inf,un).get('fullname','') if un else '')),
                    ("مورخ : "+hx['app_dt']) #(form_sabt_data[f'step_{step["name"]}_dt'] or '')),
                    ]"""
        hx['data_json'].update({f'step_{step["name"]}_ap':xap['ap'],
                                f'step_{step["name"]}_un':xap['un'],
                                f'step_{step["name"]}_dt':xap['dt']
                                })            
        # breakpoint()
        hx['app-color']="bg-"+val_in_dic(x_color,form_sabt_data[f'step_{step["name"]}_ap'])
        hx['stp']=[str(step['i']+1) +' - '+ step['title']]
        
        #if out_mode=='json'
        #   return hx['data_json']
        #else:
        return hx['data_json'],DIV(k_form.chidman(hx,x_data_s,step,request=request),_class="container-fluid "+fsc_class) #DIV(,_style="background-color:#555;")
    def show_step_cur(self,step={},step_n=0,info=False,out_mode=''): #like=row_edit
        '''
            0209012 
            step=x_data_s['steps'][step_n]
        '''
        x_data_s=self.x_data_s
        if not step:
            step=k_tools.nth_item_of_dict(x_data_s['steps'],int(step_n))
        hx={'data':[],'stp':'','app':[],'data_json':{}}
        for field_name in step['tasks'].split(','):
            if field_name in x_data_s['labels']:
                hx['data']+=[DIV(DIV(x_data_s['labels'][field_name],_class="col text-center bg-info text-light"),_class='row border-top')]
            else:
                hh=self.c_form.show_step_1_row(field_name,request,mode='input')
                hx['data']+=[self._show_row(hh,step)]
                #[DIV(DIV(hh[0],_class='col-3 text-right'),DIV(hh[1],_class='col-6 text-right'),DIV(hh[2],_class='col-3 text-right'),_class='row border-top')]
                hx['data_json'][field_name]={'name':str(hh[4]),'value':hh[5],'help':str(hh[2]),'title':str(hh[3])}#(hh[1] if type(hh[1])==str else '')
        hx['app1']=[DIV(BUTTON(step['app_kt'][xx],_type='BUTTON',_class=f'w-100 btn btn-{x_color[xx]}',_onclick=f"app_key('{xx}')") if xx in step['app_kt'] else '' ,_class='col-'+{'y':'8','r':'2','x':'2'}[xx]) for xx in ['x','y','r']]
        hx['app']=['نتیجه','-'*10,'اقدام:','توسط:','مورخ :'] if info else []
        hx['app']+=[INPUT(_type='hidden',_id='cur_step_name',_name='cur_step_name',_value=step['name'])]
        hx['app']+=[INPUT(_type='hidden',_id='text_app',_name='text_app',_value='')]
        hx['stp']=[str(step['i']+1) +' - '+ step['title']]
        hx['app-color']=''
        #if out_mode=='json'
        #   return hx['data_json']
        #else:
        return hx['data_json'],DIV(
                DIV(k_form.chidman(hx,x_data_s,step,request=request),_class="container-fluid form_step_cur")
                ,DIV(*hx['app1'],_class="row p-2"))
                     #,_action=URL('save',args=request.args)
    def _show_row(self,hh,step):
        task_cols_width=step.get('task_cols_width','3,6,3')
        tcw=task_cols_width.split(',')
        return DIV(*[DIV(hh[i],_class=f'col-{tcw[i]} text-right') for i in range(0,3) if tcw[i]!='0'],_class='row border')
        #hx['data']+=[DIV(DIV(hh[0],_class='col-3 text-right'),DIV(hh[1],_class='col-6 text-right'),DIV(hh[2],_class='col-3 text-right'),_class='row border-top')]
    def app_review (self,step_name): 
        '''
            0209018
        
        htm_1=[DIV(
                DIV('',_class='col-4'),
                DIV(BUTTON("بازبین مرحله آخر",_type='submit',_class='btn ',_onclick=f"app_key('ir')"),_class='col-4'), 
                DIV('',_class='col-4')
                ,_class='row')]
        #htm_1+=[HR()]
        htm=DIV(htm_1)# FORM(DIV(htm_1,_class="container form_step_cur"),_action=URL('save_app_review',args=request.args),_id="form1") 
        return XML(k_htm.x_toggle_s(XML(htm),head='اصلاح'))
        '''
        #return DIV(A('اصلاح',_class="btn btn-warning"))
        return DIV(
            BUTTON("اصلاح",_type='submit',_class='btn btn-warning',_onclick=f"app_key('ir_{step_name}')")
            #INPUT(_type='hidden',_id='review_step_name',_name='review_step_name',_value=step_name)
            ,_style="text-align:center;")
    #-- def show_form:start ----------------------------------------------
          
        
    #-- def xform:start ------------------------------------------------------------
    
# ------------------------------------------------------------------------------------------ 
def _save_out(xid,err_show=False):
    args=request.args
    if xid:#
        args[2]=xid
        x_url=session.view_page_old or 'xform'
        link=URL(x_url,args=args)
    else:#call from x_table_i
        link=URL('xtable_i',args=request.args,vars={x:request.vars[x] for x in ['data_filter','data_sort','cols_filter','paper_num','table_class','data_page_n','data_page_len']})
    return _auto_redirect(link,delay=.5,err_show=err_show)+[DIV('request.args= '+str(request.args[2]),_class="row")] 
    
def _auto_redirect(link,delay=.2,err_show=False,title="بازگشت به فرم"):
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
    if not 'xform' in session.view_page:
        x_url=session.view_page_old or 'xform'
        redirect(URL(x_url)) #return 'refer to this page is uncorrect'
    session.view_page_old=session.view_page
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
        c_form=k_form.C_FORM(x_data_s,xid)
        c_form.cur_step_name=request.vars['cur_step_name']
        #if 'section' in request.vars:
        if session.view_page=='xform_section':
            c_form.all_data['f_nxt_s']=0
        update_step=session['update_step'] if 'update_step' in session else True 
        x_r=c_form.save(new_data=request.post_vars,update_step=update_step)
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
    if not 'xform' in session.view_page:
        return 'refer to this page is uncorrect'
    session.view_page='save_app_review'
    #print('form-save_app_review')
    x_data_s,db_name,tb_name,msg=_get_init_data()
    xid=request.args[2] or 1
    c_form=k_form.C_FORM(x_data_s,xid)
    c_form.cur_step_name=request.vars['text_app'][3:] # text_app= ir_<cur_step_name>
    tt=c_form.save_app_review(request_data=request.vars)
    
    htm_form=_save_out(xid)
    htm_form+=[tt]
    return DIV(htm_form)
    try:
        return dict(htm=DIV(htm_form)) 
    except Exception as err:
        return DIV("*****",htm_form) #,x=response.toolbar())
#------------------------------------------------------------------------------------------------------------
def list_0():
    import k_icon,k_htm,k_tools
    from x_data import x_data_cat
    #x_data_cat=x_data.x_data_cat
    trsx={x:[] for x in x_data_cat}
    n=0
    titels=['n','','نام فرم','تعداد منتظر اقدام شما','تعداد کل',""]
    afi=k_tools.access_from_internet()
    
    for db_name,db_obj in x_data.items():
        for tb_name,tb_obj in db_obj.items():
            if tb_obj['base']['mode']=='form' and ((not afi) or ('internet' in tb_obj['base'])):
                n+=1
                db1=DB1(db_name)
                total_n=db1.count(tb_name)['count']
                x_where=f'''`f_nxt_u` like "%{session['username']}%"'''
                for_me_n=db1.count(tb_name,where=x_where)['count']
                for_me_n_link=A(for_me_n,_href=URL('xtable',args=[db_name,tb_name],vars={'data_filter':x_where}),_class="btn btn-primary") if for_me_n else ''
                
                multi_app=[]
                if for_me_n and 'multi_app' in tb_obj['base']:
                    #print("multi_app="+str(multi_app))
                    for m_a_step,m_a_users in tb_obj['base']['multi_app'].items():
                        if session['username'] in m_a_users:
                            multi_app+=[A(XML(k_icon.auto_app(24)),_href=URL('xtable_i',args=[db_name,tb_name,m_a_step]))]
                if multi_app:
                    for_me_n_link=XML(k_htm.xtd_div(multi_app+[for_me_n_link]))    
                    
                code=tb_obj['base']['code'] if 'code' in tb_obj['base'] else '900'
                xcat=code[0] 
                n1=len(trsx[xcat])+1
                
                _class="btn btn-primary btn-sm"
                tools=[]
                if session["admin"]:
                    tools=[
                        k_htm.a("T",_target="box",reset=False,_class=_class,_title="جدول",_href=URL('data','xtable',args=[db_name,tb_name])),
                        k_htm.a("M0",_target="box",reset=False,_class=_class,_title="ساخت فیلدهاو جدول",_href=URL("data","rc",args=["creat_table_4_form",db_name,tb_name])) ,
                        k_htm.a("M1",_target="box",reset=False,_class=_class,_title="ساخت فیلدهاو جدول",_href=URL("data","rc",args=["creat_table_4_form",db_name,tb_name,"do"])) ,
                        k_htm.a("U",_target="box",reset=False,_class=_class,_title="بروز رسانی نتیجه فرم",_href=URL("data","rc",args=["update_f_nxt_u",db_name,tb_name,"do-x"])),
                        k_htm.a("D",_target="box",reset=False,_class=_class,_title="نمایش ستونهای اضافه در جدول",_href=URL("data","rc",args=["columns_dif",db_name,tb_name,"do-x"])),
                        k_htm.a("P",_target="box",reset=False,_class=_class,_title="pivot table",_href=URL("pivot",args=[db_name,tb_name])),
                        k_htm.a("A",_target="box",reset=False,_class=_class,_title="به روز رسانی فیلدهای اتوماتیک",
                            _href=URL("data","rc",args=["update_auto_filed",db_name,tb_name,"do-x"]
                                    ,vars={'select_cols':XML(','.join([x for x in tb_obj['tasks'] if tb_obj['tasks'][x]['type']=='auto']))}
                                    )),
                        k_htm.a("L",_target="box",reset=False,_class=_class,_title="لیست فیلد های لینک شده",_href=URL('data','rc',args=['find_linked_target_fields',db_name,tb_name])),                                  
                    ]
                tools+=[k_htm.a(XML(k_icon.search(24)),_target="box",reset=False,_class=_class,_title="جستجو در اطلاعات فرم",_href=URL("form","search",args=[db_name,tb_name,""]))]
                tools=TABLE(TR([TD(x,_class="m-0 p-0 border-0") for x in tools]),_class="table m-0 p-0 ")
                    
                tx=[A(tb_obj['base']['title'],_href=URL('xtable',args=[db_name,tb_name])),
                    for_me_n_link,
                    total_n,
                    tools,
                    ]
                tn= [DIV(n,_title=code)]  
                tn1= [DIV(n1,_title=code)] 
                trsx[xcat]+=[tn1+['']+tx]
                trsx["-"]+=[tn+[db_name+","+tb_name]+tx]
 
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
    #tt+=[XML(t0)]
    return dict(htm=DIV(tt,_dir='rtl'),server_python_add=k_tools.server_python_add(),access_from_internet=k_tools.access_from_internet())
#----------------------------------------------------------------------------------------------------- 
def list_0_mr(): #mr=manage report
    import k_icon,k_htm
    from x_data import x_data_cat
    #x_data_cat=x_data.x_data_cat
    trsx={x:[] for x in x_data_cat}
    n=0
    titels=['n','نام فرم','فیلد های هوشمند','سامان دهی و مدیریت و اعتبار دهی','تعداد ثبت','تعدا د فراداده']
    x_sum=[0,0,0,0]
    rows=[]
    for db_name,db_obj in x_data.items():
        for tb_name,tb_obj in db_obj.items():
            if tb_obj['base']['mode']=='form':
                n+=1
                db1=DB1(db_name)
                total_n=db1.count(tb_name)['count']
                n_task=len(tb_obj['tasks'])
                n_step=3*len(tb_obj['steps'])+2
                n_all=(n_task+n_step)*total_n
                row=[n,tb_obj['base']['title'],
                    n_task,n_step,
                    total_n,
                    n_all,
                    ]
                x_sum[0]+=n_task
                x_sum[1]+=n_step
                x_sum[2]+=total_n
                x_sum[3]+=n_all
                rows+=[row]
    rows+=[['-','SUM']+x_sum]
    from k_htm import C_TABLE
    table1=C_TABLE(titels,rows).creat_htm()           
    return dict(table=table1,x_sum=x_sum[3])
#-----------------------------------------------------------------------------------------------------   
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
  
    db1=DB1(db_name)
    tasks=x_data_s['tasks']
    
    c_filter=C_FILTER(tasks,x_data_s) 
    #filter_data=c_filter.data_filter_obj["value"]#k_form.template_parser(request.vars.get('data_filter'),x_dic={})#eval(flt) if flt else ''
    
    
    filter_data=["AND",c_filter.data_filter_obj["value"]]+c_filter.data_filter_x
    if auth.where:filter_data+=[auth.where]#__where__list__
    '''
        auth.where='cp_code NOT LIKE "AQRC%"'
            نکته این شرط باعث حذف شدن فیلدهاییتکمیل نشده هم می شود
    '''
    order=c_filter.data_sort["value"] or x_data_s['order']
    x_select=db1.select(table=tb_name,where=filter_data,result='dict_x',page_n=request.vars['data_page_n'],page_len=request.vars['data_page_len'],order=order)
    #xxxprint(out_case=3, msg=["filter_data",filter_data,""],vals={'filter_data':filter_data,"session['auth_prj']":session['auth_prj'],'sql':x_select["sql"]})
    #if rows:rows.reverse()
    trs,new_titles,nr=_xtable_show(x_select["rows"],x_select['titles'],tasks,x_data_s,c_filter)
    #import k_err
    #k_err.xreport_var([trs,new_titles])
    from k_tools import C_URL
    c_url=C_URL()
    from k_htm import C_TABLE
    c_table=C_TABLE(new_titles,trs)
    if 'xx' in request.vars:
        pass
    if c_url.ext=='': #html

        table_class=request.vars['table_class'] if request.vars['table_class'] else '0'
        table1=c_table.creat_htm(table_class,_id="table_f")   
        
        #print(f'job={job}')
        if session["admin"] or k_user.user_in_xjobs_can('creat',x_data_s,step_index='0'):
            #jobs=k_tools.nth_item_of_dict(x_data_s['steps'],0)['jobs']
            #k_user.user_in_jobs(jobs):
            new_record_link=k_htm.a('+',_target="box",_class='btn btn-primary',_title='NEW RECORD',
                _href=URL('xform_sd',args=(args[0],args[1],"-1"),vars={'form_case':x_data_s['base'].get('form_case',1)})) 
        else:
            new_record_link='-'
        import k_date,k_icon
        btm_mnu= DIV(A("XLS",XML(k_icon.download(20)),_title="Download XLS",_class="btn btn-success",_href=URL('xtable.xls',args=args+[args[0]+"_form_"+k_date.ir_date('yymmdd-hhggss')],vars=request.vars)),
                     A("CSV",XML(k_icon.download(20)),_title="Download CSV",_class="btn btn-warning",_href=URL('xtable.csv',args=args+[args[0]+"_form_"+k_date.ir_date('yymmdd-hhggss')],vars=request.vars)))
        return dict(style=style1,script=scripts['table cell display'],
            table_filter=c_filter.htm,
            table_head=_xtable_head(x_data_s,x_select,nr,new_record_link),
            table=table1,btm_mnu=btm_mnu
            ,xtime=cornometer.xreport())
    elif c_url.ext=='xls':
        tt="\ufeff" # BOM
        #return tt+'\n'.join([','.join([str(cel) for cel in row]) for row in [new_titles]+trs])
        return c_table.export_csv(request.args[-1])
        #return C_TABLE(x_select['titles'],x_select["rows"]).export_csv(request.args[-1])
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
  
    db1=DB1(db_name)
    tasks=x_data_s['tasks']
    
    c_filter=C_FILTER(tasks,x_data_s) 
    filter_data1=c_filter.data_filter_obj["value"] if show_filter else ''

    filter_data=["AND",f'''`f_nxt_u` like "%{session['username']}%"''',f'''`f_nxt_s` like "%{f_nxt_s}%"''']
    
    if auth.where or filter_data1:
        filter_data+=[filter_data1,auth.where]#__where__list__
    order=c_filter.data_sort["value"] or x_data_s['order'] or 'id'
    if order=='None':order='id'
    x_select=db1.select(table=tb_name,where=filter_data,result='dict_x',page_n=request.vars['data_page_n'],page_len=request.vars['data_page_len'],order=order)
    #xxxprint(3,vals={"sql":x_select['sql']})#x_select['sql']
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

    json_data_cur,step_cur=C_FORM_HTM(x_data_s,-1).show_step_cur(step_n=f_nxt_s)
    
    table2=FORM(
            DIV(table1),step_cur,
            #DIV(k_form.chidman(hx,x_data_s,step),_class="container-fluid form_step_cur"),
            #INPUT(_type='hidden',_id='text_app',_name='text_app',_value=''),
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
    
    #chek for user error
    # جلوگیری از پاک شدن اطلاعات فیلدهای تکرار  شده با خالی گذاشتن آنها
    new_req={}
    for x,x_val in request.vars.items():
        n=0
        for step,step_v in x_data_s['steps'].items():
            if x in step_v['tasks']:n+=1
        if n==1 or x_val:new_req[x]=x_val
    htm_form+=[k_form.C_FORM(x_data_s,xid).save(new_data=new_req)['html_report'] for xid in xid_list]
    
    
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
         
        #xprint('select_cols='+str(select_cols))
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
            jobs=k_tools.nth_item_of_dict(x_data_s['steps'],0)['xjobs']
            form_url=URL('xform_sd',args=(args[0],args[1],idx))
            #id_l=A(idx,_title='open form '+idx,_href=form_url,_class="btn btn-primary") #if session["admin"] or k_user.user_in_jobs(jobs) else n
            id_l=k_htm.a(idx,_title='open form 1'+idx,_href=form_url,_class="btn btn-primary",_target="box")
            cls1='app_'+x_dic["f_nxt_u"] if x_dic["f_nxt_u"] else ''
            tds=[{'value':n,'class':cls1},{'value':id_l}]
            
            #---------------
            x_select_cols=[fn for fn in select_cols]
            tds_i=k_form.get_table_row_view(row[0],row,titles,x_select_cols,x_data_s,request=request)
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
            if step['tasks']:
                new_titles+=[{'name':tasks[x]['title'],'title':x} for x in step['tasks'].split(',') if (x not in x_data_s['labels'])]
            if select_cols=='form_view_cols_full':
                new_titles+=[{'name':"^"+str(step['i']+1)+"-"+y,'title':" مرحله "+f"step_{step['name']}_{x}",'class':'bg-info'} for x,y in app_dic1.items()]
            elif select_cols=='form_view_cols_1':
                new_titles+=[{'name':"^"+str(step['i']+1),'title':" مرحله "+",".join([f"step_{step['name']}_{x}" for x in app_dic1]),'class':'bg-info'}]
        new_titles+=[{'name':"S",'title':'f_nxt_s','width':'30px'},{'name':"U",'title':'f_nxt_u','width':'30px'}]
        #thead=THEAD(TR(*tds))
        #---------------        
        trs=[]
        

        for i,row in enumerate(rows):

            x_dic=dict(zip(titles,row))

            n=str(i+1)
            idx=f"{x_dic['id']}"
            jobs=k_tools.nth_item_of_dict(x_data_s['steps'],0)['xjobs']
            form_url=URL('xform_sd',args=(args[0],args[1],idx),vars={'form_case':x_data_s['base'].get('form_case',1)})
            #id_l=A(idx,_title='open form '+idx,_href=form_url,_class="btn btn-primary") #if session["admin"] or k_user.user_in_jobs(jobs) else n
            id_l=k_htm.a(idx,_title='open form 1'+idx,_href=form_url,_class="btn btn-primary",_target="box")
            cls1='app_'+x_dic["f_nxt_u"] if x_dic["f_nxt_u"] else ''
            tds=[{'value':n,'class':cls1},{'value':id_l}]
            
            for st_n,step in x_data_s['steps'].items():
                if step['tasks']:
                    x_select_cols=[fn for fn in step['tasks'].split(',') if fn not in x_data_s['labels']]
                    tds_i=k_form.get_table_row_view(row[0],row,titles,x_select_cols,x_data_s,request=request)
                    tds+=[{'value':x} for x in tds_i]           

                if select_cols=='form_view_cols_full':
                    tds+=[{'value':x_dic[f"step_{step['name']}_{x}"]} for x in app_dic1]
                elif select_cols=='form_view_cols_1':  
                    tds+=[{'value':str(x_dic[f"step_{step['name']}_ap"]),'title':",".join([str(x_dic[f"step_{step['name']}_{x}"]) for x in app_dic1])}]

            tds+=[{'value':x_dic["f_nxt_s"],'class':cls1},{'value':x_dic["f_nxt_u"],'class':cls1}]
       
            trs+=[tds]
        return trs,new_titles,len(rows)    
def _sabege():
    if len(request.args)<3 :
        return "err: arg number send to fun(sabege) is < 3"
    #breakpoint()
    x_data_s,db_name,tb_name,msg=_get_init_data()
    
    db1=DB1(db_name)
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
    db1=DB1(db_name)
    if args[2]=="":
        tasks=x_data_s['tasks']
        val_dic={x:tasks[x]['title'] for x in tasks if 'auth' not in tasks[x]}
        out+=[FORM(DIV(
                    DIV('متن جستجو :',_class='col-1'),
                    DIV(INPUT(_name='search_text',_value=request.vars['search_text'],_style='width:100%'),_class='col-2'),
                    DIV('ردیف های جستجو :',_class='col-1'),
                    DIV(k_htm.select(_options=val_dic,_name='s_cols',_multiple=True),_class='col-7'),
                    DIV(INPUT(_value='جستجو',_type='submit',_style='width:100%')),
                    _class='row'),
                 )]
        #,DIV())]
        """
                DIV(
                    DIV('ردیف های  نتیجه :',_class='col-2'),
                    DIV(k_htm.select(_options=val_dic,_name='o_cols',_multiple=True),_class='col-10'),
                    _class='row'),
                """
    if search_text:
        
        s_cols=request.vars['s_cols'].split(',') if request.vars['s_cols'] else ''
        fields=s_cols or args[3] or db1.columns_list(tb_name) 
        where=' OR '.join([C_SQL().where_cell(field_name,f'%{search_text}%','like') for field_name in fields])
        rows,titles,rows_num=db1.select(tb_name,where=where,limit=0)
        tasks=x_data_s['tasks']
        c_filter=C_FILTER(tasks,x_data_s) 
        rows,titles_2,nr=_xtable_show(rows,titles,tasks,x_data_s,c_filter)
        o_cols=request.vars['o_cols']#or ''
        table=k_htm.C_TABLE(titles_2,rows).creat_htm(titels=o_cols) #[])# .split(',')
        out+=[table]
        out+=["search_text => "+search_text]
        #out+=["o_cols => "+str(o_cols)]
        out+=[f"where={where}"]
    return dict(x=DIV(*[DIV(x) for x in out]))
#----------------------------------------------------------------------------------------------------------------
def date_picker():
    '''
        goal 1=creat 1 persian calender table for select date
        هدف = ساخت 1 جدول تقویم ایرانی برای 1 ماه برای انتخاب تقویم 
        با نمایش روز های تعطیل در انواع مختلف
        steps:
            1:select category (select_cat)
            2:select 1 data from select_cat
        input:
            url args:
                1:session name for save out_text
                2:def date in format yyyy-mm-dd
        output:
            date:str
                format = yyyy/mm/dd
            save result in sesstion 
    '''
    
    obj_name_x=request.args[0] if request.args else ''
    text_app=request.vars['text_app']
    # close and return result
    if text_app and obj_name_x:
        session[obj_name_x]=text_app
        session[obj_name_x+'_wd']=request.vars['text_app_wd']
        return 'j_box_iframe_win_close | '+text_app
    # start pro
    import k_htm,jdatetime,k_form,k_date,k_time
    
    today='14'+jdatetime.date.today().strftime('%y/%m/%d')
    def_date=request.args[1].replace("-",r"/") if (request.args and len(request.args)>1) else today
    #print(f'today={today} - def_date= {def_date} - {def_date[:4]} - {def_date[5:7]}')
    yy_v=request.vars['yy_v'] or def_date[:4] or '1404' #'1403' #jdatetime.date.today().strftime('%y')
    yy_obj=k_htm.select(_options=[str(x) for x in range(1340,1405)],_name='yy_v',_value=yy_v,add_empty_first=False,_onchange="submit();")
    yy_n=int(yy_v)
    mm_v=request.vars['mm_v'] or def_date[5:7] #jdatetime.date.today().strftime('%m')
    mm_obj=k_htm.select(_options=[str(x).zfill(2) for x in range(1,13)],_name='mm_v',_value=mm_v,add_empty_first=False,_onchange="submit();")
    mm_n=int(mm_v)
    #print(mm_n)
    style="""<style>
    div.hd {
        background-color:#3e506b;
        color:#fff;
        text-align:center;
    }
    div.cl {
        text-align:center;
    }
    </style>
    """
    mm_len=k_date.ir_mon_len(yy_n,mm_n)
    date=k_date.st_date(yy_n,mm_n,1)
    w0=k_date.ir_weekday(date,w_case=0)
    td1=[['','']]*w0
    tr=[[DIV(x,_class="hd") for x in ['ش','ی','د','س','چ','پ','ج']]]
    #return f"{date}-{mm_len}-{w0}"
    for x_ruz in range(1,mm_len+1):
        date=k_date.st_date(yy_n,mm_n,x_ruz)
        
        style_add="border:3px solid #00f;" if date==today else "border:3px solid #0f0;" if date==def_date else''
        color=k_date.tatil_mode(date,out_case='color')
        w0+=1
        wd=k_date.ir_weekday(date,w_case=2)
        td1+=[[BUTTON(x_ruz,_class="btn",_style=f"background-color:{color};"+style_add,
                _onclick=f"""document.getElementById('text_app').value='{date}';
                            document.getElementById('text_app_wd').value='{wd}';
                """)
            ,color]]
        if divmod(w0, 7)[1]==0:
            #print(str(td1))
            tr+=[[DIV(x[0],_class="cl",_style=f"background-color:{x[1]}") for x in td1]]
            td1=[]
    if td1:
        td1+=[['','']]*(7-len(td1))
        tr+=[[DIV(x[0],_class="cl",_style=f"background-color:{x[1]}") for x in td1]]
    mm_c=k_htm.a('=',_target="",_href =URL(f='date_picker',args=[obj_name_x]),_title='ماه جاری',_class="",_style="font-size=1.5em;font-family:tahoma;")
    def mm_a_b(yy_v,mm_v):
        '''
            a=after
            b=befor
            find after & befor month od 1 date (yy_v,mm_v)
        '''
        yy=int(yy_v)
        mm=int(mm_v)
        mmx=yy*12+mm
        mm_b=list(divmod(mmx-2,12))
        mm_b[1]+=1
        mm_a=list(divmod(mmx,12))
        mm_a[1]+=1
        return f'{mm_b[0]}-{mm_b[1]:02d}-00',f'{mm_a[0]}-{mm_a[1]:02d}-00'
    mm_b_date,mm_a_date=mm_a_b(yy_v,mm_v)
    #print(f'{mm_b_date}---{mm_a_date}')
    mm_b=k_htm.a('>',_target="",_href =URL(f='date_picker',args=[obj_name_x,mm_b_date]),_title='ماه قبل',_class="btn")
    mm_a=k_htm.a('<',_target="",_href =URL(f='date_picker',args=[obj_name_x,mm_a_date]),_title='ماه بعد',_class="btn")
    return dict(htm=DIV(XML(style),FORM(
        TABLE(TR(TD(mm_a),TD(mm_c),TD(mm_obj),TD(yy_obj),TD(mm_b)),TR(TD(TABLE(tr),_colspan=5))), #_style="width:150px"
        INPUT(_id='text_app',_name='text_app',_value='',_type='hidden',),#
        INPUT(_id='text_app_wd',_name='text_app_wd',_value='',_type='hidden',),
        ))
    )
    '''
    return dict(style=XML(style),f=FORM(
        yy_obj,mm_obj,TABLE(tr),
        INPUT(_id='text_app',_name='text_app',_value='',_type='hidden',),#
        INPUT(_id='text_app_wd',_name='text_app_wd',_value='',_type='hidden',),
        )
    )
    '''
    #date=x_mon+"/"+('00'+str(x_ruz+1))[-2:] 
#----------------------------------------------------------------------------------------------------------------
def ss_set():
    '''
        goal 1=creat sql by pick category then pick data
        هدف = ساختن دستور اسکیوال با انتخاب دسته و یک  مقدار
        steps:
            1:select category (select_cat)
            2:select 1 data from select_cat
        input:
            url args:
                1:db (database name)
                2:tb (table name)
                3:session name for save out_text
        output:
            sql: for selecting data that select_cat=data
            save result in sesstion
    '''
    args=request.args
    response.title='S*S:'+'-'.join(args)
    x_data_s,db_name,tb_name,msg=_get_init_data()
    if not x_data_s: return msg
    text_app_val=request.vars['text_app_val']
    obj_name_x=args[2] #f'{db_name}|{tb_name}|{args[2]}'
    if text_app_val:
        
        if text_app_val=='#clear#':
            session[obj_name_x+'_val'],session[obj_name_x+'_ttl'],text_app_val='','',''
        else:
            session[obj_name_x+'_val']=text_app_val
            session[obj_name_x+'_ttl']=request.vars['text_app_ttl']
        return 'j_box_iframe_win_close | '+text_app_val
 
    db1=DB1(db_name)
    tasks=x_data_s['tasks']
    #--------------------------------------------------------------------------------------------------------------------------------------
    val_dic={x:tasks[x]['title'] for x in tasks if 'auth' not in tasks[x]}
    sel1=request.vars['sel1'] or session[obj_name_x+'_sel1'] or list(val_dic)[0]
    sel1_o=k_htm.select(_options=val_dic,_name='sel1',_onchange="submit();",add_empty_first=False,_value=sel1)
    
    
    session[obj_name_x+'_sel1']=sel1
    sel1_ttl=val_dic[sel1]
    sign,sign_o,sel2,sel2_o='','','',''
    #if sel1 in ["None",None]:sel1='prj'
    if sel1:
        traslate_dict = k_form.reference_select(tasks[sel1]['ref'])[0] if tasks[sel1]['type']=='reference' else {}
        val_dic = db1.grupList_of_colomn(tb_name,sel1,traslate_dict=traslate_dict)
        
        #010921# i1=XML('<input name="sign" id="sign" value="=" onchange="submit();">')
        signs=[" = "," != "," > "," < "," like "]
        sign=request.vars['sign'] or session[obj_name_x+'_sign'] or signs[0]
        sign_o=k_htm.select(_options=signs,_name='sign',_onchange="submit();",add_empty_first=False,_value=sign)#,_value=request.vars['sign']
        session[obj_name_x+'_sign']=sign
        if sign:
            sel2=request.vars['sel2'] or session[obj_name_x+'_sel2'] or list(val_dic)[0]
            if not sel2 in val_dic:sel2 =list(val_dic)[0]
            sel2_o=k_htm.select(_options=val_dic,_name='sel2',_onchange="submit();",add_empty_first=False,_value=sel2)#,_value=request.vars['sel2']_onchange="set_val();
            session[obj_name_x+'_sel2']=sel2
            sel2_ttl=val_dic[sel2]['title']
    result_val='"{}"{}"{}"'.format(sel1,sign,sel2)
    result_ttl='"{}"{}"{}"'.format(sel1_ttl,sign,sel2_ttl)
    #result_val_htm=XML(f'<div name="result" id="result">{result}</div>')

    return dict(htm=FORM(
                DIV(
                    DIV(sel1_o,_class="col-5"),
                    DIV(sign_o,_class="col-2"),
                    DIV(sel2_o,_class="col-5"), 
                    _class="row",_style='width:100%'),
                HR(), 
                DIV(    
                    DIV(result_val,_id='result_val',_class="col-4"),
                    DIV(result_ttl,_id='result_ttl',_class="col-5"),
                    DIV(BUTTON('حذف فیلتر',_class="btn btn-primary",_style='width:30%;height:30px;background-color:#ff5;color:#f00;',_onclick='clear_text_app()'),_class="col-3"),
                    _class="row",_style='width:100%'),
                HR(), 
                DIV(    
                    BUTTON('ok',_class="btn btn-primary",_style='width:100%;height:30px;background-color:#5f5;color:#000;',_onclick='fill_text_app()'),
                    INPUT(_id='text_app_ttl',_name='text_app_ttl',_value='',_type='hidden',), 
                    INPUT(_id='text_app_val',_name='text_app_val',_value='',_type='hidden',),
                    _class="row",_style='width:100%;height:90%'),
                SCRIPT("""
                    function fill_text_app(){
                        document.getElementById('text_app_val').value=document.getElementById('result_val').innerText;
                        document.getElementById('text_app_ttl').value=document.getElementById('result_ttl').innerText;
                    }
                    function clear_text_app(){
                        document.getElementById('text_app_val').value='#clear#';
                        document.getElementById('text_app_ttl').value='#clear#';
                    }
                """)    
                ,_id="form5"))
    #<input type="submit">
def get_session():
    if not request.args: return "not request.args"
    
    x=request.args[0]
    return session[x]
def ss_input_htm(db_name,tb_name,obj_name):
    '''
    o1=INPUT(_id=obj_name+'_val',_value=session[obj_name+'_val'])
    o2=[INPUT(_id=obj_name+'_ttl',_readonly='readonly',_value=session[obj_name+'_ttl']),
        k_htm.a("*",_target="box",reset=False,_href=URL('ss_set',args=[db_name,tb_name,obj_name]),j_box_params=f"'','{obj_name}_val,{obj_name}_val;{obj_name}_ttl,{obj_name}_ttl'")
        ]
    return XML(k_htm.x_toggle_s(o1,'-',add_objs=o2))
    '''
    obj_name_x=db_name+"_"+tb_name+"_"+obj_name
    ss_ttl_val=session[obj_name_x+'_ttl'] if session[obj_name_x+'_ttl'] else ''
    ss_val_val=session[obj_name_x+'_val'] if session[obj_name_x+'_val'] else ''
    return TABLE(
    TR(
        TD(INPUT(_id=obj_name+'_ttl',_readonly='readonly',_value=ss_ttl_val,_style='width:100%;',_title=ss_ttl_val),_style="width:90%"),
        TD(k_htm.a("*",_target="box",reset=False,_href=URL('ss_set',args=[db_name,tb_name,obj_name_x])
            ,j_box_params=f"ajax_do='',ajax_val_set='{obj_name}_val,{obj_name_x}_val;{obj_name}_ttl,{obj_name_x}_ttl'"),_style="width:10%"),
        ),
    TR(TD(INPUT(_id=obj_name+'_val',_value=ss_val_val,_class="filter_menu",_style='width:100%;'),_colspan="2",_style='width:100%;')),
    #TR(TD(obj_name_x)),
    _style="width:100%;",_class="table_filter_in")
def test_ajax_set():
    return dict(d=DIV(ss_input_htm('user','user','xx1') , ss_input_htm('user','user','xx2')))
def report_sessions():
    return TABLE(*[TR(TD(x),TD(session[x])) for x in session])
#astan.spks@gmail  hsjhk$hs\;s1403
#======================================================================================
def pivot():
    x_data_s,db_name,tb_name,msg=_get_init_data()
        
    data2_rows,data2_titles,data2_rows_num=DB1(db_name).select(tb_name,limit=0)
    data=[data2_titles]+data2_rows
    
    import k_file_x,json
    x_rows="[]" #"['frd_modir','f_nxt_u']"
    x_cols=""
    x_vlas=""
    x_agrg="Count" #Sum
    x_rndr="Heatmap"#Table
    set1=f'''
            rows: {x_rows}, 
            cols: ["{x_cols}"],
            vals: ["{x_vlas}"],
            aggregatorName: "{x_agrg}",
            rendererName: "{x_rndr}"'''
    set2="{"+set1+"}"
    tb2=json.dumps(data)
    htm0="" # f"<a class='btn btn-primary' href={URL('tmsh','aqc_report_daily_pivot',args=['user_day'])}>نفرات</a> - "
    #htm0+=f"<a class='btn btn-primary' href={URL('tmsh','aqc_report_daily_pivot',args=['prj'])}>پروژه</a> "
    table=XML(k_file_x.pivot_make_free(tb2,set2,htm0=htm0))
    return table
    #return dict(table=)
def prj_inf():
    """
    spks/form/prj_inf
    """
    
    cprj_id=request.vars['cprj_id'] 
    obj_inf={'type':'reference','len':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d},{cp_code},{cp_name}'},'title':'پروژه جاری','prop':['update']}

    #obj_inf={'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_code}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'کد پروژه'},
    x_data_verify_task('cprj_id',obj_inf,'','')
    prj_obj=k_form.obj_set(i_obj=obj_inf,x_dic={},x_data_s={}, need=['input'])
    _class="btn btn-primary"
    nn=k_htm.a('نامه ها',_target="box",reset=False,_class=_class,_href=URL('form','xtable',args=['paper','a'],vars={'data_filter':f'cprj_id={cprj_id}'})) if (session["admin"] or session["username"]=='ks') else 'نامه ها'
    return dict(htm=FORM(prj_obj['input'],
        nn,"-",
        k_htm.a('صورتجلسه',_target="box",reset=False,_class=_class,_href=URL('form','xtable',args=['doc_mm','a'],vars={'data_filter':f'c_prj_id={cprj_id}'})),"-",
        k_htm.a('گزارش عملکرد',_target="box",reset=False,_class=_class,_href=URL('form','xtable',args=['person_act','a'],vars={'data_filter':f'prj_id={cprj_id}'})),"-",
        k_htm.a('ماموریت ساعتی',_target="box",reset=False,_class=_class,_href=URL('form','xtable',args=['off_mamurit_saat','a'],
            vars={'data_filter':f'(c_prj_id = {cprj_id}) OR (c_prj_id like "%,{cprj_id},%") OR (c_prj_id like "{cprj_id},%") OR (c_prj_id like "%,{cprj_id}")'})),"-",
        DIV(cprj_id)
        ))
    
    