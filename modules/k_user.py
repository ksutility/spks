from gluon.custom_import import track_changes; track_changes(True)
from gluon import URL
from gluon import current
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
xjob = 1 extra text for define users by:
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
    db1=DB1('user')
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
            "my_folder":f'{u_inf["eng"].strip()}-{unx}',
            "p_id":u_inf["p_id"],
            "loc":u_inf["loc"],
            'pass_is_safe':pass_is_safe(u_inf["ps"])
            }
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
#a_users=load_user_inf()
#all_users=ALL_USERS()

def jobs_load_inf():
    db1=DB1('job')
    rows,titles,rows_num=db1.select('a',where={},limit=0)
    jobs={}
    for row in rows:
        j_inf=dict(zip(titles,row))
        jobs[j_inf['code']]={x:j_inf[x] for x in ['title','base_user']} 
        jobs[j_inf['code']]['users']=j_inf['users'].split(',')
    return jobs
a_jobs=jobs_load_inf()

def user_in_xjobs_can(do,x_data_s={},c_form='',step_index='0',un='',xjobs=''):###
    step_name=step_index
    form_sabt_data=c_form.form_sabt_data if c_form else {}
    '''
        according form_inf(form_sabt_data) retun that user(un) can act(do) in xjobs(xjobs or steps[step_name]['xjobs']) ?  
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
        xjobs=str list :optional_1
            list of job_code separate by ,
            '' : steps[step_name]['xjobs']
        step_index:str :optional_1
            selected step of 1 form
    optional_1:
        1 of xjobs , (x_data_s, step_index) is need
        if xjobs : ignor (x_data_s, step_index)
    '''
    if not un:
        from gluon import current
        session=current.session
        un=session["username"]
    if not un:
        return False
    if not xjobs:
        import k_user,k_tools
        xjobs=x_data_s['steps'][step_name]['xjobs'] #k_tools.nth_item_of_dict(x_data_s['steps'],step_name)['xjobs']

    #xxxprint(out_case=3,msg=['user_in_xjobs_can',xjobs,un],vals=form_sabt_data)
    step=x_data_s['steps'][step_name]
    for xjob in xjobs.split(','):
        if do=='view':
            if not 'auth' in step :
                return True  
            else:
                for xjob in step['auth'].split(','):
                    users_list=C_XJOB(xjob,x_data_s,c_form).users_list() 
                    if un in users_list:return True
        elif xjob =='*':
            if do == 'creat':
                return True
            elif do == 'edit':
                step_un=form_sabt_data.get(f'step_{step_name}_un','')
                if ((not step_un) or (un==step_un)):
                    import k_err
                    k_err.xxxprint(3,msg=[step_un,un])
                    return True
            return False   
        else:
            users_list=C_XJOB(xjob,x_data_s,c_form).users_list() 
            #xxxprint(3,msg=['users_list',users_list,''])
            if un in users_list:return True
        '''
        if xjob[0] != "#":
            if (un in a_jobs[xjob]['users']) or (un == a_jobs[xjob]['base_user']):
                return True #for do==creat / edit /view
        if xjob[0] == "#" and  len(xjob) > 6:
            jx=xjob.split('#')
            if jx[1]=="task":
                
                x_un=form_sabt_data.get(jx[2],'')
                #print('x_un=',x_un)
                if un==x_un:return True
            elif jx[1]=="step":
                
                x_un=form_sabt_data.get(f'step_{jx[2]}_un','')
                #print('x_un=',x_un)
                if un==x_un:return True
        '''
    #print("user_in_jobs=>false")
    return False

def _step_changer(step_index,form_sabt_data):###
    '''
        مشخص کردن فردی که می تواند یک مرحله پر شده از یک فرم را تغییر دهد
    '''
    return form_sabt_data.get(f'step_{step_index}_un','')

def jobs_masul(x_data_s,step_index,c_form,form_all_data ):
    '''
        used in x_nxt_u
        
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
    form_sabt_data=c_form.form_sabt_data
    #breakpoint()
    #import k_tools
    
    x_step_changer=_step_changer(step_index,form_sabt_data)
    if x_step_changer: return x_step_changer    
    if form_sabt_data['f_nxt_u'] in ['y','x']:  # y=form is fill ok ,x=form is remove / kill
        return form_sabt_data['f_nxt_u']    

    x_step=x_data_s['steps'][step_index]

    if 1>0: #try:
        return C_XJOB(x_step['xjobs'],x_data_s,c_form).users_list()[0]
        '''
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
        '''
    #except:
    #    return ''
class C_XJOB():
    def __init__(self,xjob_code,x_data_s,c_form=''):
        self.code=xjob_code
        self.x_data_s=x_data_s
        self.c_form=c_form
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
        فرد مسئول در آیتم شماره 0 لیست بر گردانده می شود
        '''
        code=self.code
        if code =='*':
            return ['','*']
        elif code[0] != "#":
            x_users=[]
            for x_code in code.split(","):
                x_users+=[a_jobs[x_code]['base_user']]+a_jobs[x_code]['users']
            return x_users
        elif code[0] == "#" and  len(code) > 6:
            jx=code.split('#')
            if jx[1]=="task":
                x_un=self.c_form.all_data.get(jx[2],'') if self.c_form else '?'
                return [x_un]
            elif jx[1]=="step":
                x_un=self.c_form.all_data.get(f'step_{jx[2]}_un','') if self.c_form else '?'
                return [x_un]
 
def xjobs_inf(jobs,x_data_s,c_form=''):
    '''
    توصیح افراد عضو یک سمت
    بر اساس سمتهای تعریف شده در یک مرحله از فرم
    '''
    t_d,t_i=[],[]
    t_users=set()
    for job in jobs.split(','):
        c_xjob=C_XJOB(job,x_data_s,c_form)
        t_d+=[c_xjob.describe()]
        t_users.update(c_xjob.users_list())
    xjobs={
    'describe':",".join(t_d),
    'inf':",".join(list(t_users))
    }     
    return xjobs

#--------------------------------------------------------------- not used


def how_is_connect(subject,shoud_login=True):
    import k_date,os,k_tools
    from gluon import current
    from gluon.http import redirect
    if shoud_login:
        if not current.session['username']:redirect(URL('spks','user','login',args=['go']))
    u_ip=str(current.request.client)
    if k_tools.access_from_internet():#u_ip[:11]!='192.168.88.':
        if (not user_can_access_from_internet()) or (not subject in 'form'):
            redirect(URL('spks','user','msg_access_form_internet')) 
    xdate=k_date.ir_date('yymmdd')
    xtime=k_date.ir_date('hh:gg:ss')
    file_n=os.path.join("c:\\","temp",'user_log',f'{xdate}-{subject}-user_log.txt')
    u_log=USER_LOG(ip=u_ip,un=current.session["username"],xtime=xtime)
    log=f'{xtime} , {u_ip} , {current.session["username"]} , {current.request.url}'
    with open(file_n,"a",encoding='utf8') as f:
        f.writelines('\n'+log)
    return file_n + " | " +log , u_log.report()
#how_is_connect()

import functools
#decorator
# not work 
def user_can_access_from_internet():
    if current.session['username'] in ['ks','aha','ase','my','rms','akr','fms','hal','hdr','mmn'] : return True
    if current.session['pass_is_safe'] : return True
    return False
    #pass_is_safe
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

def user_in_xjobs(xjobs,x_data_s,un='',c_form=''):
    '''
        old name = user_in_jobs
        row_data={} : old = > c_form.all_data
        according form_inf(row_data) retun that un is in xjobs ?  
        مشخص می کند که آیا کاربر مشخص شده در شغلهای مشخص شده می باشد یا خیر 
        از اطلاعات _ ردیف برای اطلاعات تکمیلی برای کاربر های خاص بر اساس مرحله و یا فیلد استفاده می کند
    inputs:
    -------
        un:str
            username
        xjobs=list of xjob_code separate by ,
        row_data:dict
            data of recored form for user(#task#<task_name>,#step#<n> )
    '''
    from gluon import current
    session=current.session
    
    if session["admin"]:return True
    
    if not un: un=session["username"]
    
    if not un:  return False
    #xxxprint(msg=['user_in_jobs',xjobs,un],vals=row_data)
    for xjob in xjobs.split(','):
        users_list=C_XJOB(xjob,x_data_s,c_form).users_list()   
        #xxxprint(3,msg=[xjob,users_list,('t' if c_form else 'f')])
        if '*' in users_list or un in users_list:return True
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
        if current.session["admin"] or user_in_xjobs_can('view',x_data_s=self.x_data_s,xjobs=self.x_data_s['base']['auth']):return {'auth':True}
        return {'auth':False,'msg':"شما اجازه دسترسی به این فرم را ندارید"}
    def auth_where(self):
        '''
            تهیه بخش جستجو در اس کی ال برای فیلتر کردن فرمهایی از فرم که فرد اجازه دیدن آنها را دارد
            این بخش بیشتر بر اساس دسترسی بر اساس پروژه تنظیم می شود
        '''
        from gluon import current
        if 'auth_prj' in self.x_data_s['base']: # در صورت تعریف متغیر دسترسی بر حسب پروژه در قسمت مبنای دیکشنری اطلاعات فرم
            if not current.session['auth_prj']=="*": # در صورتی که فرد ادمین نباشد
                auth_prj_n=self.x_data_s['base']['auth_prj'] #auth_prj_name
                if auth_prj_n[0]=="#":
                    return auth_prj_n[1:]
                else:
                    auth_prj_v=current.session['auth_prj']
                    return {auth_prj_n:auth_prj_v.split(",") if auth_prj_v else ['  ']}
        return ''
#-------- unused---------------------------------------------------------
def can_user_edit_step(step,step_index,x_data_s,form_sabt_data,un=''):
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
        
    return user_in_jobs(step['xjobs'],x_data_s,c_form=c_form)
    #return form_sabt_data[f'step_{step_index}_un']    

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
def auth(auth_jobs,x_data_s,c_form):
    '''
        آیا کاربر جاری حق دسترسی به این بخش را دارد 
    inputs:
    ------
        auth_jobs:str   jobs str_list separate by ,
            jobs that can access (read) data of cur section of program
    '''
    from gluon import current
    session=current.session
    res=(session["admin"] or user_in_xjobs(auth_jobs,x_data_s,c_form=c_form))
    #print (f'un={session["username"]},session["admin"]={session["admin"]},auth_jobs={auth_jobs},res={res}')
    return res
def creat_scr_pass():
    at='!@#$%^&*'
    bt='abcdefghijklmnopqrstuvwxyz'
    ct='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    dt='0123456789'
    def sel(tt):
        import random
        mylist = list(tt)
        return random.choice(mylist)
    s1= sel(at)
    #s2=    
    return sel(at)+sel(ct)+"_"+sel(bt)+sel(bt)+sel(bt)+"-"+sel(dt)+sel(dt)+sel(dt)+sel(dt)+"-"+sel(bt)+sel(bt)+sel(bt)
def pass_is_safe(x_pass):
    if not x_pass: return False
    if len(x_pass)<8: return False
    
    def eshterak(txt1,txt2):
        res=''
        for t in txt1:
            if t in txt2:
                res+=t
        return res
    #--------------------------
    x_txts=[
        '!@#$%^&*',
        'abcdefghijklmnopqrstuvwxyz',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        '0123456789']
    for txt2 in x_txts:
        if len(eshterak(x_pass,txt2))==0: return False
    return True       
def pre_timesheet(x_un,x_mon):
    """
    x_mon=mmdd
    """
    import k_time
    rows,titles,rows_num=DB1('person_act').select('a',where=["AND","`date1` LIKE '{}%' ".format(x_mon,),"`frd_1` LIKE '{}%'".format(x_un[:3])],limit=0)#,result='dict_x')
    #print(str(xxx))
    res={}
    
    rows,titles,rows_num
    for row in rows:
        time=row[titles.index('time')]
        date=row[titles.index('date1')]
        if not date in res:
            res[date]=[]
        res[date]+=[time]
    res2={}
    for date,times in res.items():
        res2[date]=k_time.sum_times(times)#  ','.join(times)
    '''
    '''
    return res2
  