#from gluon.cache import Cache
#cache=Cache()
k_cache={}

from gluon import current
session=current.session
#from functools import lru_cache #,cache
#010929
# breakpoint()
""" 
    note:
        / = or
        
    form['steps'][name of step][step detail]:{'tasks':'','x_jobs','','title','','app_keys':'','app_titls':'','oncomplete_act':''}
        step_detail of N th form['steps']   :
        * 2 to 7 is same as same in:
                                1-  form['steps'][INF_X,N] Array in this program 
    #                           2-  N th Line ( after description line) of step_section(section2) of form_dateil file (step information describ of task "N") example : inf_1,inf_2,inf_3
    # INF_X = form['steps'][X,task_inf num]   = x th inf of task_inf      
#------------------------------------------------------
form                  
    [steps] step detail Information acording INF_X:
        [x]
    -------------- user data ------------------
            ['tasks']:(1)           Step_Task_numbers   
                list of int :list shomare task hay marbut be in step
                   in "N th Line of step_section of form_dateil File"  :n  (serial from last)                  n=total number of task 
                                                                       :n_start-n_end          
                                                                       :n1;n2;n3;...;ni
                   in "form['steps'][N]['tasks'] Array in this program "            :n1;n2;n3;...;ni        ni=number of field
            ['x_jobs']:(2)            Step_grup_define    :
                tarif gruh karbar mojaz (job_name / *task_number / #Step_number /$user name )
                    job_name    :
                        job_name of users . according to "job" table in "user.db" file
                    *task_name  :
                        users defined in task=tasks['task_name'] 
                            task['type']='user'     (that task shoud be user Type)    
                    #Step_name:
                        user compelete n_th Step   
                        note:number in (*task_number / #Step_number) shoud be for previuse completed parts
            ['name']:(3)            Step_name           :
                is use for 3 record name (UA ,UD,APP) -see part 11 to 13 
            ['title']:(4)    
                Step_title          :titel of Step in target_language ( in current it is farsi )
            ['app_keys']:(5)    
                Step_app_alter      :alternative aprove case for user (???) -- old=['act_keys']
                       x:no
                       Y:yes
                       R:review
                       note: free=YXR ( all case)
            ['app_titls']:(6)   
                Step_app_alter_titel:onvan jahat bakhshay mothtalef app_alter -- old =['act_titls']:
            ['oncomplete_act']:(7)  
                Step_oncomplete_act :karhaii ke pas a takmil bakhsh marbute bayad anjam shavad
                mail;name1;name2;mame3  name:(^job_titel / *task_number / #Step_number)
            ['read_users']:(8)  
                read users= users link1^users link2^...^users link_x
                               users link= job name / user name list
                               job name = text (job name in set.mdb) / link ( *n n=task_number / #n n=step_number) 
                               user name list = link ( *n n=task_number sample=*2 note that  this task shoud be a user field)
        ---------------- auto data    
            ['jobs_titles']:(9)        
                Step_mojaz_grup_titel       :onvan group mojaz
            ['jobs_users']:(10)        
                Step_mojaz_grup_user        :list karbarhay mojaz ( ba tavagoh be "INF_2:" va mavared digar)
            ['s_u_f']:
                user_filed                  :name filde zakhire name takmilgar(auto "s_u_f_"+n)
            ['s_d_f']:
                date_filed                  :name filde zakhire tarikhe takmil(auto "s_d_f_"+n)
            ['s_a_f']:
                app_filed             :name filde zakhire natige takmil(auto "s_a_f_"+n)
                *note1: form['steps'][1]['s_a_f']=Result of form
                * frome 931008 F_NEXU is form result
                *note2: for 11,12,13
                           if Step_name<>"" :  n="_" + Step_name  else e=the number of step
            ['s_u']:
                user_name               :name takmilgar
            ['s_d']:
                date_val            :tarikh takmil
            ['s_a']:
                app_val             :natige takmil
"""    
'''
form_xinf   =>keys=['f_step','f_revn','f_revs','f_nexu','reject_text'] =>
    from of:
    share.f_step,share.f_revn,share.f_revs,share.f_nexu,share.reject_text
'''
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from gluon.html import *
#from gluon.cache import CacheInRam
cache_ram={} #CacheInRam()
import share_value as share
from k_sql import DB1
from k_err import xxxprint,xprint,xalert,xreport_var
import time
import k_htm
from k_time import Cornometer
debug=False  
db_path='applications\\spks\\databases\\'
#cf=curent form
## ---------------------------------------------------------------------------------################################
def get_inf_file(form_name):
    ''' 
    not_used 020905
    
    read text file of form
    010929
        all var is global
        input:
            form_name
        output:
            form['base']:
                form_inf
            form['steps']:
                step_inf
            form['tasks']:
                task_inf
            form['pre_text']:
                pre_text
            
            share.task_total,share.step_total,
            share.form['db_n'],share.form['tb_n'],share.form_tb_backup,share.form['show_order'],share.form['scrt_inf']
            share.form['scrt_inf']=form security inf
        output:share.task_inf[)
    '''
    ##  ---------------------------
    def dbname_of_formname(formname):
        ''' 010929
            use=3(file):admin_set(1 hit),x_form(1 hit),x_sql(1 hit)
            input
            ------
                formname=cc-nn-rr   
                    exam:f-01-05    cc=form case    nn=form number  rr=form rev
            output
            ----- 
                filename of database_file for 1 form that name is "formname"
        '''
        a=formname.split("-")
        return share.base_path_data_read + share.dbc_form_prefix + a[0] + "-" + a[1] + ".db"
    ##  ---------------------------------------------------------------------------------################################
    
    share.form['name']=form_name
    file_name=share.base_path_data_read + share.dbc_form_prefix + form_name + ".txt"       #input 
    import json
    f = open(file_path)
    form = json.load(f)
    f.close()  
    # ---------------/read file  -----------------------------------------

    form_inf=form['base']
    #------------------------------------------------------------
    if form_inf['db_n']=="" :
        form_inf['db_n']= DBName_of_formName(form_inf['name']) 
    else:
        form_inf['db_n']=share.base_path_data_read + share.dbc_form_prefix + form_inf['db_n'] + ".db"
        #db_path+ref['db']+'.db'
    form_inf['tb_n']=form_inf['tb_n'] or form_inf['name'] 
    for t in ['caption','filter_inf','user_my_section','pre_set']:
        session["form_"+t]=form_inf[t]
    form_inf['tb_backup'] = form_inf['tb_n'] + "-bak"
    share.form=form_inf    
    #---------------------------------------read 2th sectin of file------------------------------------------------
    def task_n_list(tasks_spt,last_task_n):
        ''' 010929
        input
        ------
            tasks_spt:str   (tasks list spetial text)
            
            last_task_n:int
        output
        ------
            tasks:list
                list of tasks
            last_task_n:int
        '''
        if ";" in tasks_spt:
            tasks=[int(x) for x in tasks_spt.split(";")]
            last_task_n=int(tasks[-1]) 
        elif "-" in tasks_spt:
            n1,n2=[int(x) for x in tasks_spt.split("-")]
            tasks=[k for k in range(n1,n2)]
            last_task_n+=n2
        else:
            n=int(tasks_spt)
            tasks=[k for k in range(last_task_n+1,last_task_n+n)]
            last_task_n+=n
        return tasks,last_task_n
    #---  /func -----------------------------
    x_sum=0
    #step_inf=[''] #start form 1
    i=0
    for st_name,step in form['steps'].items():
        step['tasks'],x_sum=task_n_list(step['tasks'],x_sum)
        step['name']=st_name
        step['title']=step['title'] or step['name']
        step['n']=i        
        t= "_" + st_name
        step['s_u_f']:"s_u_f" + t   #    11-step_user_filed
        step['s_d_f']:"s_d_f" + t   #    12-step_date_filed
        step['s_a_f']:"s_a_f" + t   #    13-step_action_filed
        ss=stp+['','','']
        """
        step_i={
                'x_jobs':ss[1],   #   2
                'act_keys':ss[4],  #   5
                'act_titls':ss[5], #   6
                'oncomplete_act':ss[6],    #   7
                'read_users':ss[7],    #   8
        step_inf.append(step_i)
        """
    """
    #---------------------------------------read 3th sectin of file------------------------------------------------
    #  task_inf [number of task][task detail]
    #  inf_0:['val']=value - result value that task get from user , this will store in file after user fill own section 
    #task_inf=['']   #start form 1
    for tk_name,task in form['tasks'].items():
        ss=stp+['','','','']
        task_i={'type':ss[0],      #   inf 1:['type']
                'tbl_n':ss[1],     #   inf 2:['tbl_n']=output table name(optional)
                'field_n':ss[2],   #   inf 3:['field_n']=output field name  
                'inf':ss[3],       #   inf 4:['inf']=task_inf (see down) 
                'title':ss[4],      #   inf 5:['title']=task_caption 
                'i6':ss[5]}        #   inf 6:['i6']=adition inf 
                #  ['i6'] to ['i10'] adition inf
        #  baray "User" abb userha ra dar 7 va name kamele anhara dar 10 garar midahim       
        task_i['i7']=task_i['inf']    
        
        sc= task_i['type'].upper()
        if sc== "USER":
            #Out_users_list,Out_users_list=users_of_task (In_user_grup_name,In_user_grup_name)
            task_i['i7'],task_i['i10']=x_user.users_of_task(task_i['inf'],task_i['i6'],form)
            # users_list="":usersFullName_list=""
            # users_list,te=Users_of_SmartXjobgroup(share.task_inf[i]['inf'].split(share.ST_splite_chr2)[1],"cur_user")
                # if users_list="" : do_report('err',"user not found",share.task_inf[i]['inf'])
            # xx=share.task_inf[i]['i6'].split(share.ST_splite_chr2)[1]
            # user_fn_add=share.task_inf[i]['i6'][len(xx)+1:]
            # if isnull(users_list) : users_list=""
            # usersFullName_list = i_user.make_user_fullname(users_list,user_fn_add) 
            # check for + (+text1)
            # if user_fn_add[:1]="+" :
                # users_list="nouser" + share.ST_splite_chr2 + users_list
                # usersFullName_list="لازم نيست" + share.ST_splite_chr2 + usersFullName_list
                # user_fn_add=user_fn_add[1:]
            # task_i['i7']=users_list
            # task_i['i10']=usersFullName_list  
            
        elif sc== "GET":
            tt1=task_i['inf'].split(share.ST_splite_chr2)[1]
            tt2=task_i['inf'].split(share.ST_splite_chr2)[2]
            if tt2=="" :tt2=tt1
            task_i['i7']=Replace(tt1,share.ST_splite_chr4,share.ST_splite_chr2)
            task_i['i10']=Replace(tt2,share.ST_splite_chr4,share.ST_splite_chr2)
        elif sc== "XGET":
            task_i['i7'],task_i['i10']=xget_select_do(task_i['inf'])
        elif sc== "FILE":
            # no need
            pass
        elif sc== "INDEX":
            # no need   
            pass
        elif sc== "DATE":
            # no need   
            pass
        else:
            break_pro("اطلاعات فایل سازنده فرم درست نمی باشد" + chr(13) + "Section 3 (task inf) : line = " + i ,"s")
    task_inf.append(task_i)
    #------------------------------------------------read 4th sectin of file------------------------------------------------
    pre_text={'user':[['',''] for x in user_inf],
                'task':[['',''] for x in task_inf]}
    for i,stp in enumerate(dd['note'][1:]):
        note_i={'ut':stp[0].lower(),    #u/t:user or task
                'index':int(stp[1]),    #index of user or task
                'pos':stp[2],           #0/1 0=befor 1=fater
                'txt':stp[3]}           #text(note) for att to orginal text
        ut={'u':'user','t':'task'}[note_i['ut']]
        pre_text[ut][note_i['index']][note_i['pos']]+=note_i['txt']
    #------------------------------------------------read 5th sectin of file--------section task----------------------------------------
    #section_task=dd['section_task'] start from 1 (row 0 is for help)
    """
    return form #{'base':form_inf,'steps':step_inf,'tasks':task_inf,'pre_text':pre_text}
#---------------------------------------------------------------------------------################################
def set_data_by_form_code(): # t_form_name,t_form_code,t_form_rev,t_form_index)
    '''
        not_used 020905
    '''
    #use in flist and formshow
    #set nesesery data for form by input data in address '?formcode=...'

    er_m=""
     
    form_inf={'form_code':'','form_rev':'00','form_index':'','form_name':''} #defult values => 'name':'defult'
    ff={x:(request.vars[x].upper() or form_inf[x]) for x in form_inf}

    #f_new=request.vars["newform"]
    #----------------
    if ff['form_code']=="" : 
        if ff['form_name'] !="" :
            ff['form_code'],ff['form_rev']=formname_to_formcode(t_form_name)
    #----------------
    for x in form_inf: 
        if ff[x]=='':ff[x]=session[x]
    #----------------
    f_file=share.base_path_data_read + share.dbc_form_prefix + ff['form_code'] + "-" + ff['form_rev'] +".txt"
    if find_path(f_file):
        ff['form_name']=ff['form_code'] + "-"  + ff['form_rev']
        for x in form_inf: session[x]=ff[x]
        #if f_new : 'sakhtan form jadid
        #   response.redirect("formshow.asp?newform=ok")
        #else
        #   if fi=0 :
        #       response.redirect("flist.asp?form_name=" + session("form_name"))
        #   else
        #       response.redirect("formshow.asp")
    else:
        do_report('err', "form code=" + t_form_code + "<br>your form code is not correct<br>" + "کد فرم وارد شده اشتباه است")
#---------------------------------------------------------------

#---------------------------------------------------------------------------------################################  
def obj_set_form_history_parts(ix,xmode):
    '''
        not_used 020905
    '''
    t=""
    x_mode=xmode.lower()
    def_val=share.task_inf[ix]['val']
    x_c=share.task_inf[ix]['type'].lower()
    if x_c in ["text","num"]:
        tx=def_val
        if tx:
            t={"f":"بله","t":"y"}[x_mode]
        elif not tx:
            t={"f":"خير","t":"-"}[x_mode]
        else:
            t=tx
    elif x_c=="user":
        if x_mode=="f":
            d_un=dic_un_get()
            t= d_un.item(def_val)
        elif x_mode=="t":
            t=def_val
    elif x_c=="file" :
        t=""
        saved_file_fullname = share.task_inf[ix]['val']
        if saved_file_fullname and saved_file_fullname!="-" :
            pre_folder=share.task_inf[ix]['i7']
            filename=smart_text_2_text (fname)
            #   if pre_folder<>"" : pre_folder="\" + pre_folder
            #   path=folderpath_maker_by_filename(saved_file_fullname,path_full_patern)
            #   if path<>"" : path="\" + path
            #   path= share.ksf["path_upload"] + pre_folder + path
            
            #t="<a href=" + x_str.qq_add("download.asp?path=" + path + "&file=" + saved_file_fullname) + "target=" + x_str.qq_add("_blank") + ">" + saved_file_fullname + " </a>"
            #931208
            #t="<a href=" + x_str.qq_add("download.asp?file=" + saved_file_fullname + "&pfolder=" + pre_folder + "&patern=" + path_full_patern) + "target=" + x_str.qq_add("_blank") + ">" + saved_file_fullname + " </a>"
            
            t=out_jdownload_link (saved_file_fullname , pre_folder , path_full_patern)
            t="<div dir='ltr' >" + t + "</div>"
        else:   
            t="<div dir='ltr' > - </div>"   
    elif x_c=="do":
        pass
    elif x_c=="date":    
        t="<div dir='ltr' >" + def_val + "</div>"
    elif x_c=="private":pass 
    elif x_c=="check":   
        temp2="checked" if def_val=="1" else ""
        t="<input  class='largercheckbox' type='checkbox' value='true' " + temp2 +" disabled readonly>"
    elif x_c=="get":
        t= def_val  
    else: #"xget","auto","index","date" 
        t= def_val      
    return t + "\n" 
#----------------------------------------------------
#---------------------------------------------------------------------------------################################
def smart_text_2_text(base_val):
    #old= smart_text_lost_to_text(base_val,section=-1)
    #1400/10/13 ok use:5,5 2(file):),install_db(1 hit),formsave(4 hits)       ??do_act(3 hits)
    '''
        ##---------------------------------------------------------------------------------################################
    def smart_text_to_text(txt):
        #1400/10/13 ok use:2,2
        def text_select_by_pat(txt,slicer,pat_t1,pat_t2):
            #1400/10/12
            ###
            like fscommander   
            slicer:'split chrs' can be '' 
            if slicer= ""
                goal        =  descide          =pat_t1,pat_t2  test    #result: if txt='abcdefg'
                ----------------------------------------------------------------
                1 to n      =   x first         ="s",n          s,3     'abc'
                e-n to e    =   x last          ="e",n          e,3     'efg'
                n to end    =   all -x first    ="s",-n         s,-3    'defg'
                1 to e-n    =   all -x last     ="e",-n         e,-3    'abcd'
                x to x+n    =                   =x,n            2,2     'bc'
                e-x to e-x+n=                   =-x,n           -4,2    'de'
            if slicer!= "" all of above is for text choose
            ###
            tsl=txt.split(slicer) if slicer else txt #text_splited_list
            n=int(pat_t2)
            sc=pat_t1.lower()
            if sc=="s":
                r=(0,n) if n>0  else (n,len(tsl))
            elif sc=="e":
                r=(-n,len(tsl)) if n>0  else (0,-n) 
            else:
                x=int(pat_t1)
                r=(x-1,n) if x>0  else (-x ,-x+n)
            return tsl[r[0]:r[1]]
        #---------------------------------------------
        #--out use=0(file):
        # txt is 
        #       1:fix text ( that shoud not bo start by "*")
        #       2:*xn   (x=c/u/t/x  n=number)
        #       3:*xn*s*t1*t2 (*xn like up s=splite characters t1=s/e/num/-num t2=num/-num 
        #               s,t1,t2=> define text choos patern    
        #       sapmle = *t12*-*s*2  => 1_th + 2_th part of t12 (teext of 12_th field)
        txt=txt.lower()
        if txt[:1]=="*" :   
            if len(txt)>2:
                txt_pr,pat1,pat2,pat3=txt[2:]+'***'.split("*")
                sc=txt[:2]
                if sc=="*c": #curent 
                    break_pro( "c","")
                    txt_pr1=txt_pr[:1]
                    if txt_pr1=="n":    #curent form number 
                        re=str(session("form_index"))
                elif sc=="*u" :
                    s2=txt_pr[:1]
                    num=int(txt_pr[1:])
                    step_i=share.form['steps'][num]
                    re={"a":step_i[16],  #user app 
                        "d":step_i[15],  #date
                        "n":step_i[14], #user name abb
                        "c":session("username")}[s2]       #curent user abb 
                elif sc=="*t"  
                    num = int(txt_pr)
                    re=share.task_inf[num]['val']
                elif sc=="*x"        #select value for selected text (in xget or ...)
                    num = int(txt_pr)
                    x1_ar=share.task_inf[num]['i7']
                    x2_ar=share.task_inf[num]['i10']
                    
                    for i,x1 in  enumerate(x1_ar)
                        if x1.lower()==share.task_inf[num]['val'].lower() :
                            re=x2_ar[i]
                            break #exit for
                if pat2 : re=text_select_by_pat(re,pat1,pat2,pat3)  
        else:
            re=txt  
        return re
    ##----------------------------
    au_txt=""
    b_val=base_val.split(share.st_splite_chr2)[section] if section>-1 else base_val
    au_ar=b_val.split("^")
    for au_i in au_ar:
        au_txt+= smart_text_to_text(au_i)
    return au_txt   
    '''
    return template_parser(base_val)
#---------------------------------------------------------------------------------################################
def formname_to_formcode(form_name):
    #--out use=2(file):install_db(1 hit),y_base(1 hit)
	fname_ar=form_name.split("-")
	form_code='{}-{}'.format(fname_ar[0],fname_ar[1])
	form_rev=fname_ar[2]
	return form_code,form_rev        
#=================================================================================================================
#====================================================== used =====================================================    
#---------------------------------------------------------------------------------################################
def template_parser(x_template,x_dic={},rep=''):
    '''
    use in kswt:ok 020905
    rename:021126 - old name=format_parser
    func type : simple 
    goal:
    ------
        out_source template_parser =to=> web2py>gluon>template
        help:
            https://web2py.readthedocs.io/en/latest/template.html
    input:
    ------
        x_template:str
            input template str 
            python str by internal code in {{}} =like=> 'abc {{=x}} de{{=y[2]}}f'
        x_dic=dict
            {VAR1:VAL1,...} = var set dict  
                
    ------
    Usage examples:
    >>> template_parser("""abc-{{=a}}""",{'a':'abc'})
    abc-abc
    >>> template_parser("""abc-{{=a.upper()}}""",{'a':'abc'})
    abc-ABC
    >>> template_parser("""abc-{{=a[2].upper()}}""",{'a':'abc'})
    abc-C
    '''
    #return x_template.format(task=task_inf,step=form['steps'],session=session,**x_dic)
    import k_date
    if type(x_template)==str:
        xx=x_template.strip()
        from gluon import template
        x_dic1=x_dic.copy()
        from gluon import current
        session=current.session
        x_dic1.update({'session':session,'_i_':session['username'],'_d_':k_date.ir_date('yy/mm/dd')})
        #xxxprint(msg=['inf','template_parser',xx],vals=x_dic)
        
        try:
            """
                این فرایند خطا گیری برای کمک به رفع خطا در بخش های زیر می باشد
                1-auto filed:                    before source field is filled
                    فیلد های اتومات در مرحله قبل از پر شدن فیلد های مبنای اطلاعات آنها
            """
            x1= template.render(content=xx,context=x_dic1) 
            #xxxprint(msg=['inf',x1+"|"+str(rep),xx],vals=x_dic)
            return x1.format(**x_dic1)  #remove 020926
        except Exception as err:
            
            xxxprint(msg=['err',err,x_template],err=err,vals=x_dic,launch=True)
            return 'error in template_parser :'+str(err)
            ui.msg('error in template_parser')
    else:
        return x_template
#---------------------------------------------------------------------------------################################
def get_table_row(i,row,titles,fildes,select_cols,all_cols,ref_i):
    '''
    use in kswt:ok 020905
    '''
    import k_htm
    re1={}
    for fn in all_cols:#fn=field name
        try:
            v=row[titles.index(fn)]
        except:
            v=''
            #help:use this fun becuse 1 field like 'xlink' no have data in db
        f=fildes[fn]
        sc=f['type']
        if not v or v=='None':v=''
        if sc=='text':
            re1[fn]=htm_correct(v)
        elif sc=='reference':
            ref=f['ref']
            if fn not in ref_i:ref_i[fn]=reference_get_inf(ref)
            try:
                re1[fn]=ref_i[fn][v]
            except:
                re1[fn]='error'
        elif sc=='fdate':
            re1[fn]=v
        elif sc=='link':
            re1[fn]=v
        elif sc=='xlink':
            re1[fn]='<->'
    tds=['{:03d}'.format(row[0])]
    for fn in select_cols:#fn=field name
        f=fildes[fn]
        #- print(f['type'])
        if f['type'] in ['link','xlink']:
            p=[x.format(**re1) for x in f['link']['pro']]
            #- print(str(p))
            args=[x.format(**re1) for x in f['link']['args']]
            #tds.append(A(re1[fn],_href=URL('prj','file','f_list',args=('pp',re1[fn]))))#link
            tds.append(A(re1[fn],_href=URL(*p,args=tuple(args))))
        else:
            tds.append(re1[fn])
    return tds  
    ##--------------------------------------
    trs=[TR('id',xid)]
    for fn,f in fildes.items():
        if 'hide' in f['prop']:continue
        if 'readonly' in f['prop']: #readonly
            trs.append(TR(f['title'],f['value']))
            continue
        sc=f['type']
        if sc=='text':
            #ix=INPUT(_name=f['name'], _id=f['name'],_value=f['value'],_style='width:100%')
            ix=XML(f"<textarea name={fn} id={fn} rows='2' style='width:100%'>{f['value']}</textarea>")#cols="50"
            #if 'disabled' in f:ix=XML(f"<INPUT name={f['name']} id={f['name']} value={f['value']} style='width:100%' disabled>")
            trs.append(TR(f['title'],ix))
        elif sc=='reference':
            ref=f['ref']
            db2=DB1(ref['db'])
            rows2,tit2,row_n=db2.select(ref['tb'],limit=0)
            val_dic={str(r[tit2.index(ref['id'])]):ref['format'].format(*[r[tit2.index(x)] for x in ref['format_args']]) for r in rows2}
            trs.append(TR(f['title'],k_htm.select(_options=val_dic,_name=fn,_value=f['value'])))
        elif sc =='fdate':
            trs.append(TR(f['title'],INPUT(_class='fDATE',_name=fn,_id=fn,_value=f['value'])))
        elif sc =='link':
            trs.append(TR(f['title'],XML(f"<INPUT name={fn} id={fn} value={f['value']} style='width:100%'>")))#INPUT(_name=fn,_id=fn,_value=f['value']),_style='width:100%'))
        else:
            trs.append(TR(f['title'],f['value']))
    trs.append(TR(TD(A('Cancel- goto list',_href=URL(args=(args[0],args[1]))),_style='width:40%'),TD(INPUT(_type='submit',_style='width:100%,background-color:#ff00ff'),_style='width:60%')))
    return TABLE(*trs,_style='width:100%')
#-----------------------------------------------
#@k_tools.x_cornometer
def get_table_row_view(xid,row,titles,tasks,select_cols,x_data_s,id_cols=False,request={}):#,all_cols,ref_i):
    #use in:2(show_xtable,show_kxtable)
    #cm=Cornometer(i)
    '''
    INPUTS:
    ------
        xid:int
            id of 
            
    '''
    tds=[]
    if id_cols:
        tds+=['{:03d}'.format(xid)]
    x_dic=dict(zip(titles,row))
    c_form=C_FORM(x_data_s,xid)
    for field_name in select_cols:#fn=field name  
        tds.append(c_form.show_step_1_row(field_name,request,mode='output-mini')[1])
    return tds  
#----------------------------------------------------------------------------------------------------------------------------------------------------
#@lru_cache() #smaxsize=20) #Cache(maxsize=20)#.action(time_expire=60, cache_model=cache.ram, session=True, vars=True, public=True)
#@k_tools.x_cornometer
def reference_select (ref_0,form_nexu=False,form_data={},debug=False):
    #debug=False
    #ceck cach
    
    idx="-".join([ref_0[x] for x in ref_0])+"|"+str(form_data)
    #if debug: print(f"idx={idx}")
    if idx in k_cache:
        if k_cache[idx]['time']-time.time()<5:
            #print (f'k-cache = ok {time.time()}|'+idx)
            return k_cache[idx]['val']
    #print (f'k-cache = -- {time.time()}|'+idx)
    '''
    use in kswt:ok 020905
    
    old name=xget_select_do,reference_get_inf
    goal: make dedicated select list of refrence obj = dict of keys:titels that
        ساخت لیست نهایی شده بر اساس تعریف شی رفرنس 
        پر کردن بخش های مپلیت در داخل تعریف کلید و عنوان شی رفرنس با استفاده از فیلدهای جدول رفرنس در ردیف مورد نظر
        input:
        -------
            ref:#spks__x_form__task__ref
                {'db':'xx{}xx','tb':'xx{}xx','where':'xx{}xx','key':'xx{}xx','val':'xx{}xx'}
                'db'=database path format
                    format by field_name in current table
                'tb'=table name format
                    format by field_name in current table
                'where'=sql where (for find data) format
                    format by field_name in current table
                'key':=format for make keys in output dict 
                    format by field_name in tarjet table 
                'val'=format for make values/titles in output dict 
                    format by field_name in tarjet table 
        output:
        -------
            dict( {key:val} /{val:tit} ) of founded field   
            {'key_1':'val/tit_1','key_2':'val/tit_2',...}
    '''
    ref=ref_0.copy()
    #if debug :xxxprint(msg=['ref1',idx,''],vals=ref) 
    for x in ['db','tb','key','val']:
        if not x in ref:
            do_report('err',x + " is not in Ref /n ref shoud have ['db','tb','key','val']" +  ref)
    
    for x in ['db','tb','where']:
        ref[x]=template_parser(ref.get(x,''),x_dic=form_data) #.format(task=task_inf,step=form['steps'],session=session)
    if debug :xxxprint(msg=['ref2',idx,''],vals=form_data)    
    #dbn=share.base_path_data_read + share.dbc_form_prefix + ref['db']+".db"#db_path+ref['db']

    if form_nexu:
        ref['where']=((ref['where'] + " and ") if ref['where'] else "") + "f_nexu <> 'x' "
    rows,tits,row_n=DB1(ref['db']).select(table=ref['tb'],where=ref['where'],limit=0,debug=debug)
    if debug :
        print(f"where={ref['where']}")
        xxxprint(msg=['where',idx,ref['where']],args=rows)
    if rows :
        output_data={ref['key'].format(**dict(zip(tits,row))):ref['val'].format(**dict(zip(tits,row))) for row in rows}
        #if debug :xxxprint(msg=['output_data',idx,''],vals=output_data) 
        k_cache[idx]={'val':output_data,'time':time.time()}
        return output_data
    return {}#'msg':ref['where']}

#----------------------------------------------------------------------------------------------------------------------------------------------------
#@k_tools.x_cornometer
def obj_set(i_obj,x_dic,x_data_s='',xid=0, need=['input','output'],request='',c_form=''): 
    import k_htm
    form_update_set_param="form;form"
   
    #cm=Cornometer(f"obj-{i_obj['type']}-{i_obj['name']}")
    '''
    use in kswt:ok 020905
    old name= obj_set_form_active_parts
    goal:
        make inputer=html_input_obj (1 input in  form) for a task by task_inf in x_data
        in 2 case  accordind need var
                    input:for input data
                    output:for show data
                    
    input:
    ------
        i_obj:dict
            data_def of this task (x_data[db][tb]["tasks"][name])
        x_dic=dict
            dict(zip(names,row)) = this form save and edited data
                save data =xdic['field_name']
                edited data=xdic['__objs__']['field_name']
        xid=?
        
        need=['input','output'] / ['input'] / ['output']
        
        
    obj=field   fields={'name':..,...} , obj={,,,}
        تلفیق برنامه مرتبط با تولید شی
        need  مشخص کننده اینکه چه بخشهایی باید در خروجی باشند
        note:
            <if 'output' in need:obj['output']=value or obj['value'] or obj['def_value']}>
            omited(can be omit) in each case    
        input:
            form_update_set_param
        def:
            form_update_set
            htm_correct
            reference_select
            htm_select
            template_parser
    '''
    sc=i_obj['type']
    def obj_pars(i_obj,obj_type,force=False):
        if force or 'input' in need or obj_type in ['file']:
            #cm.tik('obj template_parser start')
            obj={x:template_parser(i_obj[x],x_dic,rep=f'{x}:{i_obj["name"]}') for x in i_obj}#['file_name','ext','path','pre_folder']}
            #xreport_var([i_obj,x_dic,obj,''],True)
            #cm.tik('obj template_parser end')
        else:
            obj=i_obj.copy()
        if debug:
            xxxprint(msg=['obj',obj['name'],''],vals=x_dic,vals2=obj)    
        return obj
    if x_data_s:db_name,tb_name=x_data_s['base']['db_name'],x_data_s['base']['tb_name']
    
    obj=obj_pars(i_obj,obj_type=sc)
    
    
    
    def form_update_set(form_update_set_param):
        xmode,xname=form_update_set_param.lower().split(";")
        if xmode== "form": #updae form
            #form_update_set_param="form;frm1"
            return  xname + ".submit();" #  "'frm1.submit();'"
        elif xmode=="file": #like to file
            #form_update_set_param="file;formshow.asp"
            #xget_link_ar=split(select_addition_inf,";")
            #        link_go=x_str.qq_add("formshow.asp?xresult=" + obj_name + ";" ) + " + document.getelementbyid(" + x_str.qq_add(obj_name) + ").value"
            link_go=f'"{xname}?xresult=' #("formshow.asp?xresult=")
             
            for i in share.form['steps'][session["f_step"]+1]['tasks']:
                if share.task_inf[i]['field_n'].lower()!="auto" :
                    #send => name ,sql
                    o_name=share.task_inf[i]['field_n']
                    link_go+=f' + "{o_name};" + document.getelementbyid("{o_name}").value + ";"'
            return "document.location.assign(" + link_go + ");" #link_go 
    ##---------------------------------------------------------------------------------################################
    
    _name=obj['name']
    onact_txt,x_class='',''
    _n=f"name='{_name}' id='{_name}'" 
    _len=int(obj['len']) if 'len' in obj else 256
    _value=(request.post_vars[_name] or request.vars[_name]) if request else ''
    _value=_value or (str(x_dic[obj['name']]) if (obj['name'] in x_dic) and x_dic[obj['name']] else '') or (str(obj.get('value','') or obj.get('def_value','')) if 'input' in need else  '')
    #if '__val__' not in x_dic:x_dic['__val__']={}
    #x_dic['__val__'][obj['name']]=_value
    x_dic[obj['name']]=_value
    obj['value']=_value
    obj['help']=''
    obj['output']=_value 
    obj['output_text']=_value # output in simple text
    obj['input']=obj.get('input',_value ) # if read im prop
    obj['help_txt']=''
    obj['data_json']=_value
    '''
        input may creat by auto_x
    '''
    #xprint('output='+str(obj['output']))
    #cm.tik('step 3')
    def x_auto():
        ''' 
            اطلاعات این فیلد یا در آیتم auto نشان داده می شود و یا در آیتم ref
            this field info is show in ["auto"] item or in ["ref"] item
        '''
        obj["value"]=obj['output_text']=_value #au_txt
        
        obj['output']=DIV(_value,_class="input_auto")
        obj['data_json']=_value
        obj['help']="خود کار"
        if 'input' in need :
            if 'auto-x' in obj: #input is creat in auto_x that have ref
                au_txt=obj['auto-x']
            else:
                if 'auto' in obj:
                    au_txt=obj['auto']
                elif 'ref' in obj:
                    x_dt=reference_select(obj['ref'],form_data=x_dic)
                    #xxxprint(vals=obj['ref'])
                    #xxxprint(vals=x_dic)
                    #xxxprint(msg=['x_dt','',''],vals=x_dt)
                    au_txt=x_dt['__0__'] if x_dt else ''
            #_len=60 if len(au_txt)>60 else len(au_txt)+2
            if len(au_txt)>60:
                obj['input']=XML(f"<textarea readonly class='input_auto' {_n} rows='2' style='width:100%'>{au_txt} </textarea>")
            else:
                obj['input']=XML(f"<input {_n} value='{au_txt}'  readonly class='input_auto'  style='width:100%'>" )#size='{_len}'
            if au_txt and au_txt=='***':
                print(au_txt)
                #if c_form:c_form.report()
            x_dic[obj['name']]=au_txt        
            msg=""
            jcode1=""
            form=share.form
            if "uniq" in obj : #"singel" 
                xquery1=f"[{form['tb']}].[{_name}]='{au_txt}' and [{form['tb']}].[id]<> {session('form_index')}"
                n= x_sql.sql_count(share.form['db'],share.form['tb'], xquery1)
                if n>0 : 
                    msg="خطا : اطلاعات این فیلد تکراری می باشد و قبلا در فرم دیگری ثبت شده است. لطفا از اطلاعات غیر تکراری در گذشته برای این فیلد استفاده نمایید." 
                    jcode1="alert('" + msg + "');re=false;"
                    obj['input']+="<h1 style='color:#ff5555;' >" + msg + "</h1>"
            if _value!=au_txt:
                import k_str
                ddif=k_str.compare_2_str(au_txt,_value)
                if ddif != '=':
                    obj["value"]=au_txt
                    
                    #alert_not_match_value
                    msg1=""" new = {new_val}\n old = {old_val} \n ------------- \n {ddif}""".format(new_val=au_txt,old_val=_value,ddif=ddif) if _value else ''
                    msg2=update_1_obj_in_table({obj['name']:au_txt})
                    msg3="""<h4 title="{des} \n {msg1} \n ============== \n {msg2}" class={_class}>{alert}</h4>""".format(
                        msg1=msg1,msg2=msg2,des='تغییرات به شرح زیر می باشد',_class="bg-warning",alert="گزارش تغییر") if (msg1 or msg2) else ''
                    
                    obj['output_text']=obj['output']=XML(f'''<div >{msg3}{au_txt}</div>''')
                    #obj['input']=XML(f'''<div >{obj['input']}{msg1}</div>''')
                    #obj['help']=XML(f'''<div >{msg3}</div>''')
                    obj['help']=DIV(XML(msg3))
                    obj['help_txt']='change' if msg3 else ''
             
    #------------------------------------------------------------------------------------------------------------------
    def update_1_obj_in_table(set_dic,x_where=''):
        #saved_file_fullname,new_file_fullname)
        '''
        inputs:
        ------
            set_dic : dict
                exam = {obj['name']:new_file_fullname},
            x_where : none / dict / str /list 
                exam = {obj['name']:saved_file_fullname}
                none => update cur id = {'id':<cur_id>}
        '''
        if c_form:
            if hasattr(c_form, 'db1'):
                db1=c_form.db1 
            else:
                #from k_sql import DB1
                db1=DB1(c_form.db_name)
            tb_name=c_form.tb_name
            xid=c_form.xid
        else:
            db1=DB1(obj['db_name'])
            tb_name=obj['tb_name'] 
        #obj_name=obj['name']
        if not x_where:
            if xid:
                if xid>0:
                    x_where={'id':xid}
                else:
                    return '--'
            else:
                return 'error : not find id - c_form is not present'
        res1=db1.update_data(tb_name,set_dic,x_where)
        return XML(res1['msg'])
    #------------------------------------------------------------------------------------------------------------------ 
    readonly='readonly' if 'readonly' in obj['prop'] else '' #:obj['input']=obj['output']    
    if sc=='text':#sc
        def htm_correct(x):
            if x:
                t= x.replace('"','|')
                t= t.replace('None','')
                t= t.replace('none','')
                return t
            else:
                return ''
        ##------
        _value=htm_correct(_value)
        if 'output' in need:
            obj['output']=htm_correct(_value)
            obj['output_text']=obj['output']
        else: #'input' in need
            _dir='dir="ltr"' if ('lang' in obj and obj['lang']=='en') else 'dir="rtl"' 
            def set_x(x,obj):
                return f'''{x}="{obj[x]}"''' if x in obj else ''
            xx=['placeholder','data-slots','data-accept','dir','size','pattern']    
            tt=' '.join([set_x(x,obj) for x in xx])
            #---------
            if "update" in obj['prop']:onact_txt= " onchange='" + form_update_set(form_update_set_param) + "'"
            if "optional" in obj['prop']: 
                x_class= " class='input_optional' " 
                if _value=="" : _value="-"
            if "uniq" in obj: 
                uniq_where=obj["uniq"]
                onact_txt= f''' onchange="ajax_chek_uniq('{db_name}','{tb_name}','{_name}','#{_name}','{uniq_where}');"'''#;event.preventDefault()
            t_val= f' value="{_value}"' #'' if 'placeholder' in obj else
            if _len<60 :
                obj['input']=XML(f'''
                    <input type="text" {_n} {x_class} {_dir} {tt} {t_val} size="{_len}" maxlength="{_len}" style='width:100%' onkeyup="txt_key('{_name}',{_len});" {onact_txt} required {readonly}>''')
                #if 'disabled' in obj:ix=XML(f"<INPUT name={obj['name']} id={obj['name']} value={obj['value']} style='width:100%' disabled>")
            else:   
                obj['input']=XML(f'''
                    <textarea {_n} {x_class} {_dir} rows="2" style='width:100%' maxlength="{_len}" onkeyup='txt_key("{_name}",{_len});'  {onact_txt} {readonly} > {_value} </textarea>''' )
                #style='width:100%'
            
            ##--------  
            or_v=""
            js_ff_chek="" #msg is define correct in top of select
            js_ff_act=f'fa_coreect_obj("{_name}");'
        obj['help']=XML(f"<a title='تعداد کاراکتر باقی مانده ، قابل اضافه کردن به متن' href = 'javascript:void(0)'> x * <b id='label{_name}'>{_len-len(_value)}</b></a> ")
    elif sc== "num": #sc #ok 010808
        x_min=f"{obj['min']} " if 'min' in obj else "*"
        x_max=f"{obj['max']}" if 'max' in obj else "*"
        obj['help']=x_min + " - "+ x_max #f"{obj['min']} تا {obj['max']}"
        if 'input' in need :
            if "update" in obj['prop']:onact_txt= " onchange='" + form_update_set(form_update_set_param) + "'"
            if "uniq" in obj: 
                uniq_where=obj["uniq"]
                onact_txt= f''' onchange="ajax_chek_uniq('{db_name}','{tb_name}','{_name}','#{_name}','{uniq_where}');"'''#;event.preventDefault()
            x_min=f" min={obj['min']} " if 'min' in obj else ""
            x_max=f" max={obj['max']}" if 'max' in obj else ""
            x_step=f" step={obj['step']}" if 'step' in obj else ""
            obj['input']=XML(f'''
                <input type="number" {_n}{x_min}{x_max}{x_step} value="{_value}" {onact_txt} required {readonly}>''')
                #onchange='num_key("{_name}",{obj["min"]},{obj["max"]});' 
            
            ##--
            or_v=""
            js_ff_chek="" #msg is define correct in top of select
    elif sc=="check": #sc
        checked="checked" if _value=="1" else ""
        val_x="1" if _value=="1" else "0"
        #- print ("checked value="+ _value)
        if "update" in obj['prop']:onact_txt= " onchange='" + form_update_set(form_update_set_param) + "'"
        o_txt="style='width: 50px;height: 30px;transform: scale(1.01);margin: 0px;color:#hca;background color:#a00;' class='largercheckbox' type='checkbox' value='1'" 
        if 'output' in need:
            obj['output']=XML(f'''<input {_n} {o_txt} {checked} {readonly} onclick="return false;"/>''') #disabled="disabled"
        elif 'input' in need:
            obj['input']=XML(f'''<input {_n} type="hidden" value={val_x} ><input {o_txt} {checked} {readonly} required onchange="this.previousSibling.value=this.checked ?'1':'0' ">''')
            #f''<input {_n} type='hidden' value='0'>
            #                    <input {_n} {o_txt} {checked} {onact_txt}>   ''')
        obj['data_json']=1 if checked else 0
        obj['help'],or_v,js_ff_chek="","",""  #msg is define correct in top of select
    elif sc in ["select","user","reference"]: #sc
        onact_txt=obj['onchange']
        if "update" in obj['prop'] : onact_txt+= form_update_set(form_update_set_param) 
        # onact_txt= " onchange='" + form_update_set(form_update_set_param) + "'" 
        _multiple=('multiple' in i_obj['prop'])

        obj['key']=_value
        if sc=='user':
            obj['ref']={'db':'user','tb':'user','key':'{un}','val':'{un}-{m_w} {pre_n} {name} {family}'}
        if sc in ['reference','user']:
            tt_dif=0
            # obj['select']= 1 field to cach reference_select inf
            if 'select' not in obj:
                #tt_dif=time.time()
                #_select=cache_ram(str(obj['ref']),reference_select(obj['ref']))#,time_expire=60)
                #ref_t1=str(obj['ref'])
                
                #if ref_t not in cache_ram:
                #    cache_ram[ref_t]=reference_select(obj['ref'],form_data=x_dic)
                #_select= cache_ram[ref_t]   
                _select= reference_select(obj['ref'],form_data=x_dic,debug=False)
                #tt_dif=(time.time()-tt_dif)*10000
                obj['select']=_select
            else:
                _select=obj['select']
        elif sc=='user':
            pass
            #select_base_list,select_describ_list=x_user.users_of_task(base_data,select_addition_inf)
        _select=obj['select']
        _select={x:x for x in _select} if type(_select)==list else _select
        ##----------
        if debug:
            xprint('select='+ str(_select))
            xprint('value='+ str(_value))
            xprint('tt_dif='+ str(tt_dif))
        
        try:
            def select_1_or_multi(_value,_multiple):
                if not _value:return''
                if _multiple:
                    if type( _value)==list:
                        return ' | '.join([_select[x] for x in _value])
                    else: #type( _value)==str:
                        return ' | '.join([_select[x] for x in _value.split(',')])
                else:
                    if _value in _select:
                        return _select[_value]
                    else:
                        return ''
            obj['title']=select_1_or_multi(_value,_multiple)
            obj['output']=XML(f'''<a  title="{obj['title']}">{_value}</a>''')
            obj['data_json']=_value
        except Exception as err:
            obj['output']+=" -e" #XML( A("- e",_title=f"an error ocured<br>{str(err)}"))#> -e</a>'''
            xxxprint(msg=["err",'',''],err=err,vals=_select) 
        obj["value"]=_value
        obj['output_text']=obj['title'] #_select[_value] if (type(_value)==str and _value in _select) else ""
        if 'show_full' in obj['prop']:obj['output']=obj['output_text']
        if 'input' in need:
            import k_htm
            obj['input']=k_htm.select(_options=_select,_name=_name,_value=_value #.split(',') if _multiple else _value 
                ,_onchange=onact_txt,can_add=("can_add" in obj['prop']),_multiple=_multiple
                ,add_empty_first=True if (not 'add_empty_first' in obj) else obj['add_empty_first'],
                )
        or_v= " or j_n='...'"
        js_ff_chek= " || j_n=='...'" #msg is define correct in top of select
        obj['help']=obj['title']
        if readonly: obj['input']= XML(f'''<input type="text" {_n} value="{_value}" readonly style="background-color:#aaa">''')
    #elif sc =='fdate':
        
    elif sc=='fdate': #sc
        import k_date
        obj['format']='yyyy/mm/dd' #obj['format']
        _value=_value or k_date.ir_date(obj['format'])
        #if "update" in obj['prop']:onact_txt=form_update_set(form_update_set_param) 
        onchange= form_update_set(form_update_set_param) if "update" in obj['prop'] else ""
        #x_end= " readonly >" if "readonly" in obj['prop'] else f''' onchange='date_key("{_name}","{def_val}","{x_format}");' {onact_txt} >'''
        #obj['input']="<input type='text' " + _n + " value='" + def_val + "' size='" + maxlen +"' maxlength='" + maxlen +"' dir='" + d_lan + "' class='date-picker' " + x_end  
        readonly= "readonly" if "readonly" in obj['prop'] else ''
        if 'input' in need :
            obj['input']=INPUT(_class='fDATE',_name=_name,_id=_name,_value=_value,_readonly=readonly,_required=True,_onchange=onchange)
        obj['help']=DIV(obj['format'],_dir='ltr')
        obj['stnd6']=_value[2:4]+_value[5:7]+_value[8:10] if (_value and len(_value)>9) else "_"*6 #6 digit standard for date
        msg ,or_v,js_ff_chek="",'',''
    elif sc=='time_c': #sc
        onchange= form_update_set(form_update_set_param) if "update" in obj['prop'] else ""
        if 'input' in need :
            obj['input']=INPUT(_name=_name,_id=_name,_value=_value,_type="text",_class="timepicker_c",_required=True,_dir="ltr",_onchange=onchange)#_type="time"
        obj['help']=''
        msg ,or_v,js_ff_chek="",'',''
    elif sc=='time_t': #sc
        onchange= form_update_set(form_update_set_param) if "update" in obj['prop'] else ""
        update="update" if "update" in obj['prop'] else ""
        if 'input' in need :
            _maxtime=obj['time_inf']['maxTime'] if ('time_inf' in obj and 'maxTime' in obj['time_inf']) else '24:00'
            _time_inf=obj['time_inf'] if 'time_inf' in obj else ''
            obj['input']=INPUT(_name=_name,_id=_name,_value=_value,_type="text",_class="timepicker_t",
                _required=True,_dir="ltr",_time_inf=_time_inf,_maxtime=_maxtime,_update=update)#_type="time"
        obj['help']=''
        msg ,or_v,js_ff_chek="",'',''
    
    
        #xxxprint(msg=['auto',obj["value"],''],vals=obj)
    elif sc=="auto": #sc
        x_auto()
    elif sc=="auto-x": #sc
        obj2=obj.copy()
        obj2['type']='auto'
        if 'ref' in obj:
            obj2['auto-x']=x_dic['__objs__'][obj['ref']]['output_text']
        else:
            if obj['auto']=='_cur_user_':obj2['auto']='{{=session["username"]}}- {{=session["user_fullname"]}}'
            elif obj['auto']=='_cur_user_id_':obj2['auto']='{{=session["username"]}}'
            elif obj['auto']=='_cur_user_name_':obj2['auto']='{{=session["user_fullname"]}}'
        return obj_set(obj2,x_dic,x_data_s,xid, need,request,c_form)
            #x_auto()    
    elif sc=="index": #sc
        if 'input' in need:
            x_dt=reference_select(obj['ref'],form_data=x_dic)
            x_list=[x_dt[x] for x in x_dt if x_dt[x]]
            from k_num import SMART_NUM_LIST
            smart_num_list=SMART_NUM_LIST(x_list)
                
            #if def_val=="" : 
            index_new=str(smart_num_list.max()+1).zfill(_len)# index_ar[0] #else =def_val
            index_hlp=str(smart_num_list)
            
            #if len(index_new)>60 : obj['len']=60 else obj['len']=len(index_new)
            #if select_addition_inf[:5].lower()=="updat" :  onact_txt= " onblur='" + form_update_set(form_update_set_param) + "'" 
            x_end= "' readonly class='input_auto' >" if "readonly" in obj['prop'] else f'''' onchange='index_key("{_name}","{index_hlp}","{index_new}",true);' {onact_txt}>'''
            obj['input']=XML(f'''<input {_n} value='{index_new}' size='{_len} {x_end}''')
            obj['help']=XML(f"""<a href = 'javascript:void(0)' title='{index_hlp}' >لیست اعداد استفاده شده</a>""")
        msg=""  

    elif sc=="file": #sc
        import k_file
        #print('file_name='+obj['file_name'])
        obj['file_name']=k_file.name_correct(template_parser(obj['file_name'],x_dic))
        #obj['file_name'] = ''.join(c for c in x_file_name if c.isalnum()) # Remove non-alphanumeric characters 
        from gluon import current
        #_value=current.session['uploaded_name'] or _value
        #if _value==None:_value==''
        #_value=obj['file_name']#_value or 
        #print(f'value={_value},type={type(_value)},len={len(_value)}')
        show_link=XML(URL('file','download',args=['auto']+obj['path'].split(',')+[_value]))
        obj['s_ext']=_value.rpartition(".")[2] #s_xt=saved_extention
        
        import k_set,os 
        obj['true_path']=os.path.join(*[x for x in [k_set.C_SET().base_folder,'auto']+obj['path'].split(',') if x])
        
        import json
        todo=json.dumps({'do':'sql','db':db_name,'tb':tb_name,'set_dic':{obj['name']:"$filefullname$"},'where':{'id':xid}})
        
        upload_link=XML(URL('file','upload',args=['auto']+obj['path'].split(','),
            vars={'filename':obj['file_name'],'file_ext':obj['file_ext']
                ,'todo':todo
                ,'from':'form'}
            ))#'{un}-{user_filename}'
        #upload_link=XML(URL('file','upload',args=['auto']+obj['path'].split(','),vars={'filename':obj['file_name'],'file_ext':obj['file_ext'],'todo':{'do':'sql','db':db_name,'tb':tb_name,'set_dic':{obj["name"]:filename},'x_where':{'id':xid}}
        del_link=XML(URL('file','delete',args=['auto']+obj['path'].split(',')+[_value], vars={'todo':todo}))
        def file_rename_manage(old_file_full_name,new_file_name):
            '''
                بررسی و تشخیص تغییر سیستم نام گذاری فایل بعد از دریافت و ذخیره سازی فایل با روش نام گذاری قبلی
                و اعلام یک آلارم در کنار لینک نمایش فایل در جدول و در فرم
            '''
            if old_file_full_name and new_file_name:
                old_file_name=old_file_full_name.rpartition(".")[0]
                
                #alert_not_match_value
                msg="""<div title="{alert} \n --------- \n{des} \n new = {new_val}\n old = {old_val}" class={_class}><a href={href}><h4>R</h4></a></div>""".format(
                    new_val=new_file_name,old_val=old_file_name,
                    des='نام فایل باید به شرح زیر تغییر پیدا کند',_class="bg-warning",
                    href=URL(args=current.request.args,vars={'rename_file':1}) if session["admin"]  else '',
                    alert="نیاز به تغییر نام") if (new_file_name !=old_file_name) else ''
                
                return msg
                #if old_file_name !=new_file_name :return f"""<h3 title="file name is not match \n new computed name = {new_file_name}\n old name = {old_file_name}" class="bg-danger">error<h3>""" 
            return ''
        #----------------------------------------------------------------
        
        # alert_not_match_value : check file is exist - بررسی وجود فایل
        file_path=os.path.join(obj['true_path'],_value)
        file_exist=os.path.exists(file_path)
        des="فایل پیدا نشد"
        alert="عدم دسترسی به فایل"
        if not file_exist:
            msg1=[f"""<h4 title="{alert}\n -------- \n {des} \n path : \n {file_path}\n " class="btn-danger">?</h4>"""]
        else:
            msg1=[file_rename_manage(_value,obj['file_name'])]#check fine is renamed ?
            
        if msg1 and c_form:
            #c_form.report()
            xxxprint(3,msg=[_value,obj['file_name'],''],vals={'file_name':obj['file_name'],'x_dic':x_dic,'_value':_value,'msg1':msg1})
        # vars = 'from':'form' => for pass write_file_access in file.py(_folder_w_access) 
        #<input {_n} value="{_value}" readonly>
        bt_view=f'''<a class="btn btn-info" title='مشاهده فایل' href = 'javascript:void(0)' onclick='j_box_show("{show_link}",false);'>{_value}</a>'''
        file_icon=obj['s_ext'] #"F"
        bt_view_mini=f'''<a class="file-{obj['s_ext']}" title='مشاهده فایل {_value}' href = 'javascript:void(0)' onclick='j_box_show("{show_link}",false);'>{file_icon}</a>''' if _value else ''
        bt_del=f'''<a class="btn btn-danger" title='حذف فایل-{del_link}' href = 'javascript:void(0)' onclick='j_box_show("{del_link}",true);'>x</a>''' if _value else ''
        bt_del=''
        msg2=DIV(*[XML(x) for x in msg1]) if msg1 else ''
        #msg2=msg1 #if msg1 else ''
        obj['input']=XML(f'''
            <div >
            {bt_view}{bt_del}
            <a class="btn btn-primary" title='{obj['file_name']}' href = 'javascript:void(0)' onclick='j_box_show("{upload_link}",true);'>بارگزاری فایل</a></div>
            ''')
        obj['output']=XML(f'''<div>{bt_view}{msg2}</div>''')    
        obj['data_json']=obj['file_name']
        obj['output-mini']=XML(f'''<div>{bt_view_mini}{msg2}</div>''') 
        obj['help']=msg2
        
        #os.path.join(
        
        """
        def path_x(pre_folder,file_name,pattern):
            path1=k_file.folderpath_maker_by_filename(file_name,pattern)
            return os.path.join([x for x in [share.ksf["path_upload"],pre_folder,path1] if x])
        """    
       
        #---------------------------------
        
        def rename_file_in_form  ():
            '''
            goal:
                baresi mikonad ke agar name file avaz shode ast:
                    1-name file roy server ra avaz konad
                    2-name file dar database ra avaz konad 
                compare saved_file_fullname ,new_filename
            inputs:
                saved_file_fullname
                    =obj['value']
                new_filename    
            -------   
                saved_file_fullname =str
                    filename.ext
            '''
            saved_file_fullname=obj['value']
            new_filename=obj['file_name']
            
            saved_file_name=saved_file_fullname.split(".")[0]
            saved_file_ext=saved_file_fullname.split(".")[1]
            new_file_fullname=new_filename + "." + saved_file_ext
            #saved_file_name="-" : for when file is optional
            msg=''
            if saved_file_name.lower()!= new_filename.lower() and (saved_file_name!="-") and (saved_file_name!="") :
              
                #old_path=path_x(pre_folder=pre_folder,file_name=saved_file_fullname,pattern=path_full_patern)
                path=obj['true_path']
 
                res1=k_file.file_move((path,saved_file_fullname),(path,new_file_fullname))
                
                res2=update_1_obj_in_table(set_dic={obj['name']:new_file_fullname},x_where={obj['name']:saved_file_fullname})
 
                msg=DIV("نام فایل تغییر یافت"
                    ,_title="با توجه به تغییر مشخصات فایل نام فایل تغییر یافت"+f"""\n
                    old file name = {saved_file_fullname} \n
                    new file name = {new_file_fullname}\n -------- \n {res1}\n -------- \n {res2}""")
            return new_file_fullname,msg
            #/compare
        if 'rename_file' in request.vars:
            new_file_fullname,msg=rename_file_in_form()
            obj['help']=msg
        else:
            obj['help']=''
        """   
        #---------------------------------------------------------------------------------################################
        saved_file_fullname= def_val
        #obj1={x:template_parser(obj[x]) for x in ['file_name','ext','path','pre_folder']}

        path=path_x(pre_folder=obj['pre_folder'],file_name=obj['name'],pattern=obj['path'])
        x_file.dir_make (path)
        
        new_file_fullname=rename_file_in_form  (saved_file_fullname,obj['file_name'],obj['pre_folder'],obj['path_pattern'],path,obj_name)
        
        if "optional" in obj['prop'] :    
            xclass="input_optional  "
            if not new_file_fullname: new_file_fullname="-"
            sami_file=0
        else:
            xclass="input_file"
            x_where="id <> " + session("form_index")  + " and " + obj_name + " like '%" + obj['file_name'] + "%'"
            sami_file=x_sql.sql_count(share.form['db_n'],share.form['tb_n'], x_where )
        obj['input']="<input type='hidden' " + _n + " value=" + new_file_fullname +  " >"
        
        if sami_file>0 : #chek obj['file_name'] is used later (exist in other obj)
            e_t= "خطا : نام فایل استفاده شده توسط این فرم قبلا نیز استفاده شده است ." + "<br>"
            e_t+= "دلیل : احتمالا فرم در زمان پر کردن بخش های قبل با مشکل مواجه شده است" + "<br>"
            e_t+= "روش حل مشکل : فرم را به مراحل قبل برگردانید و دوباره تایید نمایید." + "<hr> "
            e_t+= "number of like file = " + sami_file + " <br> sql where => (" + x_where + ")"
            obj['input']+= "<div>" + e_t + "</div>"  
        else:
            if new_file_fullname=="" : 
                xlink1="لطفا فایل مربوطه را پیوست نمایید"
            elif new_file_fullname=="-" : 
                xlink1="-"
            else: 
                xlink1=out_jdownload_link (new_file_fullname , obj['pre_folder'] , obj['path'])
            obj['input']+= "<div id='link1" + _name + "'  style='float:left;width:95%' class='" + xclass + "'>" + xlink1 + "</div>" 
            if "optional" in obj['prop'] and len(xlink1)>1 : 
                obj['input']=obj['input'] + "<div id='link2" + _name + "' style='float:right;width:4%;' class='" + xclass + "' ><a  title='remove file' href = 'javascript:void(0)' onclick='clear_file_field(" + f'"{_name}"' + ");'> x </a> </div> "  
            link_x="','".join(obj[x] for x in ['pre_folder','path','file_name','ext','name'])  
            link=f"\"if (event.shiftkey) {{ jupload_big('{link_x}');}} else {{ jupload('{link_x }');}}\"" 
            obj['help']="<a  href = 'javascript:void(0)' onclick=" + link + "> upload new file </a>" # <a  href = 'javascript:void(0)' onclick=" + link_x2 + "> * </a>"
            
            or_v,js_ff_chek="",""   # msg is define correct in top of select
        """   
        
        #if c_form:c_form.report()
    elif sc=="f2f": #sc 
        db2,tb2=obj['ref']['db'],obj['ref']['tb']
        new_form_link=k_htm.a('+',_href=URL('form','xform_sd',args=[db2,tb2,'-1'],vars={'f2f_id':x_dic['id'],'form_case':1}),_target="box",_title='فرم جدید') #box
        
        #table of record data - جدول اصلاعات ثبت شده
        res=DB1(db2).select(tb2,where={'f2f_id':x_dic['id']},limit=0,result='dict_x',order='id',last=False)
        #xreport_var([{'res':res}])
        x_r_input,x_r_output,show_cols,titles=[],[],obj['ref']['show_cols'],res['titles']
        from x_data import x_data
        show_cols_tit=[x_data[db2][tb2]['tasks'][x]['title'] for x in show_cols]
        for i,row in enumerate(res['rows']):#.reverse():          
            xid=row[titles.index('id')]
            url=URL('form','xform_section',args=[db2,tb2,xid])
            link=XML(k_htm.a(i+1,_href=url,_target="box",_title='بازبینی',_class='btn btn-info'))
            x_r_input+=[[link , *[row[titles.index(x)] for x in show_cols]]]
            x_r_output+=[[row[titles.index(x)] for x in show_cols]]
        rec_table_input=k_htm.C_TABLE(['']+show_cols_tit,x_r_input).creat_htm(div_class='div2')
        rec_table_output=k_htm.C_TABLE(show_cols_tit,x_r_output).creat_htm(div_class='div2')

        
        #json
        json_list=[]
        for row in res['rows']:
            xd=dict(zip(titles,row))
            xd2={x:xd[x] for x in show_cols}
            json_list+=[xd2]
        obj['data_json']=json_list
        
        
        obj['output']=DIV(rec_table_output)
        obj['input']=DIV(rec_table_input,new_form_link)
    elif sc=="do": #sc
        do_name,do_param=base_data.split(share.st_splite_chr2)
        
        path = "do_act.asp?do=" + do_name + "&param=" + do_param 
        link_x1='"j_box_show' + ("_test" if share.ksf["debug_mode"]==0 else "" ) + f"('{path}');\"" #=> j_box_show('path') or j_box_show_test('path')
        obj['input']="<input type='hidden' " + n_set + " value=1 >" 
        obj['input']+="<a  href = 'javascript:void(0)' onclick=" + link_x1 + "> انجام شود</a>"
        obj['help'],or_v,js_ff_chek="","",""  #'msg is define correct in top of select
    """
            elif md== "private":
        pass
    elif md=="check":
        temp2="checked" if def_val=="1" else ""
        h_code1="<input " +  n_set + " class='largercheckbox' type='checkbox' value='true' " + temp2 +" >"
        h_code2,or_v,js_ff_chek="","",""  #msg is define correct in top of select
    elif md=="session":
        sizelen,session_i=base_data.split(splite_chr)
        def_val=session("form-to-form").split(";")[int(session_i)]
        h_code1="<input type='text' " +  n_set + " value='" + def_val + "' size='" + sizelen + "' readonly>" 
        h_code2,or_v,js_ff_chek="","",""  #msg is define correct in top of select
    """
    ##----------------------------
    #cm.tik('link start')
    if 'link' in obj: #sc end 
        r1='input' if 'input' in need else 'output'
        
        x_link=obj['link']
        target=x_link['target'] if 'target' in x_link else 'box'
        
        if 'url' in x_link:         
            p=[template_parser(x,x_dic) for x in x_link['url']]#'pro'
            args=[template_parser(x,x_dic) for x in x_link['args']]
            vars={x:template_parser(x_link['vars'][x],x_dic) for x in x_link['vars']}
            #obj[r1]=XML(A(DIV(obj[r1],_href=URL(*p,args=tuple(args),vars=vars))))
            show_link=URL(*p,args=tuple(args),vars=vars)
        elif 'x_url' in x_link:
            show_link=x_link['x_url']
        elif r1=='output':
            show_link=obj[r1]
        else:
            show_link=obj['value']
        #obj[r1]=XML(A(DIV(obj[r1]),_href='javascript:void(0)',_title=show_link,_onclick=f'j_box_show("{show_link}",false)' ))
        text=''
        _class=''
        reset=True
        if obj[r1]:
            text=x_link['text'] if 'text' in x_link else obj[r1]
            _class= x_link['class'] if 'class' in x_link else 'btn'
            reset=x_link['reset'] if 'reset' in x_link else reset
        x_link=k_htm.a(text,show_link,target,_class=_class,reset=reset) if show_link else ''
        obj[r1]=x_link if r1=='output' else DIV(obj[r1],x_link)
      
    ##----------------------
    if "private" in obj['prop']:
        pass
    ## trs.append(TR(obj['title'],obj['value']))
    #cm.tik('end')
    #cm.report()
    
    if '__objs__' not in x_dic:x_dic['__objs__']={}
    x_dic['__objs__'][obj['name']]=obj
    
    ##obj['js']=
    return obj #,cm.records()
    
class C_FORM_B():#
    def __init__(self,x_data_s,xid,new_data={},form_sabt_data={}):
        if type(x_data_s)==tuple:
            db_name,tb_name=x_data_s
            self.x_data_s=get_x_data_s(db_name,tb_name)[0]
            self.db_name=db_name
            self.tb_name=tb_name
        else:
            self.x_data_s=x_data_s
            self.db_name=x_data_s['base']['db_name']
            self.tb_name=x_data_s['base']['tb_name']
    def get_x_fields(self):
        #import k_err 
        #k_err.xreport_var([self.x_data_s]) 
        rep={
        'base':[x for x in self.x_data_s['tasks'] ], #list(self.x_data_s['tasks'].keys()),
        'step_apps':[f'step_{name}_{t}'  for name in self.x_data_s['steps'] for t in ['un','dt','ap']],
        'form_need':['f_nxt_s','f_nxt_u'],
        'backup_add':['xid']
        }
        return rep #
        
class C_FORM():
    '''
        مدیریت اقدامات مربوط به 1 فرم 
        در حالت های نمایش تکی یا 1 ردیف از جدول سوابق ثبت فرم
    '''
    def __init__(self,x_data_s,xid,new_data={},form_sabt_data={}):
        '''
            بارگذاری اطلاعات لازم مرتبط با فرم در داخل متغیر های کلاس
        inputs:
        ------
            x_data_s : dict 
                inf of fields of form
            xid : str
                index of current_record_of_form
            new_data : dict
                new data of current_record_of_form that shoud save - enter by user
            form_sabt_data : dict
                recorded data of current_record_of_form
        '''
        if type(x_data_s)==tuple:
            db_name,tb_name=x_data_s
            self.x_data_s=get_x_data_s(db_name,tb_name)[0]
            self.db_name=db_name
            self.tb_name=tb_name
        else:
            self.x_data_s=x_data_s
            self.db_name=x_data_s['base']['db_name']
            self.tb_name=x_data_s['base']['tb_name']
        self.xid=int(xid)
        if form_sabt_data:
            self.form_sabt_data=form_sabt_data
        else:
            self.__set_form_sabt_data()
        self.all_data=self.form_sabt_data.copy()
        self.new_data={}
        self.__set_new_data(new_data)
        self.last_text_app=''
        self.__set_f_nxt_s()
        self.cur_step=''
        self.cur_step_name=''
    def __set_new_data(self,new_data): 
        #self.new_data=new_data.copy() if not hasattr(self, 'new_data') else 
        self.new_data.update(new_data)
        self.all_data.update(new_data)
    def __set_form_sabt_data(self):
        '''
            دریافت اطلاعات ثبت شده فرم از دیتابیس
            #form_sabt_data= data of 1 sabt /record of 1 form
        '''
        db1=DB1(self.db_name )
        rows,titles,rows_num=db1.select(self.tb_name,where={'id':self.xid})
        if self.xid<1 or (not rows): #-1
            self.form_sabt_data={x:'' for x in titles}
        else:
            self.form_sabt_data=dict(zip(titles,rows[0]))
        self.db1=db1 
    def set_step_app(self,cur_step_name,text_app,reset=False):
        '''
        input:
            با فرض تایید 1 مرحله توسط کاربر جاری در همین لحظه
            cur_step_name:str
                name of curent step
        output:    
            به روز رسانی / ثبت اطلاعات مربوط به تایید 1 مرحله در داخل کلاس
        '''
        import k_date
        if reset:
            x_d= {f'step_{cur_step_name}_ap':''}
            """    
                    f'step_{cur_step_name}_un':'',
                    f'step_{cur_step_name}_dt':'',
                    
                }"""
        else:
            text_app=text_app.lower()
            x_d= {
                    f'step_{cur_step_name}_un':current.session['username'],
                    f'step_{cur_step_name}_dt':k_date.ir_date('yy/mm/dd-hh:gg:ss'),
                    f'step_{cur_step_name}_ap':text_app
                }
            if text_app=="x" :x_d['f_nxt_u']="x"
        self.new_data.update(x_d)
        self.all_data.update(x_d)
        return x_d
    def set_form_app(self):
        '''
        input:
            با فرض تایید 1 مرحله توسط کاربر جاری در همین لحظه
        output:   
            به روز رسانی اطلاعات مدیریت فرم در داخل کلاس
        '''
        #x_d={'f_nxt_s':str(new_step_name)}
        self.__set_f_nxt_s()
        x_d={'f_nxt_s':self.f_nxt_s}
        #print (x_d)
        x_d["f_nxt_u"]=self.f_nxt_u()
        #import k_err k_err.xreport_var([new_step_name,re1,self.all_data,self.x_data_s])  
        self.new_data.update(x_d)
        self.all_data.update(x_d)
        return x_d
    def __set_f_nxt_s(self):
        f_nxt_s=','.join([step_name for step_name in self.x_data_s['steps'] if self.step_state(step_name)[1]=='edit'])
        if not f_nxt_s:f_nxt_s='-'
        #print (f'f_nxt_s={f_nxt_s}')
        self.f_nxt_s=f_nxt_s
        x_d={
                'f_nxt_s':f_nxt_s
            }
        self.new_data.update(x_d)
        self.all_data.update(x_d)
        return f_nxt_s
        if self.xid=='-1':
            f_nxt_s=0 
        else:
            f_nxt_s=self.form_sabt_data['f_nxt_s']
            f_nxt_u=self.form_sabt_data['f_nxt_u']
            if f_nxt_s:
                if f_nxt_u=="x":
                    f_nxt_s=-int(f_nxt_s)
                else:
                    f_nxt_s=int(f_nxt_s)
            else:
                f_nxt_s=0
        self.f_nxt_s=f_nxt_s
    def f_nxt_u(self):
        import k_user
        f_nxt_s=self.f_nxt_s #self.all_data['f_nxt_s'] #tas
        if not f_nxt_s or f_nxt_s=='-': return '' 
        step_x_ap=f'step_{f_nxt_s}_ap'
        last_text_app=self.all_data.get(step_x_ap,'')
        self.last_text_app =last_text_app
        #import k_err 
        #k_err.xreport_var([last_text_app,self.all_data,self.form_sabt_data,self.x_data_s]) 
        _f_nxt_u=",".join([(k_user.jobs_masul(self.x_data_s,f_nxt_s,c_form=self,form_all_data=self.all_data) if last_text_app!="x" else "x") for f_nxt_s in f_nxt_s.split(',')])
        x_d={
            'f_nxt_u':_f_nxt_u
            }
        self.new_data.update(x_d)
        self.all_data.update(x_d)
        return _f_nxt_u
    def __new_db_data(self,f_nxt_s,new_data,reset=False):# USE ONLY BY : SAVE
        '''
        goal:
            تهیه یک دیکشنری از اطلاعاتی که قرار است در دیتا بیس به روز رسانی شوند
            reset:
                True:all field in cur step of form shoud be reset =>(set to '')
                False:all field in cur step of form shoud be save
        inputs:
        -------
            new_data:dict
                request.vars  \ or auto_data_by _pro
        '''
        x_data_s=self.x_data_s
        steps=x_data_s['steps']
        import k_err 
        #k_err.xxxprint(msg=["@@@ : ", str(xx),''])
        #k_err.xreport_var([f_nxt_s,step,steps])
        step=steps[self.cur_step_name]
        step_fields=step['tasks'].split(',')
     
        vv={}
        for step_field in step_fields:#t=field name
            if not step_field in new_data:
                continue
            req_field=new_data[step_field]
            if step_field in x_data_s['labels']:
                continue
            if x_data_s['tasks'][step_field]['type']=='file':
                continue
            if 'uniq' in x_data_s['tasks'][step_field]:
                url = f'''/spks/km/uniq_inf.json/{x_data_s['base']['db_name']}/{x_data_s['base']['tb_name']}/{step_field}'''
                data = {'uniq_value':req_field,'uniq_where':x_data_s['tasks'][step_field]['uniq']};
            vv[step_field]=(lambda x:','.join(x) if type(x)==list else (x or " ").strip())(new_data[step_field]) if not reset else ''
        #c_form=k_form.C_FORM(x_data_s,xid,vv)
        self.__set_new_data(vv)
        
        self.set_step_app(self.cur_step_name,new_data['text_app']) #dict2=
        self.set_form_app() #dict2.update()
        #vv.update(dict2)
        #return vv
        
    def __update(self,f_nxt_s,text_app,new_data):# USE ONLY BY : SAVE
        xid=self.xid
        rr=''
         
        if text_app=='r': 
            db1=DB1(self.db_name )
            result=db1.row_backup(self.tb_name,xid)
            #xx=self.x_data_s['steps'][self.cur_step_name]['start_step']
            last_step_name = self.x_data_s['steps'][self.cur_step_name]['start_step']
            x_d= {f'step_{last_step_name}_ap':''}
            xxxprint(vals={'x_d':x_d})
            self.new_data.update(x_d)
            self.all_data.update(x_d)
            #back_step=xx['start_step']
            #x_data={"step_"+ back_step +"_ap" :''} if back_step else {}
            #new_step_name = str(f_nxt_s-1)
            x_data={}
            rr="backup<br>"+"<br>".join([f'{x}={str(y)}' for x,y in result.items()])
        elif text_app=='x':
            x_data={"f_nxt_u":'x','f_nxt_s':''}
            #new_step_name = str(f_nxt_s) #"x-"+
        elif text_app=='y':
            x_data={}
            #new_step_name = str(f_nxt_s+1)
        self.__new_db_data(self.cur_step_name,new_data,reset=(text_app=='x'))
        #xxx->return "vv=<br>"+str(vv),"update not done"
        db1=DB1(self.db_name )
        new_data=self.new_data

        new_data.update(x_data)
        xu = db1.update_data(self.tb_name,new_data,{'id':xid})
        xxxprint(vals={'new_data1':self.new_data,'new_data2':new_data,'update_result':xu})
        p1=A(f"#{xid}-update",_onclick="$(this).next().toggle()",_class='toggle')
        p2=DIV(XML(f"{db1.path}<br> UPDATE: <hr>{rr}<hr>"))
        return  {'html_report':DIV(p1,p2,k_htm.val_report(xu)),'id':xid,'db_report':xu}
    def __insert(self,new_data):# USE ONLY BY : SAVE
        self.__new_db_data(0,new_data)
        #xreport_var([vv])
        db1=DB1(self.db_name )
        r1=db1.insert_data(self.tb_name,self.new_data)#.keys(),vv.values())
        #rr=f"{db1.path}<br> INSERT:result=" + "<br>".join([f'{x}:{r1[x]}' for x in r1])
        
        p1=A(f"#{r1['id']}-insert",_onclick="$(this).next().toggle()",_class='toggle')
        p2=DIV(XML(f"{db1.path}<br> INSERT:<hr>"))
        #rr=f"{db1.path}<br> INSERT:{k_htm.val_report(r1)}"
        return {'html_report':DIV(p1,p2,k_htm.val_report(r1)),'id':r1['id'],'db_report':r1}   
    def save(self,new_data,update_step=True,cur_step_name=''): #WIP 030701
        #--------------------------------
        #import k_err
        #k_err.xreport_var(new_data)
        xid=self.xid
        text_app=new_data['text_app'].lower()
        if xid==-1: #xid=='-1':
            x_r=self.__insert(new_data)
            #print('__insert')
        else:
            '''
            if update_step:
                f_nxt_s=int(self.form_sabt_data['f_nxt_s'] or '0')
            else:
                f_nxt_s=int(self.form_sabt_data['f_nxt_s'] or '1')-1
            '''
            #self.cur_step_name='0'
            if not cur_step_name :
                cur_step_name=new_data['cur_step_name'] or self.cur_step_name
            self.cur_step_name=cur_step_name
            x_r=self.__update(cur_step_name,text_app,new_data)
            #print('__update')
        return x_r #DIV(XML(r1)),xid,r_dic
        #--------------------------------     
    def save_app_review(self,request_data):
        xid=self.xid
        db1=DB1(self.db_name)
        
        '''
        f_nxt_s=int(self.form_sabt_data['f_nxt_s'] )
        new_step_name=f_nxt_s-1 if self.form_sabt_data['f_nxt_u']!='x' else f_nxt_s
        cur_step_name=new_step_name
        '''
        self.set_step_app(self.cur_step_name,request_data['text_app'],reset=True)  #dict2=
        self.set_form_app() #dict2.update()
        result=db1.row_backup(self.tb_name,xid)
        xu = db1.update_data(self.tb_name,self.new_data,{'id':xid})
        xxxprint(vals={'new_data':self.new_data,'update_result':xu,'cur_step':self.cur_step_name})
        htm_form=['UPDATE:'] 
        try:
            if xu['exe']['done']:
                htm_form+=[DIV("با موفقیت انجام شد",_class="container bg-info h3 text-center")]
        except:
            pass
        htm_form+=[f"{db1.path}<br> UPDATE: "+str(xu)+"<hr> backup<br>"+"<br>".join([f'{x}={str(y)}' for x,y in result.items()])]
        return htm_form
    def show_step_1_row(self,field_name,request,mode): #)x_data_s,xid,form_sabt_data,field_name,mode(
        '''
        input
        ------
            mode='output'/'input'
        output:
        ------
            titel,value,help
        '''
        import k_user
        x_data_s=self.x_data_s
        xid=self.xid
        #form_sabt_data=self.form_sabt_data
        form_sabt_data=self.all_data

        fd=x_data_s['tasks'][field_name]#fd=field_data
        htm_1=DIV(fd['title'],_title=field_name)#htm_1=html for 1th_part(=field name) of row
        if 'hide' in fd['prop']:
            return [htm_1,'*','']
        if 'auth' in fd :
            if (not k_user.user_in_xjobs(fd['auth'],x_data_s,c_form=self)):
                return [htm_1,'*',''] 
        if mode=='output-mini':
            if 'file'!= fd['type'] : mode='output'
            
        x_obj=obj_set(i_obj=fd,x_dic=form_sabt_data,x_data_s=x_data_s,xid=xid, need=[mode],request=request,c_form=self)
        return [htm_1,x_obj[mode],x_obj['help'],fd['title'],field_name,x_obj['data_json']]
        #------------------------------------------------- 
    def un_what_can_do_4_step(self,step_name,x_un=''):
        ''' 030907
        goal:
            کاربر آ چه کاری در مرحله ب می تواند انجام دهد
        output:
        ------
            edit / view / ret_edit
                edit : can edit                     می تواند تغییرات انجام دهد
                view : can not edit only can view می تواند فقط اطلاعات را مشاهده کند 
                ret_edit : can return 4 edit می تواند فرم را برای انجام تغییر به 1 مرحله قبل برگرداند   
        '''    
        import k_user        
        #print(f' ? user_in_xjobs_can-step_name:{step_name},un={x_un}')
        if k_user.user_in_xjobs_can('edit',self.x_data_s,c_form=self,step_index=step_name,un=x_un):
            #print(f'user_in_xjobs_can-step_name:{step_name},un{x_un}')
            return self.step_state(step_name)[1]
        if k_user.user_in_xjobs_can('view',self.x_data_s,c_form=self,step_index=step_name,un=x_un):
            return 'view'
        return '-'
    def step_state(self,step_name):
        '''
            مشخص کردن اینکه 1 مرحله در وضعیت آماده برای ویرایش می باشد - با توجه به نتایج مراحل دیگر
            step_state= str 0 to 4
                '0': filled and not can review - start & end (where)
                '1': filled and     can review - start & not end (where) & filled
                '2': curent for fill           - start & not end (where) & not filled
                '3': empty or fill and review  - not start (where)
                
                
        '''
        step=self.x_data_s['steps'][f'{step_name}']
        start_where=step['start_where'] #"'{step_0_ap}' =='y' and not '{step_2_ap}' in ['y','x']"
        end_where=step['end_where']
        #print(start_where)
        start_where_prs=start_where.format(**self.all_data)
        end_where_prs=end_where.format(**self.all_data)
        start=eval(start_where_prs)
        end=eval(end_where_prs)
        ss=f"start_where={start_where},end_where={end_where}"

        if not start:
            act_where=3 #befor
        elif end:
            act_where=0 #after
        else:
            act_where=1 #current
            #print(start_where_prs)
            #act_where_v=eval(start_where_prs) and not eval(end_where_prs)
            #if act_where==1:# step_name == self.f_nxt_s:
            if self.all_data[f'step_{step_name}_ap'] in ['y','x']:  #step_name == self.f_nxt_s-1:
                #print('ret_edit {step_name}')
                act_where=1
                return [act_where,'ret_edit',ss]
            else:
                #print(f'form_sabt_data => {step_name} => {start_where}'+ "---" + start_where_prs + " : " + str(start_where_v) )
                act_where=2
                return [act_where,'edit',ss]  
        return [act_where,'view',ss]
    def report(self):
        import k_err
        k_err.xreport_var([{'all_data':self.all_data,'new_data':self.new_data,'form_sabt_data':self.form_sabt_data}])
def get_x_data_s(db_name,tb_name):
    from x_data import x_data
    if not db_name in x_data:return False,'error : "{}" not in ( x_data )'.format(db_name)
    x_data_s1=x_data[db_name]#x_data_select
    
    if not tb_name in x_data_s1:return False,'error : "{}" not in ( x_data["{}"] )'.format(tb_name,db_name)
    x_data_s=x_data_s1[tb_name]
    return x_data_s,'ok'
def _alert_not_match_value(old_val,new_val,_class="bg-danger",alert="error",des='تغییرات به شرح زیر می باشد'):
    if old_val !=new_val :
        return f"""<h4 title="{des} \n new = {new_val}\n old = {old_val}" class={_class}>{alert}<h4>""" 
    return ''
def input_validate(in_data,data_inf):
    '''
    goal :
        check that 1 input data is valid according type
    input:
    ------
        data_inf:dict
            'type': text / num / ref
    '''
    sc=data_inf['type']
    if sc=='text':
        if type(in_data)==str:
            return True
        return False  
    if sc=='num':
        def is_str_int(txt):
            try:
                x=int(txt)
                return True
            except:
                return False
        def is_str_float(txt):
            try:
                x=float(txt)
                return True
            except:
                return False        
        if type(in_data) in [int,float]:
            return True
        elif is_str_float(in_data) or  is_str_int(in_data): 
            return True
        return False 
    if sc=='ref':
        if in_data in data_inf['select']:
            return True
        else:
            return False
def chidman(hx,x_data_s,step,form_case=2,request=''):
    import k_user,k_tools
    form_case=k_tools.int_force((request.post_vars['form_case'] or request.get_vars['form_case']) if request else form_case,form_case)
    xjobs=k_user.xjobs_inf(step['xjobs'],x_data_s)
    
    
    if form_case==1:
        return [DIV(
                    DIV(hx['stp'],_class='col text-right'),
                    DIV(xjobs['describe'],_title=xjobs['inf'],_class='col text-warning',_dir='rtl'),
                    _class='row text-light bg-dark' )
                ]+hx['data']+[
                    DIV(DIV(_class="col"),*[DIV(x,_class=f"col {hx['app-color']}") for x in hx['app']],_class=f"row")
                ]
        #return DIV(DIV(hx['stp'],_class='col-2 text-right border-left'),DIV(htm_1,_class='col-10'),_class='row border-bottom')
    elif form_case==2:
        htm_1=[DIV(x,_class='row') for x in hx['app']]
        return DIV(
                    DIV(DIV(hx['stp'],_class='row'),
                        DIV(xjobs['describe'],_title=xjobs['inf'],_class='row text-warning'),
                        _class='col-2 text-right border-left text-light bg-dark'),
                    DIV(hx['data'],_class='col-8'),
                    DIV(htm_1,_class=f"col-2 {hx['app-color']}"),
                    _class="row border-bottom ")   
