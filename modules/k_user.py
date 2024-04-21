from gluon.custom_import import track_changes; track_changes(True)
from k_sql import DB1
import k_htm
import k_form
from k_err import xxprint,xprint,xalert,xxxprint
from x_data import x_data ,x_data_verify_task
import k_date
now = k_date.ir_date('yy/mm/dd-hh:gg:ss')
db_path='applications\\spks\\databases\\'
def load_user_inf():
    db1=DB1(db_path+'user.db')
    rows,titles,rows_num=db1.select('user',where={},limit=0)
    users={}
    for row in rows:
        u_inf=dict(zip(titles,row))
        users[u_inf['un']]={'fullname':'{m_w} {pre_n} {name} {family}'.format(**u_inf)}
        #users[u_inf['un']]=u_inf
    return users
a_users=load_user_inf()
def load_job_inf():
    db1=DB1(db_path+'job.db')
    rows,titles,rows_num=db1.select('a',where={},limit=0)
    jobs={}
    for row in rows:
        j_inf=dict(zip(titles,row))
        jobs[j_inf['code']]={x:j_inf[x] for x in ['title','users']} 
    return jobs
a_jobs=load_job_inf()
def user_in_jobs(un,jobs,row_data):
    '''
        inputs:
        -------
            jobs=list of job_code separate by ,
    '''
    for job in jobs.split(','):
        if job =='*':return True
        if job[0] != "#":
            if un in a_jobs[job]['users'].split(','):
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
    return False
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
                tt+=['تکمیل کننده فیلد '+x_data_s['tasks'][jx[2]]['title']]
                #xxxprint(vals=x_data_s['tasks'],launch=True)
                continue
            elif jx[1]=="step":
                #xxxprint(msg=['',str(jx),''],launch=True)
                tt+=['تکمیل کننده بخش شماره '+str(int(jx[2])+1)]
                
                continue
    return tt
def jobs_masul(jobs,x_data_s):
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
    res=(session["admin"] or user_in_jobs(session["username"],auth_jobs,{}))
    print (f'session["admin"]={session["admin"]},auth_jobs={auth_jobs},res={res}')
    return res