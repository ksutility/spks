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
def user_in_jobs(jobs,row_data={},un=''):
    '''
        according form_inf(row_data) retun that un is in jobs ?  
        مشخص می کند که آیا کاربر مشخص شده در شغلهای مشخص شده می باشد یا خیر 
        از اطلاعات _ ردیف برای اطلاعات تکمیلی برای کاربر های خاص بر اساس مرحله و یا فیلد استفاده می کند
    inputs:
    -------
        un:str
            username
        jobs=list of job_code separate by ,
        row_data:dict
            data of recored form for user(#task#<task_name>,#step#<n> )
    '''
    if not un:
        from gluon import current
        session=current.session
        un=session["username"]
    #xxxprint(msg=['user_in_jobs',jobs,un],vals=row_data)
    for job in jobs.split(','):
        if job =='*':return True
        if job[0] != "#":
            if (un in a_jobs[job]['users'].split(',')) or (un == a_jobs[job]['base_user']):
                return True
        if job[0] == "#" and  len(job) > 6:
            jx=job.split('#')
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
def step_changer(step_index,form_sabt_data):
    '''
        مشخص کردن فردی که می تواند یک مرحله پر شده از یک فرم را تغییر دهد
    '''
    return form_sabt_data[f'step_{step_index}_un']
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
    x_step_changer=step_changer(step_index,form_sabt_data)
    if x_step_changer: 
        return x_step_changer==un # if user is editor of x_step
        
    return user_in_jobs(step['jobs'],row_data=form_sabt_data)
    #return form_sabt_data[f'step_{step_index}_un']    
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
    x_step_changer=step_changer(step_index,form_sabt_data)
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
def jobs_title(jobs,x_data_s):
    '''
    عنوان هر سمت
    بر اساس سمتهای تعریف شده در یک مرحله از فرم
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
                tt+=[' ' + x_data_s['tasks'][jx[2]]['title']]
                #xxxprint(vals=x_data_s['tasks'],launch=True)
                continue
            elif jx[1]=="step":
                #xxxprint(msg=['',str(jx),''],launch=True)
                tt+=['تکمیل کننده بخش شماره '+str(int(jx[2])+1) + ' فرم جاری ']
                
                continue
    return tt
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
