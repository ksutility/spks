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
##---------------------------------------------------------------------------------################################
def get_inf_db(form,in_index):
    '''
    not_used 020905
    
    read database of form
        input:
        -------
            form['base']['db_n']
                old=in_db_name
            form['base']['tb_n']
                old=in_table_name
            session["form_index"]
                old=in_index
            form['tasks']
                old=task_inf
            form['steps']
                old=form['steps']
         outpu:
        -------
            form['steps']
            form['tasks']
            form['xinf']:
                form_xinf
            
    #--out use=3(file):x_sql(1 hit),install_db(1 hit),formshow(1 hit)
    #db=database  session("form_index")
    old use =get_inf_db(task_total,step_total,form_db_n,form_tb_n,f_step,f_revn,f_revs, rejecttext)'db=database
    #*****get >> form['steps']  14,15,16     task_inf 0
    '''
    in_db_name=form['base']['db_n']
    in_table_name=form['base']['tb_n']
    task_inf=form['tasks']
    # --- /input
    db1=DB1(in_db_name)
    rs=db1.select(in_table_name,where={'id':in_index},limit=1,result='dict')
    if rs :
        for step in form['steps'][1:]:
            step['s_u']=rs[step['s_u_f']].lower()
            step['s_d']=rs[step['s_d_f']].lower()
            step['s_a']=rs[step['s_a_f']]
        for task in form['tasks'][1:]:
            if task['tbl_n']=="" : #*
                task['val']=rs[task['field_n']] #*
                #share.task_inf[i]['type']=field_vb_type(rs.fields(share.task_inf[i]['field_n']).type )'*
        
        form_xinf={
            'f_step':int(rs["f_step"] or 0),
            'f_revn':rs["f_revn"],
            'f_revs':rs["f_revs"],
            'f_nexu':rs["f_nexu"],
            'rejecttext':rs["f_desc"]}
    else:
        session["new_form"]="ok"
        form_xinf={'f_step':0}
    form['xinf']=form_xinf  
    return form
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
def obj_set_Form_active_parts_x(ix,form_update_set_param,xfield_titel): 
    '''
        not_used 020905
    '''
    #--out use=3(file):flist(1 hit),formshow(1 hit),formshow_admin(1 hit)

    t=share.task_inf[ix]
    h_code1,h_code2,js_chekvalid_code = obj_set(t['type'],t['field_n'],t['val'],t['inf'],t['i10'],t['i7'],t['i6'],form_update_set_param,xfield_titel) #'okey
    #['val'] = def_val megvar avaliye
    #['type'] = mode (num;text;get;user)
    #['field_n'] = obj name
    #['inf'] = base_data 
    #['i10'] = select_describ_list
    #['i7'] = select_base_list
    #['i6'] = select_addition_inf
    return h_code1,h_code2,js_chekvalid_code
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
def template_parser(x_template,x_dic={}):
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
    if type(x_template)==str:
        try:
            xx=x_template.strip()
            from gluon import template
            x1= template.render(content=xx,context=x_dic) 
            return x1.format(**x_dic)  #remove 020926
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
        if 'read' in f['prop']: #readonly
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
            db2=DB1(db_path+ref['db']+'.db')
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
#----------------------------------------------------------------------------------------------------------------------------------------------------
def reference_select (ref_0,form_nexu=False,form_data={}):

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
    #xxxprint(msg=['ref1','',''],vals=ref) 
    for x in ['db','tb','key','val']:
        if not x in ref:
            do_report('err',x + " is not in Ref /n ref shoud have ['db','tb','key','val']" +  ref)
    
    for x in ['db','tb','where']:
        ref[x]=template_parser(ref.get(x,''),x_dic=form_data) #.format(task=task_inf,step=form['steps'],session=session)
    #xxxprint(msg=['ref2','',''],vals=ref)    
    #dbn=share.base_path_data_read + share.dbc_form_prefix + ref['db']+".db"#db_path+ref['db']
    dbn=db_path+ ref['db']+".db"
    if form_nexu:
        ref['where']=((ref['where'] + " and ") if ref['where'] else "") + "f_nexu <> 'x' "
    rows,tits,row_n=DB1(dbn).select(table=ref['tb'],where=ref['where'],limit=0)
    if rows :
        output_data={ref['key'].format(**dict(zip(tits,row))):ref['val'].format(**dict(zip(tits,row))) for row in rows}
        #xxxprint(msg=['output_data','',''],vals=output_data) 
        return output_data
    return {}#'msg':ref['where']}

#----------------------------------------------------------------------------------------------------------------------------------------------------
def obj_set(i_obj,x_dic,x_data_s='',xid=0, need=['input','output'],request=''): 
    import k_htm
    form_update_set_param="form;form"
    cm=Cornometer(f"obj-{i_obj['type']}-{i_obj['name']}")
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
            data_def of this task (x_datat[db][tb]["tasks"][name])
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
    db_name,tb_name=x_data_s['base']['db_name'],x_data_s['base']['tb_name']
    cm.tik('obj template_parser start')
    obj={x:template_parser(i_obj[x],x_dic) for x in i_obj}#['file_name','ext','path','pre_folder']}
    #xreport_var([i_obj,x_dic,obj,''],True)
    cm.tik('obj template_parser end')
    
    if debug:
        xxxprint(msg=['obj',obj['name'],''],vals=x_dic,vals2=obj)
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
    sc=obj['type']
    _name=obj['name']
    onact_txt,x_class='',''
    _n=f"name='{_name}' id='{_name}'" 
    _len=int(obj['len']) if 'len' in obj else 256
    _value=request.vars[_name] if request else ''
    _value=_value or str(obj.get('value',obj['def_value'])) or (str(x_dic[obj['name']]) if (obj['name'] in x_dic) and x_dic[obj['name']] else '')
    obj['value']=_value
    obj['output']=_value 
    obj['output_text']=_value # output in simple text
    obj['input']=_value  # if read im prop
    #xprint('output='+str(obj['output']))
    cm.tik('step 3')
    if sc=='text':
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
                    <input type="text" {_n} {x_class} {_dir} {tt} {t_val} size="{_len}" maxlength="{_len}" style='width:100%' onkeyup="txt_key('{_name}',{_len});" {onact_txt} required>''')
                #if 'disabled' in obj:ix=XML(f"<INPUT name={obj['name']} id={obj['name']} value={obj['value']} style='width:100%' disabled>")
            else:   
                obj['input']=XML(f'''
                    <textarea {_n} {x_class} {_dir} rows="2" style='width:100%' maxlength="{_len}" onkeyup='txt_key("{_name}",{_len});'  {onact_txt} > {_value} </textarea>''' )
                #style='width:100%'
            
            ##--------  
            or_v=""
            js_ff_chek="" #msg is define correct in top of select
            js_ff_act=f'fa_coreect_obj("{_name}");'
        obj['help']=XML(f"<a title='تعداد کاراکتر باقی مانده ، قابل اضافه کردن به متن' href = 'javascript:void(0)'> x * <b id='label{_name}'>{_len-len(_value)}</b></a> ")
    elif sc== "num": #ok 010808
        x_min=f"{obj['min']} " if 'min' in obj else "*"
        x_max=f"{obj['max']}" if 'max' in obj else "*"
        obj['help']=x_min + " - "+ x_max #f"{obj['min']} تا {obj['max']}"
        if 'input' in need :
            if "update" in obj['prop']:onact_txt= " onchange='" + form_update_set(form_update_set_param) + "'"
            x_min=f"min={obj['min']} " if 'min' in obj else ""
            x_max=f"max={obj['max']}" if 'max' in obj else ""
            obj['input']=XML(f'''
                <input type="number" {_n} {x_min} {x_max} value="{_value}" {onact_txt} required>''')
                #onchange='num_key("{_name}",{obj["min"]},{obj["max"]});' 
            
            ##--
            or_v=""
            js_ff_chek="" #msg is define correct in top of select
    elif sc=="check": 
        checked="checked" if _value=="1" else ""
        val_x="1" if _value=="1" else "0"
        #- print ("checked value="+ _value)
        if "update" in obj['prop']:onact_txt= " onchange='" + form_update_set(form_update_set_param) + "'"
        o_txt="style='width: 50px;height: 30px;transform: scale(1.01);margin: 0px;color:#hca;background color:#a00;' class='largercheckbox' type='checkbox' value='1'" 
        if 'output' in need:
            obj['output']=XML(f'''<input {_n} {o_txt} {checked} onclick="return false;"/>''') #disabled="disabled"
        elif 'input' in need:
            obj['input']=XML(f'''<input {_n} type="hidden" value={val_x} ><input {o_txt} {checked} required onchange="this.previousSibling.value=this.checked ?'1':'0' ">''')
            #f''<input {_n} type='hidden' value='0'>
            #                    <input {_n} {o_txt} {checked} {onact_txt}>   ''')
        obj['help'],or_v,js_ff_chek="","",""  #msg is define correct in top of select
    elif sc in ["select","user","reference"]:
        onact_txt=obj['onchange']
        if "update" in obj['prop'] : onact_txt+= form_update_set(form_update_set_param) 
        # onact_txt= " onchange='" + form_update_set(form_update_set_param) + "'" 
        _multiple=('multiple' in i_obj['prop'])

        obj['key']=_value
        if sc=='reference':
            tt_dif=0
            # obj['select']= 1 field to cach reference_select inf
            if 'select' not in obj:
                tt_dif=time.time()
                #_select=cache_ram(str(obj['ref']),reference_select(obj['ref']))#,time_expire=60)
                ref_t=str(obj['ref'])
                #if ref_t not in cache_ram:
                #    cache_ram[ref_t]=reference_select(obj['ref'],form_data=x_dic)
                #_select= cache_ram[ref_t]   
                _select= reference_select(obj['ref'],form_data=x_dic)
                tt_dif=(time.time()-tt_dif)*10000
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
            xprint( 'select='+ str(_select))
            xprint( 'value='+ str(_value))
            xprint( 'tt_dif='+ str(tt_dif))
        
        try:
            def select_1_or_multi(_value,_multiple):
                if _multiple:
                     return ','.join([_select[x] for x in _value.split(',')])
                else:
                    return _select[_value]
            obj['output']=XML(f'''<a  title="{select_1_or_multi(_value,_multiple)}">{_value}</a>''')
        except Exception as err:
            obj['output']+=" -e" #XML( A("- e",_title=f"an error ocured<br>{str(err)}"))#> -e</a>'''
            
        if 'input' in need:
            import k_htm
            obj['input']=k_htm.select(_options=_select,_name=_name,_value=_value.split(',') if _multiple else _value 
                ,_onchange=onact_txt,can_add=("can_add" in obj['prop']),_multiple=_multiple )
        or_v= " or j_n='...'"
        js_ff_chek= " || j_n=='...'" #msg is define correct in top of select
        obj['help']=''
    #elif sc =='fdate':
        
    elif sc=='fdate':
        import k_date
        obj['format']='yymmdd' #obj['format']
        _value=_value or k_date.ir_date(obj['format'])
        if "update" in obj['prop']:onact_txt=form_update_set(form_update_set_param) 
        #x_end= " readonly >" if "readonly" in obj['prop'] else f''' onchange='date_key("{_name}","{def_val}","{x_format}");' {onact_txt} >'''
        #obj['input']="<input type='text' " + _n + " value='" + def_val + "' size='" + maxlen +"' maxlength='" + maxlen +"' dir='" + d_lan + "' class='date-picker' " + x_end  
        readonly= "readonly" if "readonly" in obj['prop'] else ''
        if 'input' in need :
            obj['input']=INPUT(_class='fDATE',_name=_name,_id=_name,_value=_value,_readonly=readonly,_required=True)
        obj['help']=DIV(obj['format'],_dir='ltr')
        msg ,or_v,js_ff_chek="",'',''
    elif sc=='time':
        if 'input' in need :
            obj['input']=INPUT(_name=_name,_id=_name,_value=_value,_type="time",_required=True)
        obj['help']=''
        msg ,or_v,js_ff_chek="",'',''
    elif sc=="auto":
        ''' 
            اطلاعات این فیلد یا در آیتم auto نشان داده می شود و یا در آیتم ref
            this field info is show in ["auto"] item or in ["ref"] item
        '''
        if 'auto' in obj:
            au_txt=obj['auto']
        elif 'ref' in obj:
            x_dt=reference_select(obj['ref'],form_data=x_dic)
            xxxprint(vals=obj['ref'])
            xxxprint(vals=x_dic)
            xxxprint(msg=['x_dt','',''],vals=x_dt)
            au_txt=x_dt['__0__'] if x_dt else ''
        _len=60 if len(au_txt)>60 else len(au_txt)+2
        obj['input']=XML(f"<input {_n} value='{au_txt}' size='{_len}' readonly class='input_auto' >" )
        obj['output_text']=obj['output']=au_txt
        obj['help']=""
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
    elif sc=="index":
        def index_select_do(ref,obj_name):
            for x in['db','tb','where']:
                ref[x]=template_parser(ref[x],x_dic)
            x_query=ref['where'] + " and f_nexu <> 'x' and id <> " + session("form_index")
            dbn=share.base_path_data_read + share.dbc_form_prefix + ref['db'] +".db"
            tt = sql_sum(dbn,ref['tb'],x_query,obj_name,"max,count,smartnum")
            new_n=tt(0)+ sgn(tt(1))
            return [str(new_n), tt(2)] 
        index=index_select_do(obj['ref'],obj['name'])
            #index_ar(1)=smart_num_list
        #if def_val=="" : 
        new_index= index_ar[0] #else new_index=def_val
        new_index=new_index.zfill(_len)
        
        #if len(new_index)>60 : obj['len']=60 else obj['len']=len(new_index)
        #if select_addition_inf[:5].lower()=="updat" :  onact_txt= " onblur='" + form_update_set(form_update_set_param) + "'" 
        x_end= "' readonly class='input_auto' >" if "readonly" in obj['prop'] else f'''' onchange='index_key("{_name}","{index_ar(1)}","{new_index}",true);' {onact_txt}>'''
        obj['input']=f'''<input {_n} value='{new_index}' size='{obj['len']} {x_end}'''
        obj['help']=" <b id='label" + _name + "'>" + index_ar(1) + "</b> "
        obj['help']=" <a href = 'javascript:void(0)' title='" + index_ar(1) + "' >لیست اعداد استفاده شده</a>"
        msg=""  

    elif sc=="file":
        import k_file
        #print('file_name='+obj['file_name'])
        obj['file_name']=k_file.name_correct(template_parser(obj['file_name'],x_dic))
        #print('file_name='+obj['file_name'])
        #obj['file_name'] = ''.join(c for c in x_file_name if c.isalnum()) # Remove non-alphanumeric characters 
        from gluon import current
        #_value=current.session['uploaded_name'] or _value
        #if _value==None:_value==''
        #_value=obj['file_name']#_value or 
        #print(f'value={_value},type={type(_value)},len={len(_value)}')
        show_link=XML(URL('file','download',args=['prj']+obj['path'].split(',')+[_value]))
        upload_link=XML(URL('file','upload',args=['prj']+obj['path'].split(','),vars={'filename':obj['file_name'],'file_ext':obj['file_ext'],'todo':f'sql;{db_name};{tb_name};{xid};{obj["name"]}','from':'form'}))#'{un}-{user_filename}'
        # vars = 'from':'form' => for pass write_file_access in file.py(_folder_w_access) 
        #<input {_n} value="{_value}" readonly>
        obj['input']=XML(f'''
            <div >
            <a class="btn btn-info" title='مشاهده فایل' href = 'javascript:void(0)' onclick='j_box_show("{show_link}",true);'>{_value}</a> - 
            <a class="btn btn-primary" title='{obj['file_name']}' href = 'javascript:void(0)' onclick='j_box_show("{upload_link}",true);'>بارگزاری فایل</a></div>
            ''')
        obj['output']=XML(f'''
            <div >
            <a  href = 'javascript:void(0)' title='{show_link}' onclick='j_box_show("{show_link}");'>{_value}</a> </div> ''')    
        """    
        def path_x(pre_folder,file_name,pattern):
            path1=k_file.folderpath_maker_by_filename(file_name,pattern)
            return "\\".join(x for x in [share.ksf["path_upload"],pre_folder,path1] if x)
        def rename_file_in_form  (saved_file_fullname,new_filename,pre_folder,path_full_patern,path,obj_name):
            '''
                baresi mikonad ke agar name file avaz shode ast:
                    1-name file roy server ra avaz konad
                    2-name file dar database ra avaz konad 
                compare saved_file_fullname ,new_filename
            '''
            saved_file_name=saved_file_fullname.split(".")[0]
            #saved_file_name="-" : for when file is optional
            if saved_file_name.lower()!= new_filename.lower() and (saved_file_name!="-") and (saved_file_name!="") :
                saved_file_ext=saved_file_fullname.split(".")[1]
                old_path=path_x(pre_folder=pre_folder,file_name=saved_file_fullname,pattern=path_full_patern)
                new_file_fullname=new_filename + "." + saved_file_ext
                k_file.file_move(old_path,saved_file_fullname,path,new_file_fullname,true)
                update_1_obj_in_table(new_file_fullname,obj_name)
                ou1=["با توجه به تغییر مشخصات فایل نام فایل تغییر یافت" + "<br>",
                    "old file name = " + saved_file_fullname + "<br>",
                    "new file name = " + new_file_fullname + "<br>"]
                return new_file_fullname
            #/compare
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
        obj['help']=''
    elif sc=="do":
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
    cm.tik('link start')
    if 'link' in obj:
        r1='input' if 'input' in need else 'output'
        #-----
        x_link=obj['link']
        p=[template_parser(x,x_dic) for x in x_link['url']]#'pro'
        args=[template_parser(x,x_dic) for x in x_link['args']]
        vars={x:template_parser(x_link['vars'][x],x_dic) for x in x_link['vars']}
        #obj[r1]=XML(A(DIV(obj[r1],_href=URL(*p,args=tuple(args),vars=vars))))
        show_link=URL(*p,args=tuple(args),vars=vars)
        obj[r1]=XML(A(DIV(obj[r1]),_href='javascript:void(0)',_title=show_link,_onclick=f'j_box_show("{show_link}")' ))

    ##----------------------
    if "private" in obj['prop']:
        pass
    ## trs.append(TR(obj['title'],obj['value']))
    cm.tik('end')
    #cm.report()
    
    if '__objs__' not in x_dic:x_dic['__objs__']={}
    x_dic['__objs__'][obj['name']]=obj
    
    return obj,cm.records()

    


    
