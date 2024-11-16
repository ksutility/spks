# -*- coding: utf-8 -*-
"""
020805-add 3 columns func(add,ren,del)
    -   add exec func
001119-update select (can get where_dict)-v1.07
#ver 1.10 1402/09/05-
"""
from k_ui import var_report
import datetime
#from gluon import cache,current
#cache=cache.Cache(current.request)
import jdatetime #khayyam
from k_err import xxxprint,xxprint,xprint
debug=0 #False # True#
today=jdatetime.date.today().strftime('%y-%m-%d') #khayyam.JalaliDate.today().strftime('%y-%m-%d')
def f_now():
    x=str(datetime.datetime.now())#trftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    return today + "-" + x
def report_txt(x_txt_list):
    x_list=x_txt_list.split(',')
    return ", ".join([x+'='+str(eval(x)) for x in x_list])
def report_db_change(db_name,t1,dif_list,idx=1):#030815
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
            return q_name+q_where
        elif type(q_where)==list:
            if len(q_where)==2 and type(q_where[0])==list and type(q_where[1]) in [list,tuple]:
                return q_name + " AND ".join([self.where_cell(w_n,q_where[1][i]) for i,w_n in enumerate(q_where[0])])
            elif q_where[0]=="AND": #__where__list__":
                return q_name + " AND ".join([self.where(q_w,add_where_text=False) for q_w in q_where[1:] if q_w])
            elif q_where[0]=="OR": #__where__list__":
                return q_name + " OR ".join([self.where(q_w,add_where_text=False) for q_w in q_where[1:] if q_w])    
        elif type(q_where)==dict:
            return q_name + " AND ".join([self.where_cell(name,q_where[name]) for name in q_where]) 
        else:
            xxxprint(msg=["error","where type not correct",''],launch=True)
    #-------------------------------------------
    def add_limit(self,sql,offset,page_n,page_len,limit,order,last):
        if not limit:return sql
        x_order = f'ORDER BY ' + order
        x_order += ' DESC' if last else ''
        if offset:        
            return sql+f' {x_order} limit {offset},{limit}' if limit else sql
        else:   #if page_n:
            from k_tools import int_force
            x_page=int_force(page_n,1) 
            x_page_len=int_force(page_len,20) 
            x_offset=(x_page-1) * x_page_len 
            return sql+f' {x_order} limit {x_offset},{x_page_len}' if limit else sql
#===================================================================================
class DB1():
    import sqlite3
    # path=d:\\temp\\example1.db
    con,cur,path,dbn="","","",""
    tables_name={}
    columns={}
    def __init__(self,path='example2.db'):
        self.con = self.sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.path=path
        self.get_tables_name()#prn=True)
        self.dbn=self.path.partition("//")[2]
    ##---@cache(time_expire=5, cache_model=cache.ram)
    #@cache.action(time_expire=300, cache_model=cache.ram, session=True, vars=True, public=True)
    def _exec(self,sql,val_list=[],fetch=False):
        
        result={'def':'_exec','sql':sql,'data':[]}
        #if debug:
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
            result.update({'done':False,'Error':str(err)})  
            xxxprint(msg=['err',sql, self.path],err=err,vals=result)
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
        xprint(sql)
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
            xxxprint(msg=['err','count',table_name],vals=result)
        return result    
    #--------------------------------------------
    def sql_set(self,_top,_fields_name,_table_name, _where , _order):
        xtop=f" TOP {_top} " if _top else ""
        xwhere=C_SQL().where(_where)
        xorder=" ORDER BY {_order}" if _order else ""
        return f"SELECT {xtop} {_fields_name} FROM {_table_name} {xwhere} {xorder}"    
    #---------------------- main func ----------------------------------------------------------------------------------------------    
    def select(self,table='',sql='',where='',result='list',offset=0,page_n=1,page_len=20,limit=20,last=True,order='id',debug=False):
        table_name=table
        #select_data 
        ''' 
            020905 add order to func
            030625 re_creat by C_SQL
            ------------------------
        INPUTS:
           where:C_SQL.where 
           
        result='list/dict'
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
    def insert_data(self,table_name,name_list_or_nv_dict,val_list=[]):
        if type(name_list_or_nv_dict)==dict:
            val_list=list(name_list_or_nv_dict.values())
            name_list=list(name_list_or_nv_dict.keys())
        else:
            name_list=name_list_or_nv_dict
            #val_list=val_list
        ''' if data isnot exist => add data         , return add_row_number, insert_result = true
            if data is  exist   => don't add data   , return find_row_number,insert_result = false'''
        find=self.select(table=table_name,where=[name_list,val_list],result='dict_x')
        
        if find['done']:
            find.update({'done':False,'result':'عدم وارد کردن اطلاعات به دلیل پیدا کردن اطلاعات مشابه'})
            return find
        #find empty
        where_dic={x:'-' for x in name_list}
        set_dic={n:val_list[i] for i,n in enumerate(name_list)}
        find2=self.select(table=table_name,where=where_dic,result='dict_x')

        if find2['done']:
            rep=self.update_data(table_name,set_dic,{'id':find2['id']})
            rep['done']=True
            xxxprint (msg=['inset','find empty row = ok',''],vals=rep)
            return rep
        #----------
        x_v="?,"*(len(val_list))
        sql_t='INSERT INTO {} ({}) VALUES ({})'.format(table_name,",".join(name_list),x_v[:-1])#NSERT OR IGNORE INTO
        #ui.msg(sql_t+"/n"+str(val_list))
        rep=self._exec(sql_t, val_list)
        xid=self.cur.lastrowid
        rep.update({'id':xid,'sql':sql_t+"|"+str(val_list),'done':True})
        if debug:xxxprint (msg=["result",'',''] ,vals=rep)
        return rep

    def update_data(self,table_name,set_dic,x_where):
        ''' set_dic={'name11':'val11','name12':'val12'..}
            x_where: dict /str
                dict= {'name21':'val21','name22':'val22'..}
                str='name21 Like val21'
                
        '''
        #try:
        xr={}
        if debug:xxxprint(msg=["start",'',''])
        sql_where=C_SQL().where(x_where)
        
        # بررسی وجود حداقل 1 رکورد با شرایط تعیین شده 
        find1=self.select(table=table_name,where=x_where,result='dict_x')
        if not find1['done']: # any record not found
            xr['msg']=' هیچ ردیفی پیدا نشد'
            xr['msg']+=' لذا آپدیت انجام نشد '
            report_db_change(self.path,r1, [])
            return xr
        if debug:xxxprint(msg=["find1",'',''],vals=find1 )
        
        # انجام تغییرات و به روز رسانی
        s_set=self._dic_2_set(set_dic)
        
        xr['sql']='UPDATE {} SET {}' .format(table_name,s_set)+ sql_where
        xr['where']=sql_where
        xr['exe']=self._exec(xr['sql'])
        xr['rowcount']=self.cur.rowcount
        r1=('updated <{}> rows --- sql={}'.format(xr['rowcount'],xr['sql']))
        if debug:xxxprint(msg=["data",'rowcount = updated',''] ,vals=xr)
        if xr['rowcount']==0:# any record not found
            xr['msg']=' رکورد پیدا شد ولی تغییر توسط برنامه نتوانست اعمال شود'
            report_db_change(self.path,r1, [])
            return xr
        # بررسی تغییرات  
        find2=self.select(table=table_name,where=x_where,result='dict_x')
        
        if debug:xxxprint(msg=["find2",'',''],vals=find2 )
        xr['dif']={} #different s
        if not find2:   
            rows2,titles2,row_num2=self.select(table_name,limit=0)
            id_list=[x[0] for x in rows2]
            for i,row in enumerate(find1['rows']):
                row=row[1:]
                if not row[0] in id_list:
                    xxprint('err_x',f'{row[0]} not in {str(id_list)}')
                row_x= id_list.index(row[0])   
                row2=rows2[row_x]
                dif_list=[j for j,x in enumerate(row) if x!=row2[j]]
                dif=['row({}),col({}):{}=>{}'.format(row_x,titles2[j],row[j],row2[j]) for j in dif_list]
                report_db_change(self.path,r1, dif,idx=i+1)
                xr['dif'][row[0]]=dif
            xr['id']=str(find1['ids'])
        else: 
            xr['id']=str(find2['ids'])
            tt=find2['titles']
            # مقایسه اطلاعات قبل و بعد از تغییر به صورت ردیف به ردیف
            for i,f1 in enumerate(find1['rows']):
                f2=find2['rows'][i]
                dif_list=[j for j,x in enumerate(f1) if x!=f2[j]]
                dif=['row({}),col({}):{}=>{}'.format(f1[0],tt[j],f1[j],f2[j]) for j in dif_list]
                report_db_change(self.path,r1, dif)
                rrp={f'dif- {i}':x for i,x in enumerate(dif)}
                rrp.update({'updtaed':len(dif)})
                if debug:xxxprint(msg=["result",'',''] ,vals=rrp)
                #xxprint ('db-update','row {}:dif={}----\n####   {}'.format(f1[0],len(dif),'\n####   '.join(dif)))
                xr['dif'][f1[0]]=[tt[j] for j in dif_list] 
                xr['report']=rrp
        if debug:xxxprint(msg=["end",'',''] )
        return xr
        #except: #Error as e:   print(e)
        #   return False
    
    
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
    def chek_uniq(self,tb_name,field_name,uniq_where,uniq_value):
        '''
            بررسی اینکه مقدار داده شده در فیلد مشخص شده یکتا می باشد و خیر و ارائه یک لیست از موارد مشابه در آن فیلد
        '''
        if debug:xxxprint (msg=['param=','uniq_where:'+uniq_where,''],vals=locals())
        if uniq_where: uniq_where=uniq_where.replace("`",'"')+ " AND " 
        rows,titles,rows_num=self.select(tb_name,where=uniq_where + f'{field_name} like "%{uniq_value}%"')
        like_list=[row[titles.index(field_name)] for row in rows]
        is_uniq=uniq_value not in like_list
        return is_uniq,like_list
    #======================================================================================================================
    """
    def make_where_role(self,name_list):
        return " AND ".join(['{}=?'.format(n) for n in name_list])
    def make_where(self,where_dic):
        return " AND ".join(["`{}`='{}'".format(n,where_dic[n]) for n in where_dic])
    def _where_set(self,q_val):
        q_name=" where "
        if type(q_val)==list:
            if type(q_val[0])==dict:
                return q_name+self._dic_2_set(q_val)
        elif type(q_val)==dict:
            return q_name+self.make_where(q_val)
        elif type(q_val)==str and q_val!='':
            return q_name+q_val
        return ''  
    def select_a(self,table='',sql='',where='',result='list',offset=0,page_n=1,page_len=20,limit=20,last=True,order='id',debug=False):
        table_name=table
        #select_data 
        ''' 010909
            020905 add order to func
            ------------------------
                  
        result='list/dict'
        '''
        def _sql_add_limit(sql,offset,page_n,page_len,limit):
            if not limit:return sql
            x_order = f'ORDER BY ' + order
            x_order += ' DESC' if last else ''
            if offset:        
                return sql+f' {x_order} limit {offset},{limit}' if limit else sql
            else:   #if page_n:
                x_page=int(page_n) if page_n else 1 
                x_page_len=int(page_len) if page_len else 20
                x_offset=(x_page-1) * x_page_len 
                return sql+f' {x_order} limit {x_offset},{x_page_len}' if limit else sql
        #-------------------------------------------------------------------------------------
        row_num=self.count(table_name=table_name,where=where)['count']
        if where:
            if type(where)==str:
                sql="SELECT * FROM {} WHERE {} ".format(table_name,where)
                sql_x=_sql_add_limit(sql,offset,page_n,page_len,limit)
                rows=self._exec(sql_x,fetch=True)['data']
                if debug:xxxprint(msg=[self.dbn,sql,"len="+str(len(rows))])
                titles = self._titles()        
            if type(where)==dict:
                find1=self.find_row(table_name,where)
                
                if find1:
                    rows=find1['rows']
                    titles=find1['titles']
                else:
                    rows=[[]]
                    titles=[]
                    xxxprint(msg=['err',f'sql={find1["sql"]}',''])
            else:
                find1=0/1
        else:
            #print('--'+str(type(where_dic))+'---'+str(where_dic))
            if sql=="":
                sql="SELECT * FROM {} ".format(table_name)
            sql_x=_sql_add_limit(sql,offset,page_n,page_len,limit)
     
            x_re=self._exec(sql_x,fetch=True)
            rows=x_re['data'] if x_re['done'] else []
            titles = self._titles()#[description[0] for description in self.cur.description]
        if debug:
            xxxprint (msg=['data','tb:'+table_name,''],vals=locals(),args=titles)
            print(f"K-sql.select:\n\t : sql={sql_x}\n\t : path={self.path}\n\t : result_nim={len(rows)}")
    
        
        
        if result=='list':
            return rows,titles,row_num,sql
        else: #dict
            if rows:
                return {t:rows[0][i] for i,t in enumerate(titles)}
        return False
    def find_row(self,table_name,name_list_or_nv_dict,val_list=[],):
        '''
            input:
                1=>find_row(table_name,name_list,val_list)
                2=>find_row(table_name,name_value_dict)
            return:
                rs_id:list
                    list of row id of find search
                rows:list of list
        '''
        #try:
        import k_err
        x=name_list_or_nv_dict
        if type(x)==list:
            name_list=x
            sql_where = self.make_where_role(name_list)
            x1=[name_list_or_nv_dict,val_list]
        elif type(x)==dict:
            name_list=x.keys()
            sql_where = self.make_where_role(name_list)
            val_list=x.values()
            x1=x
        elif type(x)==str:
            sql_where=x
            x1=x
        else:
            
            k_err.xxprint('err','type of name_list_or_nv_dict shoud be list/dict but is=>'+str(type(x)))
            k_err.quit()
            return False
        
        
        if True:
            sql_t2="SELECT * FROM {} WHERE ".format(table_name)#rowid,
            if debug : k_err.xxxprint(msg=['sql',sql_t2 + sql_where,''],args=val_list)
            self.cur.execute(sql_t2 + sql_where,tuple(val_list))
            rows=self.cur.fetchall()
            self.con.commit()
            titles = self._titles()
            result={'sql':sql_t2,'sql_where':sql_where,'val_list':val_list,
            'rows':rows,'titles':titles,
            'items':{},'ids':[],'id':-1,'n':0,'done':True}
            #---------------------------
            if not rows: 
                result['done']=False
            else:
                result['items']= {t:rows[0][i] for i,t in enumerate(titles)}
                result['ids']=[x[0] for x in rows] 
                result['id']=result['ids'][0]
                result['n']=len(result['ids'])
            #C_SQL.test_where(x1,result,self,table_name)   

            test=self.select(table_name,'',x1,result='dict_x')
            msg= 'find_row = ' if test['rows']==rows else  '!!! find_row != '  
            xxxprint(out_case=3,msg=[msg,'',''],inspect_n=2,session_report=True,vals={'sql':sql_t2,'test_sql':test['sql']})
            
            return  result
        """
"""
#============= not used =======================
def make_select_role(self,table_name,name_list):
        return "SELECT * FROM {} WHERE ".format(table_name) + self.make_where_role(name_list)


D:\ks\I\web2py-test\applications\spks\controllers\data.py (12 hits)
    Line  418:         rows,titles,rows_num=db1.select(table_name,limit=0)
    Line  511:         rows,titles,rows_num=db1.select(tb_name,where={'id':xid})
    Line  584:             rows,titles,rows_num=db1.select(tb_name,where={'id':xid})
    Line  681:             rows,titles,rows_num=db1.select(table=tb_name,where=filter_data,page_n=request.vars['data_page_n'],page_len=request.vars['data_page_len'],order=x_data_s['order'])
    Line  721:         rows1,ttls1,rows_num=db1.select(tb_name)#'paper')
    Line  754:     rows1,titles1,rows_num=db1.select(tb_name,limit=0)
    Line  761:     rows2,titles2,rows_num=db2.select(ref['tb'],limit=0)
    Line 1094:         rows,titles,rows_num=db1.select(table=tb_name,where={},limit=0)
    Line 1126:         rows,titles,rows_num=db1.select(table=tb_name,where={},page_n=1,page_len=20)#limit=20)
    Line 1213:         rows,titles,rows_num=db1.select(table=dt['tb1'],where={},limit=0)  #limit=20) 
    Line 1315:     rows1,titles1,row_num1=db1.select('a',limit=0)
    Line 1316:     rows2,titles2,row_num2=db2.select('a',limit=0)
    
user.py (3 hits)
    Line  55:     rs=db1.select('user',sql,result='dict')#share.setting_dbFile1,sql)
    Line 107:         rs=db1.select(table_name='user',sql=sql,result='dict')
    Line 333:             rs=db1.select('user',sql)
  
    controllers/user.py#54._user_chek_ps_get_Inf()

k_sql.py (4 hits)
    Line 448:         rows,titles,base_row_id=self.select(table_n,where={'id':xid})
    Line 529:             rows2,titles2,row_num2=self.select(table_name,limit=0)
    Line 577:         rows,titles,row_n=self.select('',sql,limit=0)
    Line 603:         rows,titles,rows_num=self.select(tb_name,where=uniq_where + f'{field_name} like "%{uniq_value}%"')
    
    k_sql.py#457.row_backup()
    k_sql.py#457.row_backup()   
    k_sql.py#612.chek_uniq(
    
k_user.py (2 hits)-ok
    Line  33:     rows,titles,rows_num=db1.select('user',where={},limit=0)
    Line  65:     rows,titles,rows_num=db1.select('a',where={},limit=0)

    16:10:17--k_user.py#33.load_user_inf() > - : secect = select_a,
    16:10:17--k_user.py#65.load_job_inf() > - : secect = select_a,    
    
form.py (5 hits)-ok
    Line 324:             rows,titles,rows_num=db1.select(tb_name,where={'id':xid})
    Line 525:     rows,titles,rows_num=db1.select(tb_name,where={'id':xid})
    Line 576:     rows,titles,rows_num=db1.select(tb_name,where={'id':xid})
    Line 801:         rows,titles,rows_num=db1.select(table=tb_name,where=filter_data,page_n=request.vars['data_page_n'],page_len=request.vars['data_page_len'],order=x_data_s['order'])
    Line 852:     rows,titles,rows_num=db1.select(tb_name,where={'xid':str(xid)})

    controllers/form.py#324.inf_g() 
    controllers/form.py#525.save()  
    controllers/form.py#576.save_app_review()   
    controllers/form.py#801.xtable()
    controllers/form.py#852._sabege()      
    
k_form.py (4 hits)
    Line  593:             rows2,tit2,row_n=db2.select(ref['tb'],limit=0)
    Line  751:     rows,tits,row_n=DB1(dbn).select(table=ref['tb'],where=ref['where'],limit=0,debug=debug)
    Line 1240:         rows,titles,rows_num=db1.select(self.tb_name,where={'id':self.xid})
    
    k_form.py#751.reference_select()
    k_form.py#694.reference_select()
    k_form.py#751.reference_select()
    k_form.py#1240._set_form_sabt_data()
    
    k_form.py#1297._set_form_sabt_data()
        
+
k_user.py#33.load_user_inf()    

k_user.py#65.load_job_inf() 

controllers/user.py#55._user_chek_ps_get_Inf()  

    


k_user.py#33.load_user_inf()    

k_user.py#65.load_job_inf() 

controllers/user.py#55._user_chek_ps_get_Inf()  
    
k_user.py#33.load_user_inf()    
+
    2
k_user.py#65.load_job_inf() 
+
    1
controllers/user.py#55._user_chek_ps_get_Inf()  
+
    1
controllers/form.py#801.xtable()    
+
    4
    
+
    42
controllers/form.py#324.inf_g() 
+
    2
controllers/form.py#852._sabege()   
+
    1
controllers/form.py#576.save_app_review()   
+
    1
        
+
    1
k_sql.py#457.row_backup()   
+
    1
    
+
    








 ----------------------------------------------------------------------------------------------------------------
 """
    
        #except:
        #    return none #not found
"""
"""