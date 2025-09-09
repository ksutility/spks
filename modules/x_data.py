# -*- coding: utf-8 -*-
# ver 1.00 1401/09/24 
# -------------------------------------------------------------------------
#f = open('applications\prj\databases\example2.json','w')
#import json
#json.dump(tasks,f)
"""
help  
x_data={
    '<db_file_name>':{
        '<table_name>':{
            'tasks':{
                <task_i>
                ...
            }
            'views':{
                'input':[field_name_i,...]
                'view1':[field_name_i,...]
                'view2':[field_name_i,...]
            }
            'cols_filter':[filter_i_val,...] or {filter_i_name:filter_i_val,...}
        }
    }
---------------------    
انواع اقدام ها - تسک ها   و ویژگیهای خاص هر یک
tasks
    کلیه تسکها/ عملگر های یک موضوع / جدول در داخل این بخش به صورت یک دیکشنری جیسون تعریف می شوند
    each task defin format :
        'task name':{'prop name1':'prop val 1',...}
   
    task type:str
        text:
            'placeholder':
                sample = "0...-...-...."
            'data-slots': str
                sample = "."
            'data-accept': str
                sample = "\d"
            'dir':'ltr'
            'size':
            'len':str
                example = '9'
            'pattern':pattern
                sample="0[0-9]{{3}}-[0-9]{{3}}-[0-9]{{4}}"
            'lang':'en'
                optional
            'width':str 
                sample = '10'
            'title':str
                sample = 'شماره نامه'   
            'uniq':str
                if this item present fied accept only uniq value
                اگر این آیتم در مشخصات فیلد وجود داشته باشد در زمان ورود فقط مقادیر یکتا را می پذیرد
                value of this item show "uniq where sql"
            note : 1 of  'lang' or 'dir'  can be used
        link :
            'link':{'pro':['<app name>','<module name>','<func name>'],'args':['<arg_1>','<arg_2>',...,'<arg_n>']
                '<app name>','<module name>','<func name>' : format
                '<arg_1>','<arg_2>',...,'<arg_n>':format 
                format = text + {python script includ <value_nameS> } + text
                <value_nameS>=1 of [x for x in field['paper']]  
        xlink:
            'xlink' differenc by 'link' is:
                'xlink' not have value in base database file
                در فایل بانک اطلاعاتی فیلدی و اطلاعات ثبت شده ندارد
        reference:
            'ref':dict =exam=> {'db':'prj','tb':'a','key':'{id}','val':'{id:03d}-{name}'}
                'db':str 'database_neme' 
                'tb':str 'table_name',
                'key':format
                    exam = 
                        '{id}'
                        '{un}'
                        '{code}'
                'val':format
                    exam =
                        '{id:03d}-{name}'
                        '{un}-{family}'
                        '{un}-{m_w} {pre_n} {name} {family}'
                'where':query
                    exam =
                        '''prj1 = "{{=__objs__['prj2']['value']}}"'''
                            mean = > dest_db.prj1=current_form.prj2.value
                        'prj1={prj2}'
                            same exam (=exam1)
                        '''c_prj_id = "{{=__objs__['c_prj_id']['value']}}" AND sub_p =  "{{=__objs__['sub_p']['value']}}"'''
        reference addition data:
            sample:
                1:
                    text:
                        'c_prj_id':{'type':'reference','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update','multiple']},
                        'c_prj_txt':{'type':'auto-x','ref':'c_prj_id'},
                    result:
                2:
                    text:
                        'c_prj_id':{'type':'reference','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d},{cp_code},{cp_name}'},'title':'پروژه','prop':['update']},
                        'cp_code':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_code}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'کد پروژه','prop':['hidden']},
                        'cp_name':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_name}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'نام پروژه','prop':['hidden']},
                        
                3:
                    text:
                        'c_prj_id':{'type':'reference','title':'پروژه','prop':['update'],
                            'ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d},{cp_code},{cp_name}'},
                            'team':{'cp_code':{'val':'{cp_code}','title':'کد پروژه'},'cp_name':{'val':'{cp_name}','title':'نام پروژه'}},},
                4:
                    text:
                        'c_prj_txt':{'type':'auto','len':'50','auto':"{{=__objs__['c_prj_id']['output_text'][5:]}}",'title':'نام پروژه'},
                            
        index:
            'len':num_str : number in str format
                *important*         
            'ref'::dict =exam=> {'db':'test','tb':'b','key':'{id}','val':'{indx1}','where':''}
            exam =
                'rev':{'type':'index','len':'2','ref':{'db':'doc_mm2','tb':'attch','key':'{id}','val':'{rev}','where':f"f_code = {'f_code'}"},'title':'شماره','prop':['update']},
        auto:
            exame:
            'a':{'type':'auto','len':'250','title':'نام مدرک','auto':"{{=__objs__['doc_srl_code']['output_text'][5:].strip()}}"}, #"{{=__objs__['doc_srl_code']['select'][doc_srl_code]}}"
    prop:['prop1','prop2',...]
        readonly:
            عدم امکان تغییر فیلد ورودی
        hidden:
            فیلد وجود ددارد ولی نمایش داده نمی شود
            مناسب برای امکان آپدیت 1 مقدار 
            مخصوصا برای فیلدهای نمایشگر مرتبط با 1 فیلد رفرنس
            برای مشاهده آن از اینسپکت در مرورگر می توان استفاده کرد
---------------------    
'base'
    'form':
        'table+': table taht have 2 addition ccolumn ( 1= sabt_user,2=sabt_date)
        'form'
        ''='table'
---------------------
__objs__
    'auto':"{{=__objs__['prj']['select'][prj][5:].strip()}}-{name}"
    'where':'''prj = "{{=__objs__['prj']['value']}}"'''
--------------------
__0__
    target specific key in ref for auto(type) object in tasks
    tasks.
-------------------
steps.xjobs= list of name of xjobs 
        * in job = all user that have pass
        #task#<task-name> = user that fill <task-name>
        #step#<step-name> = user that fill <step-name>:
    sample:        
        'dccm'
        '#step#0'
        '#task#ref'
        '*'
        'dccm,arm'
    
-------------------
                steps:
                    app_keys =>shoud be small leter

                task:
                    ref,select,user:
                        prop:
                            multiple =>can select multiple item
--------------------
'data_filter':{
    '':'همه همکاران',
    'code is Null':'نیاز به تعیین پروژه',
    'code = "36"':'پروژه پیوندراه',
    'prj = "29" AND x_des like "%L-%"':'-Lپروژه گیتها',
    'act_todo != ""':'دارای ارجاع',
    'lno like "%xxxx%"':'جستجوی نامه'},   
-------------------
'uniq':{'where':''}
    prossecc:
        ks-form.js >    ajax_chek_uniq()
        km.py >         chek_uniq()
                        uniq_inf()
        k_form.py >     
        
    note:
        git: 107-add where to uniq field
        - " error = error that accur when " is in uniq_where_text like=>'uniq':{'where':'sel="x"'}
        -- repare " error by replace " by ` in x_data.py>uniq_where_text and rereplace in k_sql.py>chek_uniq()
-------------------
'auto':"{{=__objs__['prj']['select'][prj][5:].strip()}}-{name}"
	'auto':'{{import k_time}}{{=k_time.add("10:55","5:25")}}'
	'auto':'{{import k_time}}{{=k_time.add(time_st,time_len)}}'

'sp_order' =spesial order :1 step of form that shoud run in unsecoenc
-----------------------
prompt:
    لیست زیر انواع 
    سبک ارتباطی (Communication Preference
    در
    پرسونای کارفرما  
    است  آنرا کامل کن و برای هر کدام 1 کد 4 حرفی پیشنهاد بده
    خروجی در فرمت زیر باشد
    [code]:'[persian title](english title) - [persian describ]'
    "
    
    "
    [کد 4 حرفی]:[عنوان فارسی]()-[]
"""
x_data_cat={
    '-':'همه فرمها',
    '1':'اطلاعات اصلی',
    '2':'فرمهای پرسنلی',
    '3':'عمومی',
    '4':'DCC',
    '8':'مدیریت',
    '9':'موارد متفرقه',
    }
'''
import json
with open("myfile.json", "r",encoding='utf8') as fp:
    data = fp.read()
x_data=json.loads(data)
'''      
# c_prj_id
x_data={
    'a_cur_subject':{ #db
        'a':{
            'base':{'mode':'form','title':'موضوعات و پروژه های جاری','code':'100','multi_app':{'0':['ks'],'1':['ks']},},
            'tasks':{
                'prj_id':{'type':'reference','title':'پروژه',
                    'ref':{'db':'a_prj','tb':'a','key':'{id}','val':'{code}-{name}'},'prop':['update'],
                    'team':{'prj':{'val':'{code}','title':'کد پروژه'},'prj_name':{'val':'{name}','title':'نام پروژه'}},},
                #'prj':{'type':'auto','ref':{'db':'a_prj','tb':'a','key':'__0__','val':'{code}','where':'''id = "{prj_id}"'''},'title':'پروژه'},#,'prop':['report']
                #'prj_name':{'type':'auto','len':'50','auto':"{{=__objs__['prj_id']['output_text'][5:]}}",'title':'نام پروژه'},
                'sub_p_id':{'type':'reference','title':'زیر پروژه',
                    'ref':{'db':'a_sub_p','tb':'a','key':'{id}','val':'{code}-{name}','where':'''prj_id = "{prj_id}"'''},'prop':['update'],
                    'team':{'sub_p':{'val':'{code}','title':'کد زیر پروژه'},'sub_p_name':{'val':'{name}','title':'نام زیر پروژه'}},},
                    
                #'sub_p':{'type':'auto','ref':{'db':'a_sub_p','tb':'a','key':'__0__','val':'{code}','where':'''id = "{sub_p_id}"'''},'title':'زیر پروژه'},#,'prop':['report']
                #'sub_p_name':{'type':'auto','len':'50','auto':"{{=__objs__['sub_p']['output_text'][4:]}}",'title':'نام زیر پروژه'},
            
                'cp_code':{'type':'text','title':'کد موضوع','len':'10','uniq':''},
                'cp_name':{'type':'text','title':'نام کامل','len':'140','lang':'fa'},
                'cp_name2':{'type':'text','title':'نام کامل 2 ','len':'140','lang':'fa'},
                'sm_name':{'type':'text','title':'نام مختصر','len':'40','lang':'fa'},
                'alt_names':{'type':'text','title':'نام های متفرقه','len':'250','lang':'fa'},
                'salimi':{'type':'text','title':'نام در سیستم مهندس سلیمی','len':'150','lang':'fa'},
                #'c2_prjs':{'type':'reference','width':'20','title':'زیر پروژه های مرتبط','ref':{'db':'a_sub_p','tb':'a','key':'{code2}','val':'{code2}-{name2}'},'prop':['multiple']},
                'dspln':{'type':'reference','title':'دیسیپلین اصلی','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{code} , {name} , {name_e}'},},
                'mdr_prj':{'type':'user','title':'مسئول پیگیری پروژه'},
                'dsplns':{'type':'f2f','len':'60','title':'دیسیپلینها','ref':{'tb':'dsplns','show_cols':['d_name','per','des']},},
                'wbs_l1':{'type':'f2f','len':'60','title':'WBS- لایه 1','ref':{'tb':'wbs_l1','show_cols':['wbs_l1_name','wbs_l1_code']},},
                'cat':{'type':'select','title':'دسته','select':{'P':'پروژه','F':'فرایند'}},
                'contract':{'type':'f_link','title':'قرارداد','ref':{'db':'a_contract','tb':'a','key':'{id}','val':'{date}-{subject}','show_cols':['date','subject']},'prop':['update','multiple'] },
            },
            'steps':{
                'pre':{'tasks':'cp_name','xjobs':'dcc_dsn','title':'ثبت','app_keys':'','app_titls':'','oncomplete_act':''},#cp_code,cp_name
                's1':{'tasks':'prj_id,prj,prj_name,sub_p_id,sub_p,sub_p_name,cp_code,cat,dspln,mdr_prj,contract','xjobs':'dccm','title':'گام2','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'dsplns,wbs_l1,sm_name,alt_names','xjobs':'dcc_dsn','title':'تکمیل','app_keys':'','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'sub_p_id','xjobs':'dccm','title':'تصویب','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'cat,dspln,mdr_prj,salimi,sub_p_id','view1':'cp_code,cp_name','view2':'sm_name,alt_names,salimi'},
            },
            'cols_filter':{
                '':'همه',
                },
            'data_filter':{'':'همه موارد',
                'cat is Null':'نوع مشخص نشده',
                'cat = "P"':'همه پروژه ها',
                'cat = "F"':'همه فرایندها',
                },
        },
        'dsplns':{
            'base':{'mode':'form','title':'دیسیپلینها -  پروژه های جاری','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','len':'5','title':'فرم مبنا','ref':{'tb':'a','key':'{id}','val':'{cp_code} , {cp_name}'},'prop':['readonly']},
                'd_name':{'type':'reference','title':'نام دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{code} , {name} , {name_e}'},},
                'per':{'type':'user','title':'مسئول دیسیپلین'},
                'des':{'type':'text','len':'250','title':'سایر اقدامات'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,d_name,per,des','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            
        },
        'wbs_l1':{
            'base':{'mode':'form','title':'پروژه های جاری – wbs  لایه 1 ','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','len':'5','title':'فرم مبنا','prop':['readonly'],
                    'ref':{'tb':'a','key':'{id}','val':'{cp_code} , {cp_name}'},
                    'team':{'cp_code':{'val':'{cp_code}','title':'کد پروژه'},'cp_name':{'val':'{cp_name}','title':'نام پروژه'}},},
                'wbs_l1_name':{'type':'text','title':'دسته موضوع اقدام','len':'250',},
                'wbs_l1_code':{'type':'index','len':'1','title':'کد دسته  موضوع اقدام','start':1,'ref':{'db':'a_cur_subject','tb':'wbs_l1','key':'{id}','val':'{wbs_l1_code}','where':'''f2f_id = "{{=__objs__['f2f_id']['value']}}"'''},},
                'des':{'type':'text','len':'250','title':'توضیحات'},
                'wbs_l2':{'type':'f2f','len':'60','title':'WBS- لایه 2','ref':{'tb':'wbs_l2','show_cols':['wbs_l2_name','wbs_l2_code']},},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,cp_code,cp_name,wbs_l1_name,wbs_l1_code,des','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'wbs_l2','xjobs':'dccm','title':'اطلاعات کلی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            
        },
        'wbs_l2':{
            'base':{'mode':'form','title':'پروژه های جاری – wbs  لایه 2 ','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','len':'5','title':'فرم مبنا','prop':['readonly'],
                    'ref':{'tb':'wbs_l1','key':'{id}','val':'{cp_code} , {cp_name}'},
                    'team':{'cp_code':{'val':'{cp_code}','title':'کد پروژه'},'cp_name':{'val':'{cp_name}','title':'نام پروژه'},
                            'wbs_l1_name':{'val':'{wbs_l1_name}','title':'دسته موضوع اقدام'},'wbs_l1_code':{'val':'{wbs_l1_code}','title':'کد دسته  موضوع اقدام'}
                            },},
                'wbs_l2_name':{'type':'text','title':'موضوع اقدام','len':'250',},
                'wbs_l2_code':{'type':'index','len':'1','title':'کد موضوع اقدام','start':1,'ref':{'db':'a_cur_subject','tb':'wbs_l2','key':'{id}','val':'{wbs_l2_code}','where':'''f2f_id = "{{=__objs__['f2f_id']['value']}}"'''},},
                'des':{'type':'text','len':'250','title':'توضیحات'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,cp_code,cp_name,wbs_l2_name,wbs_l2_code,des','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            
        },
    },
    
    #-------------------------------------------------------------------- prj
    'a_prj':{ #db
        'a':{
            'base':{'mode':'form','title':'کد پروژه','code':'101'},
            'tasks':{
                'code':{'type':'text','title':'کد پروژه','len':'4','uniq':''},
                'name':{'type':'text','title':'نام پروژه','len':'140','lang':'fa'},
                'per':{'type':'reference','width':'5','title':' نماینده پروژه','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{m_w} {pre_n} {name} {family}'},'prop':[]},
                'cnt_name':{'type':'text','title':'نام قراردادی پروژه','title_e':'contracte name'},
                'cmn_name':{'type':'text','title':'نام رایج','title_e':'common name'},
                'date':{'type':'fdate','title':'تاریخ ثبت'},
                'code_hlp':{'type':'text','title':'راهنمای کد'},
                'client':{'type':'text','title':'کارفرما'},
                'client_mn':{'type':'text','title':'مدیر پروژه کارفرما'},
                'client_pr':{'type':'text','title':'کارشناسان کلیدی کارفرما '},
                'serv_type':{'type':'select','title':'نوع خدمات','select':{'D':'design-طراحی','S':'supervition-نظارت','-':'نا مشخص'},'prop':['multiple']},
                'prj_dur':{'type':'num','min':1,'max':1200,'len':'4','title':'مدت حدودی( ماه)'},
            },
            'steps':{
                'pre':{'tasks':'lable_1,name,per,date,code,code_hlp','xjobs':'dcc_prj','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'client,client_mn,serv_type','xjobs':'dcc_prj','title':'اطلاعات کلی','app_keys':'','app_titls':'','oncomplete_act':''},
                'sbt':{'tasks':'code','xjobs':'dccm','title':'ثبت نهایی','app_keys':'y,x,r','app_titls':'','oncomplete_act':''},
            },
            'views':{
            },
            'labels':{
                'lable_1':'همه فیلدهای فرم راتکمیل نمایید',
            },
            'cols_filter':
                {'':'همه',
                'code':'شماره',
                'code,name':'شماره و موضوع',
                },
            'data_filter':
                {'':'همه نامه ها',
                'code is Null':'نیاز به تعیین پروژه',
                'code = "36"':'پروژه پیوندراه',
                'prj = "29"':'پروژه گیتها',
                'prj = "29" AND x_des like "%L-%"':'-Lپروژه گیتها',
                'prj = "48"':'پروژه استاندارد سازی',
                'act_todo != ""':'دارای ارجاع',
                'x_act_todo != ""':'نیاز به اقدام',
                'act_pey != ""':'پی گیری',
                'lno like "%xxxx%"':'جستجوی نامه'},
            
        }
    },
    
    #-------------------------------------------------------------------- prj
    'a_sub_p':{ #db
        'a':{
            'base':{'mode':'form','title':'کد زیر پروژه','code':'102'
            },
            'tasks':{
                #'prj_id':{'type':'reference','width':'5','title':'آیدی پروژه','ref':{'db':'a_prj','tb':'a','key':'{id}','val':'{code}-{name}'},'prop':['update']},
                #'prj':{'type':'auto','ref':{'db':'a_prj','tb':'a','key':'__0__','val':'{code}','where':'''id = "{prj_id}"'''},'title':' پروژه'},
                'prj_id':{'type':'reference','title':'پروژه',
                    'ref':{'db':'a_prj','tb':'a','key':'{id}','val':'{code}-{name}'},'prop':['update'],
                    'team':{'prj':{'val':'{code}','title':'کد پروژه'},'prj_name':{'val':'{name}','title':'نام پروژه'}},},
                'code':{'type':'text','title':'کد زیر پروژه','len':'3','uniq':"prj=`{{=__objs__['prj']['value']}}`"},
                'name':{'type':'text','len':'160','title':'نام زیر پروژه'},
                'code2':{'type':'auto','len':'8','auto':'{{=prj[:4].upper()}}-{code}','title':'کد کامل زیر پروژه'},
                'name2':{'type':'auto','len':'256','auto':"{{=__objs__['prj_id']['output_text'][5:].strip()}}-{name}",'title':'نام کامل زیر پروژه'},
                'des':{'type':'text','len':'250','title':'توضیح زیر پروژه'},
                'date':{'type':'fdate','title':'تاریخ ثبت'},
                'auth_users':{'type':'reference','width':'20','title':' افراد دارای حق دسترسی','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{m_w} {pre_n} {name} {family}'},'prop':['multiple']},
                'cat_1':{'type':'text','title':'موارد جاری'},
                'cat_2':{'type':'text','title':'دسته 2'},
                
            },
            'steps':{
                'pre':{'tasks':'prj_id,prj,prj_name,name,code','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'code2,name2,des,date','xjobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
                'set_auth':{'tasks':'auth_users,prj_id','xjobs':'dccm','title':'دسترسی','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'all':{'input':'prj,code,name,des,cat_1,cat_2','view1':'','view2':'des'},
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'a_step':{ #db
        'a':{
            'base':{'mode':'form','title':'کد مرحله','code':'103'},
            'tasks':{
                #'prj':{'type':'reference','width':'5','title':' پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                #'prj_id':{'type':'auto','ref':{'db':'a_prj','tb':'a','key':'__0__','val':'{id}','where':'''code = "{prj}"'''},'title':'آیدی پروژه'},
                'prj_id':{'type':'reference','title':'پروژه',
                    'ref':{'db':'a_prj','tb':'a','key':'{id}','val':'{code}-{name}'},'prop':['update'],
                    'team':{'prj':{'val':'{code}','title':'کد پروژه'},'prj_name':{'val':'{name}','title':'نام پروژه'}},},
                'sub_p':{'type':'reference','width':'5','title':' زیر پروژه','ref':{'db':'a_sub_p','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}"'''},'prop':[]},
                'code':{'type':'text','title':'کد مرحله','len':'2'},
                'name':{'type':'text','title':'نام مرحله'},
                'date':{'type':'fdate','title':'تاریخ ثبت'},
            },
            'steps':{
                'pre':{'tasks':'prj_id,prj,prj_name,sub_p','xjobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'date,code,name','xjobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'a_dspln':{ #db
        'a':{
            'base':{'mode':'form','title':'کد دیسیپلین','code':'104'},
            'tasks':{
                'code':{'type':'text','title':'کد','len':'2','uniq':''},
                'name_e':{'type':'text','title':'DECIPLINE NAME'},
                'name':{'type':'text','title':'نام دیسیپلین'},
                'n':{'type':'text','title':'ترتیب'},
                'des':{'type':'text','title':'توضیح'},
            },
            'steps':{
                'pre':{'tasks':'code,name_e,name','xjobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'n,des','xjobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'code,name_e,name','view1':'','view2':''}
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'a_clint':{ #db
        'a':{
            'base':{'mode':'form','title':'لیست کارفرمایان','code':'104'},
            'tasks':{
                'name':{'type':'text','title':'نام کارفرما'},
                'des':{'type':'text','title':'توضیح'},
            },
            'steps':{
                'pre':{'tasks':'name','xjobs':'dcc_prj','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'des','xjobs':'dcc_prj','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'name','view1':'','view2':''}
            },
        },
        'Competitors':{
            'base':{'mode':'form','title':'لیست رقبا','code':'104','rev':'00-040515'},
            'tasks':{
                'name':{'type':'text','title':'نام شرکت رقیب'},
                'szmn':{'type':'reference','title':'سازمان','prop':['update'],
                        'ref':{'db':'a_clint','tb':'a','key':'{id}','val':'{id:03d},{name}'},
                        'team':{'szmn_name':{'val':'{name}','title':'نام سازمان'}},},
                'com':{'type':'text','title':'کانال ارتباطی'},
                'subj':{'type':'text','title':'نوع فعالیت'},
                'des':{'type':'text','title':'توضیح'},
            },
            'steps':{
                's0':{'tasks':'name,szmn,szmn_name','xjobs':'dcc_prj','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'com,subj','xjobs':'dcc_prj','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'des','xjobs':'dcc_prj','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'name','view1':'','view2':''}
            },
        },
        'persona':{ 
            'base':{'mode':'form','title':'پرسونای شخصی کارفرمایان','code':'108','rev':'00-040513',
            },
            'tasks':{
                #'un':{'type':'text','title':'نام کاربری','len':'3','uniq':''},
                'm_w':{'type':'select','select':['آقای','خانم'],'title':'جنسیت'},
                'pre_n':{'type':'select','select':['','مهندس','دکتر'],'title':'پیش نام'},
                'name':{'type':'text','title':'نام','len':'15'},
                'family':{'type':'text','title':'فامیل','len':'35'},
                'rsm':{'type':'text','title':'نام رسمی سازمانی'},
                'szmn':{'type':'reference','title':'سازمان','prop':['update'],
                        'ref':{'db':'a_clint','tb':'a','key':'{id}','val':'{id:03d},{name}'},
                        'team':{'szmn_name':{'val':'{name}','title':'نام سازمان'}},},
                'pos':{'type':'text','title':'سمت رسمی سازمانی'},
                'date':{'type':'fdate','len':'10','title':'تاریخ شروع سمت','prop':[]},
                'rsm_t':{'type':'auto','len':'50','auto':"{rsm} - {pos} {szmn_name}",'title':'عنوان رسمی کامل'},
                'dcst':{'type':'select','title':'روش تصمیم‌گیری','help_e':'Decision Style','prop':['update'],
                    'select':{'QIND':'سریع و فردی (Quick Individual) - تصمیم‌گیری سریع توسط فرد، بدون مشورت گسترده، اغلب بر اساس اعتماد به تجربه شخصی یا مشاور.',
                        'COLL':'جمعی / خانوادگی (Collective/Family-based) - تصمیم‌گیری با مشارکت اعضای خانواده یا گروه نزدیک؛ نیازمند هماهنگی نظرات مختلف.',
                        'RSCH':'تحقیق‌محور و محتاط (Research-based) - تصمیم‌گیری پس از بررسی عمیق اطلاعات، تحلیل ریسک و مقایسه چند گزینه.',
                        'STEP':'مرحله‌ای (Stepwise) - تصمیم‌گیری تدریجی، هر مرحله پس از مشاهده و ارزیابی نتایج مرحله قبلی انجام می‌شود.',
                        'CONS':'مشورت‌محور (Consultative) - تصمیم‌گیری بر اساس مشاوره با متخصصان، مشاوران فنی یا دوستان باتجربه پیش از هر اقدام.',
                        'EMOT':'احساسی و شهودی (Emotional/Intuitive) - تصمیم‌گیری سریع و مبتنی بر حس و شهود شخصی، بیشتر از تحلیل منطقی متأثر از احساسات و ترجیحات شخصی.',
                        'OPPO':'فرصت‌محور (Opportunistic) - صمیم‌گیری بر اساس استفاده از فرصت‌های پیش‌بینی‌نشده (مثل تخفیف، موقعیت خاص زمین یا سرمایه).',
                        'FINC':'اولویت‌محور مالی (Financial-priority) - تمرکز اصلی بر بودجه و مسائل مالی؛ تصمیم‌ها بر اساس کمترین هزینه یا بیشترین بازده مالی اتخاذ می‌شود.',
                        'CNSV':'محافظه‌کارانه (Conservative) - تمایل به انتخاب راه‌حل‌های آزموده‌شده، کم‌ریسک و پایبند به عرف و استانداردهای سنتی.',
                        'HYBR':'هیبرید (Hybrid) - ترکیبی از چند سبک (مثلاً شروع با تحقیق و سپس تصمیم جمعی یا احساسی)؛ انعطاف‌پذیر نسبت به شرایط پروژه.'
                    }},
                'dcst_t':{'type':'auto-x','ref':'dcst','title':'روش تصمیم‌گیری - متن','prop':['hidden']},
                'dtl':{'type':'select','title':'میزان دخالت در جزئیات طراحی','help_e':'Detail Involvement','prop':['update'],
                    'select':{'DETL':'جزئی‌نگر (Detail-oriented) -  علاقه‌مند به بررسی و تایید تمام جزئیات نقشه‌ها، متریال‌ها و مراحل طراحی و اجرا؛ تمایل به کنترل نزدیک روی روند کار.',
                            'BIGP':'کلی‌نگر (Big-picture) - تمرکز بر تصویر کلی و نتیجه نهایی پروژه؛ علاقه‌مند به دیدن کانسپت و ایده کلی به جای جزئیات فنی.',
                            'HNDW':'اعتماد کامل به مشاور (Hands-off) - واگذاری کامل تصمیمات به تیم مشاور؛ انتظار خروجی بدون دخالت مستقیم و صرفاً دریافت گزارش‌های دوره‌ای.',
                            'BALA':'متعادل (Balanced) - پیگیری جزئیات مهم اما واگذاری تصمیم‌های کم‌اهمیت به مشاور؛ تعادل بین کنترل و اعتماد.',
                            'ITRV':'بازنگر مکرر (Iterative Reviewer) - علاقه‌مند به بررسی طرح در هر مرحله و ارائه بازخورد مستمر برای اصلاحات جزئی و مرحله‌ای.'
                    }},
                'dtl_t':{'type':'auto-x','ref':'dtl','title':'میزان دخالت در جزئیات طراحی - متن','prop':['hidden']},
                'com':{'type':'select','title':'سبک ارتباطی ترجیحی','help_e':'Communication Preferencet','prop':['update'],
                    'select':{'FORM':'رسمی و مکتوب (Formal & Written) - ترجیح به نامه‌نگاری، ایمیل و گزارش‌های رسمی؛ تأکید بر مستندسازی و روند اداری مشخص.',
                            'INFR':'غیررسمی و مستقیم (Informal & Direct) - تمایل به تماس تلفنی یا پیام‌رسان برای پاسخ سریع؛ تمرکز بر سادگی و سرعت ارتباط.',
                            'FACE':'حضوری و تعاملی (Face-to-Face Interactive) - علاقه‌مند به جلسات حضوری، بازدید از پروژه و تعامل چهره‌به‌چهره با تیم طراحی و اجرا.',
                            'DGVL':'دیجیتال و تصویری (Digital & Visual) - ترجیح به استفاده از داشبورد آنلاین، رندر سه‌بعدی و گزارش‌های تصویری برای درک پروژه.',
                            'HYBR':'ترکیبی و منعطف (Hybrid & Flexible) - استفاده از ترکیب چند روش ارتباطی بسته به موقعیت (مثلاً جلسات حضوری برای تصمیمات مهم و پیام‌رسان برای هماهنگی روزمره).',
                            'EXPR':'نمایشی و تجربه‌محور (Experiential/Showcase) - علاقه به دیدن ماکت، نمونه واقعی یا بازدید پروژه‌های مشابه به جای گزارش‌های صرفاً نوشتاری یا تصویری.'                 
                    }},
                'com_t':{'type':'auto-x','ref':'com','title':'سبک ارتباطی ترجیحی - متن','prop':['hidden']},
                'ccm':{'type':'select','title':'روش ارتباط  فعلی','help_e':'Current Communication Method','prop':['update'],
                    'select':{'AUTO':'اتوماسیون (Automation System) - سامانه اتوماسیون اداری',
                            'EMAL':'ایمیل (Email) - طریق پست الکترونیک رسمی یا شخصی',
                            'EITA':'ایتا (Eitaa) - پیام‌رسان ایتا',
                            'PHYS':'فیزیکی (Physical) - مکاتبات کاغذی یا تحویل فیزیکی اسناد'
                    }},  
                'ccm_t':{'type':'auto-x','ref':'ccm','title':'روش ارتباط  فعلی - متن','prop':['hidden']},
                'el':{'type':'select','title':'سطح مشارکت در فرآیند','help_e':'Engagement Level','prop':['update'],
                    'select':{'HIGH':'فعال (High Engagement) - مشارکت بسیار بالا در فرآیند؛ حضور در اکثر جلسات، بررسی مستمر جزئیات و پیگیری پیشرفت پروژه به صورت مداوم.',
                            'MODR':'متوسط (Moderate Engagement) - مشارکت در تصمیم‌های کلیدی و جلسات مهم؛ واگذاری جزئیات اجرایی به مشاور ولی پیگیری دوره‌ای روند پروژه.',
                            'LOWE':'کم (Low Engagement) - مشارکت حداقلی؛ کارفرما فقط گزارش‌های دوره‌ای دریافت می‌کند و تصمیم‌های عمده را به تیم مشاور واگذار می‌کند.',
                            'ONDE':'مرحله‌ای (On-Demand) - مشارکت مقطعی در نقاط عطف پروژه؛ ورود فقط هنگام نیاز به تصمیم‌های خاص یا تأیید بخش‌های کلیدی.',
                            'CONS':'مشورتی (Consultative Engagement) - مشارکت از طریق ارائه بازخورد در جلسات مشاوره؛ بدون حضور مستقیم در مراحل روزمره اما مؤثر در تصمیمات نهایی.'
                    }},
                'el_t':{'type':'auto-x','ref':'el','title':'سطح مشارکت در فرآیند - متن','prop':['hidden'],},
                'ira':{'type':'select','title':'نگرش نسبت به نوآوری و ریسک','help_e':'Innovation & Risk Attitude','prop':['update'],
                    'select':{'INRV':' نوآور و ریسک‌پذیر (Innovative & Risk-taking) - مشتاق ایده‌های جدید، پذیرش متریال مدرن و طراحی‌های غیرمتعارف حتی با ریسک بالا.',
                        'BALA':' میانه‌رو (Balanced) -  پذیرش نوآوری در صورت وجود توجیه فنی و اقتصادی؛ مایل به تعادل بین ریسک و امنیت.',
                        'CNSV':'محافظه‌کار (Conservative) - تمایل به استفاده از روش‌ها و طرح‌های سنتی و آزموده‌شده؛ پرهیز از ریسک بالا.',
                        'OPRT':'فرصت‌محور (Opportunistic) - پذیرش نوآوری در شرایطی که منافع کوتاه‌مدت یا موقعیت ویژه‌ای ایجاد شود (مثل تخفیف یا مزیت رقابتی خاص).',
                        'PRAG':'عمل‌گرا و نتیجه‌محور (Pragmatic) - پذیرش نوآوری صرفاً در صورت بهبود مستقیم عملکرد یا نتایج ملموس پروژه.',
                        'EXPL':'جستجوگر و آزمایشی (Exploratory) - علاقه‌مند به آزمایش ایده‌های جدید و پیشرو بودن در تجربه متدهای نوین، حتی بدون تضمین نتیجه.',
                    }},
                'ira_t':{'type':'auto-x','ref':'ira','title':'نگرش نسبت به نوآوری و ریسک - متن','prop':['hidden'],},
                'cip':{'type':'select','title':'اولویت‌های تعامل با مشاور','help_e':'Consultant Interaction Priorities','prop':['update'],
                    'select':{'RESP':' سرعت پاسخ‌دهی (Response Speed) -  تمایل به دریافت پاسخ فوری به سوالات، درخواست‌ها و تغییرات پروژه. ',
                            'TRAN':' شفافیت فرآیند (Transparency) - نیاز به گزارش شفاف از وضعیت پروژه، هزینه‌ها، زمان‌بندی و تصمیمات کلیدی.',
                            'CRTV':' خلاقیت و ایده‌های نو (Creativity & Innovation) - انتظار ارائه پیشنهادهای نوآورانه و متمایز در طراحی و راهکارهای پروژه.',
                            'COST':'هزینه و کنترل بودجه (Cost & Budget Control) - تمرکز بر مدیریت مالی، صرفه‌جویی و پایبندی به بودجه توافق‌شده.',
                            'QUAL':'کیفیت خروجی (Quality Focus) -  تمرکز بر دستیابی به بالاترین کیفیت طراحی و اجرا حتی با هزینه بالاتر.',
                            'TIME':'تعهد و پایبندی به زمان (Time Commitment) - اولویت‌بخشی به تحویل به‌موقع مراحل پروژه و رعایت دقیق برنامه زمان‌بندی.',
                            'SUPP':'پشتیبانی و خدمات پس از تحویل (Post-Delivery Support) - اهمیت وجود پشتیبانی فنی و خدمات مشاوره‌ای حتی پس از تحویل پروژه.',
                            'CONT':'ارتباط مستمر و در دسترس بودن (Availability & Contact) - نیاز به امکان ارتباط مداوم و آسان با مشاور در طول پروژه.',
                            'CULT':'هماهنگی با ارزش‌ها و فرهنگ مشتری (Cultural Fit) - اطمینان از اینکه مشاور ارزش‌ها، فرهنگ و اولویت‌های شخصی یا خانوادگی را در طراحی رعایت کند.',
                            'FLEX':'انعطاف‌پذیری و سازگاری (Flexibility) -  تمایل به همکاری با مشاوری که توانایی تطبیق با تغییرات نیازها و شرایط پروژه را داشته باشد.'
                    }},
                'cip_t':{'type':'auto-x','ref':'cip','title':'اولویت‌های تعامل با مشاور - متن','prop':['hidden'],},
                'des_1':{'type':'text','len':1500,'lang':'fa','title':'توضیحات اضافه'},  

            },
            'steps':{
                's0':{'tasks':'m_w,pre_n,name,family,rsm,szmn,szmn_name,pos,rsm_t,date','xjobs':'dcc_prj','title':'ثبت','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'dcst,dtl,com,ccm,el,ira,cip,dcst_t,dtl_t,com_t,ccm_t,el_t,ira_t,cip_t,des_1','xjobs':'dcc_prj','title':'تایید مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
                's2':{'tasks':'des_1','xjobs':'dccm','title':'تایید مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
            },
            'views':{
                'all':{'input':'m_w,pre_n,name,family,rsm,szmn,pos,date','view1':'dcst','view2':'dtl'}
            },
            'cols_filter':{
                '':'همه',
            },
            'data_filter': 
                {
                },
        }
    },
    
    #--------------------------------------------------------------------
    #'eng'
    #--------------------------------------------------------------------
    'a_doc':{ #db
        'a':{
            'base':{'mode':'form','title':'کد نوع مدرک','code':'105'},
            'tasks':{
                'dspln':{'type':'reference','width':'5','title':' دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':[]},
                'doc_cat_id':{'type':'reference','title':'دسته','prop':['update'],
                            'ref':{'db':'a_doc_cat','tb':'a','key':'{id}','val':'{id:03d},{code},{name}'},
                            'team':{'doc_cat_cd':{'val':'{code}'},'doc_cat_nm':{'val':'{name}'}},},
                'code':{'type':'text','title':'کد مدرک','len':'2'},
                'name':{'type':'text','title':'نام مدرک'},
                'name_e':{'type':'text','title':'doc name'},
                'code3':{'type':'text','title':'کد مدرک - 3 حرفی','len':'3'},
                'des':{'type':'text','title':'توضیح'},
                
            },
            'steps':{
                'pre':{'tasks':'dspln,code,lable_1','xjobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'name,name_e,code3,des,doc_cat_id,doc_cat_nm,doc_cat_cd','xjobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'labels':{
                'lable_1':'فرم را تکمیل کنید',
            },
            'views':{
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'a_doc_cat':{ #db
        'a':{
            'base':{'mode':'form','title':'دسته بندی مدارک','code':'106','rev':'00-040617'},
            'tasks':{
                'code':{'type':'text','title':'کد دسته'},
                'name':{'type':'text','title':'عنوان دسته'},
                'name_e':{'type':'text','title':'cat name'},
                'des':{'type':'text','title':'توضیح'},
                
            },
            'steps':{
                '0':{'tasks':'code,name','xjobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                '1':{'tasks':'des,name_e','xjobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
        }
    },
    #--------------------------------------------------------------------
    'a_contact_grup':{ #db
        'a':{
            'base':{'mode':'form','title':'گروه مقابل مکاتبه','code':'103'},
            'tasks':{
                #'prj':{'type':'reference','width':'5','title':' پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                #'prj_id':{'type':'auto','ref':{'db':'a_prj','tb':'a','key':'__0__','val':'{id}','where':'''code = "{prj}"'''},'title':'آیدی پروژه'},
                'prj_id':{'type':'reference','title':'پروژه',
                    'ref':{'db':'a_prj','tb':'a','key':'{id}','val':'{code}-{name}'},'prop':['update'],
                    'team':{'prj':{'val':'{code}','title':'کد پروژه'},'prj_name':{'val':'{name}','title':'نام پروژه'}},},
                'sub_p':{'type':'reference','width':'5','title':' زیر پروژه','ref':{'db':'a_sub_p','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}"'''},'prop':['update']},
                'grup_code':{'type':'text','title':'کد گروه','len':'4','uniq':"prj=`{{=__objs__['prj']['value']}}`,sub_p=`{{=__objs__['sub_p']['value']}}`"},
                'grup_name':{'type':'text','title':'نام گروه'},
            },
            'steps':{
                'pre':{'tasks':'prj_id,prj,prj_name,sub_p,grup_code,grup_name','xjobs':'dccm','title':'تعریف اولیه','app_keys':'y','app_titls':'','oncomplete_act':''},
            },
            'views':{
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'a_loc':{ #db
        'a':{
            'base':{'mode':'form','title':'نام و آدرس دفاتر شرکت','code':'106'
            },
            'tasks':{
                'name':{'type':'text','title':'نام دفتر'},
                'code':{'type':'index','len':'3','title':'کد دفتر','ref':{'db':'a_loc','tb':'a','key':'{id}','val':'{code}','where':''},'uniq':''},
                'addres':{'type':'text','title':'آدرس دفتر'},
                'mdr':{'type':'user','title':'مدیر دفتر','prop':['show_full']},
                'date_s':{'type':'fdate','title':'تاریخ شروع بهره برداری'},
                'date_e':{'type':'fdate','title':'تاریخ خاتمه بهره برداری'},
            },
            'steps':{
                'pre':{'tasks':'name,code,addres,mdr','xjobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'date_s','xjobs':'dccm','title':'تکمیل','app_keys':'','app_titls':'','oncomplete_act':''},
                'st2':{'tasks':'date_e','xjobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #-----------------------------------------------------------------------
    'paper':{ #db
        #from paper='cdate','sbj','comment','attach','lv_archiv','lv_per_archiv','lv_onvan','io_t','paper_num','num_x','num_link','folder'
        # 'base':{'mode':'form','title':'نامه ها','auth':'dccm,ppr_vue','code':'901','auth_prj':'prj1','multi_app':{'0':['ks'],'1':['ks']},
        
        'a':{
            'base':{'mode':'form','title':'نامه ها','auth':'dccm,ppr_vue','code':'401','auth_prj':'#cp_code NOT LIKE "AQRC%"','multi_app':{'0':['ks'],'1':['ks']},
            },
            'tasks':{
                'prj_id':{'type':'reference','width':'30','ref':{'db':'a_sub_p','tb':'a','key':'{id}','val':'{id:03d}-{code2}-{name2}'},'title':'پروژه','prop':['update']},
                'prj1':{'type':'auto','ref':{'db':'a_sub_p','tb':'a','key':'__0__','val':'{prj}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'کد پروژه'},
                'prj2':{'type':'auto','ref':{'db':'a_sub_p','tb':'a','key':'__0__','val':'{code2}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'کد کامل زیر پروژه'},
                'cprj_id':{'type':'reference','len':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d},{cp_code},{cp_name}'},'title':'پروژه جاری','prop':['update']},
                'cp_code':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_code}','where':'''id = "{{=__objs__['cprj_id']['value']}}"'''},'title':'کد پروژه جاری '},
                'cp_name':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_name}','where':'''id = "{{=__objs__['cprj_id']['value']}}"'''},'title':'نام پروژه جاری'},
                'man_crt':{'type':'reference','width':'5','title':'تهیه کننده','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{family}'},'prop':['readonly']},#,'prop':['readonly']
                'man_ar_mng':{'type':'reference','width':'5','title':'مسئول طرح معماری','ref':{'db':'user','tb':'user','key':'{id}','val':'{un}-{family}'}},#,'prop':['readonly']
                
                
                'lno':{'type':'text','width':'10','title':'شماره نامه','link':{'url':['spks','km','set_ppr'],'args':[],'vars':{'lno':'{lno}'},'reset':False},'prop':['readonly']},
                'lno_p':{'type':'num','width':'10','title':'شماره پیشنویس','prop':[]},
                
                'date_s':{'type':'fdate','width':'10','title':'تاریخ اولین ارجاع','prop':[]},
                'date_e':{'type':'fdate','width':'10','title':'تاریخ آخرین ارجاع','prop':['readonly']},
                
                
                'cdate':{'type':'fdate','width':'10','title':'تاریخ ثبت','prop':['readonly']},#'prop':['hide']
                'sbj':{'type':'text','width':'50','title':'موضوع نامه','prop':['readonly']},
                'comment':{'type':'text','width':'30','title':'خلاصه','prop':['readonly']},
                'attach':{'type':'text','width':'10','title':'ضمایم','prop':['hide']},
                'io_t':{'type':'text','width':'5','title':'نوع','prop':['readonly']},
                'lv_archiv':{'type':'text','width':'50','title':'کلاس آرشیو','prop':['readonly']},
                'lv_per_archiv':{'type':'text','width':'50','title':'آرشیو شخصی','prop':['readonly']},
                'lv_onvan':{'type':'text','width':'250','title':'به- عنوان','prop':['readonly']},
                'paper_num':{'type':'text','width':'6','title':'شماره کوچک','prop':[]},
                'num_x':{'type':'text','width':'10','title':'num_x','prop':[]},
                'num_link':{'type':'text','width':'10','title':'num_link','prop':[]},
                'folder':{'type':'text','width':'20','title':'محل فایلها','link':{'url':['spks','file','f_list_sd'],'args':['pp','{folder}'],'vars':{}},'prop':[],'reset':False},#'hide']},
                'pr_err':{'type':'text','width':'250','title':'خطا','prop':[],'help':'خطا در دریافت خودکار اطلاعات نامه توسط playwright'},
                
                'outbox':{'type':'text','width':'5','title':'ارسالی','prop':['readonly']},
                'x_des':{'type':'text','width':'30','title':'مفهوم*','title_add':'توضیح دستی'},#,'prop':['readonly']
                'x_num':{'type':'text','width':'30','title':'کد*','title_add':'جهت انتخاب و یا مرتب سازی راحتتر نامه ها و موضوعات خاص'},#,'prop':['readonly']
                'x_inf':{'type':'text','width':'30','title':'اطلاعات*','title_add':'اطلاعات اضافی'},
                'x_to_grup':{'type':'reference','width':'5','title':'گروه گیرنده*','ref':{'db':'a_contact_grup','tb':'a','key':'{grup_code}','val':'{grup_name}',
                     'where':'''prj = "{prj1}" and sub_p = "{{=prj2[-3:] if prj2 and len(prj2)>3 else ''}}"'''},'prop':['readonly']},#,'prop':['readonly']
                #    'where':'''prj = "{{=__objs__['prj1']['value']}}" and sub_p = "{{=__objs__['prj2']['value'][-3:]}}"'''},'prop':['readonly']},#,'prop':['readonly']
                
                
                'act_todo':{'type':'text','width':'150','title':'ارجاع نامه','prop':[]},
                'x_act_todo':{'type':'text','width':'150','title':'اقدامات لازم*','prop':[]},
                'x_act_rec':{'type':'text','width':'150','title':'اقدامات انجام شده*','prop':[]},
                'x_act_pey':{'type':'text','width':'150','title':'پیگیری*','prop':[]},      
                'x_act_type':{'type':'select','title':'نوع اقدام*','select':{'I':'INFO-اطلاع','D':'DO-اقدام','F':'FOLLOW UP-پیگیری','DF':'DO & FOLLOW UP-اقدام و پیگیری','OK':'ALL ACT DONE-اقدامات انجام شده'}},
                 #,'get_inf':{'type':'xlink','width':'20','title':'دانلود','link':{'pro':['ksw','aqc','import_paper_inf'],'args':['{lno}']},'prop':['hide']}                
            },
            'steps':{
                #lno,
                'pre':{'tasks':'cprj_id,cp_code,cp_name,prj_id,prj1,prj2','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'x_act_type,man_crt,x_num,x_des,x_inf,x_to_grup,x_act_rec,x_act_pey,x_act_todo,lable_1,act_todo,lable_2','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'x_act_type','xjobs':'dccm','title':'بررسی','app_keys':'','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'folder,lno,sbj,comment,io_t,attach,lv_onvan,lv_archiv,lv_per_archiv,paper_num,num_x,num_link,cdate,date_s,date_e','xjobs':'_auto_','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'all':{'input':'prj_id,man_crt,x_num,x_des,x_inf,x_to_grup,x_act_todo,x_act_rec,x_act_pey,act_todo','view1':'lno,lno_p,sbj,pr_err',
                    'view2':'comment,date_s,date_e,cdate,io_t,outbox,man_ar_mng,paper_num,num_x,num_link,attach,folder,lv_onvan,lv_archiv,lv_per_archiv'}
            },
            'labels':{
                'lable_1':'فیلد ارجاع نامه توسط نرم افزار اسکرپ اتوماسیون پر می شود در زمان بررسی هر نامه باید آنرا خالی کرد تا نشانه تکمیل اقدامات لازم باشد',
                'lable_2':' اگر فیلد ارجاع نامه  پر باشد  حتمی باید اقدام جدید را بررسی کرد - حتی اگر فیلد نوع اقدام نیاز به اقدامی را نشان ندهد ',
            },
            'cols_filter':
                {
                'prj2,cprj_id,lno,sbj,date_s,io_t,lv_onvan,lv_archiv,paper_num,folder,x_act_type,act_todo,x_act_todo,x_act_rec,x_act_pey,x_des':'بررسی 31',
                '':'همه',
                'lno':'شماره',
                'lno,sbj':'شماره و موضوع',
                'lno,sbj,date_s':'شماره، موضوع، تاریخ',
                'lno,sbj,date_s,io_t':'شماره، موضوع، تاریخ، نوع',
                'lno,sbj,date_s,io_t,folder':'شماره،موضوع،تاریخ،ص-و،فایلها', 
                'lno,sbj,date_s,io_t,x_num,x_des':'ش.م.ت.ن-دستی : شماره و شرح',
                'cprj_id,lno,sbj,date_s,io_t,x_num,x_des,act_todo,x_act_todo,x_act_rec,x_act_pey':'شماره،موضوع،تاریخ،ص-و،توضیح،اقدام (لازم،سابقه، پی گیری)',
                'folder,lno,sbj,date_s,comment,io_t,x_to_grup,act_todo,x_act_todo,x_act_rec,x_act_pey,x_act_type,x_inf,x_inf,x_des':'بررسی 1',
                'folder,lno,sbj,date_s,io_t,lv_onvan,lv_archiv,paper_num,num_x,num_link,cdate,attach,lv_per_archiv':'بررسی 2',
                'prj2,cprj_id,lno,sbj,date_s,io_t,lv_onvan,lv_archiv,paper_num,folder':'بررسی 3',
                
                
                'prj2,lno,sbj,date_s,io_t,lv_onvan,lv_archiv,paper_num,folder,pr_err':'بررسی 4',
                }, #table_view cols filter
                #cols_filter={'':'همه','lno,sbj':'2',}
            'data_filter':
                {'':'همه نامه ها',
                'prj_id = "112"':'پروژه صحن جامع',
                'cprj_id = "3"':'مدیریت سوابق',
                'cprj_id = "57"':'تیرپارک',
                'prj_id is Null':'نیاز به تعیین پروژه',
                'prj_id = "36"':'پروژه پیوندراه',
                'prj1 = "HRG1"':'پروژه گیتها',
                'prj_id = "29" AND x_des like "%L-%"':'-Lپروژه گیتها',
                'prj_id = "48"':'پروژه استاندارد سازی',
                
                'act_todo is Null':'دارای ارجاع',
                'x_act_todo is Null':'نیاز به اقدام',
                'act_pey is Null':'پی گیری',
                '(x_act_type = "D" OR x_act_type = "F" OR x_act_type = "DF")':'نیاز به پی گیری یا اقدام',
                'lno like "%xxxx%"':'جستجوی نامه'},
            'order':'date_s'    
                
        },#,
        'p':{
            'base':{'mode':'form','title':'نامه های پیش نویس','auth':'dccm','code':'9011'
            },
            'tasks':{
                'lno':{'type':'text','width':'10','title':'شماره نامه','link':{'url':['spks','km','set_ppr'],'args':[],'vars':{'lno':'{lno}'}},'prop':['readonly']},
                'lno_p':{'type':'num','width':'10','title':'شماره پیشنویس','prop':[]},
                
                'date_s':{'type':'fdate','width':'10','title':'تاریخ اولین ارجاع','prop':[]},
                'date_e':{'type':'fdate','width':'10','title':'تاریخ آخرین ارجاع','prop':['readonly']},
                'sbj':{'type':'text','width':'50','title':'موضوع نامه','prop':['readonly']},
                'comment':{'type':'text','width':'30','title':'خلاصه','prop':['readonly']},
                'attach':{'type':'text','width':'10','title':'ضمایم','prop':['hide']},
                'io_t':{'type':'text','width':'5','title':'نوع','prop':['readonly']},
            },
            'steps':{
                'pre':{'tasks':'lno','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'cols_filter':{},
            'data_filter':{}
        },#,
    },
    
    #--------------------------------------------------------------------
    'user':{ #db
        'user':{
            'base':{'mode':'form','title':'لیست همکاران','data_filter':'loc like "01%"','code':'201','cols_filter':'name,family,tel_wrk,loc,office,p_id,file_pic_per',
                },
            'tasks':{
                'un':{'type':'text','title':'نام کاربری','len':'3','uniq':''},
                'ps':{'type':'text','title':'پسورد','prop':['hide'],'len':'20','auth':'dcc_prj'},
                'm_w':{'type':'select','select':['آقای','خانم'],'title':'جنسیت'},
                'pre_n':{'type':'select','select':['','مهندس','دکتر'],'title':'پیش نام'},
                'name':{'type':'text','title':'نام','len':'15'},
                'family':{'type':'text','title':'فامیل','len':'35'},
                'a_name':{'type':'text','title':'نام در اتوماسیون','len':'70'},
                'eng':{'type':'reference','title':'رسته / دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{name}'}},
                #'tel_mob':{'type':'text','title':'موبایل','len':'13','placeholder':"0...-...-....",'data-slots':"."},#,'data-accept':"\d"
                #'tel_mob':{'type':'text','title':'موبایل','len':'13','placeholder':"0...-...-....",'pattern':"0[0-9]{{3}}-[0-9]{{3}}-[0-9]{{4}}"},
                
                #'tel_wrk':{'type':'text','title':'تلفن','len':'10','placeholder':"....-..-..",'data-slots':".",'data-accept':"\d"},
                'tel_wrk':{'type':'text','title':'تلفن داخلی','len':'10','placeholder':"....-..-..",'auth':'*'},
                'loc':{'type':'reference','title':'محل کار','ref':{'db':'a_loc','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['show_full']},
                'office':{'type':'select','select':['طراحی','نظارت','پشتیبانی','مدیریت'],'title':'بخش'},
                #'discipline':{'type':'text','title':'رسته'}
                
                'job':{'type':'text','title':'سمت','len':'50'},#,'ref':{'db':'user','tb':'job','key':'id','val':'{id}{name}'}
                'p_id':{'type':'num','len':4,'lang':'fa','title':'شماره پرسنلی','uniq':''},
                'end':{'type':'fdate','title':'تاریخ خاتمه کار','prop':['hazf']},
                'file_rqst':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}-09-rqst','file_ext':"pdf,jpg",'path':'form,hrm,cv,{un}','title':'فرم درخواست ثبت نام','auth':'dccm,#task#un,off_ens'},
                'file_pic_per':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}0-pic_per','file_ext':"jpg",'path':'form,hrm,cv,{un}','title':'عکس پرسنلی','img':"""style='height:100px;' """},
                'file_shnsnm':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}1-shnsnm','file_ext':"pdf",'path':'form,hrm,cv,{un}','title':'شناسنامه','auth':'dccm,#task#un,off_ens'},
                'file_mdrk_thsl':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}2-mdrk_thsl','file_ext':"pdf,jpg",'path':'form,hrm,cv,{un}','title':'آخرین مدرک تحصیلی','auth':'dccm,#task#un,off_ens'},
                'file_ot':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}3-ot','file_ext':"zip",'path':'form,hrm,cv,{un}','title':'سایر مدارک','auth':'dccm,#task#un,off_ens'},
                'file_off':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}4-off','file_ext':"pdf",'path':'form,hrm,cv,{un}','title':'مدارک اداری','auth':'dccm,#task#un,off_ens'},
                'login_ip':{'type':'text','title':'آی پی ورود ویژه','len':'3'},
                'auth_prj':{'type':'reference','title':'حق دسترسی به پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['multiple']},
                'auth_prj_id':{'type':'auto','ref':{'db':'a_prj','tb':'a','key':'__0__','val':'{id}','where':'''code = "{auth_prj}"'''},'title':'آیدی پروژه'},
                'file_access':{'type':'text','title':'فایل های قابل دسترس','len':'20'},
                
                'tel_mob':{'type':'text','title':'موبایل','len':'13','auth':'dccm,#task#un,off_ens'},
                'date':{'type':'fdate','title':'تاریخ تولد'},#old
                'rlgn':{'type':'text','title':'مذهب','len':'10'}, 
                'mltr':{'type':'select','select':['-','معاف','پایان خدمت'],'title':'نظام وظیفه','hlp':'militrian'},  
                'Idc_num':{'type':'text','title':' کد ملی','len':'10'},	
                'shnsnme_num':{'type':'text','title':'شماره شناسنامه','len':'10'}, 	
                'father': {'type':'text','title':'نام پدر','len':'15'},	
                'brt_pos': {'type':'text','title':'محل تولد','len':'15'},	 
                'mrg_case':{'type':'select','select':['متاهل','مجرد'],'title':'وضعیت تاهل'},  
                'mrg_date':{'type':'fdate','title':'تاریخ ازدواج ','value':'0000/00/00','prop':['textchange']}, 
                'n_suprt':{'type':'num','min':0,'max':10,'title':'تعداد افراد تحت تکفل'}, 
                'n_child':{'type':'num','min':0,'max':6,'title':'تعداد فرزندان'}, 
                'edu_l_cert_grade':{'type':'select','select':['-','دیپلم','کاردانی','کارشناسی','کارشناسی ارشد','دکتری'],'title':'آخرین مقطع تحصیلی'},  
                'edu_l_cert_date':{'type':'fdate','title':'تاریخ اخذ مدارک تحصیلی'}, 
                'edu_l_cert_pos': {'type':'text','title':'محل تحصیل','len':'15'}, 
                'edu_l_cert_univ': {'type':'text','title':'دانشگاه','len':'15'},  
                'edu_l_cert_dcpln': {'type':'text','title':'رشته تحصیلی','len':'15'},	
                'start_date': {'type':'fdate','title':'تاریخ استخدام'},	
                'file_cv': {'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}5-cv','file_ext':"pdf",'path':'form,hrm,cv,{un}','title':'رزومه','auth':'dccm,#task#un'},
                'file_ins_rec':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}6-ins-rec','file_ext':"pdf",'path':'form,hrm,cv,{un}','title':' سنوات بیمه بیرون از آستان قدس','auth':'dccm,#task#un'},
                'home_adrs':{'type':'text','title':'آدرس محل سکونت','len':'50'}, 	
                'tel_home': {'type':'text','title':'موبایل','len':'13'},
                'mrf_name': {'type':'text','title':'معرف','len':'10'},	
                'idc_p1_file':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}7-idc-p1','file_ext':"jpg",'path':'form,hrm,cv,{un}','title':'عکس روی کار ملی','auth':'dccm,#task#un'}, 
                'idc_p2_file':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}8-idc-p2','file_ext':"jpg",'path':'form,hrm,cv,{un}','title':'عکس پشت کارت ملی','auth':'dccm,#task#un'}, 
                'idc_serial': {'type':'text','title':'شماره سریال پشت کارت ملی','len':'10'},	
                'job_rec':{'type':'f2f','len':'60','title':'سابقه سمتها','ref':{'tb':'job_rec','show_cols':['loc','office','job','date_st']},},
                },
            'steps':{
                '0':{'tasks':'m_w,pre_n,name,family,a_name,eng,office,job,un,loc,auth_prj,auth_prj_id','xjobs':'dccm,edu','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                '1':{'tasks':'file_ot,file_off','xjobs':'off_ens','title':'تکمیل','app_keys':'y,r','app_titls':'','oncomplete_act':'','auth':'dccm'},#'xjobs':'#task#un,dccm',
                '2':{'tasks':'p_id','xjobs':'off_ens,dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':'',
                        'start_step':'1','start_where':"'{step_1_ap}' == 'y'",'end_where':"False",'auth':'dccm,#task#un,off_ens',},
                'b':{'tasks':'Idc_num,tel_wrk,file_pic_per','xjobs':'edu','title':'ثبت توسط مسئول آموزش','app_keys':'y','app_titls':'','oncomplete_act':'',
                        'name':'b','auth':'dccm,#task#un,edu,off_ens','start_step':'0','start_where':"'{step_0_ap}' == 'y'",'end_where':"False"},
                'd':{'tasks':'file_pic_per,date,job_rec,Idc_num,p_id,tel_mob,tel_wrk,end,loc','xjobs':'dccm','title':'ثبت توسط مسئول dcc','app_keys':'y','app_titls':'','oncomplete_act':'',
                        'name':'d','start_step':'0','start_where':"'{step_0_ap}' == 'y'",'end_where':"False"},
                'c1':{'tasks':'tel_mob,date,rlgn,mltr,shnsnme_num,father,brt_pos,mrg_case,mrg_date,n_suprt,n_child,lable_1,edu_l_cert_grade,edu_l_cert_date,edu_l_cert_pos,edu_l_cert_univ,edu_l_cert_dcpln,start_date,home_adrs,tel_home,mrf_name',
                        'xjobs':'#task#un','title':'ثبت اطلاعات توسط فرد- بخش 1','app_keys':'y','app_titls':'','oncomplete_act':'',
                        'name':'c1','auth':'dccm,#task#un,off_ens','start_step':'','start_where':"True",'end_where':"'{step_c2_ap}' == 'y'"},
                'c2':{'tasks':'file_cv,file_mdrk_thsl,file_shnsnm,file_ins_rec,idc_p1_file,idc_p2_file,idc_serial',
                        'xjobs':'#task#un','title':'ثبت اطلاعات توسط فرد-بخش 2','app_keys':'y,r','app_titls':'','oncomplete_act':'',
                        'name':'c2','auth':'dccm,#task#un,off_ens','start_step':'c1','start_where':"'{step_c1_ap}' == 'y'",'end_where':"'{step_c3_ap}' == 'y'"},  
                'c3':{'tasks':'mrf_name',
                        'xjobs':'off_ens','title':'تایید اطلاعات ثبت شده','app_keys':'y,r','app_titls':'','oncomplete_act':'',
                        'name':'c3','auth':'dccm,#task#un,off_ens','start_step':'c2','start_where':"'{step_c2_ap}' == 'y'",'end_where':"False"},           
            },
            'labels':{
                'lable_1':'کلیه اطلاعات تحصیلی مربوط به آخرین مدرک تحصیلی می باشد',
            },
            'views':{
                'all':{'input':'pre_n,file_pic_per,file_shnsnm,file_mdrk_thsl,file_ot,file_off,auth_prj,auth_prj_id','view1':'un,name,family','view2':'p_id','auth':'dccm'},
                't1':{'input':'file_rqst','view1':'un,name,family','view2':'p_id','auth':'dccm'},
                },
            'cols_filter':{
                '':'همه',
                'name,family,tel_wrk':'تلفن داخلی',
                'name,family,tel_wrk,loc,office,p_id':'منتخب'
                },
            'data_filter':{
                '':'همه همکاران',
                'loc = "011"':'معاونت طراحی',
                'loc like "01%"':'همکاران دفتر مرکزی مشهد',
                'loc = "101"':'همکاران دفتر تهران',
                'loc = "102"':'همکاران دفتر حرم رضوی',
                },
        },
        'job_rec':{
            'base':{'mode':'form','title':'پرسنل - سابقه سمتها','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','len':'5','title':'فرم مبنا','ref':{'tb':'user','key':'{id}','val':'{un} , {name}{family}'},'prop':['readonly']},
                'loc':{'type':'reference','title':'محل کار','ref':{'db':'a_loc','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['show_full']},
                'office':{'type':'select','select':['طراحی','نظارت','پشتیبانی','مدیریت'],'title':'بخش'},         
                'job':{'type':'text','title':'سمت','len':'50'},
                'date_st':{'type':'fdate','title':'تاریخ شروع کار'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,loc,office,job,date_st','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            
        },
    },
    #--------------------------------------------------------------------
    'job':{ #db
        'a':{ 
            'base':{'mode':'form','title':'سمتها','help':'job list','code':'112'
            },
            'tasks':{
                'code':{'type':'text','title':'کد سمت','len':'10','uniq':''},
                'title':{'type':'text','title':'عنوان سمت','lang':'fa'},
                'users':{'type':'reference','title':'لیست همکاران مرتبط','ref':{'db':'user','tb':'user','key':'{un}','val':'{name}-{family}'},'prop':['multiple']},
                'base_user':{'type':'reference','title':'مسئول','ref':{'db':'user','tb':'user','key':'{un}','val':'{name}-{family}'}},
                'acts':{'type':'text','title':'شرح خدمات سمت','len':'256'},
            },
            'steps':{
                's0':{'tasks':'title,code,acts','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'users,base_user,acts','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{},
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}  
        }
    },
    #--------------------------------------------------------------------
    'act':{ #db
        'a':{ 
            'base':{'mode':'form','title':'لیست اقدام -  گزارش عملکرد','help':'act list of a person','code':'112'
            },
            'tasks':{
                'code':{'type':'text','title':'کد','len':'4','uniq':''},
                'title':{'type':'text','title':'عنوان','lang':'fa'},
                'name':{'type':'text','title':'name','lang':'fa'},
                'smpl':{'type':'text','title':'نمونه موارد زیر مجموعه','lang':'fa'},
            },
            'steps':{
                's0':{'tasks':'title,code','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'title,code,name,smpl','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{},
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}  
        }
    },
    #--------------------------------------------------------------------
    'doc_num':{ #db
        'a':{
            'base':{'mode':'form','title':'شماره گذاری مدارک','help':'document_numbering','code':'401','rev':'xx-040617'
            },
            'tasks':{
                'prj':{'type':'reference','width':'5','title':'پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'prj_id':{'type':'auto','ref':{'db':'a_prj','tb':'a','key':'__0__','val':'{id}','where':'''code = "{prj}"'''},'title':'آیدی پروژه'},
                'prj_name':{'type':'auto','len':'50','auto':"{{=__objs__['prj']['output_text'][5:]}}",'title':'نام پروژه'},
                'sub_p':{'type':'reference','width':'5','title':'زیر پروژه','ref':{'db':'a_sub_p','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{prj}"'''},'prop':['update']},
                'sub_p_name':{'type':'auto','len':'50','auto':"{{=__objs__['sub_p']['output_text'][4:]}}",'title':'نام زیر پروژه'},
                'doc_cat':{'type':'select','title':'دسته مدرک','select':{'OUT':'اسناد خروجی پروژه','PMO':'اسناد مدیریت پروژه'},'prop':['update','no_empty']},
                
                
                'step_x1':{'type':'select','title':'فاز','select':{'A':'Assessment - مطالعات ارزیابی و امکان سنجی','B':'Basic of Design - فاز  0 - مطالعات و شکل گیری مبانی و انگاره',
                    'C':'Concept Design - فاز 1 -  طراحی مبانی و کلیات ','D':'Detail Design - فاز 2 - طراحی جزئیات و اجزا مورد نیاز','E':'Execution process -فاز 3 - مرحله اجرا (نظارت و نظارت عالیه )'},'prop':['update']},
                'step_x2':{'type':'reference','title':'بازبینی','ref':{'db':'a_step','tb':'a','key':'{id}','val':'{code}-{name}','where':'''prj = "{prj}" AND sub_p =  "{sub_p}" '''},'prop':['update','no_empty'],'add_x':['len','مرحله جاری']}, 
                #AND code_x1 =  "{step_x1}"
                #'step_x2':{'type':'reference','title':'بازبینی','ref':{'db':'a_step','tb':'a','key':'{code_x2}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}" AND sub_p =  "{{=__objs__['sub_p']['value']}}" '''},'prop':['update','no_empty'],'add_x':['len','مرحله جاری']},
                # AND code_x1 =  "{{=__objs__['step_x1']['value']}}"
                'step':{'type':'auto','len':'50','auto':"{step_x1}{step_x2}",'title':'کد مرحله'},
                'dspln':{'type':'reference','width':'5','title':'دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'doc_t':{'type':'reference','width':'5','title':'نوع مدرک','ref':{'db':'a_doc','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'step_name':{'type':'auto','len':'50','auto':"{{=__objs__['step_x1']['output_text']}} - {{=__objs__['step_x2']['output_text']}}",'title':'نام مرحله'},
                
                'dspln_name':{'type':'auto','len':'50','auto':"{{=__objs__['dspln']['output_text'][3:]}}",'title':'نام دیسیپلین'},
                'doc_t_name':{'type':'auto','len':'50','auto':"{{=__objs__['doc_t']['output_text'][3:]}}",'title':'نام نوع مدرک'},
                
                'doc_p_code':{'type':'auto','len':'24','auto':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}','title':'پیش کد مدرک'},
                'doc_srl_code':{'type':'text','len':'4','lang':'en','title':'کد سریال مدرک','uniq':'doc_p_code=`{doc_p_code}`'},
                'doc_srl_name':{'type':'text','len':'250','title':'نام مدرک'},
                'doc_a_code':{'type':'auto','len':'50','auto':'{doc_p_code}-{doc_srl_code}','title':'کد کامل مدرک'},
                'doc_rec':{'type':'f2f','len':'60','title':'سوابق','ref':{'db':'doc_rec','tb':'a','show_cols':['rev','date','file_r']},
                    'var_set':{'prj':'prj','sub_p':'sub_p','step':'step','dspln':'dspln','doc_t':'doc_t','doc_srl_code':'doc_srl_code'}},
            },
            'steps':{
                '0':{'tasks':'prj,prj_id,prj_name,sub_p,sub_p_name,doc_cat','xjobs':'dccm','title':'ورود اطلاعات'},#
                '1':{'tasks':'step_x1,step_x2,step,step_name,dspln,dspln_name,doc_t,doc_t_name',
                    'cnd_flow':[{'OUT':'step_x1,step_x2,step,step_name,dspln,dspln_name,doc_t,doc_t_name',
                                'PMO':'step,step_name,dspln,dspln_name,doc_t,doc_t_name'
                                },'{doc_cat}'],
                    'xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                '2':{'tasks':'','xjobs':'dccm','title':'ورود اطلاعات'},
                '3':{'tasks':'doc_p_code,doc_srl_code','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                '4':{'tasks':'doc_srl_name,doc_a_code','xjobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''},
                '5':{'tasks':'doc_rec','xjobs':'dccm','title':'ط','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'cnd_flow':[{
                'OUT':{
                    'tasks':{
                        },
                    'steps':{
                        '1':{'tasks':'step_x1,step_x2,step,step_name,dspln,dspln_name,doc_t,doc_t_name'}
                        }
                },
                'PMO':{
                    'tasks':{
                        'step':{'auto':"_P"},
                        'step_name':{'auto':"PMO"},
                        },
                    'steps':{
                        '1':{'tasks':'step,step_name,dspln,dspln_name,doc_t,doc_t_name'}
                        }
                }
            },'{doc_cat}'],
                    
            
            'views':{
                'all':{'input':'prj,sub_p,step,dspln,doc_t,doc_srl_code,doc_srl_name','view1':'','view2':''},
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    'doc_num_1':{ #db
        'a':{
            'base':{'mode':'form','title':'شماره گذاری مدارک - فرم جدید','help':'document_numbering','code':'402','rev':'00-040617'
            },
            'tasks':{
                'c_prj_id':{'type':'reference','title':'پروژه','prop':['update'],
                            'ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d},{cp_code},{cp_name}'},
                            'team':{'c_prj_cd':{'val':'{cp_code}'},'c_prj_nm':{'val':'{cp_name}'}},},
                'doc_cat':{'type':'select','title':'دسته مدرک','select':{'OUT':'OUT - اسناد خروجی پروژه','PMO':'PMO - اسناد مدیریت پروژه'},'prop':['update','no_empty']},
                
                
                'step_x1':{'type':'select','title':'فاز','select':{'A':'Assessment - مطالعات ارزیابی و امکان سنجی','B':'Basic of Design - فاز  0 - مطالعات و شکل گیری مبانی و انگاره',
                    'C':'Concept Design - فاز 1 -  طراحی مبانی و کلیات ','D':'Detail Design - فاز 2 - طراحی جزئیات و اجزا مورد نیاز','E':'Execution process -فاز 3 - مرحله اجرا (نظارت و نظارت عالیه )'},'prop':['update']},
                'step_x2':{'type':'reference','title':'بازبینی','ref':{'db':'a_step','tb':'a','key':'{id}','val':'{code}-{name}','where':'''prj = "{prj}" AND sub_p =  "{sub_p}" '''},'prop':['update','no_empty'],'add_x':['len','مرحله جاری']}, 
                #AND code_x1 =  "{step_x1}"
                #'step_x2':{'type':'reference','title':'بازبینی','ref':{'db':'a_step','tb':'a','key':'{code_x2}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}" AND sub_p =  "{{=__objs__['sub_p']['value']}}" '''},'prop':['update','no_empty'],'add_x':['len','مرحله جاری']},
                # AND code_x1 =  "{{=__objs__['step_x1']['value']}}"
                'step':{'type':'auto','len':'50','auto':"{step_x1}{step_x2}",'title':'کد مرحله'},
                'step_name':{'type':'auto','len':'50','auto':"{{=__objs__['step_x1']['output_text']}} - {{=__objs__['step_x2']['output_text']}}",'title':'نام مرحله'},
                
                'dspln_id':{'type':'reference','width':'5','title':'دیسیپلین','prop':['update'],
                    'ref':{'db':'a_dspln','tb':'a','key':'{id}','val':'{id:03d}-{code}-{name}'},
                    'team':{'dspln_nm':{'val':'{name}'},'dspln_cd':{'val':'{code}'}},},
                'doc_t_id':{'type':'reference','width':'5','title':'نوع مدرک','prop':['update'],
                    'ref':{'db':'a_doc','tb':'a','key':'{id}','val':'{id:03d}-{code3}-{name}'},
                    'team':{'doc_t_nm':{'val':'{name}'},'doc_t_cd':{'val':'{code3}'}},},
                               
                'doc_p_code':{'type':'auto','len':'24','auto':'{c_prj_cd}-{step}-{dspln_cd}-{doc_t_cd}','title':'پیش کد مدرک'},
                'doc_srl_code':{'type':'text','len':'7','lang':'en','title':'کد سریال مدرک','uniq':'doc_p_code=`{doc_p_code}`'},
                'doc_srl_name':{'type':'text','len':'250','title':'نام مدرک'},
                'doc_a_code':{'type':'auto','len':'50','auto':'{doc_p_code}-{doc_srl_code}','title':'کد کامل مدرک'},
                'doc_rec':{'type':'f2f','len':'60','title':'سوابق','ref':{'db':'doc_rec_1','tb':'a','show_cols':['rev','date','file_r']},
                    'var_set':{'step':'step','dspln_id':'dspln_id','doc_t_id':'doc_t_id','doc_srl_code':'doc_srl_code'}},
            },#'prj':'prj','sub_p':'sub_p'
            'steps':{
                '0':{'tasks':'c_prj_id,c_prj_cd,c_prj_nm,doc_cat','xjobs':'dccm','title':'ورود اطلاعات'},#
                '1':{'tasks':'step_x1,step_x2,step,step_name,dspln_id,dspln_nm,dspln_cd,doc_t_id,doc_t_nm,doc_t_cd,doc_p_code,doc_srl_code,doc_srl_name,doc_a_code',
                    'xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                '2':{'tasks':'doc_p_code,doc_srl_code','xjobs':'dccm','title':'ورود اطلاعات'},
                '3':{'tasks':'doc_srl_name,doc_a_code','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                '4':{'tasks':'doc_rec','xjobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'cnd_flow':[{
                'OUT':{
                    'tasks':{
                        },
                    'steps':{
                        '1':{'tasks':'step_x1,step_x2,step,step_name,dspln_id,dspln_nm,dspln_cd,doc_t_id,doc_t_nm,doc_t_cd'}
                        }
                },
                'PMO':{
                    'tasks':{
                        'step':{'auto':"_P"},
                        'step_name':{'auto':"PMO"},
                        },
                    'steps':{
                        '1':{'tasks':'step,step_name,dspln_id,dspln_nm,dspln_cd,doc_t_id,doc_t_nm,doc_t_cd'}
                        }
                }
            },'{doc_cat}'],
                    
            
            'views':{
                'all':{'input':'prj,sub_p,step,dspln_id,dspln_nm,dspln_cd,doc_t_id,doc_t_nm,doc_t_cd,doc_srl_code,doc_srl_name','view1':'','view2':''},
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'dcc_cd':{ #db
        'a':{
            'base':{'mode':'form','title':'آرشیو دیسک نوری - CD','code':'402','rev':'01-040326',
            },
            'tasks':{
                'c_prj_id':{'type':'reference','len':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update','multiple']},
                'c_prj_txt':{'type':'auto-x','len':'30','ref':'c_prj_id'},
                'sbj':{'type':'text','len':'60','title':'موضوع'},
                'date':{'type':'fdate','width':'10','title':'تاریخ دریافت','prop':['update']},
                'un':{'type':'user','title':'مسئول هماهنگی'}, #cordinator
                'p_s2':{'type':'text','len':'150','title':'فرد مقابل'},
                'side2':{'type':'text','len':'150','title':'نام سازمان مقابل'},
                't_type':{'type':'select','title':'نوع تبادل','select':{'I':'Incoming-وارده','O':'Outgoing - صادره'},'prop':['update']},
                'p_post':{'type':'text','len':'150','title':'مسئول جابجایی'},
                'f_code':{'type':'auto','len':'8','auto':'aqrc-_cd-{{=str(id).zfill(3)}}','title':'کد فایل'},
                'file_pp1':{'type':'file','len':'40','file_name':'{{=f_code}}-ppr','file_ext':"pdf",'path':'form,doc_cd','title':'مکاتبه درخواست'},
                'file_pp2':{'type':'file','len':'40','file_name':'{{=f_code}}-ppr','file_ext':"pdf",'path':'form,doc_cd','title':'مکاتبه تحویل'},
                'file_cd':{'type':'file','len':'40','file_name':'{{=f_code}}-cd','file_ext':"zip,rar,7z,pdf,ppt,pptx,doc,docx,xls,xlsx,vldx",'path':'form,doc_cd','title':'فایل CD'},
            },
            'steps':{
                'pre':{'tasks':'c_prj_id,c_prj_txt,date','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'un,p_s2,side2,t_type,p_post,f_code,sbj,file_cd','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'file_pp1,file_pp2,sbj,p_s2,side2,p_post','xjobs':'#task#un','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'c_prj_id,c_prj_txt,sbj,date','view1':'p_of,p_to,side2,t_type,p_post,f_code','view2':'file_ppr,file_cd'}
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    #{{=__objs__['doc_srl_code']['select'][__objs__['doc_srl_code']['value']][5:].strip()}}
    'doc_rec':{ #db
        'a':{
            'base':{'mode':'form','title':'مرکز کنترل مدارک - DCC','help':'document_record','code':'402'
            },
            'tasks':{
                'f2f_id':{'type':'reference','title':'فرم مبنا','ref':{'db':'doc_num','tb':'a','key':'{id}','val':'{doc_a_code}-{doc_srl_name}'},},#'prop':['readonly']
                'prj':{'type':'reference','width':'5','title':'پروژه','ref':{'db':'doc_num','tb':'a','key':'{prj}','val':'{prj}-{prj_name}'},'prop':['update']},
                'sub_p':{'type':'reference','width':'5','title':'زیر پروژه','ref':{'db':'doc_num','tb':'a','key':'{sub_p}','val':'{sub_p}-{sub_p_name}'
                    ,'where':'''prj = "{{=__objs__['prj']['value']}}"'''},'prop':['update']},
                'step':{'type':'reference','width':'5','title':'مرحله','ref':{'db':'doc_num','tb':'a','key':'{step}','val':'{step}-{step_name}'
                    ,'where':'''prj = "{{=__objs__['prj']['value']}}" AND sub_p =  "{{=__objs__['sub_p']['value']}}"'''},'prop':['update']},
                'dspln':{'type':'reference','width':'5','title':'دیسیپلین','ref':{'db':'doc_num','tb':'a','key':'{dspln}','val':'{dspln}-{dspln_name}'
                    ,'where':'''prj = "{{=__objs__['prj']['value']}}" AND sub_p =  "{{=__objs__['sub_p']['value']}}" AND step =  "{{=__objs__['step']['value']}}"'''},'prop':['update']},
                'doc_t':{'type':'reference','width':'5','title':'دسته مدرک','ref':{'db':'doc_num','tb':'a','key':'{doc_t}','val':'{doc_t}-{doc_t_name}'
                    ,'where':'''prj = "{{=__objs__['prj']['value']}}" AND sub_p =  "{{=__objs__['sub_p']['value']}}" AND step =  "{{=__objs__['step']['value']}}" AND dspln =  "{{=__objs__['dspln']['value']}}"'''},'prop':['update']},
                'doc_p_code':{'type':'auto','len':'40','auto':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}','title':'پیش کد مدرک'},
                #'test1':{'type':'auto','title':'پیش کد مدرک','auto':"{{=__objs__['doc_p_code']['value']}}"},
                'doc_srl_code':{'type':'reference','len':'4','lang':'en','title':'کد سریال مدرک','ref':{'db':'doc_num','tb':'a','key':'{doc_srl_code}','val':'{doc_srl_code}-{doc_srl_name}','where':'''doc_p_code = "{{=__objs__['doc_p_code']['value']}}"'''},'prop':['update']},#
                'doc_srl_name':{'type':'auto','len':'250','title':'نام مدرک','auto':"{{=__objs__['doc_srl_code']['output_text'][5:].strip()}}"}, #"{{=__objs__['doc_srl_code']['select'][doc_srl_code]}}"
                'doc_a_code':{'type':'auto','len':'50','auto':'{doc_p_code}-{doc_srl_code}','title':'کد کامل مدرک'},
                'rev':{'type':'index','len':'2','ref':{'db':'doc_rec','tb':'a','key':'{id}','val':'{rev}','where':'''doc_a_code = "{{=__objs__['doc_a_code']['value']}}"'''},'title':'بازبینی','prop':['update']},
                'date':{'type':'fdate','width':'10','title':'تاریخ مدرک','prop':['update']},
                'f_code_r':{'type':'auto','len':'8','auto':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}-{doc_srl_code}-{rev}-{{=date[2:4]+date[5:7]+date[8:10] if date else ""}}','title':'کد فایل'},
                #'file_edt':{'type':'file','len':'40','file_name':'{f_code_r}','file_ext':"doc,docx,xls,xlsx,ppt,pptx,dwg,zip,rar",'path':'prj,{prj},{sub_p},{step},{dspln},{doc_t}','title':'فایل نهایی با فرمت تغییر پذیر'},
                #'file_fix':{'type':'file','len':'40','file_name':'{f_code_r}','file_ext':"pdf,gif,jpg,jpeg,png",'path':'prj,{prj},{sub_p},{step},{dspln},{doc_t}','title':'فایل نهایی با فرمت ثابت'},
                'file_b':{'type':'file_v','file_name':'{{=f_code_r}}-bas','title':'f_bas'},
                'file_v':{'type':'file_v','file_name':'{{=f_code_r}}-vec','title':'f_vec'},
                'file_r':{'type':'file_r','file_name':'{{=f_code_r}}-ras','title':'f_ras'},
                'file_nx':{'type':'text','len':'240','title':'names','help':'سایر نام های فایل'},
                'snd_ppr':{'type':'text','len':'240','title':'شماره نامه های ارسال فایل'},
                'des':{'type':'text','len':'240','title':'توضیح'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,prj,sub_p,step,dspln,doc_t,doc_p_code,doc_srl_code,doc_srl_name','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'doc_a_code,rev,date','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'f_code_r,lb_f_v,file_v,lb_f_r,file_r,lb_f_b,file_b','xjobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'file_nx,snd_ppr,des','xjobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'all':{'input':'prj,sub_p,step,dspln,doc_t','view1':'doc_p_code','view2':'doc_p_code'}
            },
            'labels':{
                'lb_f_v':'vector - فایلهای قابل ویرایش ارسالی برای کارفرما',
                'lb_f_r':'raster - فایلهای با فرمت ثابت ارسالی برای کارفرما',
                'lb_f_b':'base - سایر اسناد پروژه که لازم نیست برای کارفرما فرستاده شود ولی برای مدیریت سوابق و یا اصلاحات احتمالی و ...  لازم می باشد',
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'doc_rec_1':{ #db
        'a':{
            'base':{'mode':'form','title':'مرکز کنترل مدارک - DCC - جدید','help':'document_record','code':'402','rev':'00-040617'
            },
            'tasks':{
                'f2f_id':{'type':'reference','title':'فرم مبنا','ref':{'db':'doc_num_1','tb':'a','key':'{id}','val':'{doc_a_code}-{doc_srl_name}'},},#'prop':['readonly']
                'c_prj_id':{'type':'reference','title':'پروژه','prop':['update'],
                            'ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d},{cp_code},{cp_name}'},
                            'team':{'c_prj_cd':{'val':'{cp_code}'},'c_prj_nm':{'val':'{cp_name}'}},},
                'step':{'type':'reference','width':'5','title':'مرحله','ref':{'db':'doc_num_1','tb':'a','key':'{step}','val':'{step}-{step_name}'
                    ,'where':'''c_prj_id = "{{=__objs__['c_prj_id']['value']}}"'''},'prop':['update']},
                'dspln_id':{'type':'reference','width':'5','title':'دیسیپلین','ref':{'db':'doc_num_1','tb':'a','key':'{dspln_id}','val':'{dspln_id}-{dspln_cd}-{dspln_nm}'
                    ,'where':'''c_prj_id = "{{=__objs__['c_prj_id']['value']}} AND step =  "{{=__objs__['step']['value']}}"'''},'prop':['update'],
                    'team':{'dspln_cd':{'val':'{dspln_cd}'},'dspln_nm':{'val':'{dspln_nm}'}},},
                'doc_t_id':{'type':'reference','width':'5','title':'دسته مدرک','ref':{'db':'doc_num_1','tb':'a','key':'{doc_t_id}','val':'{doc_t_id}-{doc_t_cd}-{doc_t_nm}'
                    ,'where':'''c_prj_id = "{{=__objs__['c_prj_id']['value']}} AND step =  "{{=__objs__['step']['value']}}" AND dspln_id =  "{{=__objs__['dspln_id']['value']}}"'''},'prop':['update'],
                    'team':{'doc_t_cd':{'val':'{doc_t_cd}'},'doc_t_nm':{'val':'{doc_t_nm}'}},},
                'doc_p_code':{'type':'auto','len':'40','auto':'{c_prj_cd}-{step}-{dspln_cd}-{doc_t_cd}','title':'پیش کد مدرک'},
                #'test1':{'type':'auto','title':'پیش کد مدرک','auto':"{{=__objs__['doc_p_code']['value']}}"},
                'doc_srl_code':{'type':'reference','len':'4','lang':'en','title':'کد سریال مدرک',
                    'ref':{'db':'doc_num_1','tb':'a','key':'{doc_srl_code}','val':'{doc_srl_code}-{doc_srl_name}','where':'''doc_p_code = "{{=__objs__['doc_p_code']['value']}}"'''},'prop':['update'],
                    'team':{'doc_srl_name':{'val':'{doc_srl_name}'}},},
                'doc_a_code':{'type':'auto','len':'50','auto':'{doc_p_code}-{doc_srl_code}','title':'کد کامل مدرک'},
                'rev':{'type':'index','len':'2','ref':{'db':'doc_rec','tb':'a','key':'{id}','val':'{rev}','where':'''doc_a_code = "{{=__objs__['doc_a_code']['value']}}"'''},'title':'بازبینی','prop':['update']},
                'date':{'type':'fdate','width':'10','title':'تاریخ مدرک','prop':['update']},
                'f_code_r':{'type':'auto','auto':'{doc_a_code}-{{=date[2:4]+date[5:7]+date[8:10] if date else ""}}','title':'کد فایل'},
                'file_b':{'type':'file_v','file_name':'{{=f_code_r}}-bas','title':'f_bas'},
                'file_v':{'type':'file_v','file_name':'{{=f_code_r}}-vec','title':'f_vec'},
                'file_r':{'type':'file_r','file_name':'{{=f_code_r}}-ras','title':'f_ras'},
                'file_nx':{'type':'text','len':'240','title':'names','help':'سایر نام های فایل'},
                'snd_ppr':{'type':'text','len':'240','title':'شماره نامه های ارسال فایل'},
                'des':{'type':'text','len':'240','title':'توضیح'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,c_prj_id,c_prj_cd,c_prj_nm,step,dspln_id,dspln_cd,dspln_nm,doc_t_id,doc_t_cd,doc_t_nm,doc_p_code,doc_srl_code,doc_srl_name','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'doc_a_code,rev,date','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'f_code_r,lb_f_v,file_v,lb_f_r,file_r,lb_f_b,file_b','xjobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'file_nx,snd_ppr,des','xjobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'all':{'input':'prj,sub_p,step,dspln,doc_t','view1':'doc_p_code','view2':'doc_p_code'}
            },
            'labels':{
                'lb_f_v':'vector - فایلهای قابل ویرایش ارسالی برای کارفرما',
                'lb_f_r':'raster - فایلهای با فرمت ثابت ارسالی برای کارفرما',
                'lb_f_b':'base - سایر اسناد پروژه که لازم نیست برای کارفرما فرستاده شود ولی برای مدیریت سوابق و یا اصلاحات احتمالی و ...  لازم می باشد',
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'doc_tqm':{ #db
        'a':{
            'base':{'mode':'form','title':'اسناد تعالی و مدیریت کیفیت','help':'document_for_TQM','code':'402','rev':'x01-040519'
            },
            'tasks':{
                'name':{'type':'text','len':'150','title':'نام مدرک'},
                'hlp_des':{'type':'text','len':'150','title':'توضیح 1'},
                'user_crt':{'type':'user','title':'تهیه کننده','prop':{'multiple'}},
                'units':{'type':'select','title':'معاونت مرتبط','select':{'D':'design-طراحی','S':'supervition-نظارت','P':'plan - برنامه ریزی و توسعه','M':'Management - مدیریت','A':'All - کل شرکت ','-':'نا مشخص'},'prop':['multiple']},
                'doc_type':{'type':'select','title':'نوع مدرک','select':{'FR':'فرم','IN':'دستورالعمل','CL':'چک لیست','WB':'نظام نامه یا سند'},'prop':['update'],'onchange':"document.getElementById('srl').value='';"},
                #'srl':{'type':'index','len':'3','start':1,'ref':{'db':'doc_tqm','tb':'a','key':'{id}','val':'{srl}','where':'''doc_type = "{{=__objs__['doc_type']['value']}}"'''},'title':'سریال','prop':['update']},
                'code':{'type':'text','len':'40','title':'کد مدرک'},
                'f_code':{'type':'auto','len':'8','auto':'aqrc-tqm-{{=str(id).zfill(3)}}','title':'کد فایل'},
                'inc_files':{'type':'f2f','width':'60','title':'فایل های ورودی',
                    'ref':{'db':'doc_tqm','tb':'inc_files','show_cols':['nn','file_inc_r']},'var_set':{'f_code':'f_code'}},
                'files':{'type':'f2f','width':'60','title':'اسناد نهایی',
                    'ref':{'db':'doc_tqm','tb':'files','show_cols':['rev','file_1cr_r','file_2fr_r','file_2fr_v','file_3do_r','file_4er_r']},
                    'var_set':{'f_code':'f_code'}},
                #'file_inc_v':{'type':'file','len':'40','file_name':'{{=f_code}}-inc-v','file_ext':"doc,docx,xls,xlsx,zip,rar",'path':'form,doc_tqm','title':'فایل ورودی'},
                #'file_inc_r':{'type':'file','len':'40','file_name':'{{=f_code}}-inc-r','file_ext':"pdf",'path':'form,doc_tqm','title':'pdf - فایل ورودی'},
                #'file_1cr_v':{'type':'file','len':'40','file_name':'{{=f_code}}-1cr-v','file_ext':"doc,docx,xls,xlsx,zip,rar",'path':'form,doc_tqm','title':'سند اولیه'},
                #'file_1cr_r':{'type':'file','len':'40','file_name':'{{=f_code}}-1cr-r','file_ext':"pdf",'path':'form,doc_tqm','title':'pdf - سند اولیه'},
                #'file_2fr_v':{'type':'file','len':'40','file_name':'{{=f_code}}-2fr-v','file_ext':"doc,docx,xls,xlsx,zip,rar",'path':'form,doc_tqm','title':'فرمت شده'},
                #'file_2fr_r':{'type':'file','len':'40','file_name':'{{=f_code}}-2fr-r','file_ext':"pdf",'path':'form,doc_tqm','title':'pdf فرمت شده'},
                'p_file_name':{'type':'text','len':'40','title':'نام قبلی فایل'},
                'des_2':{'type':'text','len':'60','title':'توضیحات'},
            },
            'steps':{
                'pre':{'tasks':'doc_type,name,user_crt,units,code,hlp_des,p_file_name','xjobs':'dcc_grp','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'f_code,inc_files,files','xjobs':'dcc_grp','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'des_2','xjobs':'dcc_grp','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            #file_inc_v,file_inc_r,file_1cr_v,file_1cr_r,file_2fr_v,file_2fr_r
            },
            'views':{
                'all':{'input':'units','view1':'name,user_crt,code','view2':'code'}
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        },
        'files':{
            'base':{'mode':'form','title':'اسناد مدیریت کیفیت- فایلهای نهایی','code':'900'
            },
            'tasks':{
                'f2f_id':{'type':'reference','width':'5','title':'فرم مبنا','ref':{'db':'doc_tqm','tb':'a','key':'{id}','val':'{name}'},'prop':['readonly']},
                'f_code':{'type':'text','width':'30','title':'کد 1','prop':['readonly']},
                'rev':{'type':'index','start':0,'len':'2','ref':{'db':'doc_tqm','tb':'files','key':'{id}','val':'{rev}','where':'''f_code = "{{=__objs__['f_code']['value']}}"'''},'title':'بازبینی','prop':['update']},
                'date1':{'type':'fdate','title':'تاریخ تهیه سند اولیه','prop':['update']},
                'date2':{'type':'fdate','title':'تاریخ تهیه سند نهایی','prop':['update']},
                'f_code_r':{'type':'auto','len':'8','auto':'{f_code}-{rev}','title':'کد 2'},
                'file_1cr_v':{'type':'file','len':'40','file_name':'{{=f_code_r}}-1cr-v','file_ext':"md,mm,doc,docx,xls,xlsx,zip,rar",'path':'form,doc_tqm','title':'سند اولیه'},
                'file_1cr_r':{'type':'file','len':'40','file_name':'{{=f_code_r}}-1cr-r','file_ext':"pdf",'path':'form,doc_tqm','title':'pdf - سند اولیه'},
                'file_2sh_v':{'type':'file_v','len':'40','file_name':'{{=f_code_r}}-2sh-v','path':'form,doc_tqm','title':'مستندات تعامل با ذینفعان'},
                'file_2sh_r':{'type':'file_r','len':'40','file_name':'{{=f_code_r}}-2sh-r','path':'form,doc_tqm','title':'مستندات تعامل با ذینفعان - PDF'},
                'file_2fr_v':{'type':'file_v','len':'40','file_name':'{{=f_code_r}}-2fr-v','path':'form,doc_tqm','title':'سند نهایی'},
                'file_2fr_r':{'type':'file_r','len':'40','file_name':'{{=f_code_r}}-2fr-r','path':'form,doc_tqm','title':'سند نهایی  - PDF'},
                'file_2fr_a':{'type':'file_r','len':'40','file_name':'{{=f_code_r}}-2fr-a','path':'form,doc_tqm','title':'سند نهایی مصوب'},
                'date':{'type':'fdate','title':'تاریخ ابلاغ','prop':['update']},
                'eblag':{'type':'text','len':'40','title':'مستندات ابلاغ'},
                'file_3do_v':{'type':'file','len':'40','file_name':'{{=f_code_r}}-3do-v','file_ext':"md,mm,doc,docx,xls,xlsx,zip,rar",'path':'form,doc_tqm','title':'ابلاغیه'},
                'file_3do_r':{'type':'file','len':'40','file_name':'{{=f_code_r}}-3do-r','file_ext':"pdf",'path':'form,doc_tqm','title':'pdf ابلاغیه'},
                'file_4er_v':{'type':'file','len':'40','file_name':'{{=f_code_r}}-4er-v','file_ext':"md,mm,doc,docx,xls,xlsx,zip,rar",'path':'form,doc_tqm','title':'اصلاحات'},
                'file_4er_r':{'type':'file','len':'40','file_name':'{{=f_code_r}}-4er-r','file_ext':"pdf",'path':'form,doc_tqm','title':'pdf اصلاحات'},
                'suggestion':{'type':'f2f','width':'60','title':'پیشنهاد اصلاح',
                    'ref':{'db':'doc_tqm','tb':'suggestion','show_cols':['nn','user','suggest']},
                    'var_set':{'f_code':'f_code'}},
                'idea':{'type':'f2f','width':'60','title':'پیشنهاد اصلاح',
                    'ref':{'db':'suggestion','tb':'in_form','show_cols':['nn','user','idea']},
                    'var_set':{'f_code':'f_code'}},
                #er= مشخص سازی مشکلات error , cr=creat,zn=zinafan,
            },
            'steps':{
                'pre':{'tasks':'f2f_id,f_code,rev','xjobs':'*','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'f_code_r,date1,file_1cr_v,file_1cr_r','xjobs':'*','title':'فایل اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'lable_1,date2,file_2sh_v,file_2sh_r,file_2fr_v,file_2fr_r,file_2fr_a','xjobs':'*','title':'فایل نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'date,eblag,file_3do_v,file_3do_r','xjobs':'dcc_grp','title':'ابلاغ','app_keys':'','app_titls':'','oncomplete_act':''},
                's4':{'tasks':'suggestion,file_4er_v,file_4er_r','xjobs':'dcc_grp','title':'ثبت اصلاحات','app_keys':'','app_titls':'','oncomplete_act':''},#idea
            },
            'labels':{
                'lable_1':'اقدامات سند نهایی : اصلاح فرمت و اعمال تغییرات نهایی مد نظر مدیران و ذی نفعان',
            },
        },
        'inc_files':{
            'base':{'mode':'form','title':' اسناد مدیریت کیفیت - فایلهای ورودی','code':'900'
            },
            'tasks':{
                'f2f_id':{'type':'reference','width':'5','title':'فرم مبنا','ref':{'db':'doc_tqm','tb':'a','key':'{id}','val':'{name}'},'prop':['readonly']},
                'f_code':{'type':'text','width':'30','title':'کد 1','prop':['readonly']},
                'nn':{'type':'index','len':'2','ref':{'db':'doc_tqm','tb':'inc_files','key':'{id}','val':'{nn}','where':'''f_code = "{{=__objs__['f_code']['value']}}"'''},'title':'ایندکس','start':1},#,'prop':['readonly']
                'user':{'type':'user','title':'جمع آوری','prop':['multiple']},
                'date':{'type':'fdate','title':'تاریخ دریافت فایل','prop':['update']},
                'f_code_r':{'type':'auto','len':'8','auto':"""{f_code}-inc-{{=__objs__['nn']['value']}}""",'title':'کد 2'},
                'file_inc_v':{'type':'file_v','len':'40','file_name':'{f_code_r}-v','path':'form,doc_tqm','title':'فایل ورودی'},
                'file_inc_r':{'type':'file_r','len':'40','file_name':'{f_code_r}-inc-r','path':'form,doc_tqm','title':'pdf - فایل ورودی'},
                'n_file_inc':{'type':'text','len':'64','title':'نام قبلی فایل'},
                'des':{'type':'text','len':'128','title':'توضیحات'},
                
            },
            'steps':{
                'pre':{'tasks':'f2f_id,f_code,nn,date,user','xjobs':'*','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'f_code_r,file_inc_v,file_inc_r,n_file_inc,des','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
        },
        'suggestion':{
            'base':{'mode':'form','title':'اسناد مدیریت کیفیت - پیشنهاد اصلاحی','code':'900','rev':'00-040417'
            },
            'tasks':{
                'f2f_id':{'type':'reference','width':'5','title':'فرم مبنا','ref':{'db':'doc_tqm','tb':'a','key':'{id}','val':'{name}'},'prop':['readonly']},
                'f_code':{'type':'text','width':'30','title':'کد 1','prop':['readonly']},
                'nn':{'type':'index','len':'2','ref':{'db':'doc_tqm','tb':'suggestion','key':'{id}','val':'{nn}','where':'''f2f_id = "{f2f_id}"'''},'title':'ایندکس','start':1},#,'prop':['readonly']
                'user':{'type':'user','title':'پیشنهاد دهنده','prop':['multiple']},
                'date':{'type':'fdate','title':'تاریخ پیشنهاد','prop':['update']},
                'f_code_r':{'type':'auto','len':'8','auto':"""{f_code}-sug-{nn}""",'title':'کد 2'},
                'file_r':{'type':'file_r','len':'40','file_name':'{f_code_r}-r','path':'form,doc_tqm','title':'pdf - فایل ورودی'},
                'suggest':{'type':'text','len':'512','title':'متن پیشنهاد اصلاحی','height':'50px'},
                
            },
            'steps':{
                'pre':{'tasks':'f2f_id,f_code,nn,date,user,f_code_r,file_r,suggest','xjobs':'*','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
            },
        }
    },
    #--------------------------------------------------------------------
    'doc_mm':{ #db
        'a':{
            'base':{'mode':'form','title':'صورت جلسه','help':'meeting minute','code':'403','xform_cg_file':'fr-cg-doc_mm2.html',
                'multi_app':{'2':['ks'],'rev':'01-040403'},
            },
            'tasks':{
                'name':{'type':'text','width':'60','title':'عنوان جلسه'},
                'date':{'type':'fdate','title':'تاریخ جلسه','prop':['update']},
                'time_st':{'type':'time_c','title':'ساعت شروع جلسه','def_value':'07:00'},
                'user_crt':{'type':'user','title':'تهیه و تنظیم','prop':{'multiple'}},
                'user_man':{'type':'text','width':'60','title':'رئیس جلسه'},
                'units':{'type':'select','title':'معاونت مرتبط','select':{'D':'design-طراحی','S':'supervition-نظارت','P':'plan - برنامه ریزی و توسعه','M':'Management - مدیریت','-':'نا مشخص'},'prop':['multiple']},
                'mm_type':{'type':'select','title':'نوع جلسه','select':{'I':'Interior-داخلی','C':'Client-کارفرما','O':'OutSource - با برون سپارها'},'prop':['update']},
                'c_prj_id':{'type':'reference','width':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update']},
                'c_prj_txt':{'type':'auto-x','width':'70','ref':'c_prj_id'},
                'prj_name':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_name}','where':'id = "{c_prj_id}"'},'title':'نام پروژه'},
                'prj_code':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_code}','where':'id = "{c_prj_id}"'},'title':'کد پروژه','prop':['update']},
                'code_sn':{'type':'index','len':'3','ref':{'db':'doc_mm','tb':'a','key':'{id}','val':'{code_sn}','where':"prj_code = '{prj_code}' AND mm_type = '{mm_type}'"},'title':'شماره','prop':['update'],'start':1},
                'code':{'type':'auto','len':'8','auto':'aqrc-_mm-{{=date[:4]+date[5:7]+date[8:10] if date else "000000"}}-{{=str(id).zfill(4)}}-{mm_type}','title':'کد پشتیبان'},
                'stn_code':{'type':'auto','len':'8','auto':'{prj_code}-_C-{{=date[2:4]+date[5:7]+date[8:10] if date else "000000"}}-MM-A{mm_type}-{code_sn}-{{=str(id).zfill(5)}}','title':'کد فایل'},
                'file_v':{'type':'file_v','len':'40','file_name':'{{=code}}-vec','path':'form,doc__mm','title':'فایل اصلی'},
                'file_r':{'type':'file_r','len':'40','file_name':'{{=code}}-ras','path':'form,doc__mm','title':'pdf'},
                'file_a':{'type':'file','len':'40','file_name':'{{=code}}-app','file_ext':"pdf,jpg",'path':'form,doc__mm','title':'اسکن فایل امضا شده'},
                'des_1':{'type':'text','width':'60','title':'توضیحات'},
                'pos':{'type':'f2f','len':'60','title':'محل جلسه','ref':{'tb':'pos','show_cols':['name','per','per_x']},},
                'note':{'type':'f2f','len':'60','title':'مذاکرات','ref':{'tb':'note','show_cols':['p_sy','des']},},
                'todo':{'type':'f2f','len':'60','title':'مصوبات','ref':{'tb':'todo','show_cols':['p_sy','des','p_do','p_ch','dur']},},
                'attch':{'type':'f2f','len':'60','title':'پیوستها','ref':{'tb':'attch','show_cols':['name','file_v','file_r']},'var_set':{'f_code':'code'}},
                'pic':{'type':'f2f','len':'60','title':'تصاویر جلسه','ref':{'tb':'pic','show_cols':['file_pic']},'var_set':{'f_code':'code'}},
                'abstr':{'type':'text','len':'1000','title':'خلاصه جلسه'},
            },
            'steps':{
                'pre':{'tasks':'date,time_st,user_crt,user_man,units,mm_type,c_prj_id,c_prj_txt,prj_name,prj_code,code_sn,name','xjobs':'*,dcc_grp','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'code,stn_code,pos,note,todo,attch,abstr','xjobs':'#step#0,dcc_grp','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'file_v,file_r,file_a,pic','xjobs':'#step#0,dcc_grp','title':'بارگزاری فایل نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'date,time_st,user_crt,user_man,units,mm_type,c_prj_id,c_prj_txt,prj_name,prj_code,code_sn,name,des_1,stn_code','xjobs':'dcc_grp','title':'مدیریت سوابق','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'des_1','view1':'name,date,time_st,user_crt,units,mm_type,c_prj_id,c_prj_txt','view2':'code,file_v,file_r'}
            },
            'cols_filter':{
                'date,time_st,mm_type,prj_name,prj_code,code_sn,name,stn_code,pos,todo,note,attch,file_r':'لیست 1',
                '':'همه',
                
            },
            'data_filter':{'':'همه',}
        },
        'pos':{
            'base':{'mode':'form','title':'محل جلسه','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','len':'5','title':'فرم مبنا','ref':{'tb':'a','key':'{id}','val':'{date} , {c_prj_txt} , {name}'},'prop':['readonly']},
                'name':{'type':'text','len':'60','title':'نام محل'},
                'per':{'type':'text','len':'500','title':'افراد حاضر'},
                'per_x':{'type':'text','len':'250','title':'غایبین'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,name,per,per_x','xjobs':'*,dcc_grp','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            
        },
        'todo':{
            'base':{'mode':'form','title':'اقدامات جلسه','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','len':'5','title':'فرم مبنا','ref':{'tb':'a','key':'{id}','val':'{date} , {c_prj_txt} , {name}'},'prop':['readonly']},
                'p_sy':{'type':'text','len':'60','title':'اعلام'},
                'des':{'type':'text','len':'1000','title':'شرح اقدام'},
                'p_do':{'type':'text','len':'60','title':'انجام'},
                'p_ch':{'type':'text','len':'60','title':'پیگیری'},
                'dur':{'type':'text','len':'60','title':'زمان'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,p_sy,des,p_do,p_ch,dur','xjobs':'*,dcc_grp','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            
        },
        'note':{
            'base':{'mode':'form','title':'مذاکرات جلسه','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','len':'5','title':'فرم مبنا','ref':{'tb':'a','key':'{id}','val':'{date} , {c_prj_txt} , {name}'},'prop':['readonly']},
                'p_sy':{'type':'text','len':'60','title':'اعلام کننده'},
                'des':{'type':'text','len':'2500','title':'شرح'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,p_sy,des','xjobs':'*,dcc_grp','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            }, 
        },
        'attch':{
            'base':{'mode':'form','title':'فایلهای پیوست صورتجلسات','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','len':'5','title':'فرم مبنا','ref':{'tb':'a','key':'{id}','val':'{date} , {c_prj_txt} , {name}'},'prop':['readonly']},
                'f_code':{'type':'text','width':'30','title':'کد 1','prop':['readonly']},
                'nn':{'type':'index','len':'2','ref':{'where':'f_code = "{f_code}"'},'title':'شماره','start':1,'prop':['update']},
                'f_code_r':{'type':'auto','len':'8','auto':'{f_code}-att-{nn}','title':'کد 2'},
                'name':{'type':'text','len':'60','title':'عنوان فایل'},
                'per':{'type':'text','len':'20','title':'ارائه دهنده'},
                'des':{'type':'text','len':'80','title':'توضیح'},
                'file_v':{'type':'file_v','file_name':'{{=f_code_r}}-vec','title':'فایل اصلی'},
                'file_r':{'type':'file_r','file_name':'{{=f_code_r}}-ras','title':'pdf'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,f_code,nn,name,per','xjobs':'*,dcc_grp','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'f_code_r,file_v,file_r,des','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''}
            },    
        },
        'pic':{
            'base':{'mode':'form','title':'تصاویر جلسه','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','len':'5','title':'فرم مبنا','ref':{'tb':'a','key':'{id}','val':'{date} , {c_prj_txt} , {name}'},'prop':['readonly']},
                'f_code':{'type':'text','width':'30','title':'کد 1','prop':['readonly']},
                'nn':{'type':'index','len':'2','ref':{'where':'f_code = "{f_code}"'},'title':'شماره','start':1,'prop':['update']},
                'file_pic':{'type':'file_r','file_name':'{f_code}-pic-{nn}','title':'تصویر'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,f_code,nn,file_pic','xjobs':'*,dcc_grp','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
                #'s1':{'tasks':'file_pic','xjobs':'*','title':'تکمیل','app_keys':'','app_titls':'','oncomplete_act':''}
            },    
        }
    },
    #--------------------------------------------------------------------
    'person_act':{ #db
        'a':{
            'base':{'mode':'form','title':'اقدامات هر فرد','help':'person_act_manage','code':'410'
            },
            'tasks':{
                'frd_id':{'type':'auto-x','len':'4','auto':'_cur_user_un_','title':'کد همکار'},
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title': 'نام همکار'},
                'date1':{'type':'fdate','len':'10','title':'تاریخ','prop':[]},
                'prj_id':{'type':'reference','len':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d},{cp_code},{cp_name}'},'title':'پروژه','prop':['update']},
                'cp_code':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_code}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'کد پروژه','prop':['hidden']},
                'cp_name':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_name}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'نام پروژه','prop':['hidden']},
                'wbs_l1':{'type':'reference','len':'30','title':'دسته موضوع اقدام - WBS-L1','prop':['update'],
                    'ref':{'db':'a_cur_subject','tb':'wbs_l1','key':'{id}','val':'{id:03d},{wbs_l1_code},{wbs_l1_name}','where':'''f2f_id = "{prj_id}"'''},
                    'team':{'wbs_l1_name':{'val':'{wbs_l1_name}','title':'نام دسته موضوع اقدام','prop':['hidden']},
                            'wbs_l1_code':{'val':'{wbs_l1_code}','title':'کد دسته  موضوع اقدام','prop':['hidden']}},},
                'wbs_l2':{'type':'reference','len':'30','title':'موضوع اقدام- WBS-L2','prop':['update'],
                    'ref':{'db':'a_cur_subject','tb':'wbs_l2','key':'{id}','val':'{id:03d},{wbs_l1_code},{wbs_l1_name}'},
                    'team':{'wbs_l2_name':{'val':'{wbs_l2_name}','title':'نام موضوع اقدام','prop':['hidden']},
                            'wbs_l2_code':{'val':'{wbs_l1_code}','title':'کد موضوع اقدام','prop':['hidden']}},},
                'tact_cod':{'type':'reference','len':'30','ref':{'db':'act','tb':'a','key':'{code}','val':'{code}-{title}'},'title':'نوع اقدام','prop':['update','multiple']},
                'tact_ttl':{'type':'auto-x','len':'30','ref':'tact_cod','prop':['hidden']},
                'act_des':{'type':'text','len':'255','title':'شرح اقدام'},
                'act_cat':{'type':'text','len':'35','title':'دسته اقدام'},
                'time':{'type':'time_t','title':'به مدت','def_value':'0:30'},
            },
            'steps':{
                'pre':{'tasks':'frd_id,frd_1,date1,prj_id,cp_code,cp_name,wbs_l1,wbs_l1_name,wbs_l1_code,lable_1,tact_cod,tact_ttl,act_cat,lable_1,act_des,time','xjobs':'*','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
                #'pre':{'tasks':'frd_id,frd_1,date1,prj_id,cp_code,cp_name,wbs_l1,wbs_l1_name,wbs_l1_code,wbs_l2,wbs_l2_name,wbs_l2_code,lable_1,tact_cod,tact_ttl,act_cat,lable_1,act_des,time','xjobs':'*','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'frd_id,frd_1,date1,prj_id,cp_code,cp_name,act_cat,act_des,time','view1':'','view2':'','view_cols':1},
            },
            'labels':{
                'lable_1':'------------',
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'person_get':{ #db
        'a':{
            'base':{'mode':'form','title':'مشخصات افراد شناسایی شده برای جذب نیرو','help':'','code':'920'
            },
            'tasks':{
                'name_f':{'type':'text','len':'20','title':'نام'},
                'family_f':{'type':'text','len':'20','title':'نام خانوادگی'},
                'name_e':{'type':'text','len':'20','title':'name'},
                'family_e':{'type':'text','len':'20','title':'family'},
                'code_meli':{'type':'text','len':'10','title':'کدملی'},
                'tel_mob':{'type':'text','len':'10','title':'شماره موبایل'},
                'date':{'type':'fdate','len':'10','title':'تاریخ مراجعه'},
                'eng':{'type':'reference','title':'رسته / دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{name}'}},
                'eng_des':{'type':'text','len':'40','title':'توضیحات تخصص'},
                'office':{'type':'select','select':['طراحی','نظارت','پشتیبانی','مدیریت'],'title':'بخش'},
                'f_resume':{'type':'file','len':'40','title':'فایل رزومه','file_name':'cv-{{=str(id).zfill(3)}}-{{=date[:4] if date else ""}}-rsum-{family_e}-{name_e}','file_ext':"pdf,gif,jpg,jpeg,png",'path':'form,person_get'},
                'f_form':{'type':'file','len':'40','title':'فایل فرم','file_name':'cv-{{=str(id).zfill(3)}}-{{=date[:4] if date else ""}}-form-{family_e}-{name_e}','file_ext':"pdf,gif,jpg,jpeg,png",'path':'form,person_get','auth':'dcc_prj'}
            },
            'steps':{
                'pre':{'tasks':'name_f,family_f,name_e,family_e','xjobs':'dcc_prj','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'code_meli,tel_mob,date,eng,eng_des,office','xjobs':'dcc_prj','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'f_resume,f_form','xjobs':'dcc_prj','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'all':{'input':'name_f,family_f,name_e,family_e,tel_mob','view1':'code_meli,date,eng,eng_des,office','view2':'f_resume,f_form'}
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'todo':{ #db
        'a':{
            'base':{'mode':'form','title':'برنامه اقدامات لازم','help':'todo_act_4_person','code':'410'
            },
            'tasks':{
                'frd_id':{'type':'auto-x','len':'4','auto':'_cur_user_un_','title':'ثبت کننده  -کد'},
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'ثبت کننده  - نام'},
                'date1':{'type':'fdate','len':'10','title':'تا تاریخ','prop':[]},
                'prj_id':{'type':'reference','len':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d},{cp_code},{cp_name}'},'title':'پروژه','prop':['update']},
                'cp_code':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_code}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'کد پروژه'},
                'cp_name':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_name}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'نام پروژه'},
                'act_des':{'type':'text','len':'255','title':'شرح اقدام'},
                'act_cat':{'type':'text','len':'35','title':'دسته اقدام'},
                'per_do':{'type':'user','title':'اقدام کننده'},
                'date2':{'type':'fdate','len':'10','title':'تاریخ انجام','prop':[]},
                'done_des':{'type':'text','len':'255','title':'مستندات انجام'},
                'verify':{'type':'text','len':'255','title':'توضیح بررسی'},
            },
            'steps':{
                'pre':{'tasks':'frd_id,frd_1,prj_id,cp_code,cp_name,act_cat,act_des,per_do','xjobs':'*','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'date2,done_des','xjobs':'#task#per_do','title':'نتیجه','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
                's2':{'tasks':'lable_1,verify','xjobs':'#task#frd_id','title':'بررسی نتیجه','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
            },
            'views':{
                'all':{'input':'frd_id,frd_1,date1,prj_id,cp_code,cp_name,act_cat,act_des,time','view1':'','view2':'','view_cols':1},
            },
            'labels':{
                'lable_1':'تایید این مرحله نشانه مکفی بودن نتیجه می باشد',
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'a_contract':{ #db
        'a':{
            'base':{'mode':'form','title':'ثبت قراردادهای شرکت','help':'','code':'120','data_filter':'','multi_app':{'0':['ks'],'1':['ks']},
            },
            'tasks':{
                'subject':{'type':'text','title':'موضوع قرارداد','len':'250'},
                'client':{'type':'text','title':'کارفرما'},
                'date':{'type':'fdate','title':'تاریخ ابلاغ قرارداد'},
                'n_contr':{'type':'text','len':'40','title':'شماره قرارداد'},
                'prj_dur':{'type':'num','min':1,'max':1200,'len':'4','step':'0.1','title':'مدت قرارداد - ماه'},
                'serv_type':{'type':'select','title':'نوع خدمات','select':{'D':'design-طراحی','S':'supervition-نظارت','M':'MC-مدیریت طرح','-':'نا مشخص'},'prop':['multiple']},
                'f_cnt':{'type':'file','auth':'dcc_prj','len':'40','title':'فایل متن قرارداد امضا شده','file_name':'contract-{{=str(id).zfill(4)}}-{{=date[:4] if date else ""}}-','file_ext':"pdf",'path':'form,contract'},
                'f_cnt_ppr':{'type':'file','auth':'dcc_prj','len':'40','title':'نامه قرارداد در اتوماسیون','file_name':'contract-{{=str(id).zfill(4)}}-{{=date[:4] if date else ""}}-ppr','file_ext':"pdf,jpg,jpeg",'path':'form,contract'},
                'f_cnt_1p':{'type':'file','auth':'dcc_prj','len':'40','title':'سایر اسناد مرتبط','file_name':'contract-{{=str(id).zfill(4)}}-{{=date[:4] if date else ""}}-1p','file_ext':"pdf,zip",'path':'form,contract'},
                'verify_note':{'type':'text','len':'40','title':'توضیحات بررسی کننده'},
                'des':{'type':'text','len':'250','title':'توضیح'},
                
                
                'price':{'type':'num','min':1,'max':900000,'len':'6','title':'مبلغ قرارداد','help':'مبلغ قرارداد بر حسب میلیون تومان','auth':'dcc_prj'},
                'price_se':{'type':'num','min':1,'max':900000,'len':'6','title':'مبلغ نهایی','title_add':'مبلغ صورت وضعیت ارسالی بر حسب میلیون تومان'},
                'date_lse':{'type':'fdate','title':'تاریخ آخرین صورت وضعیت ارسالی'},
                'frd_peygir':{'type':'reference','len':'5','title':'مسئول پیگیری','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}- {m_w} {name} {family}'},'prop':['show_full']},
                'prj_step1':{'type':'select','title':'وضعیت کلی','select':{'1':'پروپوزال','2':'در حال قرارداد','11':'جاری','21':'گذشته  و ناتمام مالی','31':'خاتمه کامل'}},
                'price_off':{'type':'num','min':0,'max':100,'len':'6','title':'درصد تخفیف'},
                'user_cord':{'type':'user','title':'مسئول هماهنگی','prop':{'multiple'}}, #cordinator
                
                'busn_name':{'type':'text','title':'عنوان تجاری','len':'80'},
                'chlng':{'type':'text','len':'240','title':'چالش','help':'challenge'},
                'solution':{'type':'text','len':'240','title':'راهکار','help':'solution'},
                'pos_link':{'type':'text','title':'لینک موقعیت','len':'80','link':{'target':'_blank','icon_text':'G','class':'btn btn-info'},},
                'ppr_name':{'type':'text','title':'عنوان مختصر در نامه ها','len':'80'},
                'key_words':{'type':'text','title':'کلمات کلیدی','len':'120'},
                'f_busn_id':{'type':'file','auth':'dcc_prj','len':'40','title':'فایل شناسنامه تجاری','file_name':'contract-{{=str(id).zfill(4)}}-{{=date[:4] if date else ""}}-busn_id','file_ext':"pdf,zip",'path':'form,contract'},
                'f_exe_pic':{'type':'file','auth':'dcc_prj','len':'40','title':'فایل تصاویر اجرایی','file_name':'contract-{{=str(id).zfill(4)}}-{{=date[:4] if date else ""}}-exe_pic','file_ext':"pdf,zip",'path':'form,contract'},
                'f_rndr':{'type':'file','auth':'dcc_prj','len':'40','title':'فایل  رندر','file_name':'contract-{{=str(id).zfill(4)}}-{{=date[:4] if date else ""}}-rndr','file_ext':"pdf,zip",'path':'form,contract'},
            },
            'steps':{
                'pre':{'tasks':'subject,client,date,prj_dur,serv_type,des,n_contr,price','xjobs':'dcc_prj','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'f_cnt_ppr,f_cnt,f_cnt_1p','xjobs':'dcc_prj','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'verify_note,price,price_off','xjobs':'dccm','title':'تایید','app_keys':'','app_titls':'','oncomplete_act':'',
                    'start_step':'1','start_where':"'{step_1_ap}' == 'y'",'end_where':"False",},
                'b':{'tasks':'user_cord,busn_name,chlng,solution,pos_link,ppr_name,key_words,f_busn_id,f_exe_pic,f_rndr','xjobs':'tqm_a','title':'فراداده ها','app_keys':'y','app_titls':'','oncomplete_act':'',
                        'name':'b','auth':'tqm_a','start_where':"True",'end_where':"False"},
            },
            'views':{
                '1':{'input':'subject,client,date,prj_dur,serv_type,price','view1':'date,n_contr,des','view2':'des'},
                'all':{'input':'f_cnt_ppr,f_cnt,f_cnt_1p,price,price_off,n_contr,prj_dur','view1':'subject,date','view2':'des'},
            },
            'cols_filter':{
                '':'همه',
                'busn_name,chlng,solution,pos_link,ppr_name,key_words,user_cord,f_busn_id,f_exe_pic,f_rndr':'بررسی 1',
                },
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'prj_shenasname':{ #db
        'a':{
            'base':{'mode':'form','title':'شناسنامه فنی پروژه های شرکت','help':'','code':'121','rev':'01-040518',
                'data_filter':'','xform_cg_file':'prj-shenasname-st.html','multi_app':{'0':['ks'],'1':['ks']},
            },
            'tasks':{
                'prj_name':{'type':'text','title':'نام پروژه - عنوان قرارداد','len':'150','height':'50px'},
                'busn_name':{'type':'text','title':'عنوان تجاری','len':'80'},
                'pos_txt':{'type':'text','title':'موقعیت جغرافیایی - محل پروژه','len':'200'},
                'time':{'type':'text','title':'زمان پروژه','len':'500','height':'50px' },
                'prj_des':{'type':'text','title':'شرح مختصر - خلاصه','len':'1500','height':'100px'},
                'rslt_fin':{'type':'text','title':'دستاور دهای پروژه ( تجاری ، اقتصادی ) ','len':'1000','height':'75px'},
                'rslt_aue':{'type':'text','title':'مزایای معماری، شهرسازی و محیط زیست','len':'1000','height':'75px'},
                'inco':{'type':'text','title':'همکاران داخلی','len':'1000','height':'75px' ,'help':'internal coworkers'},
                'cons':{'type':'text','title':'مشاور اصلی پروژه','len':'1000','height':'50px' ,'help':'Consultant'},
                'cont':{'type':'text','title':'پیمانکاران و افراد کلیدی آنها','len':'1000','height':'50px' ,'help':'Contractor'},
                'conp':{'type':'text','title':'مشاوران همکار و افراد کلیدی آنها','len':'1000','height':'50px' ,'help':'Consultant Partner'},
                

                
                'date_st':{'type':'fdate','len':'10','title':'تاریخ شروع','prop':[]},
                'area':{'type':'num','min':1,'max':500000,'len':'6','title':'مساحت یا طول'},
                'area_unit':{'type':'select','title':'واحد مساحت','select':['متر مربع','هکتار','کیلومتر','متر','کیلومتر']},
                'scale':{'type':'text','title':'مقیاس','len':'50'},
                
                'goals':{'type':'text','title':'اهداف کلیدی','len':'1000','height':'75px'},
                'prj_type':{'type':'text','title':'نوع پروژه','len':'50'},
                
                'rslt_out':{'type':'text','title':'نتیجه‌گیری و برنامه‌های آینده','len':'300'},
                    
                
                'pos_link':{'type':'text','title':'لینک موقعیت','len':'80','link':{'target':'_blank','icon_text':'G','class':'btn btn-info'},},
                'ppr_name':{'type':'text','title':'عنوان مختصر در نامه ها','len':'80'},
                'key_words':{'type':'text','title':'کلمات کلیدی','len':'120'},
                
                'clint_id':{'type':'reference','width':'5','title':'کد کارفرما','ref':{'db':'a_clint','tb':'a','key':'{id}','val':'{id}-{name}'},'prop':['update']},
                'clint_txt':{'type':'auto-x','width':'70','ref':'clint_id','title':'کارفرما'},
                
                'f_busn_id':{'type':'file','auth':'dcc_prj','len':'40','title':'فایل شناسنامه تجاری','file_name':'contract-{{=str(id).zfill(4)}}-{{=date_st[:4] if date_st else ""}}-busn_id','file_ext':"pdf,zip",'path':'form,contract'},
                'f_exe_pic':{'type':'file','auth':'dcc_prj','len':'40','title':'فایل تصاویر اجرایی','file_name':'contract-{{=str(id).zfill(4)}}-{{=date_st[:4] if date_st else ""}}-exe_pic','file_ext':"pdf,zip",'path':'form,contract'},
                'f_rndr':{'type':'file','auth':'dcc_prj','len':'40','title':'فایل  رندر','file_name':'contract-{{=str(id).zfill(4)}}-{{=date_st[:4] if date_st else ""}}-rndr','file_ext':"pdf,zip",'path':'form,contract'},
                
                'chlng':{'type':'text','len':'240','title':'چالش','help':'challenge','height':'100px'},
                'solution':{'type':'text','len':'240','title':'راهکار','help':'solution','height':'100px'},
                'date_en':{'type':'fdate','len':'10','title':'تاریخ خاتمه','prop':[]},
            },
            'steps':{
                'pre':{'tasks':'prj_name,busn_name,pos_txt,time','xjobs':'dcc_prj','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'prj_des,rslt_fin,rslt_aue','xjobs':'dcc_prj','title':'تکمیل اطلاعات 1','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'cons,inco,cont,conp','xjobs':'dcc_prj','title':'تکمیل اطلاعات 2','app_keys':'','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'date_st,area,area_unit,scale,goals,prj_type,rslt_out,clint_id,clint_txt','xjobs':'dcc_prj','title':'تکمیل اطلاعات 3','app_keys':'','app_titls':'','oncomplete_act':''},
                's4':{'tasks':'chlng,solution','xjobs':'dcc_prj','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's5':{'tasks':'f_busn_id,f_exe_pic,f_rndr,pos_link','xjobs':'dccm','title':'تایید','app_keys':'','app_titls':'','oncomplete_act':'',
                    'start_step':'1','start_where':"'{step_1_ap}' == 'y'",'end_where':"False",},
                'b':{'tasks':'chlng,solution,ppr_name,key_words','xjobs':'tqm_a','title':'فراداده ها','app_keys':'y','app_titls':'','oncomplete_act':'',
                        'name':'b','auth':'tqm_a','start_where':"True",'end_where':"False"},
            },
            'views':{
                '1':{'input':'prj_name','view1':'','view2':''},
            },
            'cols_filter':{
                '':'همه',
                },
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'suggestion':{ #db {_cur_user_un_}
        'a':{
            'base':{'mode':'form','title':'فرم پیشنهاد ها','code':'311','rev':'01-040310'
            },
            'tasks':{
                #'u_un':{'type':'user','len':'24','def_value':'{_i_}','title':'کد همکار','prop':['update','show_full','un_free']},
                'u_un':{'type':'auto-x','len':'24','auto':'_cur_user_un_','title':'کد همکار'},
                'u_nm':{'type':'auto','ref':{'db':'user','tb':'user','key':'__0__','val':'{name} {family}','where':'''un = "{u_un}"'''},'title':'نام و نام خانوادگی'},
                'u_id':{'type':'auto','ref':{'db':'user','tb':'user','key':'__0__','val':'{p_id}','where':'''un = "{u_un}"'''},'title':'شماره پرسنلی'},
                'u_ml':{'type':'auto','ref':{'db':'user','tb':'user','key':'__0__','val':'{Idc_num}','where':'''un = "{u_un}"'''},'title':'کد ملی'},
                'u_li':{'type':'auto','ref':{'db':'user','tb':'user','key':'__0__','val':'{loc}','where':'''un = "{u_un}"'''},'title':'کد دفتر/پروژه'},
                'u_ln':{'type':'auto','ref':{'db':'a_loc','tb':'a','key':'__0__','val':'{name}','where':'''code = "{u_li}"'''},'title':'نام دفتر/پروژه'},
                'idea':{'type':'text','title':'شرح و نحوه اجرای پیشنهاد','height':'60px','len':'1500','markup':'md'},
                'idea_titl':{'type':'text','title':'عنوان پیشنهاد'},
                'idea_bnft':{'type':'text','title':'مزایا و نتایج پیشنهاد( ریالی / غیر ریالی) ','height':'60px','len':'1500'},
                'idea_dscr':{'type':'text','title':'توضیحات لازم','height':'60px'},
                'file1':{'type':'file','len':'40','file_name':'AQC0-KNM-SUG-{id:04d}-RP','file_ext':"jpg,pdf,txt",'path':'form,knm,sug','title':'پیوست','help':'در صورت نیاز'},
                'vrfy_rslt':{'type':'text','title':'نتیجه بررسی - نظریه کارشناسی شرکت','height':'60px'},
                'vrfy_meta':{'type':'text','title':'اقدامات انجام شده جهت بررسی','height':'60px'},
                'clnt_stf':{'type':'num','min':'1','max':'100', 'title':'میزان رضایت پیشنهاد دهنده از اقدامات انجام شده بر حسب درصد'},
                'clnt_stf_dscr':{'type':'text','title':'توضیحات در خصوص میزان رضایت'},
                'comp':{'type':'auto','auto':'مهندسان مشاور آستان قدس رضوی','title':'نام شرکت- موسسه'}
                #{'type':'text','title':'نام شرکت- موسسه','def_value':'مهندسان مشاور آستان قدس رضوی'},
            },
            'steps':{
                's0':{'tasks':'comp,u_un,u_nm,u_id,u_ml,u_li,u_ln,lable_1,idea_titl,idea,idea_bnft,file1','xjobs':'*','title':'ثبت پیشنهاد','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'lable_2,vrfy_rslt,vrfy_meta,idea_dscr','xjobs':'rda','title':'بررسی','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'clnt_stf,clnt_stf_dscr','xjobs':'#step#0','title':'نتیجه','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'all':{'input':'vrfy_rslt,vrfy_meta','view1':'idea,idea_bnft,idea_dscr','view2':'clnt_stf,clnt_stf_dscr'}
            },
            'labels':{
                'lable_1':'از اینکه با ارائه پیشنهادات مفید خود ما را در بهبود و توسعه شرکت یاری می فرمایید بسیار سپاسگذاریم',
                'lable_2':'باید تاریخ ، نام فرد و نظر فرد برای هر کدام از افراد موثر در بررسی ثبت شود',
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        },
        'in_form':{
            'base':{'mode':'form','title':'پیشنهاد اصلاحی مرتبط با فرمهای  سامانه','code':'900','rev':'00-040417',
                'help':'sg2=suggestion 2th case form (in_form)'
            },
            'tasks':{
                'f2f_id':{'type':'reference','width':'5','title':'فرم مبنا','ref':{'db':'{f2f_db}','tb':'{f2f_tb}','key':'{id}','val':'{id}'},'prop':['readonly']},
                'nn':{'type':'index','len':'2','ref':{'where':'''f2f_id = "{f2f_id}"'''},'title':'ایندکس','start':1},#,'prop':['readonly']
                'f_code':{'type':'auto','len':'8','auto':'aqrc-tqm-sg2-{{=str(id).zfill(3)}}-{f2f_db}-{f2f_tb}-{nn}','title':'کد فایل'},
                'user':{'type':'user','title':'پیشنهاد دهنده','prop':['multiple']},
                'date':{'type':'fdate','title':'تاریخ پیشنهاد','prop':['update']},
                'file_v':{'type':'file_v','len':'40','file_name':'{f_code}-v','path':'form,suggestion,in_form','title':'فایل ورودی'},
                'file_r':{'type':'file_r','len':'40','file_name':'{f_code}-r','path':'form,suggestion,in_form','title':'pdf - فایل ورودی'},
                'idea':{'type':'text','len':'128','title':'متن پیشنهاد اصلاحی'},
                
            },
            'steps':{
                '0':{'tasks':'f2f_db,f2f_tb,f2f_id','xjobs':'*','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
                '1':{'tasks':'nn,f_code,date,user,file_v,file_r,idea','xjobs':'*','title':'تکمیل','app_keys':'y','app_titls':'','oncomplete_act':''},
            },
        }
    },
    #--------------------------------------------------------------------
    'errors':{ #db
        'a':{
            'base':{'mode':'form','title':'مشکلات','code':'312'
            },
            'tasks':{
                'err_rec':{'type':'text','title':'شرح مشکل'},
                'err_des':{'type':'text','title':'توضیح'},
                'act':{'type':'text','title':'اقدام لازم'},
            },
            'steps':{
                's0':{'tasks':'lable_1,err_rec','xjobs':'*','title':'ثبت پیشنهاد','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'err_des','xjobs':'dccm','title':'بررسی','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'act','xjobs':'dccm','title':'نتیجه','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'all':{'input':'err_rec,err_des','view1':'act','view2':'act'}
            },
            'labels':{
                'lable_1':'از اینکه با ثبت مشکلات مشاهده شده در شرکت ما را در بهبود و توسعه شرکت یاری می فرمایید بسیار سپاسگذاریم',
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'eblag':{ #db
        'a':{
            'base':{'mode':'form','title':'ابلاغیه های شرکت','code':'301'
            },
            'tasks':{
                'name':{'type':'text','title':'عنوان ابلاغیه'},
                'date':{'type':'fdate','len':'10','title':'تاریخ ابلاغ'},
                'ppr_num':{'type':'text','title':'شماره نامه'},
                'f_eblag':{'type':'file','len':'40','title':'فایل ابلاغیه','file_name':'eblag-{{=str(id).zfill(4)}}-{{=date[:4]+date[5:7]+date[8:10] if date else ""}}','file_ext':"pdf,gif,jpg,jpeg,png",'path':'form,eblag'},
                'des':{'type':'text','title':'توضیح'},
                
            },
            'steps':{
                's0':{'tasks':'name,date,ppr_num','xjobs':'dcc_grp','title':'ثبت','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'f_eblag','xjobs':'dcc_grp','title':'افزودن فایل','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'des','xjobs':'dccm','title':'تکمیل','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'all':{'input':'name,date','view1':'ppr_num,f_eblag','view2':'des'}
            },
            'labels':{
                'lable_1':'از اینکه با ارائه پیشنهادات مفید خود ما را در بهبود و توسعه شرکت یاری می فرمایید بسیار سپاسگذاریم',
                'lable_2':'باید تاریخ ، نام فرد و نظر فرد برای هر کدام از افراد موثر در بررسی ثبت شود',
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #-------------------------------------------------------------------------------------------------------------------
    'km':{ #db  "knowledge management"
        'a':{
            'base':{'mode':'form','title':'فرم جمع آوری و ثبت دانش','code':'201','rev':'00-040425',
            },
            'tasks':{
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'درخواست کننده'},
                'date':{'type':'fdate','len':'10','title':'تاریخ','prop':[]},
                'kdes':{'type':'text','len':1500,'lang':'fa','title':'دانش','help':' محتوا، مسئله، تجربه یا راهکار به‌دست‌آمده','height':'100px'},
                'cat1':{'type':'select','title':'دسته بندی','help_e':'category 1',
                    'select':{
                            'TECH':'	دانش فنی	-   شامل نکات اجرایی، جزئیات طراحی، مصالح، ضوابط فنی و روش‌های بهینه فنی در پروژه‌ها',
                            'MGMT':'	دانش مدیریتی	-   تجربه‌ها و روش‌های مدیریت پروژه، مدیریت منابع، زمان، هزینه و قرارداد',
                            'PROC':'	دانش فرایندی	-   رویه‌ها، گام‌ها، ساختارها و بهینه‌سازی در فرآیندهای اداری یا پروژه‌ای',
                            'SOFT':'	دانش نرم‌افزاری	-   نکات فنی، روش استفاده، مشکلات متداول و راهکارهای مربوط به نرم‌افزارهای تخصصی',
                            'CONT':'	دانش قراردادی	-   نکات حقوقی، چالش‌های قراردادی، اسناد مناقصه، تفسیر شروط و...',
                            'DESN':'	دانش طراحی	-   مبانی، تحلیل‌ها، راهکارهای خلاقانه و تجربیات طراحی معماری و شهری',
                            'SITE':'	دانش کارگاهی	-   تجربه‌های اجرایی، خطاهای رایج، هماهنگی با پیمانکار، نظارت فاز اجرا',
                            'STDS':'	دانش استانداردها و ضوابط	-   تفسیر و کاربرد آیین‌نامه‌ها، مقررات ملی ساختمان، ضوابط شهرداری و آستان',
                            'QMGT':'	دانش مدیریت کیفیت	 -  چک‌لیست‌ها، خطاهای شایع، روش‌های کنترل کیفیت در طراحی یا نظارت',
                            'HUMN':'	دانش منابع انسانی	-   تجارب در مدیریت، آموزش، ارزیابی و ارتقاء منابع انسانی',
                            'CULT':'	دانش فرهنگی و بومی	-   آگاهی‌ها و رویکردهای مرتبط با معماری ایرانی-اسلامی، اقلیم، فرهنگ کاربران',
                            'DOCS':'	دانش مستندسازی	-   نحوه تهیه، مدیریت، نسخه‌بندی و بایگانی اسناد در سامانه DCC',
                            'INNO':'	دانش نوآورانه	-   روش‌ها یا ابزارهای جدید پیشنهادشده توسط همکاران برای بهبود عملکرد',
                            'GENL':'	دانش عمومی	-   سایر موارد دانشی که در دسته‌بندی بالا نگنجند ولی دارای ارزش ثبت هستند'
                    }},
                'file_att':{'type':'file','len':'40','file_name':'AQC0-KNM-EXP-{id:04d}-RP','file_ext':"jpg,pdf,txt",'path':'form,knm,exp','title':'پیوست','help':'مستندات در صورت نیاز'},
                'km_des':{'type':'text','len':1500,'lang':'fa','title':' توضیح km'},
                'km_res':{'type':'select','title':'سطح اثربخشی','help_e':'result','select':{'1':'محدود','2':'متوسط','3':'زیاد'},'prop':['no_empty']},

            },
            'steps':{
                's0':{'tasks':'frd_1,date,kdes,cat1,file_att','xjobs':'*','title':'مشخصات درخواست','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'km_des,km_res','xjobs':'kma','title':'ارزیابی','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
            },
            'views':{
                'all':{'input':'rd_1,date,cat1','view1':'km_des','view2':'km_res'}
            },
            'cols_filter':{
                '':'همه',
            },
            'data_filter': 
                {
                },
        }
    },
    #-------------------------------------------------------------------------------------------------------------------
    'rqst_it_srvc':{ #db  "request an IT service"
        'a':{
            'base':{'mode':'form','title':'درخواست IT','code':'201','rev':'01-040615','rev_his':'00-040425',
            },
            'tasks':{
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'درخواست کننده'},
                'date':{'type':'fdate','len':'10','title':'تاریخ وقوع مشکل','prop':[]},
                'stress':{'type':'select','title':'اولویت درخواست','select':{'0':'عادی','1':'فوری','2':'بحرانی'},'prop':['no_empty']},
                'cat1':{'type':'select','title':'دسته بندی','help_e':'category 1',
                    'select':{'HARD':'	سخت‌افزار   -	خرابی کیس، پرینتر، مانیتور، کیبورد، موس، کابل شبکه، تعویض قطعه',
                            'SOFT':'	نرم‌افزار   -	نصب/حذف نرم‌افزار، بروزرسانی، خطاهای نرم‌افزاری، کرک و لایسنس، اتوکد و Revit',
                            'NETW':'	شبکه    -	قطع ارتباط، کندی شبکه، مشکلات VPN، اتصال به سرور، سوئیچ یا روتر',
                            'SECU':'	امنیت   -	ویروس، فایروال، تغییر رمز، جلوگیری از دسترسی غیرمجاز، تنظیم مجوزها',
                            'MAIL':'	پست الکترونیک   -	ایجاد/رفع مشکل ایمیل شرکتی، تنظیم Outlook، بازیابی رمز عبور',
                            'ACCT':'	حساب‌های کاربری  -	ایجاد / غیرفعال‌سازی کاربر، تغییر سطح دسترسی، مشکلات ورود (Login)',
                            'EQUP':'	تجهیزات جدید    -	درخواست لپ‌تاپ، مانیتور، پرینتر، مودم، یو‌پی‌اس و لوازم جانبی',
                            'CNFG':'	تنظیمات / پیکربندی  -	تنظیم پرینتر شبکه، ستاپ نرم‌افزار، تغییر تنظیمات ویندوز یا اپلیکیشن‌ها',
                            'CONS':'	مشاوره و آموزش  -	درخواست آموزش ابزار جدید، مشاوره در انتخاب نرم‌افزار یا ارتقاء سیستم',
                            'SYSP':'	سامانه‌ها و نرم‌افزارهای سازمانی    - 	مشکل ورود به سامانه، خطای ثبت اطلاعات، عدم بارگذاری فرم‌ها',
                            'OTHR':'	سایر    -	درخواست‌هایی که در دسته‌های بالا نگنجد'}},
                'rqst':{'type':'text','len':2000,'lang':'fa','title':'شرح مشکل / درخواست','height':'100px'},
                #'frd_modir':{'type':'user','title':'مدیر','xjobs':'mod_mst','prop':['show_full','un_free'],'nesbat':'modir'},
                #'des_modir':{'type':'text','len':500,'lang':'fa','title':'توضیح مدیر'},
                'file_err':{'type':'file','len':'40','file_name':'AQC0-ITM-USR-ERR-{id:04d}-RP','file_ext':"jpg,png,pdf,txt,zip",'path':'form,itm,usr,err','title':'پیوست','help':'در صورت نیاز'},
                'it_des':{'type':'text','len':1500,'lang':'fa','title':'توضیح it','height':'70px;'},
                'it_res':{'type':'select','title':'وضعیت نهایی','help_e':'result','select':{'OK':'انجام شد','RJ':'در حیطه وظایف این واحد نمی باشد','HL':'هولد - نیاز مند موارد زیر'},'prop':['no_empty']},
                'fr_res':{'type':'select','title':'کفایت نتیجه','help_e':'result','select':{'2':'بله','1':'تقریبا','0':'خیر'},'prop':['no_empty']},
                'fr_r_des':{'type':'text','len':1500,'lang':'fa','title':'توضیح کفایت'},
                'fr_satf':{'type':'select','title':'رضایت از اقدامات','help_e':'result','select':{'5':'عالی','4':'خوب','3':'متوسط','2':'نیاز به بهبود','1':'ضعیف'},'prop':['no_empty']},
                'fr_s_des':{'type':'text','len':1500,'lang':'fa','title':'توضیح رضایت'},
            },
            'steps':{
                's0':{'tasks':'frd_1,date,stress,rqst','xjobs':'*','title':'مشخصات درخواست','app_keys':'','app_titls':'','oncomplete_act':''},
                #,frd_modir 's1':{'tasks':'des_modir','xjobs':'#task#frd_modir','title':'تایید مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
                's1':{'tasks':'cat1,file_err','xjobs':'#step#0','title':'اطلاعات تکمیلی','app_keys':'y,r','app_titls':['ثبت شد','بازگشت جهت اصلاح'],'oncomplete_act':''},
                's2':{'tasks':'it_res,it_des','xjobs':'ita','title':'اقدامات واحد IT','app_keys':'y,r','app_titls':['ثبت شد','بازگشت جهت اصلاح'],'oncomplete_act':''},
                's3':{'tasks':'fr_res,fr_r_des,fr_satf,fr_s_des','xjobs':'#step#0','title':'اقدامات واحد IT','app_keys':'y,r','app_titls':['ثبت شد','بازگشت جهت اصلاح'],'oncomplete_act':''}
            },
            'views':{
                'all':{'input':'rd_1,date,stress,cat1,rqst,file_err','view1':'it_res','view2':'fr_res'}
            },
            'cols_filter':{
                '':'همه',
            },
            'data_filter': 
                {
                },
        }
    },
    #--------------------------------------------------------------------time_st,time_len '"10:55","5:25"'	'auto':'{{import k_time}}{{=k_time.add("10:55","5:25")}}'},'''
    'off_morkhsi_saat':{ #db
        'a':{
            'base':{'mode':'form','title':'مرخصی ساعتی','data_filter':'f_nxt_u = "{{=_i_}}"','code':'201','internet':True,'multi_app':{'1':['snr'],'2':['mlk']},
            },
            'tasks':{
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'درخواست کننده'},
                'date':{'type':'fdate','len':'10','title':'تاریخ','prop':[]},
                'time_st':{'type':'time_c','title':'از ساعت','prop':['update'],'def_value':'07:00'},
                'time_len':{'type':'time_t','title':'به مدت','time_inf':{'maxTime':"03:30"},'prop':['update'],'def_value':'0:30'},
                'time_en':{'type':'auto','title':'تا ساعت','auto':'''{{import k_time}}{{=k_time.add(__objs__['time_st']['value'],__objs__['time_len']['value'])}}'''},
                #'frd_modir':{'type':'reference','len':'5','title':'مدیر مربوطه','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}- {m_w} {name} {family}'},'prop':['show_full']},
                'frd_modir':{'type':'user','title':'مدیر','xjobs':'mod_mst','prop':['show_full','un_free'],'nesbat':'modir'},
                'des_0':{'type':'text','len':150,'lang':'fa','title':'توضیحات',},
                'des_modir':{'type':'text','len':150,'lang':'fa','title':'توضیح'},
                'des_2':{'type':'text','len':150,'lang':'fa','title':'توضیحات'},
                'des_off':{'type':'text','len':150,'lang':'fa','title':'توضیحات'},
            },
            'steps':{
                's0':{'tasks':'frd_1,date,time_st,lable_1,time_len,time_en,frd_modir,des_0','xjobs':'*','title':'ثبت فرم توسط درخواست کننده','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'des_modir','xjobs':'#task#frd_modir','title':'تایید مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
                's3':{'tasks':'des_off','xjobs':'off_ens','title':'تطابق با ساعت دستگاه و ثبت اطلاعات','app_keys':'y,r','app_titls':['ثبت شد','بازگشت جهت اصلاح'],'oncomplete_act':''}
            },
            'views':{
                'all':{'input':'frd_1,time_st,time_len,frd_modir,des_0','view1':'des_off','view2':'des_modir'}
            },
            'labels':{
                'lable_1':'حداکثرمیزان مرخصی ساعتی مجاز 3:30 می باشد',
            },
            'cols_filter':{
                '':'همه',
                'frd_1,date,time_st,time_en,time_len,frd_modir':'جهت چاپ اداری',
            },
            'data_filter': 
                {'step_2_dt like "{{=_d_}}%"':'فرمهای نهایی شده در امروز',
                },
        }
    },
    #--------------------------------------------------------------------time_st,time_len '"10:55","5:25"'	'auto':'{{import k_time}}{{=k_time.add("10:55","5:25")}}'},'''
    'off_morkhsi_ruz':{ #db
        'a':{
            'base':{'mode':'form','title':'مرخصی روزانه','data_filter':'f_nxt_u = "{{=_i_}}"','code':'202','internet':True,'multi_app':{'1':['rms'],'2':['mlk']},
            },
            'tasks':{
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'درخواست کننده'},
                'date_st':{'type':'fdate','len':'10','title':'تاریخ شروع','prop':[]},
                'date_en':{'type':'fdate','len':'10','title':'تاریخ خاتمه','prop':[]},
                'date_len':{'type':'num','min':1,'max':30,'len':2,'lang':'fa','title':'تعداد روز'},
                'm_type':{'type':'select','title':'نوع مرخصی','select':['استحقاقی','استعلاجی','بدون حقوق','استعلاجی بدون حقوق'],'prop':['no_empty']},
                'tel_ezt':{'type':'text','title':'تلفن اضطراری','len':'13'},
                'frd_jnshn':{'type':'user','title':'جانشین','prop':['show_full','un_free']},
                'frd_modir':{'type':'user','title':'مدیر','xjobs':'mod_mst','prop':['show_full','un_free'],'nesbat':'modir'},
                'des_0':{'type':'text','len':150,'lang':'fa','title':'توضیح همکار',},
                'des_jnshn':{'type':'text','len':150,'lang':'fa','title':'توضیح جانشین'},
                'des_modir':{'type':'text','len':150,'lang':'fa','title':'توضیح مدیر'},
                'des_off':{'type':'text','len':150,'lang':'fa','title':'توضیح اداری'},
            },
            'steps':{
                's0':{'tasks':'frd_1,m_type,date_len,date_st,date_en,frd_jnshn,frd_modir,des_0','xjobs':'*','title':'ثبت فرم توسط درخواست کننده','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'des_jnshn','xjobs':'#task#frd_jnshn','title':'تایید جانشین','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
                's2':{'tasks':'des_modir','xjobs':'#task#frd_modir','title':'تایید مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
                's3':{'tasks':'des_off','xjobs':'off_ens','title':'تطابق با ساعت دستگاه و ثبت اطلاعات','app_keys':'y,r','app_titls':['ثبت شد','بازگشت جهت اصلاح'],'oncomplete_act':''}
            },
            'views':{
                'all':{'input':'frd_1,time_st,time_len,frd_modir,des_0','view1':'des_off','view2':'des_modir'}
            },
            'labels':{
            },
            'cols_filter':{
                'frd_1,m_type,date_len,date_st,date_en,frd_jnshn,frd_modir':'منتخب',
                '':'همه', 
            },
            'data_filter': 
                {'step_2_dt like "{{=_d_}}%"':'فرمهای نهایی شده در امروز',
                },
        }
    },
    #-------------------------------------------------------------------- 's2':{'tasks':'des_2','xjobs':'#step#0','title':'ثبت نتیجه','app_keys':'y,r,x','app_titls':['انجام شد','بازگشت جهت اصلاح','انجام نشد'],'oncomplete_act':''},
    'off_mamurit_saat':{ #db
        'a':{
            'base':{'mode':'form','title':'ماموریت ساعتی','data_filter':'f_nxt_u = "{{=_i_}}"','code':'203','internet':True,'multi_app':{'1':['snr'],'3':['mlk']},
            },
            'tasks':{
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'مامور'},
                'date':{'type':'fdate','len':'10','title':'تاریخ','prop':[]},
                'time_st':{'type':'time_c','title':'ساعت شروع ماموریت','prop':['update'],'def_value':'07:00'},
                'time_len':{'type':'time_t','title':'مدت ماموریت','time_inf':{'maxTime':"20:00"},'prop':['update'],'def_value':'0:30'},
                'time_en':{'type':'auto','title':'تا ساعت','auto':'''{{import k_time}}{{=k_time.add(__objs__['time_st']['value'],__objs__['time_len']['value'])}}'''},
                #'frd_modir':{'type':'reference','len':'5','title':'مدیر مربوطه','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}- {m_w} {name} {family}'},'prop':['show_full']},
                'frd_modir':{'type':'user','title':'مدیر','xjobs':'mod_mst','prop':['show_full','un_free'],'nesbat':'modir'},
                'des_0':{'type':'text','len':2000,'lang':'fa','title':'شرح ماموریت'},
                'des_modir':{'type':'text','len':150,'lang':'fa','title':'توضیح'},
                'des_2':{'type':'text','len':150,'lang':'fa','title':'توضیحات'},
                'des_off':{'type':'text','len':150,'lang':'fa','title':'توضیحات'},
                'c_prj_id':{'type':'reference','len':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update','multiple']},
                'c_prj_txt':{'type':'auto-x','len':'30','ref':'c_prj_id'},
            },
            'steps':{
                's0':{'tasks':'frd_1,date,lable_2,time_st,time_len,time_en,frd_modir,lable_1,des_0,c_prj_id,c_prj_txt','xjobs':'*','title':'ثبت فرم توسط درخواست کننده','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'des_modir','xjobs':'#task#frd_modir','title':'تایید مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
                's2':{'tasks':'time_len,time_en,des_2,c_prj_id,c_prj_txt','xjobs':'#step#0','title':'ثبت نتیجه','app_keys':'y,r,x','app_titls':['انجام شد','بازگشت جهت اصلاح','انجام نشد'],'oncomplete_act':''},
                's3':{'tasks':'des_off','xjobs':'off_ens','title':'انجام اقدامات اداری','app_keys':'y,r','app_titls':['انجام شد','بازگشت جهت اصلاح'],'oncomplete_act':''}
            },
            'views':{
                'all':{'input':'frd_1,time_st,time_len,frd_modir,des_0','view1':'des_jnshin','view2':'des_modir'}
            },
            'labels':{
                'lable_1':'محل و هدف ماموریت را ذکر بفرمایید',
                'lable_2':'در مرحله اول زمان ماموریت را به صورت حدودی وارد نمایید در مرحله سوم و پس از تایید مدیر و بازگشت از ماموریت می توانیر آنرا تدقیق نمایید',
            },
            'cols_filter':{
                '':'همه',
                'frd_1,date,time_st,time_en,time_len,frd_modir':'جهت چاپ اداری',
            },
            'data_filter': 
                {'step_3_dt like "{{=_d_}}%"':'فرمهای نهایی شده در امروز',
                },
        }
    },
    #--------------------------------------------------------------------time_st,time_len '"10:55","5:25"'	'auto':'{{import k_time}}{{=k_time.add("10:55","5:25")}}'},'''
    'off_mamurit_ruz':{ #db
        'a':{
            'base':{'mode':'form','title':'ماموریت روزانه',
                'data_filter':'f_nxt_u = "{{=_i_}}"','code':'204','internet':True,'multi_app':{'1':['rms'],'2':['mlk']},
            },
            'tasks':{
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'درخواست کننده'},
                'date_st':{'type':'fdate','len':'10','title':'تاریخ شروع','prop':[]},
                'date_en':{'type':'fdate','len':'10','title':'تاریخ خاتمه','prop':[]},
                'date_len':{'type':'num','min':1,'max':30,'len':2,'lang':'fa','title':'تعداد روز'},
                'm_type':{'type':'select','title':'نوع درخواست','select':['صدور حکم ماموریت','تمدید ماموریت'],'prop':['no_empty'],},
                'tel_ezt':{'type':'text','title':'تلفن همراه','len':'13'},
                'adrs_frd':{'type':'text','len':150,'lang':'fa','title':'آدرس قرار','help':'محل سوار شدن'},
                'c_prj_id':{'type':'reference','len':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update','multiple']},
                'c_prj_txt':{'type':'auto-x','len':'30','ref':'c_prj_id'},
                'adrs_prj':{'type':'text','len':150,'lang':'fa','title':'آدرس مقصد','help':'آدرس مقصد'},
                'frd_modir':{'type':'user','title':'مدیر','xjobs':'mod_mst','prop':['show_full','un_free'],'nesbat':'modir'},
                'des_0':{'type':'text','len':150,'lang':'fa','title':'توضیح همکار',},
                'des_modir':{'type':'text','len':150,'lang':'fa','title':'توضیح مدیر'},
                'des_off':{'type':'text','len':150,'lang':'fa','title':'توضیح اداری'},
                'des_mdr_aml':{'type':'text','len':150,'lang':'fa','title':'توضیح مدیر عامل'},
                'vsl_ngl':{'type':'check','title':'نیاز به وسیله نقلیه'},
                
            },
            'steps':{
                's0':{'tasks':'frd_1,m_type,date_len,date_st,date_en,tel_ezt,adrs_frd,c_prj_id,c_prj_txt,adrs_prj,frd_modir,des_0','xjobs':'*','title':'ثبت فرم توسط درخواست کننده','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'des_modir','xjobs':'#task#frd_modir','title':'تایید مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
                's2':{'tasks':'des_off','xjobs':'off_ens','title':'انجام اقدامات اداری','app_keys':'y,r','app_titls':['ثبت شد','بازگشت جهت اصلاح'],'oncomplete_act':''}
            },
            'views':{
                'all':{'input':'frd_1,time_st,time_len,frd_modir,des_0','view1':'des_off','view2':'des_modir'}
            },
            'labels':{
                'lbl_1':''
            },
            'cols_filter':{
                'frd_1,m_type,date_len,date_st,date_en,frd_jnshn,frd_modir':'منتخب',
                '':'همه', 
            },
            'data_filter': 
                {'step_2_dt like "{{=_d_}}%"':'فرمهای نهایی شده در امروز',
                },
        }
    },
    #-------------------------------------------------------------------- 's2':{'tasks':'des_2','xjobs':'#step#0','title':'ثبت نتیجه','app_keys':'y,r,x','app_titls':['انجام شد','بازگشت جهت اصلاح','انجام نشد'],'oncomplete_act':''},
    'rep_mamurit':{ #db msr=mission-report  
        'a':{
            'base':{'mode':'form','title':'گزارش ماموریت','rev':'01-040325',
                'data_filter':'f_nxt_u = "{{=_i_}}"','code':'207','xform_cg_file':'fr-cg-rep_mamurit.html','multi_app':{'1':['snr'],'3':['mlk']},
            },
            'tasks':{
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'مامور'},
                'u_li':{'type':'auto','ref':{'db':'user','tb':'user','key':'__0__','val':'{loc}','where':'''un = "{frd_1}"'''},'title':'کد دفتر/پروژه'},
                'u_ln':{'type':'auto','ref':{'db':'a_loc','tb':'a','key':'__0__','val':'{name}','where':'''code = "{u_li}"'''},'title':'نام دفتر/پروژه'},
                'date':{'type':'fdate','len':'10','title':'تاریخ','prop':[]},
                'c_prj_id':{'type':'reference','len':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update','multiple']},
                'c_prj_txt':{'type':'auto-x','len':'30','ref':'c_prj_id'},
                'prj_name':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_name}','where':'id = "{c_prj_id}"'},'title':'نام پروژه'},
                'prj_code':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_code}','where':'id = "{c_prj_id}"'},'title':'کد پروژه','prop':['hidden','update']},
                'code_sn':{'type':'index','len':'3','ref':{'db':'rep_mamurit','tb':'a','key':'{id}','val':'{code_sn}','where':"prj_code = '{prj_code}'"},'title':'شماره','prop':['update'],'start':1},
                'code':{'type':'auto','len':'8','auto':'aqrc-tqm-fr-msr-{{=date[:4]+date[5:7]+date[8:10] if date else "000000"}}-{{=str(id).zfill(4)}}','title':'کد پشتیبان'},
                'stn_code':{'type':'auto','len':'8','auto':'{prj_code}-_D-{{=date[2:4]+date[5:7]+date[8:10] if date else "000000"}}-MSR-{code_sn}-{{=str(id).zfill(5)}}','title':'کد فایل'},
                'report':{'type':'text','len':5000,'lang':'fa','title':'شرح ماموریت','height':'300px'},
                'frd_modir':{'type':'user','title':'مدیر','xjobs':'mod_mst','prop':['show_full','un_free'],'nesbat':'modir'},        
                'des_modir':{'type':'text','len':150,'lang':'fa','title':'توضیح'},
               
            },
            'steps':{
                's0':{'tasks':'frd_1,date,frd_modir,c_prj_id,c_prj_txt,prj_name,prj_code,code_sn,code,stn_code,report','xjobs':'*','title':'ثبت فرم توسط همکار','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'des_modir','xjobs':'#task#frd_modir','title':'تایید مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
            },
            'views':{
                'all':{'input':'frd_1,time_st,frd_modir','view1':'time_en','view2':'des_modir'}
            },
            'labels':{
            },
            'cols_filter':{
                'frd_1,date,frd_modir,c_prj_id,c_prj_txt':'-',
                '':'همه',
            },
            'data_filter': 
                {
                },
        }
    },
    #-------------------------------------------------------------------- 's2':{'tasks':'des_2','xjobs':'#step#0','title':'ثبت نتیجه','app_keys':'y,r,x','app_titls':['انجام شد','بازگشت جهت اصلاح','انجام نشد'],'oncomplete_act':''},
    'hr_arzyabi_amalkard':{ #db
        'a':{
            'base':{'mode':'form','title':'ارزشیابی عملکرد پرسنل','data_filter':'f_nxt_u = "{{=_i_}}"','code':'801','internet':True,'xform_cg_file':'hr_arzyabi_amalkard-st.html',
            },
            'tasks':{
                'frd_1':{'type':'user','title':'نام همکار','prop':['show_full','p_id','un_free'],},
                'job':{'type':'text','len':150,'lang':'fa','title':'پست سازمانی'},
                'c_prj_id':{'type':'reference','len':'30','value_show_case':True,
                    'ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update','multiple']},
                'cp_name':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_name}','where':'''id = "{{=__objs__['c_prj_id']['value']}}"'''},'title':'--'},
                'loc':{'type':'reference','title':'کد محل کار','ref':{'db':'a_loc','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'loc_name':{'type':'auto','ref':{'db':'a_loc','tb':'a','key':'__0__','val':'{name}','where':'''code = "{{=__objs__['loc']['value']}}"'''},'title':'نام پروژه و محل کار'},
                'frd_modir':{'type':'user','title':'مدیر','xjobs':'mod_mst','prop':['show_full','un_free'],},
                'frd_mvn':{'type':'user','title':'معاون','xjobs':'mvn_ha','prop':['show_full','un_free'],},
                'sal':{'type':'select','title':'تمدید قرارداد برای سال','select':['1404','1405','1406'],'prop':['no_empty'],},
                'dur_1':{'type':'select','title':'میزان تمدید قرارداد','select':{'12':'1 سال','6':'6 ماه','3':'3 ماه','0':'عدم تمدید'},'prop':['no_empty'],},
                'des_1':{'type':'text','len':150,'lang':'fa','title':'نظر معاون'},
                'des_2':{'type':'text','len':150,'lang':'fa','title':'نظر مدیر عامل'},
                'des_3':{'type':'text','len':150,'lang':'fa','title':'نظر حراست'},
                'an1':{'type':'select','title':'امتیاز - دانش','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad1':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an2':{'type':'select','title':'امتیاز - تعهد','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad2':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                
                'an3':{'type':'select','title':'امتیاز - دقت','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad3':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an4':{'type':'select','title':'امتیاز - نظم','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad4':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                
                'an5':{'type':'select','title':'امتیاز - کار گروهی','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad5':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an6':{'type':'select','title':'امتیاز - اخلاق','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad6':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},

                'an7':{'type':'select','title':'امتیاز - فن آوری','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad7':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an8':{'type':'select','title':'امتیاز - بهبود مداوم','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad8':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                
                'an9':{'type':'select','title':'امتیاز - استاندارد فنی','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad9':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an10':{'type':'select','title':'امتیاز - مقررات','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad10':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an_sum':{'type':'auto','auto':'{{=sum([int(x) for x in [an1,an2,an3,an4,an5,an6,an7,an8,an9,an10]])}}','title':'مجموع امتیاز'},
                
            },
            'steps':{
                's0':{'tasks':'frd_1,loc,frd_modir,loc_name,sal,job',
                    'xjobs':'off_ens,dccm','title':'ارسال فرم برای مدیر مربوطه','app_keys':'y','app_titls':'','oncomplete_act':'',
                    'step_cols_width':'6,6','task_cols_width':'4,8,0'},
                's1':{'tasks':"lb01,lb02,lb03,lb1,an1,ad1,lb2,an2,ad2,lb3,an3,ad3,lb4,an4,ad4,lb5,an5,ad5,lb6,an6,ad6,lb7,an7,ad7,lb8,an8,ad8,lb9,an9,ad9,lb10,an10,ad10,lb_sum,an_sum,lb_s2",   
                    'xjobs':'#task#frd_modir','title':'امتیاز دهی توسط مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':'',
                    'step_cols_width':'5,3,4','task_cols_width':'0,12,0',
                    'auth':'#task#frd_modir,off_ens,mdr_aml,hrst_adm,#task#frd_mvn,dccm',},
                's2':{'tasks':'dur_1','xjobs':'#task#frd_modir','title':'تکمیل اطلاعات توسط مدیر','app_keys':'y,r',
                    'oncomplete_act':'',
                    'auth':'#task#frd_modir,off_ens,mdr_aml,hrst_adm,#task#frd_mvn,dccm',},
                's3':{'tasks':'loc,loc_name,frd_mvn','xjobs':'off_ens','title':'بررسی و ارسال برای معاونت','app_keys':'y,r,x',
                    'auth':'#task#frd_modir,off_ens,mdr_aml,hrst_adm,#task#frd_mvn,dccm'},
                's4':{'tasks':'des_1','xjobs':'#task#frd_mvn','title':'بررسی توسط معاونت','app_keys':'y,r',
                    'auth':'#task#frd_modir,off_ens,mdr_aml,hrst_adm,#task#frd_mvn,dccm'},
                's5':{'tasks':'des_2','xjobs':'mdr_aml','title':'بررسی توسط مدیر عامل','app_keys':'y,r',
                    'auth':'#task#frd_modir,off_ens,mdr_aml,hrst_adm,#task#frd_mvn,dccm'},
                's6':{'tasks':'des_3','xjobs':'hrst_adm','title':'بررسی توسط حراست','app_keys':'y,r',
                      'start_step':'5','start_where':"'{step_5_ap}' == 'y'",'end_where':"False",
                      'auth':'#task#frd_modir,off_ens,mdr_aml,hrst_adm,#task#frd_mvn,dccm'},
                'b':{'tasks':'job','xjobs':'dccm','title':'-','app_keys':'y,x','app_titls':'','oncomplete_act':'',
                        'name':'b','auth':'dccm','start_step':'0','start_where':"'{step_0_ap}' == 'y'",'end_where':"False"},
                
            },
            'views':{
                'all':{'input':'frd_1','view1':'job','view2':'job'}
            },
            'labels':{
                'lb01':'عنوان',
                'lb02':'امتیاز',
                'lb03':'توضیح',
                'lb1':'توانایی و دانش تخصص در انجام امور محوله',
                'lb2':'تعهد حس مسئولیت پذیری و امانتداری و اعتماد در امور محوله',
                'lb3':'میزان تسلط و دقت در انجام وظایف و اختیارات شغلی و یافتن روشهایی جهت ارائه بهتر خدمات',
                'lb4':'رعایت نظم و مقررات سلسله مراتب اداری، ورود و خروج منظم',
                'lb5':'توانایی انجام کار گروهی و میزان مشارکت در انجام امور محوله با دیگر همکاران',
                'lb6':'رعایت ظواهر و شئونات اسلامی و اخلاقی و اداری',
                'lb7':'توانایی شناسایی، بهره گیری، کنترل و استفاده از ابزارها و فناوری های جدید در امور شغلی',	
                'lb8':'میزان بکارگیری مهارت های شغلی کسب شده در انجام وظایف و مشارکت در دوره های آموزشی شرکت',
                'lb9':'آشنایی با بخشنامه ها، آئین نامه ها و مقررات ملی ساختمان در حوزه وظایف محوله',
                'lb10':'رعایت های استاندارد های مدیریت کیفیت و تعالی و مستند سازی ابلاغی از شرکت',
                'lb_sum':'مجموع امتیازات',
                'lb_s2':'----',
            },
            'cols_filter':{
                '':'همه',
                'frd_1,loc_name,frd_modir,an1,an2,an3,an4,an5,an6,an7,an8,an9,an10,an_sum':'منتخب 1',
                'frd_1,loc_name,frd_modir,an1,ad1,an2,ad2,an3,ad3,an4,ad4,an5,ad5,an6,ad6,an7,ad7,an8,ad8,an9,ad9,an10,ad10,an_sum,dur_1':'منتخب 2',
            },
            'data_filter': 
                {'step_0_un = "{{=_i_}}" or step_1_un = "{{=_i_}} or step_4_un = "{{=_i_}}" or step_5_un = "{{=_i_}}" or step_6_un = "{{=_i_}}"':'فرمهای تکمیل شده توسط من',
                },
        }
    },
    #-------------------------------------------------------------------- 's2':{'tasks':'des_2','xjobs':'#step#0','title':'ثبت نتیجه','app_keys':'y,r,x','app_titls':['انجام شد','بازگشت جهت اصلاح','انجام نشد'],'oncomplete_act':''},
    'hr_arzyabi_amalkard_mdr':{ #db
        'a':{
            'base':{'mode':'form','title':'ارزشیابی عملکرد مدیران','data_filter':'f_nxt_u = "{{=_i_}}"','code':'802','internet':True,'xform_cg_file':'hr_arzyabi_amalkard_mdr.html',
            },
            'tasks':{
                'frd_1':{'type':'user','title':'نام همکار','xjobs':'mod_mst','prop':['show_full','p_id','un_free'],},
                'frd_modir':{'type':'user','title':'مدیر','xjobs':'mod_mst','prop':['show_full','un_free'],},
                'sal':{'type':'select','title':'تمدید قرارداد برای سال','select':['1404','1405','1406'],'prop':['no_empty'],},
                'dur_1':{'type':'select','title':'میزان تمدید قرارداد','select':{'12':'1 سال','6':'6 ماه','3':'3 ماه','0':'عدم تمدید'},'prop':['no_empty'],},
                'des_0':{'type':'text','len':150,'lang':'fa','title':'توضیح'},
                'des_1':{'type':'text','len':150,'lang':'fa','title':'جمع بندی'},
                'des_2':{'type':'text','len':150,'lang':'fa','title':'نظر مدیر عامل'},
                'des_3':{'type':'text','len':150,'lang':'fa','title':'نظر حراست'},
                'loc':{'type':'reference','title':'کد محل کار','ref':{'db':'a_loc','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'loc_name':{'type':'auto','ref':{'db':'a_loc','tb':'a','key':'__0__','val':'{name}','where':'''code = "{{=__objs__['loc']['value']}}"'''},'title':'نام پروژه و محل کار'},
                'an1':{'type':'select','title':'امتیاز – کیفیت','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad1':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an2':{'type':'select','title':'امتیاز – صرفه جویی','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad2':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},

                'an3':{'type':'select','title':'امتیاز – مشارکت','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad3':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an4':{'type':'select','title':'امتیاز – استمرار','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad4':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                
                'an5':{'type':'select','title':'امتیاز – فن آوری','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad5':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an6':{'type':'select','title':'امتیاز – ارزشیابی','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad6':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},

                'an7':{'type':'select','title':'امتیاز – ایده','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad7':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an8':{'type':'select','title':'امتیاز – اخلاق','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad8':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                
                'an9':{'type':'select','title':'امتیاز – مشورت','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad9':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an10':{'type':'select','title':'امتیاز – حل مساله','prop':['update','no_empty'],'def_value':'8','value_show_case':True,
                    'select':{'10':'عالی - 10','9':'خوب - 9','8':'متوسط - 8','7':'نیاز به بهبود - 7','6':'ضعیف - 6'}},
                'ad10':{'type':'text','len':150,'lang':'fa','title':'توضیحات '},
                'an_sum':{'type':'auto','auto':'{{=sum([int(x) for x in [an1,an2,an3,an4,an5,an6,an7,an8,an9,an10]])}}','title':'مجموع امتیاز'},
                
            },
            'steps':{
                's0':{'tasks':'frd_1,frd_modir,loc,loc_name,sal,des_0',
                    'xjobs':'off_ens,dccm','title':'ارسال فرم برای مدیر مربوطه','app_keys':'y','app_titls':'','oncomplete_act':'',
                    'step_cols_width':'6,6','task_cols_width':'4,8,0'},
                's1':{'tasks':"lb01,lb02,lb03,lb1,an1,ad1,lb2,an2,ad2,lb3,an3,ad3,lb4,an4,ad4,lb5,an5,ad5,lb6,an6,ad6,lb7,an7,ad7,lb8,an8,ad8,lb9,an9,ad9,lb10,an10,ad10,lb_sum,an_sum,lb_s2",   
                    'xjobs':'#task#frd_modir','title':'امتیاز دهی توسط مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':'',
                    'step_cols_width':'5,3,4','task_cols_width':'0,12,0','auth':'#task#frd_modir,off_ens,mdr_aml,hrst_adm,#task#frd_mvn',},
                's2':{'tasks':'des_1,dur_1','xjobs':'#task#frd_modir','title':'تکمیل اطلاعات توسط مدیر','app_keys':'y,r',
                    'oncomplete_act':'','auth':'#task#frd_modir,off_ens,dccm,mdr_aml,hrst_adm'},
                's3':{'tasks':'loc,loc_name,sal','xjobs':'off_ens','title':'بررسی و ارسال برای معاونت','app_keys':'y,r,x'
                    ,'auth':'#task#frd_modir,off_ens,dccm,mdr_aml,hrst_adm'},
                's4':{'tasks':'des_2','xjobs':'mdr_aml','title':'بررسی توسط مدیر عامل','app_keys':'y,r'
                    ,'auth':'#task#frd_modir,off_ens,dccm,mdr_aml,hrst_adm'},
                's5':{'tasks':'des_3','xjobs':'hrst_adm','title':'بررسی توسط حراست','app_keys':'y,r',
                    'start_step':'4','start_where':"'{step_4_ap}' == 'y'",'end_where':"False"
                    ,'auth':'#task#frd_modir,off_ens,dccm,mdr_aml,hrst_adm'},
                'b':{'tasks':'sal','xjobs':'dccm','title':'-','app_keys':'y,x','app_titls':'','oncomplete_act':'',
                        'name':'b','auth':'dccm','start_step':'0','start_where':"'{step_0_ap}' == 'y'",'end_where':"False"},
                
            },
            'views':{
                'all':{'input':'frd_1','view1':'job','view2':'job'}
            },
            'labels':{
                'lb01':'عنوان',
                'lb02':'امتیاز',
                'lb03':'توضیح',
                'lb1':'ارائه ساز و كار مناسب جهت بهبود كيفيت و تسريع خدمت',
                'lb2':'صرفه‌جويي و كاهش هزينه‌هاي واحد تحت مديريت',
                'lb3':'مشاركت مؤثر و همراهي در اجراي برنامه ها',
                'lb4':'ارزيابي مستمر و منظم از پيشرفت امور در واحدهای زیر مجموعه',
                'lb5':'به کارگيري روشهاي جديد فن آوري اطلاعات درانجام‌وظايف شرکت',
                'lb6':'ارزشيابي دقيق کارکنان و تعيين نقاط قوت و ضعف آنها',
                'lb7':'توان ارائه و اجراي ايده هاي بديع و نو جهت افزايش بهره وري در واحهای زیر مجموعه',
                'lb8':'گسترش ارزشهاي اخلاقي و انضباط اداري درمحيط کار',
                'lb9':'مشورت و جلب مشارکت کارکنان در تصميم‌گيريهاي مديريتي',
                'lb10':'توان حل مسائل بخش مربوطه',
                'lb_sum':'مجموع امتیازات',
                'lb_s2':'----',
            },
            'cols_filter':{
                '':'همه',
                'frd_1,frd_modir,an1,an2,an3,an4,an5,an6,an7,an8,an9,an10,an_sum':'منتخب 1',
                'frd_1,frd_modir,an1,ad1,an2,ad2,an3,ad3,an4,ad4,an5,ad5,an6,ad6,an7,ad7,an8,ad8,an9,ad9,an10,ad10,an_sum,dur_1,des_1':'منتخب 2',
            },
            'data_filter': 
                {'step_0_un = "{{=_i_}}" or step_1_un = "{{=_i_}} or step_4_un = "{{=_i_}}" or step_5_un = "{{=_i_}}" or step_6_un = "{{=_i_}}"':'فرمهای تکمیل شده توسط من',
                },
        }
    },
    #-------------------------------------------------------------------- 
    'hr_arzyabi_amuzesh':{ #db
        'a':{
            'base':{'mode':'form','title':'ارزیابی دوره های آموزشی توسط پرسنل','data_filter':'f_nxt_u = "{{=_i_}}"','code':'801','internet':True,'prop':['noname'],
            },
            'tasks':{
                'hmkr':{'type':'text','title':'نام و نام خانوادگی همکار','len':150,'lang':'fa',},
                'h_des':{'type':'text','title':'توضیحات','lang':'fa','height':"60px"},
                'date':{'type':'fdate','title':'تاریخ آموزش'},
                'edu_id':{'type':'reference','title':'دوره',
                    'ref':{'db':'amuzesh','tb':'a','key':'{id}','val':'{date}-{tchr_name}-{subj}'},'prop':['update'],
                    'team':{'date':{'val':'{date}','title':'تاریخ'},'tchr_name':{'val':'{tchr_name}','title':'نام استاد'}
                        ,'subj':{'val':'{subj}','title':'موضوع'}},},

                'an1':{'type':'select','title':'تازگی','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}},
                'an2':{'type':'select','title':'کاربرد','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}},         
                'an3':{'type':'select','title':'جزوه','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'عدم ارائه جزوه - 1'}}, 
                'an4':{'type':'select','title':'ساختار','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}},  
                'an5':{'type':'select','title':'بیان','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}},  
                'an6':{'type':'select','title':'رهبری','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}},   
                'an7':{'type':'select','title':'دانش','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}},  
                'an8':{'type':'select','title':'پاسخ','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}},  
                'an_s1':{'type':'auto','auto':'{{=int(sum([int(x)-1 for x in [an1,an2,an3,an4,an5,an6,an7,an8]])*3.125)}}','title':'استاد'},
                'an21':{'type':'select','title':'محیط','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}},  
                'an22':{'type':'select','title':'نظم','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}}, 
                'an23':{'type':'select','title':'پذیرایی','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}},
                'an24':{'type':'select','title':'امکانات','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'عالی - 5','4':'خوب - 4','3':'متوسط - 3','2':'ضعیف - 2','1':'خیلی ضعیف - 1'}},
                'an_s2':{'type':'auto','auto':'{{=int(sum([int(x)-1 for x in [an21,an22,an23,an24]])*3.125)}}','title':'شرکت'},
            },
            'steps':{
                's0':{'tasks':'edu_id,date,tchr_name,subj,lb_t1,lb_t2,lb_d1,lb_l,lb1,an1,lb2,an2,lb3,an3,lb4,an4,lb5,an5,lb6,an6,lb7,an7,lb8,an8,lb_s1,an_s1,lb_d2,lb_l,lb21,an21,lb22,an22,lb23,an23,lb24,an24,lb_s2,an_s2,lb_hmkr,hmkr,lb_h_des,h_des',
                    'xjobs':'*','title':'ارزیابی دوره آموزشی توسط شرکت کنندگان','app_keys':'y','app_titls':'','oncomplete_act':'',
                    'step_cols_width':'6,6','task_cols_width':'4,8,0',
                    'header':'''
                    <H4 class="text-center bg-white"> این فرم محرمانه می باشد </H4>
                    <h5 class="text-center" style="background-color: #f2f2f2;">
                    به منظور بهبود بخشيدن به كلاسها ودوره‌هاي آموزشي و در نتيجه استفاده مطلوبتر پرسنل از اين گونه كلاسها 
                    خواهشمنداست به سئوالات زير به دقت پاسخ دهيد. بديهي است پاسخ نامه شماتاثير مستقيم درچگونگي برگزاري كلاسهاي آموزشي خواهد داشت
                    </h5>
                    ''',
                    'footer':''},
            },
            'views':{
                'all':{'input':'hmkr','view1':'date','view2':'date'}
            },
            'labels':{
                'lb_l':'<div style="background-color: #fff;color:#000;">-------------------</div>',
                'lb_d1':'<div style="background-color: #fff;color:#000;">امتیاز دهی به استاد</div>',
                'lb_d2':'<div style="background-color: #fff;color:#000;">امتیاز دهی به شرکت</div>',
                'lb_t1':'عنوان',
                'lb_t2':'امتیاز',
                'lb1':'تازگي مطالب',
                'lb2':'کاربردی بودن مطالب',
                'lb3':'كيفيت‌ومحتواي‌جزوات‌',
                'lb4':'پيوستگي وطبقه بندي مطالب',
                'lb5':'قدرت بيان وتفهيم مطالب توسط استاد',
                'lb6':'روش اداره كلاس وميزان علاقه استاد به تدريس',
                'lb7':'تسلط استاد به موضوع',
                'lb8':'قدرت وحوصله استاد در جوابگويي ',
                'lb21':'محيط آموزش',
                'lb22':'نظم وانضباط دربموقع برگزار شدن كلاس ',
                'lb23':'نحوه  پذيرايي',
                'lb24':'امكانات آموزشي ( وايت برد ،ويدئو،……..)',
                'lb_s1':'''<div style="background-color: #ff0;color:#000;">مجموع امتیازات استاد - 0 تا 100</div>''',
                'lb_s2':'''<div style="background-color: #ff0;color:#000;">مجموع امتیازات شرکت - 0 تا 50</div>''',
                'lb_hmkr':'''<div style="background-color: #fff;color:#000;">در صورت تمایل نام خود را  ذکر بفرمایید</div>''',
                'lb_h_des':'''<div style="background-color: #fff;color:#000;">پیشنهادات - انتقادات و یا سایر توضیحات</div>''',
            },
            'cols_filter':{
                '':'همه',

            },
            'data_filter': {
                
                },
        }
    },
    #--------------------------------------------------------------------
    'tel':{ #db
        'a':{
            'base':{'mode':'form','title':'دفترچه تلفن شرکت','code':'203'
            },
            'tasks':{
                'm_w':{'type':'select','select':['آقای','خانم'],'title':'جنسیت'},
                'pre_n':{'type':'select','select':['','مهندس','دکتر'],'title':'پیش نام'},
                'name':{'type':'text','title':'نام','len':'15'},
                'family':{'type':'text','title':'فامیل','len':'35'},
                'tel_mob':{'type':'text','title':'موبایل','len':'13'},
                'tel_wrk':{'type':'text','title':'تلفن','len':'10','placeholder':"....-..-.."},
                'job':{'type':'text','title':'سمت','len':'40'},
                'com':{'type':'text','title':'شرکت / سازمان','len':'40'},
                'des':{'type':'text','title':'توضیحات','len':'250'},
            },
            'steps':{
                's0':{'tasks':'m_w,pre_n,name,family,tel_mob,tel_wrk,com,job,des','xjobs':'*','title':'ثبت فرم توسط درخواست کننده','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'m_w,pre_n,name,family,tel_mob,tel_wrk,job,des','view1':'family','view2':'family'}
            },
            'cols_filter':{'':'همه',},
            'data_filter': {},
         }
    },
    #-------------------------------------------------------------------------------------------------------------------

    #--------------------------------------------------------------------
    'amuzesh':{ #db
        'a':{
            'base':{'mode':'form','title':'آموزش','code':'304',
                },
            'tasks':{
                'subj':{'type':'text','title':'موضوع','len':'255','hlp':'عنوانی که کلاس به آن مرتبط میباشد'},
                'for_grup':{'type':'text','title':'مناسب برای گروه','len':'50','hlp':'کلاس برای چه گروه هایی مناسب است و در نظر گرفته شده است'},
                'tchr_name':{'type':'text','title':'مدرس','len':'50','hlp':'کلاس برای چه گروه هایی مناسب است و در نظر گرفته شده است'},
                'tchr_exprt':{'type':'text','title':'تخصص مدرس','len':'50','hlp':'کلاس برای چه گروه هایی مناسب است و در نظر گرفته شده است'},
                'date':{'type':'fdate','title':'تاریخ برگزاری','prop':['update']},
                'time_len':{'type':'time_t','title':'به مدت','time_inf':{'maxTime':"10:00"},'def_value':'02:00'},
                'pos':{'type':'text','title':'مکان برگزاری','len':'50'},
                'cls_mod':{'type':'select','select':['حضوری','مجازی'],'title':'نوع برگزاری'},
                'cls_org':{'type':'text','title':'برگزار شده توسط','len':'50','hlp':'کدام قسمت هماهنگی های برگزاری را انجام داده است'},
                'user_n':{'type':'num','len':3,'min':1,'max':150,'title':'تعداد شرکت کنندگان','hlp':'از پرسنل شرکت'},
                'file_code':{'type':'auto','len':'25','auto':'AQRC-HRM-ED-{{=__objs__["date"]["stnd6"]}}-{{=str(id).zfill(5)}}','title':'کد فایلها'},
                'usr_cmnt_file':{'type':'file','len':'40','title':'فایل نظر سنجی','hlp':'جمع بندی و نمودار شده',
                    'file_name':'{file_code}_ucmn','file_ext':"pdf",'path':'form,hrm,ed'},
                'cls_form_file':{'type':'file','len':'40','title':'فرم حاضرین','hlp':'تصویر اسکن شده از امضاها',
                    'file_name':'{file_code}_cfrm','file_ext':"pdf",'path':'form,hrm,ed'},
                'usr_cert_file':{'type':'file','len':'40','title':'گواهینامه ها','hlp':'جمع بندی و نمودار شده',
                    'file_name':'{file_code}_ucrt','file_ext':"pdf",'path':'form,hrm,ed'},
                'cls_lrn_file':{'type':'file','len':'40','title':'محتوای آموزش','hlp':'فایل اصلی ارائه شده',
                    'file_name':'{file_code}_clrn','file_ext':"pdf",'path':'form,hrm,ed'},
                'news_link':{'type':'text','title':'لینک خبر','len':'255','hlp':'پوشش ارتباطات و رسانه'},
                'news_file':{'type':'file','len':'40','title':'فایل خبر','hlp':'فایل کلیه خبر ها به صورت 1 فایل PDF',
                    'file_name':'{file_code}_news','file_ext':"pdf",'path':'form,hrm,ed'},
                'pics_file':{'type':'file','len':'40','title':'فایل تصویر',
                    'file_name':'{file_code}_pics','file_ext':"zip,rar,7z",'path':'form,hrm,ed'},
                },
            'steps':{
                'pre':{'tasks':'subj,for_grup,tchr_name,tchr_exprt','xjobs':'edu','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'date,time_len,pos,cls_mod,cls_org,file_code','xjobs':'edu','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'user_n,usr_cmnt_file,cls_form_file,usr_cert_file,cls_lrn_file,news_link,news_file,pics_file','xjobs':'edu','title':'تکمیل','app_keys':'y,r','app_titls':'','oncomplete_act':'','auth':'edu,dccm'},#'xjobs':'#task#un,dccm',
            },
            'views':{
                },
            'cols_filter':{
                '':'همه',
                'subj,for_grup,tchr_name,date,time_len,cls_mod':'لیست 1',
                },
            'data_filter':{
                '':'همه همکاران',
                'cls_mod = "حضوری"':'حضوری',
                'cls_mod = "مجازی"':'مجازی',
                },
        }
    },
    #--------------------------------------------------------------------
    'news':{ #db
        'a':{
            'base':{'mode':'form','title':'اخبار','code':'304',
                },
            'tasks':{
                'date':{'type':'fdate','title':'تاریخ','prop':['update']},
                'title':{'type':'text','title':'عنوان خبر','len':'250'},
                'txt':{'type':'text','title':'متن خبر','len':'2500'},
                'pos':{'type':'text','title':'مکان خبر','len':'250'},
                'imgs':{'type':'f2f','len':'60','title':'تصاویر','ref':{'tb':'imgs','show_cols':['file']},},
                'link':{'type':'text','title':'لینک خبر','len':'80','link':{'target':'_blank','text':'L','class':'btn btn-info'},},
                'imp_g':{'type':'select','title':'اهمیت','prop':['update','no_empty'],'def_value':'3','value_show_case':True,
                    'select':{'5':'5 - فوری و حیاتی','4':'4 - مهم','3':'3 - اهمیت متوسط','2':'2 - اهمیت کم','1':'1 - اطلاع عمومی'}},
                },
            'steps':{
                'pre':{'tasks':'date,title,pos','xjobs':'dcc_grp','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'txt','xjobs':'dcc_grp','title':'متن','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'imgs,link,lb01,lb02,lb03,lb04,lb05,imp_g','xjobs':'dcc_grp','title':'فراداده ها','app_keys':'y,r','app_titls':'','oncomplete_act':''},#'xjobs':'#task#un,dccm',
                },
            'labels':{
                'lb01':'1	اطلاع عمومی (General Info)	اخبار غیرحیاتی، صرفاً جهت اطلاع‌رسانی عمومی',
                'lb02':'2	اهمیت کم (Low Priority)	اخبار کم‌اهمیت که تأثیر محدودی بر عملکرد شرکت دارند',
                'lb03':'3	اهمیت متوسط (Moderate)	اخبار با تأثیر متوسط که نیاز به توجه یا اقدام محدود دارند',
                'lb04':'4	مهم (Important)	اخبار مهم که بر روند کار یا تصمیم‌گیری‌ها اثر مستقیم دارند',
                'lb05':'5	فوری و حیاتی (Critical)	اخبار بسیار مهم و فوری که نیاز به اقدام فوری دارند و تأثیر گسترده دارند',
                },
            'views':{
                },
            'cols_filter':{
                '':'همه',
                },
            'data_filter':{
                },
        },
        'imgs':{
            'base':{'mode':'form','title':'تصاویر- اخبار','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','len':'5','title':'فرم مبنا','ref':{'tb':'a','key':'{id}','val':'{date} , {title}'},'prop':['readonly']},
                'file':{'type':'file','len':'40','file_name':'AQC0-PRD-NEWS-IMG-{id:04d}-{f2f_id}','file_ext':"jpg",'path':'form,prd,news,img','title':'تصویر خبر'},
            },
            'steps':{
                #'pre':{'tasks':'f2f_id,file','xjobs':'dcc_grp','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                '0':{'tasks':'f2f_db,f2f_tb,f2f_id','xjobs':'*','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
                '1':{'tasks':'file','xjobs':'*','title':'تکمیل','app_keys':'y','app_titls':'','oncomplete_act':''},
            }, 
        },
    },
    #--------------------------------------------------------------------
    'rqst':{#db request
        'plot':{
            'base':{'mode':'form','title':'درخواست - چاپ','code':'304','rev':'01-040417'
            },
            'tasks':{
                'u_un':{'type':'auto-x','len':'24','auto':'_cur_user_un_','title':'کد همکار'},
                'u_nm':{'type':'auto','ref':{'db':'user','tb':'user','key':'__0__','val':'{name} {family}','where':'''un = "{u_un}"'''},'title':'نام و نام خانوادگی'},
                'date':{'type':'fdate','title':'تاریخ مورد نیاز برای تحویل','prop':['update']},
                'frd_modir':{'type':'user','title':'مدیر','xjobs':'mvn_ha','prop':['show_full','un_free'],'nesbat':'modir'},
                'c_prj_id':{'type':'reference','len':'30',
                    'ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update','multiple'],
                    'team':{'cp_code':{'val':'{cp_code}','title':'کد موضوع'},'cp_name':{'val':'{cp_name}','title':'نام پروژه'}},},
                'title':{'type':'text','title':'عنوان یا موضوع سفارش','len':'250','height':'50px'},
                'xtype':{'type':'select','title':'نوع سفارش','prop':['can_add','no_empty'],'def_value':'3', 'value_show_case':True,
                    'select':['کارت ویزیت','پوستر','بروشور','سربرگ','نقشه','بنر']},            
                'size':{'type':'select','title':'ابعاد نهایی','prop':['can_add','no_empty'],'def_value':'3','value_show_case':True,
                    'select':['A0','A1','A2','A3','A4','A5','B4']}, 
                'color':{'type':'select','title':'رنگ‌بندی','def_value':'3','prop':['no_empty'],'value_show_case':True,
                    'select':['رنگی','سیاه‌وسفید']},
                'paper':{'type':'select','title':'نوع کاغذ','prop':['can_add','no_empty'],'def_value':'3','value_show_case':True,
                    'select':['تحریر','گلاسه','مات','براق']}, 
                'add':{'type':'select','title':'خدمات اضافه','prop':['can_add','multiple','no_empty'],'def_value':'3','value_show_case':True,
                    'select':['لمینت','طلاکوب','خط تا','سلفون','پانچ','صحافی']}, 
                'des_1':{'type':'text','title':'توضیح - درخواست ','len':'2500'},
                'des_2':{'type':'text','title':'توضیح - برآورد','len':'250'},
                'des_3':{'type':'text','title':'توضیح - تایید نیاز','len':'250'},
                'des_4':{'type':'text','title':'توضیح - تامین مالی','len':'250'},
                'n_plot':{'type':'num','min':1,'max':999,'len':'3','title':'تعداد مورد نیاز'},
                'price':{'type':'num','min':1,'max':999000,'len':'6','title':'برآورد قیمت کل - هزار تومان'},
                'f_code':{'type':'auto','len':'8','auto':'AQC0-K8S-RQST-PLOT-{{=str(id).zfill(3)}}-{cp_code}','title':'کد فایل'},
                'file_plot_r':{'type':'file_r','len':'40','file_name':'{f_code}-r','path':'form,rqst,plot','title':'فایل چاپ','file_ext':"pdf,gif,jpg,jpeg,png,zip",},
            },
            'steps':{
                'pre':{'tasks':'u_un,u_nm,date,frd_modir,c_prj_id,cp_code,cp_name,title','xjobs':'*','title':'اطلاعات اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'xtype,size,color,paper,add,n_plot,f_code,file_plot_r,des_1','xjobs':'#step#0','title':'اطلاعات تکمیلی','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'price,des_2','xjobs':'cga','title':'ارزیابی هزینه','app_keys':'y,r','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'des_3','xjobs':'#task#frd_modir','title':'تأیید نیاز، معاونت مربوطه:','app_keys':'y,r','app_titls':'','oncomplete_act':''},
                's4':{'tasks':'des_4','xjobs':'mvn_pln','title':'تایید امکان پرداخت - معاونت برنامه ریزی و توسعه منابع ','app_keys':'y,r','app_titls':'','oncomplete_act':''},
            },
        },
    },
    #--------------------------------------------------------------------
    'survey':{ #db نظر سنجی
        'prsln':{
            'base':{'mode':'form','title':'نتایج نظر سنجی در پرس لاین','help':'survey.porsline.ir','code':'410','rev':'00-040511'
            },
            'tasks':{
                'date1':{'type':'fdate','len':'10','title':'تاریخ نظرسنجی','prop':[]},
                'c_prj_id':{'type':'reference','title':'پروژه','prop':['update'],
                            'ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d},{cp_code},{cp_name}'},
                            'team':{'cp_code':{'val':'{cp_code}','title':'کد پروژه'},'cp_name':{'val':'{cp_name}','title':'نام پروژه'}},},
                'subject':{'type':'text','len':'255','title':'موضوع'},
                'cat':{'type':'text','len':'255','title':'دسته بندی'},
                'des':{'type':'text','len':'255','title':'توضیحات'},
                'trgt':{'type':'text','len':'255','title':'جامعه مخاطبین'},
                'file_r': {'type':'file','file_name':'AQC0-SRV-PRSLN-{id:04d}-{cp_code}-r','file_ext':"pdf",'path':'form,srv,prsln','title':'نمودار نتایج - PDF'},
                'file_v': {'type':'file','file_name':'AQC0-SRV-PRSLN-{id:04d}-{cp_code}-v','file_ext':"xls,xlsx,csv",'path':'form,srv,prsln','title':'جدول اطلاعات'},
                'link_r':{'type':'text','title':'لینک نتایج','len':'80','link':{'target':'_blank','icon_text':'R','class':'btn btn-info'},},
                'link_v':{'type':'text','title':'لینک پرسشنامه','len':'80','link':{'target':'_blank','icon_text':'D','class':'btn btn-info'},},
            },
            'steps':{
                's0':{'tasks':'date1,c_prj_id,cp_code,cp_name,subject,cat,des,trgt','xjobs':'*','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'file_r,file_v,link_r,link_v','xjobs':'#step#0','title':'تکمیل','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'date1,c_prj_id,cp_code,cp_name,subject,cat,des','view1':'','view2':'','view_cols':1},
            },
            'labels':{
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'txt_bank':{ #db
        'prompt':{
            'base':{'mode':'form','title':'بانک پرامپت های هوش مصنوعی','help':'','code':'920','rev':'00-040520'
            },
            'tasks':{
                'prmpt':{'type':'text','len':'500','title':'متن پرامپت','height':'100px;'},
                'goal':{'type':'text','len':'500','title':'هدف','height':'50px;'},
                'des':{'type':'text','len':'100','title':'توضیح - تغییرات'},
            },
            'steps':{
                'pre':{'tasks':'prmpt,goal','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'des','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''}
            }
        },
        'link':{
            'base':{'mode':'form','title':'بانک لینک های مفید','help':'','code':'920','rev':'00-040520'
            },
            'tasks':{
                'link':{'type':'text','len':'500','title':'لینک','link':{'target':'_blank','icon_text':'L','class':'btn btn-info'},},
                'sbjct':{'type':'text','len':'500','title':'موضوع - توضیح لینک'},
                'cat':{'type':'select','title':'دسته','select':{'D':'design-طراحی','S':'supervition-نظارت','O':'Office-اداری','T':'Tools-کاربردی'},'prop':['can_add']},
                'des':{'type':'text','len':'100','title':'توضیح - تغییرات'},
            },
            'steps':{
                'pre':{'tasks':'link,sbjct,cat','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'des','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''}
            }
        },
        'msg':{
            'base':{'mode':'form','title':'بانک پیام ها و نامه های آماده','help':'','code':'920','rev':'00-040520'
            },
            'tasks':{
                'txt':{'type':'text','len':'500','title':'متن','height':'50px;'},
                'sbjct':{'type':'text','len':'500','title':'موضوع - توضیح '},
                'typ':{'type':'select','title':'نوع','select':{'L':'Letter-نامه','M':'Message-پیام'},'prop':['can_add']},
                'cat':{'type':'text','len':'100','title':'دسته'},
                'des':{'type':'text','len':'100','title':'توضیح - تغییرات'},
            },
            'steps':{
                'pre':{'tasks':'txt,sbjct,typ,cat','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'des','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''}
            }
        }
    },
    #--------------------------------------------------------------------
    'Benchmarking':{ #db
        'a':{
            'base':{'mode':'form','title':'بنچ مارک و مقایسه تطبیقی','help':'','code':'920','rev':'00-040526'
            },
            'tasks':{
                'sect':{'type':'text','len':'100','title':'حوزه / بخش','help':'section / domain'},
                'proc':{'type':'text','len':'100','title':'موضوع یا فرآیند','help':'process / subject '},
                'bmtp':{'type':'select','title':'نوع بنچ مارکینگ','help':' benchmarking type ',
                        'select':{'داخلی':'Internal-(بنچ‌مارکینگ داخلی)-    -مقایسه فرآیندها و عملکرد **بین واحدها یا پروژه‌های داخلی یک سازمان**.   -مثال: مقایسه روش مدیریت جلسات بین واحد معماری و واحد شهرسازی شرکت.',
                            'رقابتی':'Competitive-(بنچ‌مارکینگ رقابتی) - مقایسه با **رقبا و سازمان‌های مشابه** در صنعت.- مثال: مقایسه گزارش‌های توجیهی مالی پروژه‌های شهرسازی با سایر شرکت‌های مشاور هم‌سطح.',
                            'عملکردی':'Functional-(بنچ‌مارکینگ کارکردی / عملکردی)- مقایسه یک **فرآیند خاص** با سازمان‌های **غیررقیب اما مشابه در عملکرد**. - مثال: مقایسه سیستم آرشیو اسناد در شرکت مشاور با بانک‌ها یا سازمان‌های بایگانی ملی.',
                            'بهترین تجربه':'Best Practice-(بنچ‌مارکینگ بهترین تجربه / الگوگیری از برترین‌ها) - مقایسه با سازمان‌هایی که در یک زمینه خاص **بهترین عملکرد** را دارند (حتی اگر هم‌صنعت نباشند).- مثال: الگوگیری از رویه‌های BIM یا ISO در شرکت‌های بین‌المللی.',
                            'فرایندی':'Process-(بنچ‌مارکینگ فرآیندی)- تمرکز روی یک **فرآیند مشخص** مثل طراحی، کنترل کیفیت یا مدیریت قراردادها.- مثال: مقایسه فرآیند کنترل کیفیت نقشه‌ها با روش‌های جهانی.',
                            'استراتژیک':'Strategic-(بنچ‌مارکینگ استراتژیک)- مقایسه در سطح **استراتژی‌های کلان سازمان**.- مثال: مقایسه مدل کسب‌وکار یا استراتژی توسعه پایدار شرکت با مشاوران بین‌المللی.',
                            'شاخص ها':'Performance- (بنچ‌مارکینگ عملکردی / شاخص‌ها)- تمرکز بر روی **شاخص‌های کلیدی عملکرد (KPIs)** و مقایسه آن‌ها با دیگران.- مثال: نرخ رضایت مشتریان، زمان تحویل پروژه، درصد خطاها.',
                            'عمومی':'Generic-(بنچ‌مارکینگ عمومی / بین‌صنعتی)- مقایسه با سازمان‌هایی از صنایع کاملاً متفاوت برای گرفتن ایده‌های نو.- مثال: استفاده از روش‌های مدیریت مشتری در صنعت هتلداری برای بهبود CRM در شرکت مشاور.'
                        },},

                'refs':{'type':'text','len':'100','title':'منابع و مراکز مرجع','help':' reference sources ','link':{'target':'_blank','icon_text':'🎯','class':'btn btn-info'},}, 
                'docs':{'type':'text','len':'100','title':' نوع اسناد / مستندات مرتبط','help':' related documents '},
                'indx':{'type':'text','len':'100','title':' شاخص‌ها و معیارهای مقایسه','help':' indicators & metrics '},
                'tool':{'type':'text','len':'100','title':'ابزارهای مورد استفاده ','help':' tools used '},
                'date':{'type':'fdate','title':'تاریخ انجام بنچ مارک','help':' benchmark date '},
                'unit':{'type':'text','len':'100','title':'واحد مسئول','help':' responsible unit '},
                'prio':{'type':'select','select':{'L':'Low - کم','M':'Medium - متوسط','H':'High - متوسط'},'title':'سطح اولویت','help':' priority level '},
                'resl':{'type':'text','len':'100','title':'نتایج و بهبودهای مورد انتظار','help':' results & expected improvements '},
                'actn':{'type':'text','len':'100','title':'اقدامات اصلاحی / پیشنهادی ','help':' corrective / proposed actions '},
                'stat':{'type':'text','len':'100','title':'وضعیت اجرا','help':' execution status '},
                'attd':{'type':'text','len':'100','title':'مستندات ضمیمه','help':' attached documents '},
                'foll':{'type':'user','title':'مسئول پیگیری','help':' follow-up responsible '},  
                'des':{'type':'text','len':'100','title':'توضیح'},
            },
            'steps':{
                'pre':{'tasks':'sect,proc,bmtp,refs,docs','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'indx,tool,date,unit,prio,resl,actn,stat,attd,foll','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'des','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''}
            }
        },
    },
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    'tmsh':{ #db
        'hand_io':{
            'base':{'mode':'form','title':'ورود دستی ساعت ورود و خروج','help':'','code':'920','rev':'00-040611'
            },
            'tasks':{
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'ثبت کننده  - نام','prop':['hidden']},
                'date1':{'type':'fdate','title':'تاریخ ','prop':['readonly']},
                'time':{'type':'time_c','title':'تردد','def_value':'07:00'},
                'x_case':{'type':'select','title':'وضعیت پس از تردد','def_value':'WR','prop':['no_empty'],
                        'select':{'WR':'WORK - حضور در شرکت',
                            'MM':'ماموریت',
                            'MR':'مرخصی',
                            'EX':'خروج  - اتمام کار',
                            },},
            },
            'steps':{
                'pre':{'tasks':'frd_1,date1,time,x_case','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            }
        },
    },
    #--------------------------------------------------------------------
    'test':{ #db
        'b':{
            'base':{'mode':'form','title':'بررسی عملکرد فیلدهای هوشمند در مرحله پیش انتشار','code':'990'
                },
            'tasks':{
                'txt':{'type':'text','len':50,'lang':'fa','title':'متن','uniq':''},#'sel=`x`'
                'img':{'type':'file','len':'24','file_name':'abc-{id}-{{=dt[:4] if dt else "0000"}}','file_ext':"gif,jpg,jpeg,png",'path':'form,image','title':'تصویر','img':"""style='width:200px;' """},
                'img2':{'type':'file','len':'24','file_name':'abc-{id}-{{=dt[:4] if dt else "0000"}}','file_ext':"gif,jpg,jpeg,png",'path':'test,a','title':'تصویر','img':"""style='width:200px;' """},
                'n':{'type':'num','min':5,'max':15,'title':'عدد','prop':[]},
                'sel':{'type':'select','select':{'a':'طراحی','x':'نظارت'},'title':'واحد','prop':[]},
                'ref':{'type':'reference','len':'5','title':' مسئول اقدام','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{m_w} {pre_n} {name} {family}'},'prop':[]},
                'ch':{'type':'check','title':'با این موضع موافقم','prop':[]},
                'dt':{'type':'fdate','len':'10','title':'تاریخ انجام کار','prop':[]},
                'at':{'type':'auto','len':'24','auto':'{n}-{sel}-{ch}-{ref}-{dt:}','title':'کد اتوماتیک'},
                'indx1':{'type':'index','len':'4','ref':{'db':'test','tb':'b','key':'{id}','val':'{indx1}','where':''},'title':'شماره'},
                'fl':{'type':'file','len':'24','file_name':'abc-{{=int("0"+n)+25}}-{sel}-{{=dt[:4] if dt else ""}}','file_ext':"gif,jpg,jpeg,png,doc,docx,xls,xlsx,pdf,dwg,zip,rar",'path':'test,a,c,{txt}-{n}','title':'فایل نهایی'},#,'x':'{txt}-{n}-{sel}-{ch}-{ref}'
                'tt':{'type':'time_c','title':'زمان شروع'},
                'time_st2':{'type':'time_c','title':'از ساعت','def_value':'{tt}'},
                'frd_jnshin':{'type':'reference','len':'5','title':'جانشین','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}- {m_w} {name} {family}'},'prop':['show_full']},
                'xxlink':{'type':'f_link','len':'5','title':' فرم مرتبط - پروژه','ref':{'db':'a_prj','tb':'a','key':'{id}','val':'{code}-{name}','show_cols':['name','code']},'prop':['update','multiple'] },
            },
            'steps':{
                'pre':{'tasks':'xxlink,img,img2','xjobs':'*','title':'ثبت اطلاعات اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'txt,n,sel,indx1,img2,ref,ch,tt,dt','xjobs':'des_eng_ar','title':'ثبت اطلاعات تکمیلی','app_keys':'y,x,r','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'at,fl,time_st2','xjobs':'#step#0','title':'ثبت فراداده ها','app_keys':'y,x,r','app_titls':'','oncomplete_act':''},
                's4':{'tasks':'dt,at,fl','xjobs':'#task#ref','title':'بررسی اطلاعات','app_keys':'y,x,r','app_titls':'','oncomplete_act':''},
            },           
            'views':{
            
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}  
        }
    },
}
def set_if_ns(obj,pre_dict): # set if not set
    for prop,valu in pre_dict.items():
        if not prop in obj:obj[prop]=valu
def x_data_verify_task(obj_name,obj,db,tb):
    obj['name']=obj_name
    set_if_ns(obj,{'prop':[],
        'width':'10',
        'def_value' :'',
        'onchange':'',
        'title':obj['type']+'-'+obj_name}) 
    '''
    if not 'prop' in obj:obj['prop']=[]
    if not 'width' in obj:obj['width']='10'
    if not 'title' in obj:obj['title']=obj['type']+'-'+obj_name
    if not 'def_value' in obj:obj['def_value']=''
    if not 'onchange' in obj:obj['onchange']=''
    '''
    if obj['type']=='file_v':
        obj['type']='file'
        set_if_ns(obj,{'file_ext':"mm,md,ksm,txt,doc,docx,xls,xlsx,ppt,pptx,zip,rar,7z,dwg",
            'path':f'form,{db},{tb}',
            'len':'40'})
    elif obj['type']=='file_r':
        obj['type']='file'
        set_if_ns(obj,{'file_ext':"pdf,gif,jpg,jpeg,png",
            'path':f'form,{db},{tb}',
            'len':'40'})
    # ref        
    if obj['type']=='index':
        set_if_ns(obj['ref'],{'db':db,'tb':tb,'key':'{id}','val':('{%s}' % (obj_name))})
    elif 'ref' in obj:
        if type(obj['ref'])==dict:
            set_if_ns(obj['ref'],{'db':db})   

def x_data_verify(x_data): 
    #defult data_filter
    data_filter={'f_nxt_u != "x"':'همه موارد',
                'step_0_un = "{_i_}"':'فرم های من',
                'f_nxt_u LIKE "%{{=_i_}}%"':'فرمهای منتظر من',
                'f_nxt_u != "y" AND step_0_un = "{_i_}"':'فرمهای نهایی نشده من',
                'f_nxt_u != "y"':'فرمهای نهایی نشده'
                }
    #add team fields for refrence field
    """
    'prj_id':{'type':'reference','width':'5','title':'آیدی پروژه','ref':{'db':'a_prj','tb':'a','key':'{id}','val':'{code}-{name}'},'prop':['update']
        'team':{'prj':{'val':'{code}','title':'کد پروژه'},'prj_name':['val':'{name}','title':'نام پروژه']},},
    'prj':{'type':'auto','ref':{'db':'a_prj','tb':'a','key':'__0__','val':'{code}','where':'''id = "{prj_id}"'''},'title':'پروژه'},#
    
    =====exam =============================================================================================================================
    'sub_p_id':{'type':'reference','title':'زیر پروژه',
        'ref':{'db':'a_sub_p','tb':'a','key':'{id}','val':'{code}-{name}','where':'''prj_id = "{prj_id}"'''},'prop':['update'],
        'team':{'sub_p':{'val':'{code}','title':'کد زیر پروژه'},'sub_p_name':{'val':'{name}','title':'نام زیر پروژه'}},},
    #'sub_p':{'type':'auto','ref':{'db':'a_sub_p','tb':'a','key':'__0__','val':'{code}','where':'''id = "{sub_p_id}"'''},'title':'زیر پروژه'},#,'prop':['report']
    #'sub_p_name':{'type':'auto','len':'50','auto':"{{=__objs__['sub_p']['output_text'][4:]}}",'title':'نام زیر پروژه'},
    """
    for db_name,db_obj in x_data.items():
        for tb_name,tb_obj in db_obj.items():
            tasks_add={}
            for obj_name,obj in tb_obj['tasks'].items():
                x_data_verify_task(obj_name,obj,db_name,tb_name) #040409
                if obj['type']=='reference':
                    if 'team' in obj: 
                        for team_name,team_obj in obj['team'].items():
                            xdb=obj['ref']['db']
                            xtb=obj['ref']['tb']
                            xtask=team_obj['val'].replace("{", "").replace("}", "")
                            tit= team_obj['title'] if 'title' in team_obj else x_data[xdb][xtb]['tasks'][xtask]['title']
                            new_fld={team_name:{'type':'auto','ref':{'db':xdb,'tb':xtb,'key':'__0__','val':team_obj['val'],'where':obj['ref']['key'][1:-1]+ ' = "{' + obj_name + '}"'},'title':tit,
                                'prop':team_obj['prop'] if 'prop' in team_obj else []}}
                            #                                  'a_prj'               'a'                                  '{code}'                '{id}={prj_id}'                                       'کد پروژه'
                            #print(str(new_fld))
                            tasks_add.update(new_fld)
                # - 040410 ----------------------------------------------------------------------
                # ساخت فیلدهای f2f_db,f2f_tb,f2f_nm از روی فیلد با نام f2f_id برای تغییرات سریع جهت "اضافه شدن فیلدهای جدید لازم"
                # make fildes(f2f_db,f2f_tb,f2f_nm) from field(f2f_id) : speed change => make need fiels
                if obj['name']=='f2f_id':
                    new_fld={
                        'f2f_db':{'type':'text','title':'database','len':'40','prop':['readonly']},
                        'f2f_tb':{'type':'text','title':'table','len':'40','prop':['readonly']},
                        'f2f_nm':{'type':'text','title':'name','len':'40','prop':['readonly']}
                        }
                    tasks_add.update(new_fld)    
            #print(str(tasks_add))
            tb_obj['tasks'].update(tasks_add)
            
    for db_name,db_obj in x_data.items():
        for tb_name,tb_obj in db_obj.items():
            #print(str(tb_obj))
            for obj_name,obj in tb_obj['tasks'].items():
                #for obj_name,obj in ff_o.items():
                x_data_verify_task(obj_name,obj,db_name,tb_name) #040409
            if not 'views' in tb_obj:tb_obj['views']={}  
            if not tb_obj['views']:
                tb_obj['views']={
                    'input':list(tb_obj['tasks'].keys()),
                    'view1':{},
                    'view2':{}
                }
            if not 'base' in tb_obj:tb_obj['base']={}  
            if not 'labels' in tb_obj:tb_obj['labels']={} 
            #--------------------
            if not 'mode' in tb_obj['base']:tb_obj['base']['mode']='table'  
            tb_obj['base']['tb_name']=tb_name
            tb_obj['base']['db_name']=db_name
            #--------------------
            if not 'order' in tb_obj:tb_obj['order']='id'    
            if not 'cols_filter' in tb_obj:tb_obj['cols_filter']={'':'همه',}
            if not 'data_filter' in tb_obj:tb_obj['data_filter']={}  
            tb_obj['data_filter'].update(data_filter)
            if 'steps' in tb_obj:
                i=-1
                steps=tb_obj['steps']
                len_steps=len(steps)
                for step_name,step in steps.items():
                    i+=1
                    if step['tasks']=='**':step['tasks']=','.join(list(tb_obj['tasks'].keys()))
                    if not 'app_keys' in step or not step['app_keys']:
                        step['app_keys']='y,x,r' if i>0 else 'y,x'
                    if not 'app_titls' in step or not step['app_titls']:
                        step['app_titls']=[{'x':'حذف فرم','y':'تایید این مرحله','r':'بازگشت به مرحله قبل'}[x] for x in step['app_keys'].split(',')]
                    step['app_keys']=step['app_keys'].split(',')
                    #'app_kt'=app dict from keys and titels 
                    step['app_kt']=dict(zip(step['app_keys'],step['app_titls']))
                    step['i']=i
                    if not 'start_where' in step:
                        step['end_where']="False"
                        step['start_step']=''
                        if i==0:
                            if i==len_steps-1:
                                pass
                            else:
                                step['end_where']="'{step_"+ str(1) +"_ap}' in ['y','x']"
                        elif i==len_steps-1:
                            step['start_step']=str(i-1)
                        else:
                            step['start_step']=str(i-1)
                            step['end_where']="'{step_"+ str(i+1) +"_ap}' in ['y','x']"
                        step['start_where']="True" if not step['start_step'] else "'{step_"+ step['start_step'] + "_ap}' =='y'"
                    # sec security for all task in 1 step
                    if 'auth' in step:
                        for task in step['tasks'].split(','):
                            if task in tb_obj['labels']:continue
                            x_task=tb_obj['tasks'][task]
                            if 'auth' in x_task:
                                x_task['auth']+=','+step['auth']
                            else:
                                x_task['auth']=step['auth']
                keys=list( steps.keys())
                for k in keys:
                    name=steps[k]['name'] if 'name' in steps[k] else str(steps[k]['i']) 
                    steps[name]=steps.pop(k)
                    steps[name]['name']=name
                    #{x:step['app_titls'][i] for i,x in enumerate(step['app_keys'].split(',').reverse())} 
                #tt=','.join[step['tasks']+['step' for sn,step in tb_obj['steps'].items() ]
                #tb_obj['cols_filter']['a']=[
#------------------------------------------------------------------------------
class LINKED_TARGET_FIELDS():
    #find_linked_target_fields
    '''
        goal:
            find list of linked_target_field in all form for 1 linked_base_field
            
            بررسی اینکه چه فیلدهایی در چه جداولی (مقصد لینک) به اطلاعات یک فیلد در یک جدول (مبدا لینک) لینک هستند
            لینک هستند یعنی اگر فیلد مبدا تغییر کند فیلدهای مقصد متناضر با آن نیز باید تغییر کنند
    '''
    def __init__(self):
        trs=[]
        i=0
        for db,db_data in x_data.items():
            for tb,tb_data in db_data.items():
                for fld,fld_data in tb_data['tasks'].items():
                    db_tb2=db_tb=db+","+tb
                    db2=db
                    tb2=tb
                    det=''
                    if 'ref' in fld_data:
                        i+=1
                        ref=fld_data['ref']
                        if type(ref)!=str:
                            db2=ref['db']
                            tb2=ref['tb']
                            db_tb2=db2+","+tb2
                            tt='ref'
                        else:
                            tt='? auto_x'
                        det=str(fld_data['ref'])
                        #trs+=[[str(i),'ref',db_tb,fld,fld_data['type'],db_tb2,]]
                    if 'auto' in fld_data:
                        i+=1
                        det=str(fld_data['auto'])
                        tt='auto'
                    if det:
                        trs+=[[str(i),tt,db_tb,fld,fld_data['type'],db_tb2,det]]
        self.trs=trs
    def find(self,source='',target=''):
        trs=[]
        for tr in self.trs:
            db_tb1=tr[2]
            db_tb2=tr[5]
            if (not source or source==db_tb1) and (not target or target==db_tb2):
                trs+=[tr]
        return [['i','r-a','db_tb1','fld','type','db_tb2','data']]+trs
            

#--------------------------------------------------------------------lable_1,name, ['prj']['select'][prj]=>
if __name__ == "__main__":
    import json
    # the json file where the output must be stored
    out_file = open("x_data.json", "w",encoding='utf8')
    json.dump(x_data, out_file, indent = 4,ensure_ascii=False)
    out_file.close()
    with open("x_data.json", "r",encoding='utf8') as fp:
        data = fp.read()
    x_data1= json.loads(data)  
    if x_data1==x_data:
        print("ok") 
    else:
        print("!=") 
    print(x_data1['eblag']['a']['labels'])
else:
    x_data_verify(x_data)
    
    #import k_err
    #k_err.xxxprint(vals=x_data['user']['user']['steps'],launch=True,reset=True)