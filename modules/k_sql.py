# -*- coding: utf-8 -*-
"""
این ماژول شامل دو کلاس اصلی برای مدیریت پایگاه داده SQLite و ساخت شرط‌های SQL است.

کلاس‌ها:
--------
- C_SQL: ساخت عبارات WHERE برای SQL به‌صورت داینامیک
- DB1: مدیریت کامل پایگاه داده SQLite شامل ساخت، درج، جستجو، و به‌روزرسانی رکوردها

تاریخچه نسخه:
-------------
- 1400/11/19 - بروزرسانی select (پشتیبانی از where_dict) - ver 1.07
    -update select (can get where_dict)
- 1402/09/05 - نسخه 1.10
- 020805 - افزودن 3 تابع ستونی (add, ren, del)
    -   add exec func
"""
from k_ui import var_report
import datetime
#from gluon import cache,current
#cache=cache.Cache(current.request)
import jdatetime #khayyam
from k_err import xxxprint,xxprint,xprint
debug=False # True#
today=jdatetime.date.today().strftime('%y-%m-%d') #khayyam.JalaliDate.today().strftime('%y-%m-%d')
def f_now():
    x=str(datetime.datetime.now())#trftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    return today + "-" + x
def report_txt(x_txt_list):
    """
    دریافت یک رشته از متغیرها به صورت کاما جدا و تولید گزارش متنی از مقادیر فعلی آن‌ها.

    پارامتر:
    --------
    x_txt_list : str
        رشته‌ای شامل نام متغیرها مانند "var1,var2"

    خروجی:
    -------
    str : خروجی به فرمت "var1=..., var2=..."
    """             
    x_list=x_txt_list.split(',')
    return ", ".join([x+'='+str(eval(x)) for x in x_list])
def report_db_change(db_name,t1,dif_list,idx=1):#030815
    """AI-docstring
    ثبت تغییرات انجام‌شده در پایگاه داده در فایل متنی به منظور مستندسازی.

    پارامترها:
    ----------
    db_name : str
        مسیر فایل پایگاه داده (با پسوند .db)

    t1 : str
        توضیح کوتاه درباره عملیات انجام‌شده

    dif_list : list
        لیستی از توضیحات تغییرات انجام‌شده

    idx : int
        شماره‌گذاری ردیف تغییرات برای پیگیری راحت‌تر
    """
    name_add='' if dif_list else '_no_change'
    file_path=db_name[:-3]+name_add+ '.txt'
    if debug:xxxprint(msg=['report','file_path='+file_path,''],args=dif_list)
    f = open(file_path,'a',encoding='utf8')
    f.write('\n'+f_now() + " : " +t1 + f" - (#{idx})")
    if dif_list:f.write('\n####  '.join(['']+dif_list))
    f.close()
class C_SQL():
    def __init__(self):
        pass
    def test_where(self,q_where,res1,db1,tb1): 
        test_where=res1['sql_where']
        sql_where=self.where(q_where)
        sql_t2="SELECT * FROM {} WHERE ".format(tb1)+ sql_where
        res2=db1._exec(sql_t2,fetch=True)
        re_c=" != " if res2['data']!=res1['rows'] else " = "
        re_c2 =" !=" if sql_where!=test_where else " = "
        xxxprint(out_case=3,msg=["C_SQL",re_c, re_c2],vals={
            "res1['rows']":res1['rows'],
            "res2['rows']":res2['data'],
            "sql_where 1":test_where,
            "sql_where 2":sql_where,
            "res1":res1,
            "res2":res2,
            })
    def where_cell(self,field_name,field_select_data,act="=",int_2_int=True): #erwer
        """AI-docstring
        تولید عبارت WHERE برای SQL بر اساس نوع داده ورودی.

        ورودی‌ها:
        ---------
        q_where : str | dict | list
            شرط موردنظر برای SQL. نوع‌های پشتیبانی‌شده:
                - str: شرط SQL به‌صورت مستقیم ("id=1")
                - dict: مانند {'id': 1, 'name': 'Ali'}
                - list: لیست ترکیبی از شروط با AND یا OR

        add_where_text : bool
            اگر True باشد، کلمه "WHERE" به ابتدای رشته خروجی افزوده می‌شود.

        خروجی:
        -------
        str : عبارت شرط WHERE کامل
        """
        if type(field_select_data)==None:
            return "`{}` {} '{}'".format(field_name,act,str(field_select_data))
        elif type(field_select_data)==str:
            return "`{}` {} '{}'".format(field_name,act,field_select_data) 
        elif type(field_select_data)==int:
            pt="`{}` {} {}" if int_2_int  else "`{}` {} '{}'"
            return pt.format(field_name,act,field_select_data)
        elif type(field_select_data)==list:
            if len(field_select_data)==1:
                return "`{}` {} '{}'".format(field_name,act,field_select_data[0])
            else:
                return "`{}` in {}".format(field_name,','.join([f'{x}' for x in field_select_data]))
        elif type(field_select_data)==dict:   
            if 'sql' in field_select_data:
                return field_name + " " + field_select_data['sql']
        else:
            return "`{}` = ''".format(field_name,)        
    def where(self,q_where,add_where_text=True):
        """AI-docstring
        تولید عبارت WHERE برای SQL بر اساس نوع داده ورودی.

        ورودی‌ها:
        ---------
        q_where : str | dict | list
            شرط موردنظر برای SQL. نوع‌های پشتیبانی‌شده:
                - str: شرط SQL به‌صورت مستقیم ("id=1")
                - dict: مانند {'id': 1, 'name': 'Ali'}
                - list: لیست ترکیبی از شروط با AND یا OR

        add_where_text : bool
            اگر True باشد، کلمه "WHERE" به ابتدای رشته خروجی افزوده می‌شود.

        خروجی:
        -------
        str : عبارت شرط WHERE کامل
        """   
        """
        q_where : str/dict/list
            str: natural sql string
            list: 
                list of 2 list and (list[0] =name_list) and (list[1]= val_list):
                    [['field_name 1',...],['field_select_data 1',...]]
                    sample:[['un','sub_prj'],['atl','hrsj-100']]
                list of q_where and (list[0] = "AND" / "OR"          help_search_text=("__where__list__")
                    -list[
            dict: {'field_name 1':'field_select_data 1',...}
                sample:{'un':'atl','sub_prj':'hrsj-100'}
            -------------------    
            field_select_data : str / list  
                str: natural sql string
                    result(for sql_where) = field_name + " = " + field_select_data 
                list : 
                    result = field_name + " in " + (items of field_select_data)
                dict :
                    if field key=
                        'sql':
                            result = field_name + field_select_data['sql']
        """
        
        #--------------------------------------  
        # " AND ".join(['{}=?'.format(n) for n in name_list])
        #--------------------------------------      
        q_name= " WHERE " if add_where_text else " "
        if not q_where:return ''
        if type(q_where)==str:
            res= q_name+q_where
        elif type(q_where)==list:
            if len(q_where)==2 and type(q_where[0])==list and type(q_where[1]) in [list,tuple]:
                res= q_name + " AND ".join([self.where_cell(w_n,q_where[1][i]) for i,w_n in enumerate(q_where[0])])
            elif q_where[0]=="AND": #__where__list__":
                res= q_name + " AND ".join([self.where(q_w,add_where_text=False) for q_w in q_where[1:] if q_w])
            elif q_where[0]=="OR": #__where__list__":
                res= q_name + " OR ".join([self.where(q_w,add_where_text=False) for q_w in q_where[1:] if q_w])    
            else:
                res= q_name + " AND ".join([self.where(q_w,add_where_text=False) for q_w in q_where if q_w])
            if res== q_name:res=''
        elif type(q_where)==dict:
            res=q_name + " AND ".join([self.where_cell(name,q_where[name]) for name in q_where]) 
        else:
            xxxprint(msg=["error","where type not correct",''],launch=True)
        #xxxprint(msg=["result",str(type(q_where)),''],vals={'q_where':q_where,'res':res})
        return res
    #-------------------------------------------
    def add_limit(self,sql,offset,page_n,page_len,limit,order,last):
        x_order = f' ORDER BY ' + order if order else ''
        x_order += ' DESC' if (last and order) else ''
        sql = sql+x_order
        if not limit:return sql
        if offset:        
            return sql+f' limit {offset},{limit}' if limit else sql
        else:   #if page_n:
            from k_tools import int_force
            x_page=int_force(page_n,1) 
            x_page_len=int_force(page_len,20) 
            x_offset=(x_page-1) * x_page_len 
            return sql+f' limit {x_offset},{x_page_len}' if limit else sql
#===================================================================================
class DB1():
    import sqlite3
    # path=d:\\temp\\example1.db
    con,cur,path,dbn="","","",""
    tables_name={}
    columns={}
    def __init__(self,db_name='',path='',ext='db'):
        db_path='applications\\spks\\databases\\'
        if (path and not db_name):  
            path=path 
        else: 
            if not path:path= db_path
            path=path+db_name+"."+ext   #'example2.db'
        try:
            self.con = self.sqlite3.connect(path)
        except:
            print('error on connect to =>'+path)
        self.cur = self.con.cursor()
        self.path=path
        self.get_tables_name()#prn=True)
        self.dbn=self.path.partition("//")[2]
    ##---@cache(time_expire=5, cache_model=cache.ram)
    #@cache.action(time_expire=300, cache_model=cache.ram, session=True, vars=True, public=True)
    def _exec(self,sql,val_list=[],fetch=False):
        
        result={'def':'_exec','sql':sql,'data':[]}
        if debug:
            xxxprint(msg=["sql_exe",'',''],vals=result )
            
            self.cur.execute(sql,val_list)
            if fetch:
                result['data']=self.cur.fetchall()
            self.con.commit()
            result.update({'done':True})
            return result
        
        
        #xxxprint(msg=[self.dbn,"sql="+sql,self.path])
        try:
            self.cur.execute(sql,val_list)
            if fetch:
                result['data']=self.cur.fetchall()
            self.con.commit()
            result.update({'done':True})
            if debug:
                xxxprint(msg=[self.dbn,str(result['done'])+ " - " + sql,self.path],vals=result)
        except Exception as err:
            result.update({'done':False,'Error':str(err),'val_list':val_list})  
            xxxprint(msg=['err',err, self.path],err=err,vals={'result':result,'sql':sql})
        return result
    def _connect_sql(self,db_file= r"data.db"):
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None """
        conn = None
        try:conn = self.sqlite3.connect(db_file)
        except Error as e:  xprint(e)
        return conn
    def _dic_2_set(self,dic_list):
        def a_b(a,b):
            pt="`{}`={}" if type(b)==int else "`{}`='{}'"
            return pt.format(a,b)
        return ",".join([a_b(x,dic_list[x]) for x in dic_list])
    def close(self):
        self.con.close()
    
    def _titles(self):
        try:
            return [description[0] for description in self.cur.description]
        except Exception as err:
            xxxprint(msg=['err','',''],err=err)
    # mini func   ------------------------------------------------------------------------------------------------ 
    def get_tables_name(self,prn=False):
        '''
            self.tables_name =cash
                {path: tables_name list}
        '''
        tables_n=[]
        if self.tables_name:
            if self.path in self.tables_name:
                tables_n=self.tables_name[self.path]
                #xxxprint(msg=['cash''',''])
        if not tables_n:     
            result=self._exec("SELECT name FROM sqlite_master WHERE type='table';",fetch=True)
            tables_n=result['data'] if result['done'] else []
            #xxxprint(msg=['reload''',''])
        self.tables_name[self.path]=tables_n
        if prn:xxxprint(msg=['path=',self.path,''],args=tables_n,vals=self.tables_name)
        return tables_n
    def columns_list(self,table_n):
        result=self._exec('select * from {}'.format(table_n))
        if result['done']:
            self.columns[table_n]=self._titles()
            return self.columns[table_n]
        return []
        '''
        try:
            #self.cur.execute()
            #self.con.commit()
            
            return self._titles()
        except Exception as err:
             return []
        '''
    def columns_del(self,table_n,col_del_list):
        #report=[['Result','SQL']]
        for col_name in col_del_list:
            sql="ALTER TABLE {} DROP COLUMN {};".format(table_n,col_name)
            report=self._exec(sql)
        return report        
    def columns_ren(self,table_n,col_cur_name,col_new_name):
        #report=[['Result','SQL']]
        sql="ALTER TABLE {} RENAME COLUMN {} TO {};".format(table_n,col_cur_name,col_new_name)
        report=self._exec(sql)
        return report
    def columns_add(self,table_n,col_add_list,col_add_type=''):
        if not table_n in self.columns:self.columns_list(table_n)
        report=[]
        for col_name in col_add_list:
            if not col_name in self.columns[table_n]:
                sql="ALTER TABLE {} ADD COLUMN {} {};".format(table_n,col_name,col_add_type)
                report+=[self._exec(sql)]
        return report
    def define_table(self,table_n, fields_txt, fields_order={}):
        '''
            fields_order=   {"fields_property1":"field_11,field_12,..","fields_property2":"field_21,field_22,..",...}
                sample input=          {"TEXT NOT NULL" :"lno,sbj,i_per",
                                        "TEXT"          :"i_end,i_date"}
            goal=
                                            lno TEXT NOT NULL,
                                            sbj TEXT NOT NULL,
                                            i_per TEXT NOT NULL,
                                            i_end TEXT,
                                            i_date TEXT,
        '''
        #FIELD_ORDER_TEXT
        fo_t=',\n'.join([f'`{f}` {fo}' for fo in fields_order for f in fields_order[fo]])
        
        """ example:        self.cur.execute('''CREATE TABLE IF NOT EXISTS paper (
                                                    lno TEXT NOT NULL,
                                                    i_end TEXT,
                                                    i,
                                                    UNIQUE(lno, sbj,i_per,i_des,i_date));''')
        CREATE TABLE IF NOT EXISTS "user" ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `un` TEXT, `m_w` TEXT, `pre_n` TEXT, `name` TEXT, `family` TEXT, `ps` TEXT, `job` TEXT, `tel_mob` TEXT, `tel_wrk` TEXT, `office` TEXT, `eng` TEXT, `file_access` TEXT, `a_name` TEXT, `app_un` text, `app_dt` text, `app_ip` text )
        """
            
        field_t =  fields_txt + fo_t 
        sql='''CREATE TABLE "{}" (
                        {});'''.format(table_n,field_t)
        #sql='''CREATE TABLE IF NOT EXISTS "xx" (`id` INTEGER PRIMARY KEY AUTOINCREMENT);'''
        xxxprint(3,msg=['do','define_table',self.dbn],vals={'sql':sql})
        try:
            rep=self._exec(sql)
        except:
            rep={'sql':sql,'done':False}
        return {'def':'define_table','exec':rep}

    
    
    
    def count(self,table_name,where=''):
        result={'sql':''}
        try:
            sql_where=C_SQL().where(where)
            sql="SELECT COUNT(*) FROM {}".format(table_name)+ sql_where
            result['sql']=sql
            result=self._exec(sql,fetch=True)
            result['count']=result['data'][0][0]
        except Exception as err:
            result['count']=0
            result.update({'done':False,'Error':str(err)})  
            xxxprint(msg=['err','count',f"{self.dbn}.{table_name}"],vals=result)
        return result    
    #--------------------------------------------
    def sql_set(self,_top,_fields_name,_table_name, _where , _order):
        xtop=f" TOP {_top} " if _top else ""
        xwhere=C_SQL().where(_where)
        xorder=" ORDER BY {_order}" if _order else ""
        return f"SELECT {xtop} {_fields_name} FROM {_table_name} {xwhere} {xorder}"    
    #---------------------- main func ----------------------------------------------------------------------------------------------    
    def select(self,table='',sql='',where='',result='list',offset=0,page_n=1,page_len=20,limit=20,last=True,order='id',debug=False):
        """AI-docstring
        اجرای کوئری SELECT با پشتیبانی از فیلتر، ترتیب، صفحه‌بندی و قالب خروجی‌های متنوع.

        پارامترها:
        ----------
        table : str
            نام جدول هدف برای SELECT

        sql : str
            رشته SQL مستقیم، در صورت تنظیم نخواهد از پارامتر table استفاده شد

        where : str | dict | list
            شرایط WHERE به صورت دلخواه

        result : str
            نوع خروجی: 'list', 'dict', یا 'dict_x'

        offset : int
            شیفت اولیه نتایج در صورت استفاده مستقیم

        page_n : int
            شماره صفحه در حالت صفحه‌بندی

        page_len : int
            تعداد رکوردها در هر صفحه

        limit : int
            محدودیت تعداد نتایج

        last : bool
            اگر True باشد ترتیب نزولی در خروجی اعمال می‌شود

        order : str
            فیلد مرتب‌سازی

        debug : bool
            فعال‌سازی چاپ اطلاعات برای اشکال‌زدایی

        خروجی:
        -------
        بسته به نوع result: لیست رکوردها، دیکشنری از رکورد اول، یا ساختار کامل همراه با اطلاعات جانبی
        """
        table_name=table
        #select_data 
        ''' 
            020905 add order to func
            030625 re_creat by C_SQL
            ------------------------
        INPUTS:
           where:C_SQL.where 
           
        result='list/dict/dict_x'
            dict_x=result all data
        '''
        
        #-------------------------------------------------------------------------------------
        rows_num=self.count(table_name=table_name,where=where)['count']
        sql_where=C_SQL().where(where)
        sql_x=sql or "SELECT * FROM {}".format(table_name)
        sql_x+=sql_where     
        sql_x=C_SQL().add_limit(sql_x,offset,page_n,page_len,limit,order,last)
            
        x_re=self._exec(sql_x,fetch=True)
        rows=x_re['data'] if x_re['done'] else []
        titles = self._titles()
        
        result_1={'sql':sql_x,'sql_where':sql_where,
        'rows':rows,'titles': titles,'rows_num':rows_num
        ,'exec_report':x_re,
        'items':{},'ids':[],'id':-1,'n':0,'done':True}
        #---------------------------
        if not rows: 
            result_1['done']=False
        else:
            result_1['items']= {t:rows[0][i] for i,t in enumerate(titles)}
            result_1['ids']=[x[0] for x in rows] 
            result_1['id']=result_1['ids'][0]
            result_1['n']=len(result_1['ids'])    

        if debug:
            xxxprint (msg=['data','tb:'+table_name,''],vals=locals(),args=self._titles())
            print(f"K-sql.select:\n\t : sql={sql_x}\n\t : path={self.path}\n\t : result_nim={len(rows)}")
        
        # rows_1,titles_1,row_num_1,sql_1=self.select_a(table,sql,where,result='list',offset=offset,page_n=page_n,page_len=page_len,limit=limit,last=last,order=order,debug=False)
        # msg= 'secect = select_a' if rows_1==rows else  '!!! secect != select_a'  
        # xxxprint(out_case=3,msg=[msg,'',''],inspect_n=2,session_report=True,vals={'sql_in':sql,'sql':sql_x,'test_sql':sql_1,'rows':rows,"test_rows":rows_1,"sql_where":sql_where,"where":where})
        
        if result=='list':
            return rows,titles,rows_num
        elif result=='dict_x':
            return result_1
        else: #dict
            if rows:
                return {t:rows[0][i] for i,t in enumerate(titles)}
            return {}
        return False,False,False

    #----------------------------------------------------------------------------------------------------
    def row_backup(self,table_n,xid):
        '''
        020905
        goal:copy 1 row (that row(id)=<xid>) from <table_n> to <table_n>_backup
        '''
        rows,titles,base_row_id=self.select(table_n,where={'id':xid})
        if debug:xxxprint(msg=["data",'tb:'+'(row[0],titles)',''] ,args=[rows[0],titles])
        titles[titles.index('id')]='xid'
        r1=self.insert_data(table_n+"_backup",titles,rows[0])
        r1.update({"base_row_id":base_row_id})
        if debug:xxxprint(msg=["result",'',''] ,vals=r1)
        r1['base_row_id']=base_row_id
        return r1
    #----------------------------------------------------------------
    def insert_data(self, table_name, name_list_or_nv_dict, val_list=None, sql_do=True, debug=False):
        """
        درج داده در جدول:
          - اگر داده مشابه وجود داشته باشد: درج نمی‌شود و همان رکورد موجود بازگردانده می‌شود.
          - اگر ردیف خالی (مقادیر '-') وجود داشته باشد: با داده جدید بروزرسانی می‌شود.
          - در غیر این صورت: رکورد جدید درج می‌شود.

        Args:
            table_name (str): نام جدول
            name_list_or_nv_dict (list[str] | dict): لیست ستون‌ها یا دیکشنری {ستون: مقدار}
            val_list (list, optional): لیست مقادیر (اگر ورودی دیکشنری باشد نیاز نیست)
            sql_do (bool, optional): اجرای واقعی SQL یا فقط ساخت دستور
            debug (bool, optional): فعال‌سازی چاپ Debug

        Returns:
            dict: نتیجه عملیات شامل id، وضعیت و پیام
        """

        # --- آماده‌سازی ورودی ---
        if isinstance(name_list_or_nv_dict, dict):
            name_list = list(name_list_or_nv_dict.keys())
            val_list = list(name_list_or_nv_dict.values())
        else:
            name_list = name_list_or_nv_dict
            val_list = val_list if val_list is not None else []

        # --- بررسی وجود داده مشابه ---
        find = self.select(table=table_name, where=[name_list, val_list], result='dict_x')
        if find.get('done'):
            find.update({
                'done': False,
                'result': 'عدم وارد کردن اطلاعات به دلیل پیدا کردن اطلاعات مشابه'
            })
            return find

        # --- بررسی وجود ردیف خالی (مقدار '-') ---
        where_dic = {col: '-' for col in name_list}
        set_dic = {col: val_list[i] for i, col in enumerate(name_list)}
        find2 = self.select(table=table_name, where=where_dic, result='dict_x')

        if find2.get('done'):
            rep = self.update_data(table_name, set_dic, {'id': find2['id']})
            rep.update({
                'done': True,
                'result': '''ردیف خالی با اطلاعات جدید بروزرسانی شد
                    insert_data: empty row updated ->'''
            })
            if debug:
                xxxprint (msg=['inset',rep['result'],''],vals=rep)
            return rep

        # --- درج رکورد جدید ---
        placeholders = ",".join(["?"] * len(val_list))
        sql_t = f'INSERT INTO {table_name} ({",".join(name_list)}) VALUES ({placeholders})'

        if sql_do:
            rep = self._exec(sql_t, val_list)
            xid = self.cur.lastrowid
        else:
            rep = {}
            xid = -1

        rep.update({
            'id': xid,
            'ids': xid,
            'sql': sql_t + "|" + str(val_list),
            'done': True,
            'result': '''رکورد جدید اضافه شد
                insert_data: insert new row ->'''
        })

        if debug:
            xxxprint (msg=["result",rep['result'],''] ,vals=rep)
        return rep
    #-----------------------------------------------------
    def update_data(self, table_name, set_dic, x_where, sql_do=True, debug=False):
        """
        بروزرسانی داده‌ها در جدول.

        Args:
            table_name (str): نام جدول
            set_dic (dict): مقادیر جدید برای آپدیت، مانند {"col1": "val1"}
            x_where (dict | str): شرط WHERE (به صورت دیکشنری یا رشته SQL)
                dict= {'name21':'val21','name22':'val22'..}
                str='name21 Like val21'
            sql_do (bool, optional): اگر False باشد فقط SQL ساخته می‌شود و اجرا نمی‌شود.
            debug (bool, optional): فعال کردن پیام‌های دیباگ

        Returns:
            dict: نتیجه شامل SQL ساخته‌شده، رکوردهای تغییر یافته، تفاوت‌ها و پیام.
        """
        if debug:
            xxxprint(msg=["update_data","start",''] )

        # ساخت شرط WHERE
        sql_where = C_SQL().where(x_where)
        xr = {'where': sql_where}

        # بررسی وجود رکورد مطابق شرط
        find1 = self.select(table=table_name, where=x_where, result='dict_x', limit=0)
        sql_preview = f"SELECT * FROM {table_name} {sql_where}"

        if not find1.get('done'):
            xr.update({
                'done': 0,#False
                'msg': 'هیچ ردیفی پیدا نشد، آپدیت قابل انجام نیست'
            })
            report_db_change(self.path, sql_preview, [])
            return xr

        if debug:
          xxxprint(msg=["update_data",'found records',''],vals=find1 )
        
        # انجام تغییرات و به روز رسانی
        
        # ساخت بخش SET
        s_set = self._dic_2_set(set_dic)
        xr['sql'] = f'UPDATE {table_name} SET {s_set} {sql_where}'

        if sql_do:
            xr['exe'] = self._exec(xr['sql'])
            xr['rowcount'] = self.cur.rowcount

            log_msg = f"updated <{xr['rowcount']}> rows --- sql={xr['sql']}"
            if debug:
                xxxprint(msg=["update_data","executed",'rowcount(updated)='+xr['rowcount']] ,vals=xr)

            if xr['rowcount'] == 0:# any record not found
                xr.update({
                    'done':'1', #  False,
                    'msg': 'رکورد پیدا شد ولی تغییر اعمال نشد (rowcount=0)'
                })
                report_db_change(self.path, log_msg, [])
                return xr

            # بررسی تغییرات بعد از آپدیت
            find2 = self.select(table=table_name, where=x_where, result='dict_x', limit=0)
            xr['dif'] = [] #different s
            xr['dif_x'] = {}

            if find2 and find2.get('rows'):
                tt = find2['titles']
                # مقایسه اطلاعات قبل و بعد از تغییر به صورت ردیف به ردیف
                for i, f1 in enumerate(find1['rows']):
                    f2 = find2['rows'][i]
                    dif_list = [j for j, x in enumerate(f1) if x != f2[j]]
                    dif = [f"row({f1[0]}),col({tt[j]}):{f1[j]}=>{f2[j]}" for j in dif_list]

                    report_db_change(self.path, log_msg, dif)
                    if debug:
                        rrp={f'dif- {i}':x for i,x in enumerate(dif)}
                        rrp.update({'update_n':len(dif)})
                        xxxprint(msg=["result",f"update_data: row {f1[0]} changes",''] ,vals=rrp)

                    xr['dif'].extend(dif)
                    xr['dif_x'][f1[0]] = [tt[j] for j in dif_list]

                xr['id'] = str(find2['ids'])
                xr['update_n'] = len(xr['dif'])
            else:
                xr.update({
                    'done': False,
                    'msg': 'بعد از آپدیت رکورد یافت نشد یا قابل بازیابی نبود'
                })
                if debug:
                    xr1=self.show_change(table_name, find1, r1)
                    xxxprint(msg=["update_data","end",""] ,vals={'xr':xr,'xr1':xr1})
                return xr

            xr.update({
                'done': True,
                'msg': ','.join(xr['dif']) if xr['dif'] else 'تغییر خاصی ثبت نشد'
            })
        else:
            xr.update({
                'done': True,
                'msg': 'SQL فقط ساخته شد (بدون اجرا)'
            })

        if debug:
            xxxprint(msg=["update_data","end",""] ,vals=xr)

        return xr
    ##-------------------------------------------------------------------------------
    def show_change(self,table_name, find1, r1):
        """
            🔎 مقایسه رکوردهای قبل و بعد از آپدیت در دیتابیس
            
            پارامترها:
                table_name (str): نام جدول
                find1 (dict): داده‌های قدیمی شامل:
                    - rows: لیست رکوردهای قبل از آپدیت
                    - ids: لیست شناسه رکوردها
                r1 (Any): شناسه/اطلاعات اضافی برای ثبت گزارش
             
            خروجی:
                xr (dict): شامل کلیدهای:
                    - 'dif': تغییرات هر رکورد
                    - 'id' : لیست شناسه‌ها
            مراحل:
              1. `find1['rows']` شامل داده‌های قبل از آپدیت است.
                 - ستون اول رکورد = شناسه (`id`)
                 - بقیه ستون‌ها = مقادیر قدیمی

              2. بررسی می‌شود آیا همین شناسه (`id`) در داده‌های جدید (rows2) وجود دارد یا خیر.
                 - اگر وجود نداشت، پیام خطا ثبت می‌شود (`xxprint`) و رکورد رد می‌شود.

              3. در صورت وجود، مقادیر قدیمی (`old_values`) با مقادیر جدید (`new_values`) مقایسه می‌شوند.
                 - ستون‌هایی که تغییر کرده‌اند در `dif_list` ذخیره می‌شوند.
                 - برای هر تغییر گزارشی به صورت
                   "row(id),col(column_name): old_value => new_value"
                   ساخته می‌شود.

              4. تغییرات هر رکورد به تابع `report_db_change` ارسال می‌شود
                 تا در فایل یا لاگ ثبت گردد.

              5. خروجی نهایی در دیکشنری `xr['dif']` ذخیره می‌شود:
                 - کلید = شناسه رکورد (id)
                 - مقدار = لیست تغییرات آن رکورد
        """
         # مقداردهی اولیه خروجی
        xr = {'dif': {}, 'id': ''}
        
        # داده‌های جدید از دیتابیس
        rows2, titles2, row_num2 = self.select(table_name, limit=0)
        
        # نگاشت id → row برای دسترسی سریع
        new_data = {r[0]: r[1:] for r in rows2}

        for i, row in enumerate(find1['rows']):
            

            id_1 = row[0]          # شناسه رکورد
            old_values = row[1:]   # مقادیر قدیمی بدون id

            if id_1 not in new_data:
                xxprint('err_x', f'id {id_1} not found in new data')
                continue

            new_values = new_data[id_1]  # مقادیر جدید بدون id

            # مقایسه ستون‌ها
            dif_list = [j for j, val in enumerate(old_values) if val != new_values[j]]
            dif = [
                f"row({id_1}),col({titles2[j]}): {old_values[j]} => {new_values[j]}"
                for j in dif_list
            ]

            # ثبت تغییرات در گزارش
            if dif:
                report_db_change(self.path, r1, dif, idx=i+1)

            # ذخیره تغییرات در خروجی
            xr.setdefault('dif', {})
            xr['dif'][id_1] = dif

        # ثبت شناسه رکوردهای تغییر یافته
        xr['id'] = str(find1['ids'])
        return xr
    
    
    
   
    
    ##-----------------------------------------------------------------------------------------
    def grupList_of_colomn(self,table_name,colomn_name,where_field='',where_value='',have_sum=True,traslate_dict={}):
        '''
            update : 1400/12/16 - old_name=get_grupNameList_of_Xcolomn_in_Xtable
            input:
            -------
                have_sum:bolean True /False
                    True => func return count value of each grup 
            outpiut:
            --------
               {'title1':'value'} or {'title1':'value : (sum)'}
            (گروه بندی کردن اطلاعات موجود در ستون مفروض  از جدول  مفروض   و مشخص کردن نام گروههای مختلف ( نام مقادیر تکرار شده در ستون مورد نظر 
        '''
        xwhere=f" WHERE {where_field} ='{where_value}'" if where_field.strip() and where_value.strip() else ''
        sum_field=", COUNT(*) AS cnt" if have_sum else "" #", COUNT(*) AS cnt "
        sql= "SELECT " + colomn_name + sum_field + " FROM [" + table_name + "] " + xwhere +  " GROUP BY " + colomn_name 
        rows,titles,row_n=self.select('',sql,limit=0)

        #o1={'title':'value'}
        o1={" ":{'value':"ALL:(*)",'num':0,'title':"ALL"}}
        tt=""
        c_cnt=titles.index("cnt") #cet column number
        c_x=titles.index(colomn_name)
        #print(str(titles))
        #print(str(rows))
        #print(c_cnt,c_x,colomn_name)
        num='0'
        for row in rows:
            if have_sum : 
                num=row[c_cnt]
                tt=" : ({})".format(num) 
            c_t='{}'.format(row[c_x])
            title=traslate_dict[c_t] if traslate_dict and (row[c_x] in traslate_dict) else c_t
            value=title+tt
            o1[c_t]={'value':value,'num':int(num),'title':title}
        return o1
    def chek_uniq(self,tb_name,field_name,uniq_where='',uniq_value=''):
        '''
            بررسی اینکه مقدار داده شده در فیلد مشخص شده یکتا می باشد و خیر و ارائه یک لیست از موارد مشابه در آن فیلد
        '''
        if debug:xxxprint (msg=['param=','uniq_where:'+uniq_where,''],vals=locals())
        uniq_where=(uniq_where.replace("`",'"') if uniq_where else '') + (f' AND {field_name} like "%{uniq_value}%"' if uniq_value else '')
        rows,titles,rows_num=self.select(tb_name,where=uniq_where )
        like_list=[row[titles.index(field_name)] for row in rows]
        is_uniq=uniq_value not in like_list
        #return uniq_where,uniq_where#
        return is_uniq,like_list
    def x_update(self,tb_name,where_dic,set_dic,report=''):
        if report:
            import tk_ui as ui
        out_rep=[]
        r_insert=self.insert_data(tb_name,where_dic)
        if r_insert['done']:
            if 'i' in report:#i=insert
                msg=["ارسال اطلاعات به بانک اطلاعاتی","-"*50,str(where_dic)]
                msg+=["ثبت رکورد جدید","-"*50,str(r_insert)]
                ui.msg("\n".join(msg))
            out_rep+=[['insert',str(where_dic),'',str(r_insert)]]
        r_update=self.update_data('a',set_dic,where_dic)
    
        if r_insert['done']: #u=update
            if 'u' in report :
                msg=["اطلاعات به بانک اطلاعاتی ارسال شد","-"*50,"به روز رسانی رکوردها","-"*50,pp_inf['lno']]
                msg+=['id='+r_update['id'],'dif=',str(r_update['dif']),'update_n=',r_update['update_n']]
                ui.msg("\n".join(msg))
            out_rep+=[['update',str(where_dic),str(set_dic),str(r_update)]]
        return out_rep  
    def cols_2_list(self,tb_name,text_format,col_name_list):
        '''
            1-read many columns of 1 sql table 
            2-combine data of each row by text_format
            3-convert rows result to 1 list 
        '''
        rows,titles,rows_num=self.select(tb_name,limit=0)
        x_o=[]
        for row in rows:
            xx=[row[titles.index(col_name)] for col_name in col_name_list]
            x_o+=[text_format.format(*xx)]
        return x_o
    def cols_2_dict(self,tb_name,key_text_format,val_text_format,col_name_list):
        '''
            1-read many columns of 1 sql table 
            2-combine data of each row by text_format
            3-convert rows result to 1 list 
        '''
        rows,titles,rows_num=self.select(tb_name,limit=0)
        x_o={}
        for row in rows:
            xx=[row[titles.index(col_name)] for col_name in col_name_list]
            x_o[key_text_format.format(*xx)]=val_text_format.format(*xx)
        return x_o    
#======================================================================================================================
    def export(tb_name,cols,data):
        rep['table']=self.define_table(tb_name,fields_txt='id INTEGER PRIMARY KEY AUTOINCREMENT,', fields_order={"TEXT":cols}) 
        rep['rows']=[]
        for row in rows:
            rep['rows']+=self.insert_data(tb_name,cols,row)
 
