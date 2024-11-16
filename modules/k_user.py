from gluon.custom_import import track_changes; track_changes(True)
from gluon import URL
from k_sql import DB1
import k_htm
import k_form
from k_err import xxprint,xprint,xalert,xxxprint
from x_data import x_data ,x_data_verify_task
import k_date
now = k_date.ir_date('yy/mm/dd-hh:gg:ss')
db_path='applications\\spks\\databases\\'
shoud_login_msg=f""" <h3>برای دسترسی به این بخش </h3>
                    <h3>ابتدا باید وارد سیستم شوید</h3>
                    <a href={URL("data","index")}>ورود</a>
                """
"""
job help
--------
job = 1 obj define by 1 form and have:
    'title','users','base_user'
xuser = 1 extra text for define users by:
    job.code :
    1 field of form :
    1 step of form :
    
"""                
class USER_LOG():
    inf={}
    def __init__(self,ip='',un='',xtime=''):
        if ip:
            if not un:un=''
            if not ip in self.inf:
                self.inf[ip]={'un':[un],'start':[xtime],'log_count':0,'last':xtime}
            else:
                if un and (not self.inf[ip]['un'] or un not in self.inf[ip]['un']):
                    self.inf[ip]['un']+= [un]
                    self.inf[ip]['start']+= [xtime]
            self.inf[ip]['log_count']+=1     
            self.inf[ip]['last']=xtime   
    def report(self):
        return (self.inf)

def load_user_inf():
    db1=DB1(db_path+'user.db')
    rows,titles,rows_num=db1.select('user',where={},limit=0)
    users={}
    for row in rows:
        u_inf=dict(zip(titles,row))
        #fullname='{m_w} {pre_n} {name} {family}'.format(**u_inf)
        fullname='{m_w} {name} {family}'.format(**u_inf)
        unx=u_inf['un']#
        #unx=unx.lower()
        users[u_inf['un']]={
            "user_fullname":fullname,
            "fullname":fullname,
            "username":unx,
            "un":unx,
            'login_ip':u_inf['login_ip'],
            'ps':u_inf["ps"],
            'file_access':u_inf["file_access"],
            "my_folder":f'{u_inf["eng"].strip()}-{unx}'}
        #users[u_inf['un']]=u_inf-
    #import k_err 
    #k_err.xreport_var(['users',users]) #,[titles],rows
    return users #           'fullname' report--
class ALL_USERS():
    inf={}
    def __init__(self):
        self.inf=load_user_inf()
    def reset(self):  
        self.inf=load_user_inf()
a_users=load_user_inf()
all_users=ALL_USERS()

def load_job_inf():
    db1=DB1(db_path+'job.db')
    rows,titles,rows_num=db1.select('a',where={},limit=0)
    jobs={}
    for row in rows:
        j_inf=dict(zip(titles,row))
        jobs[j_inf['code']]={x:j_inf[x] for x in ['title','users','base_user']} 
    return jobs
a_jobs=load_job_inf()
def user_in_jobs_can(do,x_data_s={},form_sabt_data={},step_index=0,un='',jobs=''):
    '''
        according form_inf(form_sabt_data) retun that user(un) can act(do) in jobs(jobs or steps[step_index]['jobs']) ?  
        مشخص می کند که آیا کاربر مشخص شده می تواند اقدام مشخص شده را بر اساس شغل مجاز تعریف شده یا 
        مرحله مشخص شده ( و شغل مجاز آن) انجام دهد یا خیر 

    inputs:
    -------
        do:str/select 
            craet: users can craet
            edit: users can edit
            view: users can view
        x_data_s:dict :optional_1
            selected(db,tb) x_data = x_data[db][tb]
        form_sabt_data:dict
            data of recored form for user(#task#<task_name>,#step#<n> )    
        un:str
            username
        jobs=str list :optional_1
            list of job_code separate by ,
            '' : steps[step_index]['jobs']
        step_index:int :optional_1
            selected step of 1 form
    optional_1:
        1 of jobs , (x_data_s, step_index) is need
        if jobs : ignor (x_data_s, step_index)
    '''
    if not un:
        from gluon import current
        session=current.session
        un=session["username"]
    if not un:
        return False
    if not jobs:
        import k_user,k_tools
        jobs=k_tools.nth_item_of_dict(x_data_s['steps'],step_index)['jobs']

    #xxxprint(out_case=3,msg=['user_in_jobs_can',jobs,un],vals=form_sabt_data)
    for job in jobs.split(','):
        if job =='*':
            if do=='creat':
                return True
            if do=='edit':
                step_un=form_sabt_data.get(f'step_{step_index}_un','')
                if ((not step_un) or (un==step_un)):return True
            if do=='view':
                return True
            return False   
        if job[0] != "#":
            if (un in a_jobs[job]['users'].split(',')) or (un == a_jobs[job]['base_user']):
                return True #for do==creat / edit /view
        if job[0] == "#" and  len(job) > 6:
            jx=job.split('#')
            if jx[1]=="task":
                
                x_un=form_sabt_data.get(jx[2],'')
                #print('x_un=',x_un)
                if un==x_un:return True
            elif jx[1]=="step":
                
                x_un=form_sabt_data.get(f'step_{jx[2]}_un','')
                #print('x_un=',x_un)
                if un==x_un:return True
    #print("user_in_jobs=>false")
    return False

def _step_changer(step_index,form_sabt_data):
    '''
        مشخص کردن فردی که می تواند یک مرحله پر شده از یک فرم را تغییر دهد
    '''
    return form_sabt_data.get(f'step_{step_index}_un','')

def jobs_masul(x_data_s,step_index,form_sabt_data,form_all_data ):
    '''
        according form_inf(form_sabt_data) return masul of jobs  
        مسئول یک شغل را مشخص می کند - کسی که باید جواب یک مرحله یک فرم را بدهد
        از اطلاعات _ ردیف برای اطلاعات تکمیلی برای کاربر های خاص بر اساس مرحله و یا فیلد استفاده می کند
    inputs:
    -------

        x_data_s:dict
            dic data of selected form
        step_index:int
            
            
        form_sabt_data:dict
            data of recored form for user(#task#<task_name>,#step#<n> )
    outputs:
    -------
        un:str
            username
    '''
    #breakpoint()
    import k_tools
    if step_index>=len(x_data_s['steps']):
        return 'y' # y=form is fill ok 
    #if x_data_s['steps']['jobs']=='*':   
    x_step_changer=_step_changer(step_index,form_sabt_data)
    if x_step_changer: return x_step_changer    
    if form_sabt_data['f_nxt_u'] in ['y','x']:  # y=form is fill ok ,x=form is remove / kill
        return form_sabt_data['f_nxt_u']
    x_step=k_tools.nth_item_of_dict(x_data_s['steps'],step_index,up_result='y')
    
    job=x_step['jobs']
    #import k_err
    #k_err.xreport_var(['!!',x_step,job])
    if 1>0: #try:
        if job[0] != "#":
            if job[0]=='*':return ''
            return a_jobs[job]['base_user']
        if job[0] == "#" and  len(job) > 6:
            jx=job.split('#')
            if jx[1]=="task":
                x_un=form_all_data[jx[2]]
                return x_un
            elif jx[1]=="step":          
                x_un=form_sabt_data[f'step_{jx[2]}_un']
                return x_un
    #except:
    #    return ''
class C_XUSER():
    def __init__(self,xuser_code,x_data_s):
        self.code=xuser_code
        self.x_data_s=x_data_s
    def describe(self):
        '''
        توصیح افراد عضو یک سمت
        بر اساس سمتهای تعریف شده در یک مرحله از فرم
        '''
        code=self.code
        if code =='*':
            return 'همه همکاران'
        elif code[0] != "#":
            return a_jobs[code]['title']
        elif code[0] == "#" and  len(code) > 6:
            jx=code.split('#')
            if jx[1]=="task":
                return ' ' + self.x_data_s['tasks'][jx[2]]['title']
                #xxxprint(vals=x_data_s['tasks'],launch=True)
            elif jx[1]=="step":
                #xxxprint(msg=['',str(jx),''],launch=True)
                return 'تکمیل کننده بخش شماره '+str(int(jx[2])+1) + ' فرم جاری '
    
    def users_list(self):
        '''
        افراد عضو یک سمت
        بر اساس سمتهای تعریف شده در یک مرحله از فرم
        '''
        code=self.code
        if code =='*':
            return '*'
        elif code[0] != "#":
            return a_jobs[code]['users']
        elif code[0] == "#" and  len(code) > 6:
            jx=code.split('#')
            if jx[1]=="task":
                return '?'
            elif jx[1]=="step":
                return '?'
 
def xusers_inf(jobs,x_data_s):
    '''
    توصیح افراد عضو یک سمت
    بر اساس سمتهای تعریف شده در یک مرحله از فرم
    '''
    t_d,t_i=[],[]
    for job in jobs.split(','):
        c_xuser=C_XUSER(job,x_data_s)
        t_d+=[c_xuser.describe()]
        t_i+=[c_xuser.users_list()]
    xusers={
    'describe':"".join(t_d),
    'inf':"".join(t_i)}
    
    '''
        if job =='*':
            tt+=['همه همکاران']
            continue
        elif job[0] != "#":
            tt+=[a_jobs[job]['title']]
            continue
        elif job[0] == "#" and  len(job) > 6:
            jx=job.split('#')
            if jx[1]=="task":
                tt+=[' ' + x_data_s['tasks'][jx[2]]['title']]
                #xxxprint(vals=x_data_s['tasks'],launch=True)
                continue
            elif jx[1]=="step":
                #xxxprint(msg=['',str(jx),''],launch=True)
                tt+=['تکمیل کننده بخش شماره '+str(int(jx[2])+1) + ' فرم جاری ']
                
                continue
        '''        
    return xusers
def auth(auth_jobs):
    '''
        آیا کاربر جاری حق دسترسی به این بخش را دارد 
    inputs:
    ------
        auth_jobs:str   jobs str_list separate by ,
            jobs that can access (read) data of cur section of program
    '''
    from gluon import current
    session=current.session
    res=(session["admin"] or user_in_jobs(auth_jobs))
    #print (f'un={session["username"]},session["admin"]={session["admin"]},auth_jobs={auth_jobs},res={res}')
    return res
#--------------------------------------------------------------- not used

def jobs_masul_old(jobs,x_data_s):
    '''
        مسئول اصلی انجام یک سمت
    '''
    tt=[]
    for job in jobs.split(','):
        if job =='*':
            tt+=['همه همکاران']
            continue
        elif job[0] != "#":
            tt+=[a_jobs[job]['title']]
            continue
        elif job[0] == "#" and  len(job) > 6:
            jx=job.split('#')
            if jx[1]=="task":
                tt+=[x_data_s['tasks'][jx[2]]['title']+'تکمیل کننده فیلد']
                continue
            elif jx[1]=="step":
                tt+=['تکمیل کننده بخش شماره '+str(int(jx[2])+1)]
                continue
    return tt
def how_is_connect(subject):
    import k_date,os
    from gluon import current
    
    xdate=k_date.ir_date('yymmdd')
    xtime=k_date.ir_date('hh:gg:ss')
    file_n=os.path.join("c:\\","temp",'user_log',f'{xdate}-{subject}-user_log.txt')
    u_log=USER_LOG(ip=current.request.client,un=current.session["username"],xtime=xtime)
    log=f'{xtime} , {current.request.client} , {current.session["username"]} , {current.request.url}'
    with open(file_n,"a",encoding='utf8') as f:
        f.writelines('\n'+log)
    return file_n + " | " +log , u_log.report()
#how_is_connect()

import functools
#decorator
# not work 
def user_is_login(func):
    from gluon import current
    if not current.session["username"]:
        return shoud_login_msg
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator
#-------- unused---------------------------------------------------------
def can_user_edit_step(step,step_index,form_sabt_data,un=''):
    '''
       آیا کاربر مشخص شده می تواند مرحله مشخص شده را تغییر دهد
       اگر کاربری مشخص نشود کاربر جاری در نظر گرفته می شود
    '''
    if not un:
        from gluon import current
        session=current.session
        un=session["username"]
    """
        first chek that target_step if filled older   
        ابتدا بررسی می کنیم که آیا بخش مورد نظر از فرم قبلا پر شده است یا خیر
        قبلا پر شده یعنی فرم برگشت خورده است
    """
    x_step_changer=_step_changer(step_index,form_sabt_data)
    if x_step_changer: 
        return x_step_changer==un # if user is editor of x_step
        
    return user_in_jobs(step['jobs'],row_data=form_sabt_data)
    #return form_sabt_data[f'step_{step_index}_un']    
def user_in_jobs(xusers,row_data={},un=''):
    '''
        according form_inf(row_data) retun that un is in xusers ?  
        مشخص می کند که آیا کاربر مشخص شده در شغلهای مشخص شده می باشد یا خیر 
        از اطلاعات _ ردیف برای اطلاعات تکمیلی برای کاربر های خاص بر اساس مرحله و یا فیلد استفاده می کند
    inputs:
    -------
        un:str
            username
        xusers=list of xuser_code separate by ,
        row_data:dict
            data of recored form for user(#task#<task_name>,#step#<n> )
    '''
    if not un:
        from gluon import current
        session=current.session
        un=session["username"]
    if not un:
        return False
    #xxxprint(msg=['user_in_jobs',xusers,un],vals=row_data)
    for xuser in xusers.split(','):
        if xuser =='*':return True
        if xuser[0] != "#":
            if (un in a_jobs[xuser]['users'].split(',')) or (un == a_jobs[xuser]['base_user']):
                return True
        if xuser[0] == "#" and  len(xuser) > 6:
            jx=xuser.split('#')
            if jx[1]=="task":
                
                x_un=row_data[jx[2]]
                #print('x_un=',x_un)
                if un==x_un:return True
            elif jx[1]=="step":
                
                x_un=row_data[f'step_{jx[2]}_un']
                #print('x_un=',x_un)
                if un==x_un:return True
    #print("user_in_jobs=>false")
    return False

class C_AUTH_FORM():
    '''
        بررسی حق دسترسی های مختلف 1 فرد به 1 فرم
    '''
    def __init__(self,x_data_s):
        self.x_data_s=x_data_s
        x=self.all()
        self.ok=x['auth']
        self.msg=x.get('msg','')
        self.where=self.auth_where()
    def all(self):  
        '''
            بررسی دسترسی کلی 1 فرد به 1 فرد
        '''
        from gluon import current
        if not 'auth' in self.x_data_s['base']:return {'auth':True}
        if current.session["admin"] or user_in_jobs_can('view',jobs=self.x_data_s['base']['auth']):return {'auth':True}
        return {'auth':False,'msg':"شما اجازه دسترسی به این فرم را ندارید"}
    def auth_where(self):
        '''
            تهیه بخش جستجو در اس کی ال برای فیلتر کردن فرمهایی از فرم که فرد اجازه دیدن آنها را دارد
            این بخش بیشتر بر اساس دسترسی بر اساس پروژه تنظیم می شود
        '''
        from gluon import current
        if 'auth_prj' in self.x_data_s['base']: # در صورت تعریف متغیر دسترسی بر حسب پروژه در قسمت مبنای دیکشنری اطلاعات فرم
            if not current.session['auth_prj']=="*": # در صورتی که فرد ادمین نباشد
                auth_prj_v=current.session['auth_prj']
                return {self.x_data_s['base']['auth_prj']:auth_prj_v.split(",") if auth_prj_v else ['  ']}
        return ''
