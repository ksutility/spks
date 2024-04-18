# -*- coding: utf-8 -*-
# ver 1.02 1401/08/14 
# -------------------------------------------------------------------------
''' value help
    x_data :# all form "extra data" that read from x_data.py file
        ساختار اطلاعات کل فرمها که از فایل مربوطه خوانده می شود
    x_data_s :# selected x_data = x_data for <select db_file><select table>    
'''

# ---- example index page ----
from gluon.custom_import import track_changes; track_changes(True)
from datetime import datetime
from k_sql import DB1

import k_htm
import k_form
from k_err import xxprint,xprint,xalert,xxxprint
from k_time import Cornometer
from x_data import x_data ,x_data_verify_task
import k_tools

debug=False # True: for check error
row_view=[{'lno':'r','sbj':'r'}]
now = datetime.now().strftime("%H:%M:%S")
db_path='applications\\spks\\databases\\'
style1='''
        <style>
            table_y {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              text-align: center;
              width: 100%;    }

            table_y td, #customers th {
              border: 1px solid #ddd;
              padding: 8px; }

            table_y tr:nth-child(even){background-color: #f2f2f2;}

            table_y tr:hover {background-color: #ffccaa;}

            table_y th {
              padding: 8px;
              padding-top: 12px;
              padding-bottom: 12px;
              background-color: #04AA6D;
              border: 1px solid #ddd;
              
              color: white; }
        </style>
      '''
style1_x='''
        <style>
            .table_x {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              text-align: center;
              width: 100%;    }

            .table_x td, #customers th {
              border: 1px solid #ddd;
              padding: 8px; }

            .table_x tr:nth-child(even){background-color: #f2f2f2;}

            .table_x tr:hover {background-color: #ffccaa;}

            .table_x th {
              padding: 8px;
              padding-top: 12px;
              padding-bottom: 12px;
              background-color: #04AA6D;
              border: 1px solid #ddd;
              
              color: white; }
        </style>
      '''      
style2='''
        <style>
            table_y {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              text-align: center;
              width: 100%;    }

            table_y td, #customers th {
              border: 1px solid #ddd;
              padding: 8px; }

            table_y tr:nth-child(even){background-color: #f2f2f2;}

            table_y tr:hover {background-color: #ffccaa;}

            table_y th {
              padding: 8px;
              padding-top: 12px;
              padding-bottom: 12px;
              background-color: #04AA6D;
              border: 1px solid #ddd;
              
              color: white; }
           
           a.box:link, a.box:visited {
              background-color: #2222aa;
              color: white;
              padding: 14px 25px;
              text-align: center;
              text-decoration: none;
              display: inline-block;
            }
            a.box:hover, a.box:active {
              background-color: #ff33ff;
            }
            
            
            input[type=button], input[type=submit], input[type=reset] {
              width:100%;
              background-color: #4CAF50;
              border: none;
              color: white;
              padding: 16px 32px;
              text-decoration: none;
              margin: 4px 2px;
              cursor: pointer;}
          input:hover {
              background-color: #ff33ff;
            }
        </style>
      '''
def err_out(fun_name,msg):
    print(f'error in fun({fun_name}),msg=({msg})')
def ref_get(get_case,ref_case,ref_inf,filde,base_val):
    '''
        get_case:'names'/'values'
            output case 
        ref_case:'all'/'one'
            output case '
        ref_inf:1 row in list of dict    
            all data in db of ref
        filde:dic
            the filde structure inf of base table
        base_val:text
            base table value in 1 cell of 1 row 
    '''
    if get_case not in ('names','values'):err_out('ref_get',)
    rc=ref_case
    if rc=='all':
        if get_case=='names':
            return ref_inf['titles']
        else:
            return ref_inf['rows_dict'][base_val]
    elif re=='one':
        if get_case=='names':
            return filde['name']
        else:
            return filde['ref']['format'].format(*ref_inf['rows_format_args_val'][base_va])
        
#prop:['read']=readonly ['hide']=hidden in table and edit row
             
def htm_correct(x):
    if x:
        t= x.replace('"','|')
        return t.replace('None','-')
    else:
        return '-'         
#------------------------------------------------------------------------------         
def get_table_filter(tasks,x_data_s):
    '''
        use in:2(show_xtable,show_kxtable)
    goal:
    ------
        -show input form for customizing filter data
        نمایش فرم تنظیم فیلتر ها
        -set new_value of filter data in goal variabl
        
    
    output:
    ------
        select_cols, all_cols,htm_table_filter
    '''
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
            '''
        }

    cols_filter=x_data_s['cols_filter']
    cols_filter1={'name':'cols_filter','type':'select','select':cols_filter}#,$hlp='prop':["can_add"],}
    data_filter=x_data_s['data_filter']
    data_filter1={'name':'data_filter','type':'select','select':data_filter}
    all_cols=list(tasks.keys())
    #print(f'all_cols={all_cols}')
    
    flt=request.vars['cols_filter']
    if flt:
        if flt[0]=='#':
            select_cols=cols_filter[int(flt[1:])] 
        else:
            flt_list=flt.split(',')
            if flt_list[0][0] in [0,1,2,3,4,5,6,7,8,9] :
                select_cols=[all_cols[int(x)] for x in flt_list]
            else:
                select_cols=flt_list
    else:
        select_cols= all_cols
    def set_htm_var(caption,obj,width='15vw',_help='',_val='',_meta=''):
        if type(obj)==str:
            name=obj
            val=request.vars.get(name,_val)
            xw=f"width={width}" if width else ""
            tt=f'''><input {_meta} name='{name}' id='{name}' value='{val}' style='width:{width};background-color:#88aaff''>'''
        else:
            name=obj['name']
            name2=name+'-x'
            obj['onchange']=f"document.getElementById('{name}').value=document.getElementById('{name2}').value;"
            x_data_verify_task(name2,obj)
            obj['def_value']=request.vars.get(name2,obj['def_value'])
            val=request.vars.get(name,_val)
            if width:obj['width']=width
            tt=XML(k_form.obj_set(i_obj=obj,x_dic={},x_data_s=x_data_s, need=['input'])[0]['input'])
            tt+=f'''><input {_meta} name='{name}' id='{name}' value='{val}' style='width:{width};background-color:#88aaff'>'''
        return (f'''<td><label><a title='{_help}'>{caption}</a></label>{tt}</td>''')
    htm_table_filter=XML('<div><form><table class="table table-bordered table-sm"><tr >'#style="height:10px;padding:0px;margin:0px"
                            +set_htm_var(caption='data_filter',obj=data_filter1,_help=hlp['data_filter'])
                            +set_htm_var(caption='cols_filter',obj=cols_filter1,_help=hlp['cols_filter'])
                            +set_htm_var(caption='table_class',obj='table_class',width='50px',_val=6,_meta="type='number' min=-1 max=6",_help='-1 to 6')
                            +set_htm_var(caption='page',obj='data_page_n',width='80px',_val=1,_meta="type='number' min=1" ,_help='صفحه شماره')
                            +set_htm_var(caption='rows',obj='data_page_len',width='80px',_val=20,_meta="type='number'" ,_help='تعداد ردیف در هر صفحه')
                            +'<td><input type="submit"></td></tr></table></form></div>')
    return select_cols, all_cols,htm_table_filter
#-----------------------------------------------------------------------------
@k_tools.x_cornometer
def get_table_row_view(xid,row,titles,tasks,select_cols,x_data_s):#,all_cols,ref_i):
    #use in:2(show_xtable,show_kxtable)
    #cm=Cornometer(i)
    '''
    INPUTS:
    ------
        xid:int
            id of 
            
    '''
    tds=['{:03d}'.format(xid)]
    #langs=['en']#langs /dir of text for html.obj.propery(dir) 'LTR' / 'RTL'
    x_dic=dict(zip(titles,row))
    for fn in select_cols:#fn=field name
        if 'hide' in tasks[fn]['prop']:
            tds.append('*')
            continue
        x_obj,time_recs=k_form.obj_set(i_obj=tasks[fn],x_dic=x_dic,x_data_s=x_data_s,xid=xid, need=['output'])
   
        #cm.tik(fn+'-1'+str(recs))    
        tds.append(x_obj['output'])
        #cm.tik(fn+'-2')
    #cm.report()    
    return tds  
#-----------------------------------        
def get_table_row_edit(xid,row_dic,titles,tasks,f_views,x_data_s,cancel_url):#,all_cols,ref_i):
    #use in:1(show_xtable)
    #old name=get_table_form
    #cm=Cornometer(i)
    trs=[TR('id',xid)]
    x_dic=row_dic# dict(zip(titles,row))
    #for fn in select_cols:#fn=field name
    def tb_rows(tasks,name_list,out_case,prop_read_check=False):
        """
            out_case='input'/ 'output'
        """
        trs=[]
        for fn in name_list:
            o_case=out_case
            f=tasks[fn]
            if prop_read_check and ('read' in f['prop']):o_case='output'
            x_obj,time_recs=k_form.obj_set(i_obj=f,x_dic=x_dic,x_data_s=x_data_s,xid=xid, need=[o_case])
            '''
            if debug :
                xprint('x_obj='+str(x_obj))
                xprint('i_obj='+str(tasks[fn]))
                xprint('x_dic='+str(x_dic))
            '''    
            #cm.tik(fn+'-1'+str(recs))    
            #tds.append(x_obj['input'])
            trs.append(TR(A(f['title'],_title=fn),x_obj[o_case]))
            #cm.tik(fn+'-2')
        #cm.report() 
        return trs
    #------------------------------------------------ 
    submit=INPUT(_type='submit',_style='width:100%,background-color:#ff00ff' ,_onclick='app_key("Y")')
    #submit=XML("""<INPUT type='button' value='تایید و ثبت' id='submit' name='submit' onclick='app_key("Y");'""")
    tr_sbmt=TR(TD(A('Cancel- goto list',_href=cancel_url),_style='width:40%'),TD(submit,_style='width:60%'))
    if f_views:
        trs+=tb_rows(tasks,f_views['view1'],'output')
        trs+=tb_rows(tasks,f_views['input'],'input')
        trs+=[tr_sbmt]
        trs2=tb_rows(tasks,f_views['view2'],'output')
        return TABLE(TR(TD(TABLE(*trs,_style='width:100%',_class='table_x'),_style='width:70%'),TD(TABLE(*trs2,_style='width:100%',_class='table_x'),_style='width:30%;background-color:#dff')),_style='width:100%')  
    else:
        trs+=tb_rows(tasks,tasks.keys(),'input',prop_read_check=True)
        trs+=[tr_sbmt]
        return TABLE(*trs,_style='width:100%',_class='table_x')   
#------------------------------- 
def get_init_data():
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
            return False,'','', f'error: >  "{args[0]}" not defined in Fieldes'
        db_name=args[0]
        #print (db_name)
        if len(args)<2:args+=['a']
        tb_name=args[1]# if len(args)>1 else 'a'
        x_data_s,msg1=get_x_data_s(db_name,tb_name)
        if x_data_s:
            return x_data_s,db_name,tb_name,msg1
        else:
            return False,'','',msg1
    return False,'','','error : args not set correctly'
def get_x_data_s(db_name,tb_name):
    if not db_name in x_data:return False,'error : "{}" not in ( x_data )'.format(db_name)
    x_data_s1=x_data[db_name]#x_data_select
    
    if not tb_name in x_data_s1:return False,'error : "{}" not in ( x_data["{}"] )'.format(tb_name,db_name)
    x_data_s=x_data_s1[tb_name]
    return x_data_s,'ok'
    

#-------------------------------------------------------------------------------------------------------------------------------
#==== LEVEL 1 (always use by Level0) ===========================================================================------------------------------------------------------------------
def show_table():
    #show simple table(no field setting need) by all data 
    #نمایش یک جدول ساده( بدون توجه به نوع فیلد) و  شامل کلیه فیلدها
    if not session["admin"]:return 'access denied -(only admin can access this page)'
    
    def insert_test():
        pass
        r1=db.insert_data(table_name,['lno','sbj','i_per','i_des','i_date'],('12','abcd','2','3','xx'))
        out= f'filed =>{r1["sql"]}<br>add = {r1["done"]}<br><h1>{now}</h1><hr>'
    def table_show():
        thead=THEAD(TR(*[TH(x) for x in titles]))
        def edit(i):
            return A('edit',_href=URL(args=(args[0],args[1],'edit',i))) if session["admin"] else '-'
        return DIV(TABLE(thead,TBODY(*[TR(*row,edit(i)) for i,row in enumerate(rows)]),_class='table0'),_class='div_table'),len(rows)
    def row_edit(titles,vals='',comp_vals=''):
        titles.remove("id")
        if comp_vals=='':
            c_v=['' for x in titles]
        else:
            c_v=[]
            for i in range(len(titles)):
                c_v.append([c[i+1] for c in comp_vals])
        if vals=='':
            vals=['' for x in titles]
            xid=-1
        else:
            xid=vals[0]
            vals=vals[1:]
        def changed():
            for i,t in enumerate(titles):
                if request.vars[t]:
                    break
            else:
                return False
            for i,t in enumerate(titles):   
                if request.vars[t]!=vals[i]:
                    return f'{request.vars[t]} != {vals[i]}'
            return False
        def save():
            def update():
                vv={t:request.vars[t] for t in titles}
                xu=db1.update_data(table_name,vv,{'id':xid})
                return "UPDATE",BR(),"sql="+str(xu) #+"<hr>"+str(vv)
            def insert():
                vv=[request.vars[t] for t in titles]
                r1=db1.insert_data(table_name,titles,vv)
                return "INSERT",BR(),"sql="+str(r1['sql']),BR(),"row id="+str(r1['id']),BR(),"result:"+str(r1["done"])
            #---------------------------------------------------    
            if xid==-1:
                r1=insert()
            else:
                r1=update()
            return DIV(r1)
        url_b=URL(args=(args[0]))
        if changed():
            return DIV(save(),BR(),A('goto list',_href=url_b))
        else:
            i_table=FORM(DIV(TABLE(*[TR(titles[i],INPUT(_name=titel, _value=vals[i]),*c_v[i]) for i,titel in enumerate(titles)],_class='table0'),_class='div_table'),INPUT(_type='submit'), _action='', _method='post')
            cvt=request.vars['cv'] or ''
            #print('cvt='+cvt) 
            cv=INPUT(_value=cvt,_name='cv',_id='cv')
            return DIV(f'ID=:{xid}',cv,i_table,A('Cancel- goto list',_href=url_b))
#---------------------------------------------------------------------------------------------------
    args=request.args
    if len(args)>0:
        db_name=args[0]
        if len(args)<2:args+=['a']
        table_name=args[1] 
        db1=DB1(db_path+db_name+'.db')
        #- print('abc')
        rows,titles,rows_num=db1.select(table_name,limit=0)
        try:
            pass
        except:
            return f'error: table_name={table_name}'
        if len(args)>3 and args[2]=='edit':
            #--------------------
            cv=request.vars['cv']
            comp_vars=[]
            if cv:
                cvs=cv.split(',')
                comp_vars=[rows[int(x)-1] for x in cvs]
            #---------------------
            return row_edit(titles,rows[int(args[3])-1],comp_vars)
        if len(args)>2 and args[2]=='insert':
            return row_edit(titles)
        else:
            table,nr=table_show()
            l1=A(' NEW RECORD',_href=URL(args=(args[0],args[1],"insert"))) if session["admin"] else '-'
            t1=TABLE(TR(l1,"rows:"+str(nr),"time="+now,"args="+str(args)),_class='table0')
            return DIV(XML(style1),t1,table) 
    return 'error: argumwnt is needed'
#----------------------------------------------------------------------  
@k_tools.x_cornometer
def show_xtable(x_data,ref_case='one'):#,tb_name,tasks):#'example2.db'
    '''
    goal:
        show / manage a formated & costomize table
        show only cols/fields/task that defied in data_structur and 'hide' str not in its 'prop' attbute
    inputs:
        ref_case:select (one/all)
            show all ref table filde or one
        
    '''
    #from k_sql import DB1
    #set_table()
    def xtable_show(tb_name,tasks,where,x_data_s):
        ''' func desc
        goal:
        ------
            - show formated & costomize table 
            - link to edit each row for auth users
        input:
        ------
            tb_name:str
                name of table
            tasks:dict
                column/field selected {name:{props}}
            where:
                data filter = sql where
            x_data_s:dict
                table data structur
                کل ساختار اطلاعاتی مرتبط با جدول مورد نظر 
                base json inf that tasks is 1 part of it
        test:
        ------
            open url:
                /spks/data/xtable/paper/a
        '''
        rows,titles,rows_num=db1.select(table=tb_name,where=where,page_n=request.vars['data_page_n'],page_len=request.vars['data_page_len'],order=x_data_s['order'])
        #if rows:rows.reverse()
        select_cols, all_cols,htm_table_filter=get_table_filter(tasks,x_data_s)
        new_titles={'n':{'width':'30px'},'id':{'width':'30px'}}
        #xxxprint(vals=tasks)
        #xxxprint(args=select_cols,launch=True)
        for i,x in enumerate(select_cols):
            new_titles[tasks[x]['title']]={'title':f'{i} : {x}'}
        #thead=THEAD(TR(TH('n',_width='30px'),TH('id',_width='30px'),*[TH(A(tasks[x]['title'],_title=f'{i} : {x}')) for i,x in enumerate(select_cols)]))#,_style="top:0;position: sticky;")
        trs=[]

        for i,row in enumerate(rows):
            tds=get_table_row_view(row[0],row,titles,tasks,select_cols,x_data_s)#, all_cols,ref_i)
            n=str(i+1)
            n=A(n,_title='edit',_href=URL(args=(args[0],args[1],'edit',row[0]))) if session["admin"] else n
            x_edit={'title-name':'id','args':[args[0],args[1],'edit']}
            trs.append([n,*tds])
        from k_table import K_TABLE
        table_class=request.vars['table_class'] if request.vars['table_class'] else '0'
        return K_TABLE.creat_htm(trs,new_titles,table_class=table_class,table_type=""),len(rows),htm_table_filter #DIV(,_style='height:100%;overflow:auto;')
    
    def row_view(tb_name,tasks,f_views,x_data_s,xid): 
        '''
            show 
        '''
        rows,titles,rows_num=db1.select(tb_name,where={'id':xid})
        #titles.remove("id")
        #vals=list(rows[xid-1][1:])
        vals=list(rows[0]) #xid-1])
        htm_vals=get_table_row_view(xid-1,vals,titles,tasks,select_cols=tasks.keys(),x_data_s=x_data_s)#, all_cols,ref_i)
        trs=tuple([TR(x,htm_vals[i]) for i,x in enumerate(titles)])
        table=TABLE(trs)
        
        url_b=URL(args=(args[0:1]))
        bt1=A('goto list',_href=url_b)
        return DIV(table,bt1)
    def row_edit(tb_name,tasks,f_views,x_data_s,xid=-1):
        '''
            xid=id of row that shoud be edit
                if xid=-1 => insert new row 
        '''
        def form_send():
            #check form is send? (any field have value)
            for i,t in enumerate(titles):
                if request.vars[t]:
                    return True
        def changed(titles):
            def inf_rep(x):
                return f' # type={type(x)}'+(f',len={len(x)}' if type(x)==str else '')
            if form_send():    
                for i,t in enumerate(titles):
                    if request.vars[t]!=vals_dic[t]:
                        return f'{t} => {request.vars[t]} != {vals_dic[t]}' + inf_rep(request.vars[t])+inf_rep(vals_dic[t])
            return False
        def do_chang(titles):
            if form_send():
                for i,t in enumerate(titles):
                    if request.vars[t]!=vals_dic[t]:
                        print(f'val={str(vals_dic)}')
                        vals_dic[t]=request.vars[t]    
        
        def save(titles):
            def update(titles):
                vv={t:(lambda x:','.join(x) if type(x)==list else (x or " ").strip())(request.vars[t])  for t in titles} # multiple select refine output
                if x_data_s['base']['mode']=='table+':
                    import k_date
                    vv.update({'app_un':session['username'],'app_dt':k_date.ir_date('yy/mm/dd-hh:gg:ss'),'app_ip':request.client})
                result=db1.row_backup(tb_name,xid)
                xu=db1.update_data(tb_name,vv,{'id':xid})
                rr=f"{db1.get_path()}<br> UPDATE: {xu}<hr> backup<br>"+"<br>".join([f'{x}={str(y)}' for x,y in result.items()])
                #+"<brr>vv"+str(vv)+"<br>vars:"+str(list(request.vars))+"<br>titels:"+str(titles)
                return rr
            def insert(titles):
                #return "INSERT",BR(),"titles="+str(titles),BR(),"vv="+str(vv)
                vv=[(lambda x:','.join(x) if type(x)==list else (x or " ").strip())(request.vars[t])  for t in titles]
                #vv=[request.vars[t].strip() for t in titles ]
                tt=[t for t in titles]#request.vars]
                r1=db1.insert_data(tb_name,tt,vv)
                rr=f"{db1.get_path()}<br> INSERT:result="+str(r1["done"])+" => "+str(r1["sql"])+" | "+str(r1["id"]) #+"<hr>"+str(vv)
                return rr
            #--------------------------------    
            if xid==-1:
                r1=insert(titles)
            else:
                r1=update(titles)
            return DIV(XML(r1))

        #url_b=URL(args=(args[0]))
        
        
        if xid==-1:
            #rows,titles,rows_num=db1columns_list(tb_name),where={'id':1})
            titles=db1.columns_list(tb_name)
            titles.remove("id")
            vals=['' for x in titles]
            lk_u=lk_d=''
            
        else:
            rows,titles,rows_num=db1.select(tb_name,where={'id':xid})
            titles.remove("id")
            vals=list(rows[0][1:])#rows[xid-1][1:])
            
            args_u=list(args)
            args_u[3]=str(int(args[3])+1)
            args_d=list(args)
            args_d[3]=str(int(args[3])-1)
            lk_u=A('+',_href=URL(args=args_u),_class="btn btn-primary")
            lk_d=A('-',_href=URL(args=args_d),_class="btn btn-primary") #class=a1
        
        vals_dic=dict(zip(titles,vals))
        x_titels=list(set(titles)& set(request.vars.keys()))    
        ch_rep=changed(x_titels)
        t_s=save(x_titels) if ch_rep else '' 
        '''
        if len(args)>3:
            args[3]=str(int(args[3])+1)
            url_b=URL(args=args)
        else:
            url_b=URL(args=(args[0],args[1]))
        redirect(url_b)
        '''
        #return DIV(save(),BR(),A('goto list',_href=url_b))
        #else:

        """
        tasks_val_set(tasks,vals_dic,titles)
        edit_xtable_show(tasks,xid,f_views)
        """

        #return "tasks="+str(tasks)+"<br>vals_dic="+str(vals_dic)+"<br>titles="+str(titles)
        do_chang(x_titels)
        in0=XML("<INPUT type='hidden' size='5' id='text_app' name='text_app'>")
        table=get_table_row_edit(xid,vals_dic,titles,tasks,f_views,x_data_s,cancel_url=URL(args=(args[0],args[1])))
        return FORM(in0,table,TABLE(TR(lk_u,lk_d),TR(t_s)), _action='', _method='post')
#---------------------------------------------------------------------------------------------------------- 
    #tasks,f_views
    script1='''<script>
        $(document).ready(function(){
            $("table td").click(function(){
                $("#viewcell").text($(this).text());
            });
            $("table th").click(function(){
                $("#viewcell").text($(this).text());
            });
        });
    </script>
    '''      
    #flt=request.vars['filter']
    filter_data=request.vars.get('data_filter') #eval(flt) if flt else ''
    #print ('filter_data='+str(filter_data))
    #print(str(request.vars))
    #exec('xx={"a":"2"}')
    #xx=eval('{"a":"2"}') #'x={'+filter_data[1:-1]+'}')
    #return filter_data['id'] #filter_data
    args=request.args
    response.title='xtable-'+'-'.join(args)#[x] for x in range(0,len(args),2)])
      
    x_data_s,db_name,tb_name,msg=get_init_data()#x_data)
    if not x_data_s:
        return msg
    else:
        db1=DB1(db_path+db_name+'.db')
        #- print(db_name)
        tasks=x_data_s['tasks']
        f_views=x_data_s['views']
        
        #db=DB1(db_name)
        if len(args)>3 and args[2]=='view':
            return DIV(XML(style1_x),row_view(tb_name,tasks,f_views,x_data_s,int(args[3])))
        if len(args)>3 and args[2]=='edit':
            return DIV(XML(style1_x),row_edit(tb_name,tasks,f_views,x_data_s,int(args[3])))
        if len(args)>2 and args[2]=='insert':
            return DIV(XML(style1_x),row_edit(tb_name,tasks,f_views,x_data_s))
        else:
            table,nr,htm_table_filter=xtable_show(tb_name,tasks,filter_data,x_data_s)
            htm_head=DIV(TABLE(TR(  TD(A('+',_title='NEW RECORD',_href=URL(args=(args[0],args[1],"insert")),_class="btn btn-primary") if session["admin"] else '-',_width='20px')
                                ,TD(A(str(nr),_title="rows:"),_width='40px')
                                ,TD(DIV('...',_id='viewcell',_name='viewcell'))),_class="table0"))#,_style='position:sticky;top:0px')
            #return DIV(XML(style1_x),XML(script1),htm_table_filter,htm_head,table,)
            return DIV(XML(script1),htm_table_filter,htm_head,table,)
#----------------------------------------------------------------------------------------------------------    
def show_kxtable(x_data):
    x_data_s,db_name,tb_name,msg=get_init_data()
    if not x_data_s:
        return msg
    tasks=x_data_s['tasks']
    db1=DB1(db_path+db_name+'.db')
    import kytable
    def table_show(tb_name,tasks,x_data_s):
        #fieldes{name:'',type:'text' or 'reference prj' or 'select'}
        select_cols, all_cols,htm_table_filter=get_table_filter(tasks,x_data_s)
        rows1,ttls1,rows_num=db1.select(tb_name)#'paper')
        ttls2=['id']+[tasks[x]['title'] for x in select_cols]#+['link']
        wids2=['3']+[tasks[x]['width'] for x in select_cols]#+['4']
        rows2=[]
        ref_i={}
        for i,row in enumerate(rows1):
            tds=get_table_row_view(row[0],row,ttls1,tasks,select_cols, x_data_s)
            rows2.append(tds)#+[str(A('edit',_href=URL(args=(args[0],'edit',i))))])
        return kytable.kxtable_prepar(rows2,ttls2,wids2,"")
    #----------------------------------------------------
    return table_show(tb_name,tasks,x_data_s)
#----------------------------------------------------
def table_show_filter(rows,titles,filters,tasks):
    #filter={filde_name:filde_value)
    f_rows=[r for r in rows if sum([1 for x in filters if r[titles.index(x)]==str(filters[x])])==len(filters)]
    thead=['id']+[f['title'] for fn,f in tasks.items()]
    trs=[]
    for i,row in enumerate(f_rows):
        tds=[row[0]]+[row[titles.index(fn)] for fn,f in tasks.items()]
        trs.append(TR(*tds))
    n=len(f_rows)
    return (TABLE(thead,*trs),n) if n>0 else ('',n)

#---------------------------------------------------------------------------------------
def show_sptable(x_data,ref_col):
    x_data_s,db_name,tb_name,msg=get_init_data()
    if not x_data_s:
        return msg
    tasks=x_data_s['tasks']
    db1=DB1(db_path+db_name+'.db')
    #split data by col
    args=request.args

    rows1,titles1,rows_num=db1.select(tb_name,limit=0)
    tasks1=tasks #[args[0]]

    f=[x for xn,x in tasks1.items() if xn==ref_col][0]
    ref=f['ref']
    print ('ref='+str(ref))
    db2=DB1(db_path+ref['db']+'.db')
    rows2,titles2,rows_num=db2.select(ref['tb'],limit=0)
    tasks2=x_data[ref['db']][ref['tb']]['tasks']
    
    thead=['id']+[x['title'] for xn,x in tasks2.items()]
    trs=[]
    for i,row in enumerate(rows2):
        tds=[row[0]]+[row[titles2.index(fn)] for fn,f in tasks2.items()]
        filter1={ref_col:row[titles1.index(ref['key'][1:-1])]}
        tb1,n=table_show_filter(rows1,titles1,filter1,tasks1)
        
        trs.append(TR(*tds,n))
        trs.append(XML('<tr><td colspan="4">'+str(tb1)+'</td></tr>'))#TD(tb1)))
    return DIV(XML(style1),TABLE(*trs,_class="table6"))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ==== level 0 (use by user)=========================================================================================================
def index():
    f_l='لیست - '
    ff={'prj':'پروژه ها','paper':'نامه ها','a_dspln':'رسته های مهندسی','user':'لیست همکاران','job':'سمتها'}
    ff1={'xtable':'{}','select':'-'}
    trs=[]
    lnk="""/spks/""" 
    #print(URL())

    links={
    "papers=>todo !=''":lnk+"""data/xtable/paper/a?data_filter=act_todo+%21%3D%22%22&cols_filter=&table_class=2&data_page_n=1&data_page_len=20""",
    "papers=>نامه ها- پیگیری":lnk+"""data/xtable/paper/a?data_filter=act_pey+%21%3D%22%22&cols_filter=&table_class=2&data_page_n=1&data_page_len=20""",
    "papers=>ALL":lnk+"""data/xtable/paper/a""",
    "papers=>GGA-Layouts":lnk+"""data/xtable/paper?data_filter=%22prj%22%3D%2229%22+AND+%22des%22+like+%22%25L-%25%22&cols_filter=&table_class=1""",
    "papers=>standard":lnk+"""data/xtable/paper?data_filter=%22prj%22%3D%2248%22""",
    "-----------":"", 
    "spks help":lnk+"""file/f_list?xpath=D:\ks\I\web2py\Applications\spks\help""",
    "km":lnk+"""file/f_list/ks/i/dropbox/01-KM/1-ACT?xpath=d%3A """,
    "TimeSHeet":lnk+"""xfile/read/ks/i/dropbox/01-KM/1-ACT/11-KS/Timesheet/TMST-NNNN-AQC.mm?xpath=d%3A""",
    "------------":"",
    "form":lnk+"""form/xform/test/b/1""",
    "form-table":lnk+"""data/table/test/b"""
    }
    rem={
    "home":lnk+"""data/index""",
    "spks-file-index":lnk+"""file/index""",
    }
    if session["admin"]:
        trs+=[TR(*[TH(f_l+x) for x in ['0','x','kx','sp','select']])]#[TR(TH(f_l+'0'),TH(f_l+'X'),TH(f_l+'KX'),TH(f_l+'SP'),TH('update'))]
        for arg in [['prj','a'],['paper','a'],['a_dspln','a'],['user','user'],['job','a']]:#,'a'),('eng','a'),('user','user')]:
            trs+=[TR(*[A(ff[arg[0]],_href=URL(xtbl,args=(arg)))   for xtbl in ['table','xtable','kxtable','sptable','select']])]
        t1=DIV(DIV(A('admin',_href=URL('spks','default','admin'))),
              DIV(A('xxprint_reset_html',_href=URL('spks','data','_xxprint_reset_html'),_target="x_frame"))
              )
        t2="<hr>"      
        t2+='<br>'.join([f"<a href={links[x]} > {x} </a>" for x in links])    
    else:
        #redirect(URL('spks','file','index'))
        trs+=[TR(*[TH(f_l+x) for x in ['x','select']])]
        for arg in [['prj','a'],['paper','a'],['a_dspln','a'],['user','user']]:
            trs+=[TR(*[A(ff1[xtbl].format(ff[arg[0]]),_href=URL(xtbl,args=(arg)))   for xtbl in ['xtable','select']])]
        t1=DIV('-')
        t2=''
    return dict(x=DIV(TABLE(*trs,_class="table"),t1,XML(t2)))
    
def _xxprint_reset_html():
    import k_err
    return k_err.xxprint_reset_html()
def set_tables():
    # WIP
    set_table(db_name)
    return 'tables created'

def table():
    return dict(table=show_table())

def xtable():

    return dict(table=show_xtable(x_data))#,'paper',tasks['paper']))
def sptable():
    return dict(table=show_sptable(x_data,'prj'))
def kxtable():
    return dict(table=XML(show_kxtable(x_data)))#,'paper',tasks['paper']))
def ggtable():
    # WIP
    args=request.args
    #if len(args)>0:
        #try:
        #grid = SQLFORM.grid(db[args[0]],deletable=False)
        #grid = SQLFORM.grid(db.prj,deletable=False)
        #return dict(grid=grid)
        #except:
        #return f"error of open table({args[0]})"
    return "enter table name in argument of url:l="+str(args)
def select_i(x_data):
    '''
        goal 1=creat sql by pick category then pick data
        هدف = ساختن دستور اسکیوال با انتخاب دسته و یک  مقدار
        input:
            1:select category (select_cat)
            2:select 1 data from select_cat
        output:
            sql: for selecting data that select_cat=data
    '''
    args=request.args
    response.title='update-'+'-'.join(args)
    x_data_s,db_name,tb_name,msg=get_init_data()
    if not x_data_s:
        return msg
    else:
        '''
    if len(args)>0:
        if args[0] not in tasks:
            return f'error: >  "{args[0]}" not defined in Fieldes'
        db_name=args[0]
        if len(args)<2:args+=['a']
        tb_name=args[1]
        '''
        db1=DB1(db_path+db_name+'.db')
        tasks=x_data_s['tasks']#tasks[args[0]]
        ##-----
        val_dic={x:tasks[x]['title'] for x in tasks}
        s1=k_htm.select(_options=val_dic,_name='sel1',_value=request.vars['sel1'],_onchange="submit();")#$('#res1').text($(this).val())")
        ##-----
        s2,t1='',''
        if request.vars['sel1']:
            sel1=request.vars['sel1']
            traslate_dict =k_form.reference_select(tasks[sel1]['ref']) if tasks[sel1]['type']=='reference' else {}
            val_dic=db1.grupList_of_colomn(tb_name,sel1,traslate_dict=traslate_dict)
            #print(str(val_dic))
            #s2=k_htm.select(_options=val_dic,_name='sel2',_value=request.vars['sel2'],_onchange="set_val();")
            s2=k_htm.select(_options=val_dic,_name='sel2',_value=request.vars['sel2'],_onchange="submit();")
            #------
            def remove(base_str,chars):
                #remove chars from base_str
                for x in chars:
                    base_str=base_str.replace(x,'')
                return base_str
            #----
            result1='"{}"{}'.format(request.vars["sel1"],request.vars["abc"])
            t1=DIV(TABLE(   THEAD(TR(*[TH(x) for x in ['index','Grup','number']])),
                        TBODY(*[TR(A(i+1,_href=URL('xtable',args=args,vars={'data_filter':f'{result1}"{v}"'}))
                                   ,val_dic[v]['title'],val_dic[v]['num']) for i,v in enumerate(val_dic)]),_class="table0"),_class="div_table")
                        #TBODY(*[TR(i+1,*remove(val_dic[v],"()").split(':')) for i,v in enumerate(val_dic)]))
        ##-----
        #010921# i1=XML('<input name="abc" id="abc" value="=" onchange="submit();">')
        i1=k_htm.select(_options=["=","!=",">","<","like"],_name='abc',_value=request.vars['abc'],_onchange="submit();")
        v=request.vars
        result='"{}"{}"{}"'.format(request.vars["sel1"],request.vars["abc"],request.vars["sel2"])
        result_htm=XML(f'<div name="result" id="result">{result}</div>')
        return XML(f'''<form id="form5"><label>data_filter(dict)</label>
                    {TABLE(TR(s1,i1,s2,result_htm))}
                    <input type="submit">
                    {A('Open Selected List-باز کردن لیست انتخاب شده',_href=URL('xtable',args=args,vars={'data_filter':result}))}
                    </form>
                    {t1}
                    <script>
                    var filter1=0
                    function submit() {{
                        document.getElementById("form5").submit();
                    }}
                    
                    $('input[type=submit]').hide();
                    </script>''')
                    
        '''
                    function set_val(){{
                        document.getElementById("result").innerHTML='"'+document.getElementById("sel1").value+'"'+document.getElementById("abc").value+'"'+ document.getElementById("sel2").value+'"';
                        
                    }}  
                    set_val();
                    '''
        
    return 'error'
def select():
    return dict(x=DIV(XML(style2),select_i(x_data)))
#                    <a href='../xtable/paper?data_filter="prj=\\'36\\'"'>---</a>
'''
        final goal=update multi filed by sql
        هدف= تغییر و به روز رسانی چندین فیلد به صورت همزمان
'''
def rc():#run 1 command
    if not session["admin"]:
        return 'you are not admin'
    #return 'ok'
    args=request.args
    if not args:
        pass
    #- print(str(args))
    cmd=args[0]
    db_name,tb_name=args[1:3]
    db1=DB1(db_path+db_name+'.db')
    if cmd=='columns_add':
        #sample /spks/data/rlc/columns_add/user/user?col_add_list=app_u,app_d
        rep= db1.add_columns(tb_name,request.vars['col_add_list'])
    elif cmd=='columns_add_standard':  #test ok 020905---------------------
        #sample /spks/data/rc/columns_add_standard/user/user
        # note this pro shoud run 1 time for every table that x_data_s['base']['mode']='table+'
        rep=db1.columns_add(tb_name,['app_un TEXT','app_dt TEXT','app_ip TEXT'])
    elif cmd=='columns_del_x':  
        #sample /spks/data/rc/columns_del_x/user/user
        # note this pro run for correct 1 error 
        rep=db1.columns_del(tb_name,['app_u','app_d'])     
    elif cmd=='creat_backup_table':  #test ok 020905---------------------------
        #sample /spks/data/rc/creat_backup_table/user/user
        # note this pro run 1 time for every table 
        cols=db1.columns_list(tb_name)
        cols[cols.index('id')]='xid'
        rep=db1.define_table(tb_name+"_backup",fields_txt='id INTEGER PRIMARY KEY AUTOINCREMENT,', fields_order={"TEXT":cols})
        return dict(table=k_htm.val_report(rep))
    elif cmd=='columns_list':  
        #sample /spks/data/rc/columns_list/user/user
        rep1=db1.columns_list(tb_name)
        rep2=db1.columns_list(tb_name+"_backup")
        return dict(msg='cols_list',table1=k_htm.val_report(rep1),table2=k_htm.val_report(rep2))
    elif cmd=='creat_table_4_form':  
        #sample /spks/data/rc/creat_table_4_form/a_sub_p/a
        #sample /spks/data/rc/creat_table_4_form/paper/a
        # a_dspln/a  
        x_data_s=x_data[db_name][tb_name]
        cols1=list(x_data_s['tasks'].keys())
        cols2=[f'step_{i}_{t}'  for i,x in enumerate(x_data_s['steps'].keys()) for t in ['un','dt','ap']]
        cols2+=['f_nxt_s','f_nxt_u'] 
        '''
        'f_nxt_st'=form_next_step_number 0=first  
        'f_nxt_un'=form_next_user  
        '''
        cols1+=cols2
        rep={}
        rep['table-1']=db1.define_table(tb_name,fields_txt='id INTEGER PRIMARY KEY AUTOINCREMENT,', fields_order={"TEXT":cols1}) 
        rep['table-1-add']=db1.columns_add(tb_name,cols1,"TEXT")
        rep['table-2']=db1.define_table(tb_name+"_backup",fields_txt='id INTEGER PRIMARY KEY AUTOINCREMENT,', fields_order={"TEXT":['xid']+cols1}) 
        rep['table-2-add']=db1.columns_add(tb_name+"_backup",cols1,"TEXT")
    elif cmd=='creat_table_4_xtable':  
        #sample /spks/data/rc/creat_table_4_xtable/job/a
        #sample /spks/data/rc/creat_table_4_xtable/paper/a
        x_data_s=x_data[db_name][tb_name]
        cols1=list(x_data_s['tasks'].keys())
        cols2=[f'app_{t}' for t in ['un','dt','ip']]
        '''
        
        '''
        cols1+=cols2
        rep={}
        rep['table-1']=db1.define_table(tb_name,fields_txt='id INTEGER PRIMARY KEY AUTOINCREMENT,', fields_order={"TEXT":cols1}) 
        rep['table-1-add']=db1.columns_add(tb_name,cols1,"TEXT")
        rep['table-2']=db1.define_table(tb_name+"_backup",fields_txt='id INTEGER PRIMARY KEY AUTOINCREMENT,', fields_order={"TEXT":['xid']+cols1}) 
        rep['table-2-add']=db1.columns_add(tb_name+"_backup",cols1,"TEXT")    
    elif cmd=='update_fields':  
        #sample /spks/data/rc/update_fields/eng/a/code
        #sample /spks/data/rc/update_fields/user/user/eng
        #replace_inf={"%AR":"AR","%ST":"ST","%CV":"CV","%EL":"EL","%ME":"ME","%PM":"PM","%OT":"OT"}
        replace_inf={"%OT":"GE"}
        fldn=args[3]#field name
        rep1=[]
        for x,y in  replace_inf.items():
            rep=db1.update_data(tb_name,set_dic={fldn:y},x_where=f" {fldn} LIKE '{x}'")#{fldn:x})
            rep1+=[k_htm.val_report(rep)]
        return DIV(rep1)
    elif cmd=='update_auto_filed':  
        '''
            update select_cols of a table automaticaly
        '''
        #sample /spks/data/rc/update_auto_filed/paper/a?select_cols=prj,man_crt
        select_cols=request.vars['select_cols']
        print(select_cols)
        if select_cols:
            select_cols=select_cols.split(',')
        else: 
            return f"select_cols={select_cols}"
        rows,titles,rows_num=db1.select(table=tb_name,where={},page_n=1,page_len=20)#limit=20)
        x_data_s,msg1=get_x_data_s(db_name,tb_name)
        ou=''
        trs=[]
        for i,row in enumerate(rows):
            #tds=get_table_row_view(row[0],row,titles,x_data_s['tasks'],select_cols,x_data_s)
            x_dic=dict(zip(titles,row))
            xid=row[0]
            tds=[xid]
            for fn in select_cols:
                i_obj=x_data_s['tasks'][fn]
                x_obj,time_recs=k_form.obj_set(i_obj=i_obj,x_dic=x_dic,x_data_s=x_data_s,xid=xid, need=['output'])
                x_save=x_dic[fn]
                import k_tools
                tds+=[k_tools.var_compare(x_save,x_obj['output_text'])['msg']]#output_text
                #if x_save:x_save.strip()
                #if x_save!=x_obj['output']:
                #    tds+=[f" != ,{len(x_save)},{len(x_obj['output_text'])},{x_save},{x_obj['output_text']}"]
                #else:
                #   tds+=[f" == {x_save}"]
            trs+=[tds]
        from k_table import K_TABLE
        rep=K_TABLE.creat_htm(trs,['id']+select_cols,table_class='1')
        return dict(x=DIV(rep))
    #return dict(table=TABLE(THEAD([rep[0]],_class="thead-light"),TBODY(rep[1:]),_class="table table-bordered table-hover"))  
    return dict(x=k_htm.val_report(rep))
    #return dict(table=TABLE(THEAD(['cols_list'],_class="thead-light"),TBODY(rep),_class="table table-bordered table-hover"))        
def test1(): #test1
    import os,k_file
    f_path2=os.path.join("0-file",'xxx4.json')
    k_file.write('json',f_path2,tasks)
    return 'ok'
def report_inf():
    #pprint
    tt="<br>".join([str(x)+":"+str(request[x]) for x in request])
    env=request.env
    tt+="<hr>"+"<br>".join([str(x)+":"+str(env[x]) for x in env])
    return tt

def update():
    #if not 'do' in request.vars:return '"do" is not in request.vars'
    field='man_crt'
    inf={   '4':'ks',
            '21':'saa',
            '2':'at',
            '3':'ig',
            '5':'mhe',
            '6':'aav',
            '7':'mra',
            '9':'maa',
            '1':'',
            'None':''}
    db_name='paper-test1' #args[0]
    db1=DB1(db_path+db_name+'.db')
    xx=[]#{}
    for x,y in inf.items():
        xr=db1.update_data(table_name="a",set_dic={field:y},x_where={field:x})
        xx.append(k_htm.dict_2_table(xr))
        xx.append(XML("<hr>"))
    return dict(a=DIV(*xx))
def diff():
    db2=DB1(db_path+'paper-test1.db')
    db1=DB1(db_path+'paper - copy.db')
    rows1,titles1,row_num1=db1.select('a',limit=0)
    rows2,titles2,row_num2=db2.select('a',limit=0)
    dif={}
    for i,row in enumerate(rows1):
        dd=''
        for j,y in enumerate(row):
            if y!=rows2[i][j]:
                dd+=f'{titles1[j]}:({y}=>{rows2[i][j]})'
        dif[row[titles1.index('id')]]=dd
    return dict(a=k_htm.dict_2_table(dif))
