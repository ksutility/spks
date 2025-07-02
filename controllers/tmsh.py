# -*- coding: utf-8 -*-
# ver 1.00 1402/09/12
# -------------------------------------------------------------------------
''' value help
    x_data :# all form "extra data" that read from x_data.py file
        ساختار اطلاعات کل فرمها که از فایل مربوطه خوانده می شود
    x_data_s :# selected x_data = x_data for <select db_file><select table>    
'''
from gluon.custom_import import track_changes; track_changes(True)
from gluon.tools import Service
service = Service()
from k_sql import DB1
import k_htm
import k_form
from k_err import xxprint,xprint,xalert,xreport_var
from x_data import x_data ,x_data_verify_task
import k_date,k_time
import k_user
k_user.how_is_connect('tmsh')
now = k_date.ir_date('yy/mm/dd-hh:gg:ss')
# import datetime
# now = datetime.datetime.now().strftime("%H:%M:%S")

debug=False # True: for check error
db_path='applications\\spks\\databases\\'
#----------------------------------------------------------------------------------------------------------
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
            return f'error: >  "{args[0]}" not defined in Fieldes'
        db_name=args[0]
        #print (db_name)
        if len(args)<2:args+=['a']
        tb_name=args[1]# if len(args)>1 else 'a'

        if not db_name in x_data:return False,'','','error : "{}" not in ( x_data )'.format(db_name)
        x_data_s1=x_data[db_name]#x_data_select

        if not tb_name in x_data_s1:return False,'','','error : "{}" not in ( x_data["{}"] )'.format(tb_name,db_name)
        x_data_s=x_data_s1[tb_name]
        return x_data_s,db_name,tb_name,'ok'
    return False,'','','error : args not set correctly'
#---------------------------------------------------------------------------------------------------------- 
def _aqc_report_daily_file():
    import k_file_x,k_tools,k_xl_light 
    if k_tools.server_is_test():
        path1=r'\\192.168.88.196\share data\AQC\DES-AR\OTHER\KS\REPORT-DAILY-R03-030402_test.xlsm'
    else:
        path1=r'\\192.168.88.196\share data\AQC\DES-AR\REPORT-DAILY-R03-030402.xlsm'
    #path1=r"c:\temp\test\REPORT-DAILY-R03-030402_test.xlsx"
    return path1
#
def aqc_report_daily_export():
    data=_aqc_report_daily_read_1()
    from k_sql import DB1
    rep=DB1(path='applications\\spks\\databases\\aa\\aqc_report_daily.db').export('a',data[0],data[1:])
    return str(rep)
@cache(request.env.path_info, time_expire=36000, cache_model=cache.ram)
def _aqc_report_daily_read_1():
    #from xmlrpclib import ServerProxy
    from gluon.contrib.simplejsonrpc import ServerProxy
    import k_tools
    server_python_add=k_tools.server_python_add()
    #url=f'{server_python_add}//spks//tmsh//call//xmlrpc'
    URL = f'{server_python_add}/spks/tmsh/call/jsonrpc'
    server = ServerProxy(URL)#, verbose=True)
    
    #server = ServerProxy(f'{server_python_add}//spks//tmsh//call//xmlrpc')
    
    try:
        return server._aqc_report_daily_read_1_1()
        #return _aqc_report_daily_read_1_1()
    except:
        return []

#for python server - start
@service.jsonrpc
@service.jsonrpc2
def _aqc_report_daily_read_1_1():
    return "abc"
    import k_tools,k_xl_light
    if k_tools.server_is_python():
        data=[]
        data+=k_xl_light.read(wb_path =_aqc_report_daily_file(),
            ws_name='daily-report',
            row_st=2,row_en=0,col_st=1,col_en=10,empty_row='continue')
    return data
def call():
    return service()    
#for python server - end

def _aqc_report_daily_read(start_date=''):
    from gluon import current
    args=current.request.args
    #print (args)
    import k_file_x,k_tools
    read_xl=True
    read_db=True
    
    data=[]
    if read_xl: data+=_aqc_report_daily_read_1()
    if not data:data=[["نام و نام خانوادگی",'سال','ماه',"روز",'w','پروژه','دسته','اقدام',"زمان"]]

    if read_db : data+=_aqc_report_daily_read_2(start_date)
    return {'ok':True,'data':data}
  

def _aqc_report_daily_write(new_rows): 
    new_rows=[row[1:] for row in new_rows]
    import k_file_x,k_tools,kxl,k_xl_ms
    if k_tools.server_is_python():
        #k_file_x.xl_write(wb_path=path1,ws_name='daily-report',new_rows=new_rows)
        #kxl.append(wb_path=path1,sheet_name='daily-report',new_rows=new_rows)
        k_xl_ms.append(wb_path=_aqc_report_daily_file(),sheet_name='daily-report',new_rows=new_rows)
        return {'ok':True}
    else:
        return {'ok':False,'msg':"port shoud be :100"}   
       
def _aqc_report_daily_title(in_titels=''): #rows[0]
    t=in_titels if in_titels else ''
    x_titles=[  {'name':'id','width':'20px'},
            {'name':t[0],'width':'100px'},
            {'name':t[1],'width':'20px'},
            {'name':t[2],'width':'10px'},
            {'name':t[3],'width':'10px'},
            {'name':t[4],'width':'20px'},
            {'name':t[5],'width':'150px'},
            {'name':t[6],'width':'150px'},
            {'name':t[7],'width':'250px'},
            {'name':t[8],'width':'20px'}
            ]
    return x_titles
#@cache(request.env.path_info, time_expire=3600, cache_model=cache.ram)    
def aqc_report_daily_pivot():
    
    
    
    import k_file_x
    #return (str(data))
    case=request.args[0]
    if case=="user_day":
         set1="""{
            rows: ["نام و نام خانوادگی"], 
            cols: ["روز"],
            vals: ["زمان"],
            aggregatorName: "Sum",
            rendererName: "Table"}"""
    elif case=="prj":
        set1="""{
            rows: ["پروژه"], 
            vals: ["زمان"],
            aggregatorName: "Sum",
            rendererName: "Heatmap"}"""
    start_date=(request.args[1]).replace("-","/") if len(request.args)>1 else ''
    #print("start_date="+start_date)
    import json
    inp=_aqc_report_daily_read(start_date)
    if not inp['ok']:return inp['msg']
    data=inp['data']
    tb2=json.dumps(data)
    htm0= f"<a class='btn btn-primary' href={URL('tmsh','aqc_report_daily_pivot',args=['user_day'])}>نفرات</a> - "
    htm0+=f"<a class='btn btn-primary' href={URL('tmsh','aqc_report_daily_pivot',args=['prj'])}>پروژه</a> "
    return k_file_x.pivot_make_free(tb2,set1,htm0=htm0)
    
    return dict(table=XML(k_file_x.pivot_make_free(tb2,set1,htm0=htm0)))

#@cache(request.env.path_info, time_expire=3600, cache_model=cache.ram)   
def aqc_report_daily_kytable():
    inp=_aqc_report_daily_read()
    if not inp['ok']:return inp['msg']
    rows=inp['data']
    
    case="0" #request.args[0]
    import k_file_x,k_date
    cols=_aqc_report_daily_title(rows[0])
    
    tm={}  
    n_rows={}        
    for d in range(7):
        tm[d]=k_date.ir_date(add=-d)    
        n_rows[d]=[]         
    #return (str(tbl))
    for i,row in enumerate(rows[1:]):
        for d in range(7):
            if (row[1]==int(tm[d]['yyyy']) and row[2]==int(tm[d]['mm']) and row[3]==int(tm[d]['dd'])):
                n_rows[d]+=[[i+1+2]+row]
                break
            #n_rows=[[i]+row for i,row in enumerate(rows[1:]) if (row[1]==int(tm['yyyy']) and row[2]==int(tm['mm']) and row[3]==int(tm['dd']))]
    dv=[]
    for d in range(7):
        dv+=[H2(f"{tm[d]['yyyy']}/{tm[d]['mm']}/{tm[d]['dd']} - {tm[d]['www']}",_class="text-center"),
            k_htm.C_TABLE(cols,n_rows[d]).creat_htm(),HR()] 
    if case=="1":
        return k_file_x.kytable_make(rows=n_rows,titles=['id']+rows[0],widths=['3,3,20,5,2,2,7,10,10,10,4'],sum_colomn="زمان")
    else:
        return dict(div=DIV(dv))
        #return dict(t=TABLE(n_rows,_class="table table-border"))
        
def _aqc_report_daily_updata(new_data,col_titels):      
    
    #read data 
    inp=_aqc_report_daily_read()
    if not inp['ok']:return inp['msg']
    file_data=inp['data']
    
    #cut empty rows at end
    t_r=[]
    for row in new_data:
        if not row[1]:
            break
        t_r.append(row)
    new_data=t_r 
    
    #return XML("<hr>".join([str(x) for x in new_data]))
    import k_file
    #un_list=k_file.read('text',r"C:\temp\test\un_list.txt").split('\n')
    #prj_list=k_file.read('text',r"C:\temp\test\prj_list.txt").split('\n')
    un_list=DB1('user').cols_2_list(tb_name='user',text_format="{} {}",col_name_list=['name','family'])
    prj_list=DB1('a_cur_subject').cols_2_list(tb_name='a',text_format="{}",col_name_list=['cp_name'])
    import k_err
    k_err.xreport_var([un_list,prj_list])
    #print(str(un_list))
    
    data_inf={'1':{'type':'ref','select':un_list},
            '2':{'type':'num'}, #sal
            '3':{'type':'num'}, #mah
            '4':{'type':'num'}, #ruz
            '5':{'type':'text'}, #wd
            '6':{'type':'ref','select':prj_list}, #prj
            '7':{'type':'text'}, #subj
            '8':{'type':'text'}, #act
            '9':{'type':'num'}, #time
            '0':{'type':'num'},
            }
    def report_div(res,act_help,act_help_des):
        if res:    
            rep_des='نتیجه : اطلاعات مورد تایید است' 
            bg_color="#5f5"
        else:
            rep_des='نتیجه : در اطلاعات ورودی عدم انطباق های زیر وجود دارد'
            bg_color="#f55"   
        return DIV(
                DIV(act_help[1],_class="col-3"),
                DIV(act_help[0],_title=act_help_des,_class="col-3"),HR(),
                DIV(rep_des,_class="col-3"),
                _style=f"background-color:{bg_color};text-align:center;font-size:35px;",
                _class="row"
                )
    
    #return str(un_list) + str(prj_list)
    def validate_data(data):
        act_help=["بررسی ساختار اطلاعات ورودی  بر حسب فرمت ستون داده ها","گام 1 "]
        act_help_des="""در این مرحله برای هر کدام از ستونهای اطلاعات ورودی یک ساختار مشخص می شود و اطلاعات ورودی با آن ساختار مطابقت داده می شود
        انواع ساختار : متن، عدد، لیست 
        توضیح : لیست  یعنی مقدار داخل جدول باید یکی از مقادر یک لیست باشد
        اگر همه چیز درست باشد فقط پیقغام پاس شدن این مرحله نمایش داده می شود
        ولی اگر اشکالی موجود باشد اطلاعات دارای اشکال در داخل یک جدول در محل خود با رنگ قرمز نشان داده می شوند و سایر اطلاعات درست در جدول مربوطه به صورت خالی نشان داده می شوند
        """
        import k_form,k_htm
        rep_n=0

        trs=[]
        ok=True
        for r,row in enumerate(data):
            tds=[]
            for c,cell in enumerate(row):
                r_ok=k_form.input_validate(cell,data_inf[f'{c}'])
                
                if not r_ok: 
                    ok = False
                    rep_n+=1
                    tds+=[{'value':cell,'style':'background-color:#f55'}]
                    
                else:  
                    tds+=[{'value':'-','title':cell,'style':'background-color:#5f5' }]
                 
            trs+=[tds] 
        return {'ok':ok,
            'rep_des':report_div(ok,act_help,act_help_des),
            'rep_err':DIV(H1(f"ERROR : {rep_n} item"),k_htm.C_TABLE(col_titels,trs).creat_htm())
            }
    def check_duplicate(new_data,file_data,duplicate_col_check=[1,2,3,4]):
        act_help=["بررسی عدم  ورود دوباره اطلاعات موجود در اثر اشتباه کاربر","گام 2 "]
        act_help_des="""هدف از این بخش این است که با کمک یک سری روشها اطلاعاتی را که ممکن است  داپلیکیت و یا کپی ناقص  شده باشند و ورود آنها مشکل دار است را به کاربر نشان دهد
        تا کاربر پس از بررسی گزارش این مرحله در مورد ورود یا عدم ورود اطلاعات تصمیم  بگیرد
        در حال حاضر برای این موضوع روش زیر استفاده می شود
        یک سری ستون شاخص  کننده اطلاعات مشخص می شوند
        سپس برا اساس آن ستونها ردیف های هر 2 جدول ( اطلاعات جدید و اطلاعات روی فایل) بررسی می شوند و فصل مشترک آنها مشخص و نمایش داده می شود
        مثال : فرض کنید  ستونهای شاخص عبارتند از : فرد، سال، ماه و روز
        در این صورت هر کدام از 2 جدول در دسته های فرضی  که با فرد، ،سال،ماه و روز  مشخص می شوند  دسته بندی می شوند  اگر 2 جدول  دسته با مشخصه یکسانی داشته باشند یعنی در این قسمت احتمال خطا وجود دارد  و برنامه این دسته ها را نشان می دهد
        """
        #creat base dictionary for manage
        #base:base data xtract from new_data to speed check across file_data
        base={'new_data':[],'file_data':[],'sc':[]}#sc=selected colomn
        for row in new_data:
            s_row=[str(row[x+1]) for x in duplicate_col_check]
            if not s_row in base['sc']:
                base['sc'].append(s_row)
                base['new_data'].append([])
                base['file_data'].append([])
            ix=base['sc'].index(s_row)
            base['new_data'][ix].append(row)

        rep_n=0
        for i_f,row in enumerate(file_data):
            s_row=[str(row[x]) for x in duplicate_col_check]
            if s_row in base['sc']:
                ix=base['sc'].index(s_row)
                base['file_data'][ix].append([i_f]+row) 
                rep_n+=1
        err_txt1="عدم انطباق بر اساس فیلدهای روبرو :"
        rep=[]
        rep_ok=[]
        for i,s_row in enumerate(base['sc']):
            if base['file_data'][i]:
                intro=TABLE(TR(*[x for x in [err_txt1]+s_row],_style="background-color:#faa;text-align:center;font-size:30px;"),_style="direction: rtl;")
                t1=DIV('اطلاعات جدید',_style="background-color:#afa;text-align:center;font-size:24px")
                t2=DIV('اطلاعات ثبت شده در فایل',_style="background-color:#aaf;text-align:center;;font-size:24px")
                rep+=[DIV(intro,
                    DIV(t1,k_htm.C_TABLE(col_titels,base['new_data'][i]).creat_htm(),
                        t2,k_htm.C_TABLE(col_titels,base['file_data'][i]).creat_htm(),_style='border:10px dashed red;')
                    ,HR())]
            else:
                rep_ok+=[row for row in base['new_data'][i]]
        style=XML("""<style>
            table, td, th {  
              border: 1px solid #ddd;
              text-align: right;
            }
            table {
              border-collapse: collapse;
              width: 100%;
            }
            th, td { padding: 5px;}
            th { background-color:#f2f2f2; }
            </style>""")  
        ok = (not rep) or (len(rep)<=2)    
        return {'ok':ok,
            'rep_des':report_div(ok,act_help,act_help_des),
            'rep_err':DIV(style,
                        XML(f'new_data={len(new_data)} - base={len(base)}-rep_n={rep_n}-len(rep)={len(rep)}'),
                        *rep,HR(),
                        DIV(
                            DIV("اطلاعات مورد تایید در گام 2 به شرح زیر می باشند",
                                _style=f"background-color:#CFC;text-align:center;font-size:35px;")
                            ,k_htm.C_TABLE(col_titels,rep_ok).creat_htm()
                            )   
                        )
                    }
    vldt1=validate_data(new_data)
    if not vldt1['ok']:
        return DIV(vldt1['rep_des'],vldt1['rep_err'])
    re1=vldt1['rep_des']
    vldt2=check_duplicate(new_data,file_data,duplicate_col_check=[0,1,2,3])
    if not vldt2['ok']:
        return DIV(re1,HR(),vldt2['rep_des'],vldt2['rep_err'])
    re2=vldt2['rep_des']
    import k_tools
    if not k_tools.server_is_test():
        return DIV(re1,HR(),re2,HR(),H1("ادامه این فرایند در حال آماده سازی می باشد"))
    vldt3=_aqc_report_daily_write(new_rows=new_data)
    act_help=["ذخیره اطلاعات جدید در فایل اکسل","گام 3 "]
    act_help_des="""
        """
    re3=report_div(vldt3['ok'],act_help,act_help_des)
    if not vldt3['ok']:
         return DIV(re1,HR(),re2,HR(),re3,vldt3['msg'])
    return DIV(re1,HR(),re2,HR(),re3)
    
def user_timesheet():
    import k_htm,jdatetime,k_form,k_date,k_time
    x_date=request.vars['x_date'] or '14'+jdatetime.date.today().strftime('%y/%m/%d')
    x_ww=k_date.ir_weekday(x_date,in_format='yyyy/mm/dd',w_case=2)
    x_un=f'{session["username"]}- {session["user_fullname"]}'
    db_name='person_act'
    tb_name='a'
    x_data_s=x_data[db_name][tb_name]
    db1=DB1(db_name)
    rows,titles,rows_num=db1.select(tb_name,where=["AND",{'date1':x_date},"`frd_1` LIKE '{}%'".format(x_un[:3])],limit=0)
    
    
    #tuple to list , add link
    rows1=[]
    for row in rows:
        row1=list(row)
        id_n=titles.index('id')
        url=URL('form','xform_section',args=['person_act','a',row[id_n]],vars={'form_case':1})
        #url=URL('data','xtable',args=['person_act','a','edit',row[id_n]])
        #row1[id_n]=XML(A(row[id_n],_href='javascript:void(0)',_onclick=f"""j_box_show("{url}",true)""", _class="btn btn-primary"))#link
        row1[id_n]=XML(k_htm.a(row[id_n],_href=url,_target="box",_title=''))
        rows1+=[row1]
    mam_list_dict,mor_list_dict=help_tmsh_mm(x_un,x_date) 
    import k_tools
    out_titles=['id','cp_name','tact_cod','act_cat','act_des','time',]#'tact_cod',
    rows2=k_tools.list_list__2__list_list(rows1,titles,out_titles)
    rows2+=k_tools.list_dict__2__list_list(mam_list_dict,out_titles)
    rows2+=k_tools.list_dict__2__list_list(mor_list_dict,out_titles)
    
    table=k_htm.C_TABLE(out_titles,rows2).creat_htm(titels=out_titles,table_class="x",div_class='x')  

    obj_inf={'type':'fdate','prop':['update'],'def_value':x_date}
    x_data_verify_task('x_date',obj_inf,'','')
    date_gr=k_form.obj_set(i_obj=obj_inf,x_dic={},x_data_s={}, need=['input'])
    date_obj=date_gr['input']
    #date_obj=INPUT(_name="x_date",_id="x_date",_class='fDATE',_value=x_date,_onchange="submit();")

    return dict(
        x_ww= date_gr['help'], #x_ww,
        inp_date=FORM(date_obj,_name="form1",_id="form1"),#,date_obj,INPUT(_type='submit',value='ok')
        sum_time=k_time.sum_times([row[out_titles.index('time')] for row in rows2]),
        x_un=x_un,
        new_form=k_htm.a('+',_href=URL('form','xform_sd',args=['person_act','a','-1','auto_hide'],vars={'date1':x_date,'act_cat':'-','form_case':1}),_target="box",_title='فرم جدید'),
        table=table,
        hlp=help_tmsh_links(db1,tb_name,x_un,x_date))
def help_tmsh_links(db1,tb_name,x_un,x_date):
    '''
        show list of link for time sheet auto fill
    '''
    res=db1.select(tb_name,where=["AND","'date1' != '{}'".format(x_date),"`frd_1` LIKE '{}%'".format(x_un[:3])],limit=0,result='dict_x',order='date1',last=True)
    rows,titles=res['rows'],res['titles'] #,rows_num
    x_r=[]
    x_tit1=['prj_id','act_cat','act_des','time']
    x_tit2=['date1','cp_code','cp_name']+x_tit1
    #if not rows: 
    #return str(res['sql'])#rows[0])

    for row in rows:#.reverse():
        vv={x:row[titles.index(x)] for x in x_tit1}
        vv.update({'date1':x_date,'form_case':1})
        url=URL('form','xform_section',args=['person_act','a',-1],vars=vv)
        link=XML(k_htm.a('+',_href=url,_target="box",_title='فرم جدید پر شده',_class='btn btn-info'))
        x_r+=[[link , *[row[titles.index(x)] for x in x_tit2]]]
    table=k_htm.C_TABLE(['link']+x_tit2,x_r).creat_htm(div_class='div2')
    return table
    #if error : :#except Exception as err:         return XML("error in help_tmsh_links - "+"<br>"+str(res['sql'])+"<br>"+db1.path+"<br>"+str(len(rows))+"<br>"+str(err))
def help_tmsh_mm(x_un,x_date):
    '''
        mm=morakhasi v mamuriat
        show help list of inf from "morakhasi v mamuriat" forms
    '''
    import k_time
    db_mor=DB1('off_morkhsi_saat')
    rows_mor,titles_mor,rows_num_mor=db_mor.select('a',where=["AND",{'date' :x_date},"`frd_1` LIKE '{}%'".format(x_un[:3])],limit=0)
    mor_list_dict=[]
    for row in rows_mor:
        x=dict(zip(titles_mor,row))
        id_n=titles_mor.index('id')
        url=URL('form','xform_sd',args=['off_morkhsi_saat','a',row[id_n],'auto_hide'],vars={'form_case':1})
        mor_list_dict+=[{
            'act_cat':'-',
            'tact_cod':'-',
            'act_des':x['des_0'],
            'time':x['time_len'],
            'cp_name':'مرخصی سیستمی',
            'id':XML(k_htm.a(row[id_n],_href=url,_target="box",_title='',_class="btn btn-success"))
        }]
    db_mam=DB1('off_mamurit_saat')
    rows_mam,titles_mam,rows_num_mam=db_mam.select('a',where=["AND",{'date' :x_date},"`frd_1` LIKE '{}%'".format(x_un[:3])],limit=0)
    mam_list_dict=[]
    prjs=DB1('a_cur_subject').cols_2_dict('a','{0}','{1}',col_name_list=['id','cp_name'])
    prjs['0']='متفرقه'
    for row in rows_mam:
        x=dict(zip(titles_mam,row))
        id_n=titles_mam.index('id')
        c_prj_ids=(x['c_prj_id'] or '0').split(',')
        x_time=k_time.time_div(x['time_len'],len(c_prj_ids))
        for i,c_prj_id in enumerate(c_prj_ids):
            url=URL('form','xform_sd',args=['off_mamurit_saat','a',row[id_n],'auto_hide'],vars={'form_case':1})
            mam_list_dict+=[{
                'act_cat':'ماموریت سیستمی',
                'tact_cod':'-',
                'act_des':x['des_0'],
                'time':x_time[i],
                'cp_name':prjs[c_prj_id],
                'id':XML(k_htm.a(row[id_n],_href=url,_target="box",_title='',_class="btn btn-success"))
            }]
    #table_mam=k_htm.C_TABLE(titles_mam,rows_mam).creat_htm(div_class='div_mam') if rows_mam else ''
    #table_mor=k_htm.C_TABLE(titles_mor,rows_mor).creat_htm(div_class='div_mor') if rows_mor else ''
    return mam_list_dict,mor_list_dict# table_mam,table_mor
def _aqc_report_daily_read_2(start_date=''): 
    ''' aqc_report_daily_read =name_famil,yy,mm,dd,ww,prj,act_cat,act_des,time) '''
    import k_time
    def person_act_2_xl_like(person_act_row_dict):
        x=dict(person_act_row_dict)
        name_famil=' '.join(x['frd_1'].split(' ')[2:])
        #=['نام','سال','ماه','روز','ر.ه','پروژه','دسته','اقدام']
        return [
            name_famil ,#0 = name_famil
            int(x['date1'][:4]),#1 = yy
            int(x['date1'][5:7]),#2 = mm
            int(x['date1'][8:10]),#3 = dd
            '',#4 = ww
            x['cp_name'],#5 = prj
            x['act_cat'],#6 = act_cat
            x['act_des'],#7 = act_des
            k_time.time_2_num(x['time']) #8 = time
            ]    
    db1=DB1('person_act')
    where="`date1` > '{}'".format(start_date) if start_date else ''
    data2_rows,data2_titles,data2_rows_num=db1.select('a',limit=0,where=where)
    x_list=[]
    for row in data2_rows:
        x_list+=[person_act_2_xl_like(zip(data2_titles,row))]
    '''
    inp=_aqc_report_daily_read()
    if not inp['ok']:return inp['msg']
    data=inp['data']
    import k_err
    k_err.xreport_var([data])
    '''
    return x_list
def mon_report():
    # عدم حق دسترسی
    if not session['username'] in ['ks','snr','lvi','mhm','htk','hrm','atl']:return 'Error'
    if session['username'] in ['mlk','mss','nmn']:return ''
    args=request.args
    #if not args :return A1('Error')
    
    """
    spks/tmsh/mon_report?x_mon=1403/05
    """
    import k_htm,jdatetime,k_form,k_date,k_time
    mm_v=request.vars['mm_v'] or jdatetime.date.today().strftime('%m') #'14'+jdatetime.date.today().strftime('%y/%m')
    mm_obj=k_htm.select(_options=[str(x).zfill(2) for x in range(1,13)],_name='mm_v',_value=mm_v,_onchange="submit();",add_empty_first=False)
    
    #yy_v="1403" #k_htm.select(_options=['1403'],_name=fn,_value=f['value'])
    yy_v=request.vars['yy_v'] or "14"+jdatetime.date.today().strftime('%y') #def_date[:4] #'1403' #
    #print("-->>>"+jdatetime.date.today().strftime('%y'))
    yy_obj=k_htm.select(_options=['1403','1404'],_name='yy_v',_value=yy_v,add_empty_first=False,_onchange="submit();")
    yy_n=int(yy_v)
    #yy_obj
    x_mon=request.vars['x_mon'] or yy_v+r"/"+mm_v
    x_un=request.vars['x_un'] or session['username']
    un_obj=k_htm.select(_options={y['un']:y['fullname'] for x,y in k_user.ALL_USERS().inf.items() if y['loc'] in ['010','011','012','013']},_name='x_un',_value=x_un,_onchange="submit();")
    user_id=k_user.ALL_USERS().inf[x_un]['p_id'] #if session['username'] else '')
    
    db_name='time_io'
    tb_name='a'
    db1=DB1(db_name)
    rows,titles,rows_num=db1.select(tb_name,
            where=["AND",
                "`date_f` LIKE '{}%'".format(x_mon),
                {'user_id':user_id},
            ],last=False
        ,limit=0)
    
    #table=k_htm.C_TABLE(titles,rows).creat_htm()    
    #return dict(table=table)
    
    date_n=titles.index('date_f')
    time_n=titles.index('time')
    inf={}
    for row in rows:
        date,time=row[date_n],row[time_n]
        if not date in inf:
            inf[date]=[]
        inf[date]+=[time]
     
      
    # get morakhasi v mamuriat
    db_mor=DB1('off_morkhsi_saat')
    where=["AND","`date` LIKE '{}%'".format(x_mon),"`frd_1` LIKE '{}%'".format(x_un[:3])]
    rows_mor,titles_mor,rows_num_mor=db_mor.select('a',where=where,limit=0)
    db_mam=DB1('off_mamurit_saat')
    rows_mam,titles_mam,rows_num_mam=db_mam.select('a',where=where,limit=0)
    #print(where)
    #print(rows_mam)
    def mor_mam(x_date):
        mor_mam_list=[]
        for row in rows_mor:
            if row[titles_mor.index('date')]==x_date:
                x=dict(zip(titles_mor,row))
                id_n=titles_mor.index('id')
                url=URL('form','xform_sd',args=['off_morkhsi_saat','a',row[id_n],'auto_hide'],vars={'form_case':1})
                mor_mam_list+=[{
                    'act':'mor',
                    'time_st':x['time_st'],
                    'time_len':x['time_len'],
                    'time_en':x['time_en'],
                    'id':row[id_n],
                    'link':XML(k_htm.a(row[id_n],_href=url,_target="box",_title='',_class="btn btn-success"))
                    }]
        for row in rows_mam:
            if row[titles_mam.index('date')]==x_date:
                x=dict(zip(titles_mam,row))
                id_n=titles_mor.index('id')
                url=URL('form','xform_sd',args=['off_mamurit_saat','a',row[id_n],'auto_hide'],vars={'form_case':1})
                mor_mam_list+=[{
                    'act':'mam',
                    'time_st':x['time_st'],
                    'time_len':x['time_len'],
                    'time_en':x['time_en'],
                    'id':row[id_n],
                    'link':XML(k_htm.a(row[id_n],_href=url,_target="box",_title='',_class="btn btn-success"))
                    }]        
        return mor_mam_list
     
    out=[]
    row_colors=[]
    sum_min={'hzr':0,'mor':0,'mam':0,'all':0,'slh':0,'ezf':0}
    n_ok_day=0 #number of days that io_time not error
    pre_timesheet=k_user.pre_timesheet(x_un,x_mon)
    #print(f"{x_mon}-{x_un}" )
    #print("pre_timesheet = " + str(pre_timesheet))
    mm_n=int(mm_v)
    
    mm_len=k_date.ir_mon_len(yy_n,mm_n)
    for x_ruz in range(mm_len):
        date=x_mon+"/"+('00'+str(x_ruz+1))[-2:]
        #for date,times in inf.items():
        times=inf.get(date,[])
        out1=[date,k_date.ir_weekday(date,w_case=2)]
        if times:
            mor_mam_list= mor_mam(date) 
            c_day=C_TMSH_IO_day(times,mor_mam_list)
            sum_m,sum_t,o_times=c_day.hozur_time()
            for x in sum_min:
                sum_min[x]+=sum_m[x]
                if sum_min['all']>0:n_ok_day+=1
            out1+=[sum_t,c_day.sum_time['ezf'],c_day.sum_time['slh'],c_day.sum_time['mor'],c_day.sum_time['mam']]+o_times
            #out1+=[", " .join([str(c_io_time) for c_io_time in c_day.c_tmsh_io_times])]
            #out1+=[str(c_day.sum_time)+", " .join([f"{mor_mam['act']}-{mor_mam['time_len']}-{mor_mam['id']}" for mor_mam in c_day.mor_mam_list])]
            out1+=[", " .join([f"{mm['id']}-{mm['act']}" for mm in c_day.not_maches_mm])]
        else:
            out1+=['']*10
        out1+=[XML(k_htm.a(pre_timesheet.get(date,''),_target="box",_href=URL('tmsh','user_timesheet',vars={'x_date':date}),_class="btn btn-info"))]
        out+=[out1]
        row_colors+=[k_date.tatil_mode(date,out_case='color')] #[['#efe','#f00','#fa5','#f5a'][k_date.tatil_mode(date,out_case=='color')]]
    x_titels=['تاریخ','روز','حضور','اضافه کار','اصلاحی','مرخصی','ماموریت','ورود1','خروج1','ورود2','خروج2','-','عملکرد']#['date','sum','in_1','ou_1','in_2','ou_2']
    #print('row_colors = ' +str(row_colors))
    table=k_htm.C_TABLE(x_titels,out).creat_htm(table_class='x',row_colors=row_colors)    
    return dict(table=table,
        yy_obj=yy_obj,
        mm_obj=mm_obj,
        un_obj=(un_obj if session['username'] in ['ks','mlk','aaz'] else session['username']),
        hozur=k_time.min_2_time(sum_min['all']),
        ezf=k_time.min_2_time(sum_min['ezf']),
        mor=k_time.min_2_time(sum_min['mor']),
        mam=k_time.min_2_time(sum_min['mam']),
        n_day=len(inf)
        )

def hazeran():
    # عدم حق دسترسی
    if not session['username'] in ['ks','snr']:return A1('Error')
    if session['username'] in ['mlk','mss','nmn']:return ''
    
    """
    spks/tmsh/hazeran/      n_day_passed
    """
    args=request.args
    if not args :return A1('Error')
    add_day=-int(args[0]) if args else 0
    import k_htm,jdatetime,k_form,k_date,k_time
    #today='14'+jdatetime.date.today().strftime('%y/%m/%d')
    today=k_date.ir_date(xformat='yyyy/mm/dd',add=add_day)
    #return today
    
    
    db_name='time_io'
    tb_name='a'
    db1=DB1(db_name)
    rows,titles,rows_num=db1.select(tb_name,
            where={'date_f':today},last=False
        ,limit=0)
    
    
    user_id_n=titles.index('user_id')
    time_n=titles.index('time')
    inf={}
    #return str(rows)
    for row in rows:
        user_id,time=row[user_id_n],row[time_n]
        if not user_id in inf:
            inf[user_id]=[]
        inf[user_id]+=[time]
    out,n=[],0
    for user_id,times in inf.items():
        n+=1
        un,u_fn=k_user.p_id_2_un(user_id)
        t_len=k_time.min_2_time(k_time.time_2_min(times[-1])-k_time.time_2_min(times[0]))
        out+=[[n,user_id,un,u_fn]+(times+['']*6)[:6]+[t_len]]
    #rep=TABLE([TR([user_id]+times) for user_id,times in inf.items()])
    #return rep
    x_titels=['n','کد','un','نام','ورود','خروج','ورود','خروج','ورود','خروج','']    
    table=k_htm.C_TABLE(x_titels,out).creat_htm(table_class='1')#,row_colors=row_colors)   
    return dict(htm=DIV(today,table))
class C_TMSH_IO_TIME(): 
    def __init__(self,start,end,case=''):
        self.reset(start,end,case)
    def reset(self,start,end,case=''):
        self.start=start
        self.start_min=k_time.time_2_min(start)
        self.end=end
        self.end_min=k_time.time_2_min(end)
        self.len_min=self.end_min-self.start_min
        self.len_time=k_time.min_2_time(self.len_min)
        self.case=case        
    def match(self,start,end):
        start_min=k_time.time_2_min(start)
        end_min=k_time.time_2_min(end)
        st=max(start_min,self.start_min)
        en=min(end_min,self.end_min)
        match_len_min=en-st
        #print(f"start={start},end={end},match_len_min={match_len_min}")
        x_len_min=end_min-start_min
        return True if match_len_min>(x_len_min/2) else False
    def __str__(self):  
        return f'{self.start}-{self.end}-{self.case}'
class C_TMSH_IO_day():
    def __init__(self,io_times,mor_mam_list):
        c_tmsh_io_times=[]
        c_tmsh_io_times.append(C_TMSH_IO_TIME('00:00',io_times[0]))
        ll=len(io_times)
        for i in range(ll-1):
            case='' if i % 2 else 'hzr'
            c_tmsh_io_times.append(C_TMSH_IO_TIME(io_times[i],io_times[i+1],case))
        c_tmsh_io_times.append(C_TMSH_IO_TIME(io_times[-1],'24:00'))
    
        not_maches_mm=[]
        for mor_mam in mor_mam_list:
            x_re=self._find_match_io_time(c_tmsh_io_times,mor_mam)
            if not x_re:
                not_maches_mm+=[mor_mam]
        self.mor_mam_list=mor_mam_list
        self.io_times=io_times       
        self.not_maches_mm=not_maches_mm
        self.c_tmsh_io_times=c_tmsh_io_times
        
    def _find_match_io_time(self,c_tmsh_io_times,mor_mam):
        for i,c_io_time in enumerate(c_tmsh_io_times):
            if c_io_time.case=='':
                if c_io_time.match(mor_mam['time_st'],mor_mam['time_en']):
                    c_io_time.case=mor_mam['act']
                    if i==0:
                        c_io_time.reset(mor_mam['time_st'],c_io_time.end,mor_mam['act'])
                    if i==len(c_tmsh_io_times)-1:
                        c_io_time.reset(c_io_time.start,mor_mam['time_en'],mor_mam['act'])
                    return True     
        return False   
    def hozur_time(self):
        times=self.io_times
        o_times=(times+['-']*3)[:4]
        lt=len(times)
        sum_min={'hzr':0,'mor':0,'mam':0,'slh':0,'ezf':0}
        if lt%2==1:
            out_txt=f'io = {lt}'
            sum_min['hzr']=-1
            sum_min['all']=-1
            sum_time={}
            for x in sum_min:
                sum_time[x]=k_time.min_2_time(sum_min[x])
            sum_time['all']=out_txt
            sum_time['hzr']=out_txt
        else:
            for c_io_time in self.c_tmsh_io_times:
                if c_io_time.case:
                    sum_min[c_io_time.case]+=c_io_time.len_min
            #print(sum_min)
            #print(self.c_tmsh_io_times[1].start_min)
            if 420 < self.c_tmsh_io_times[1].start_min < 450:
                sum_min['slh']=self.c_tmsh_io_times[1].start_min-420
            sum_min['all']=sum([sum_min[x] for x in sum_min])
            sum_min['ezf']=sum_min['all']-440
            sum_time={}
            for x in sum_min:
                sum_time[x]=k_time.min_2_time(sum_min[x])
            out_txt=sum_time['all']
        self.sum_min=sum_min
        self.o_times=o_times
        self.out_txt=out_txt
        self.sum_time=sum_time
        return sum_min,out_txt,o_times             
