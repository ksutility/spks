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
        index:
            'len':num_str : number in str format
                *important*         
            'ref'::dict =exam=> {'db':'test','tb':'b','key':'{id}','val':'{indx1}','where':''}
    prop:['prop1','prop2',...]
        read:
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
"""
x_data_cat:{
    '1':{'titel':'ex','db':'a_prj,a_sub_p,a_step'}
}
x_data_cat={
    '-':'همه فرمها',
    '1':'اطلاعات اصلی',
    '2':'فرمهای پرسنلی',
    '3':'عمومی',
    '4':'DCC',
    '9':'موارد متفرقه',
    }
'''
import json
with open("myfile.json", "r",encoding='utf8') as fp:
    data = fp.read()
x_data=json.loads(data)
'''      
x_data={
    'a_cur_subject':{ #db
        'a':{
            'base':{'mode':'form','title':'موضوعات و پروژه های جاری','code':'100','multi_app':{'0':['ks'],'1':['ks']},},
            'tasks':{
                'cp_code':{'type':'text','title':'کد موضوع','len':'10','uniq':''},
                'cp_name':{'type':'text','title':'نام کامل','len':'140','lang':'fa'},
                'sm_name':{'type':'text','title':'نام مختصر','len':'20','lang':'fa'},
                'alt_names':{'type':'text','title':'نام های متفرقه','len':'250','lang':'fa'},
                'salimi':{'type':'text','title':'نام در سیستم مهندس سلیمی','len':'150','lang':'fa'},
                'c2_prjs':{'type':'reference','width':'20','title':'زیر پروژه های مرتبط','ref':{'db':'a_sub_p','tb':'a','key':'{code2}','val':'{code2}-{name2}'},'prop':['multiple']},
                'dspln':{'type':'reference','title':'دیسیپلین اصلی','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{code} , {name} , {name_e}'},},
                'mdr_prj':{'type':'user','title':'مسئول پیگیری پروژه'},
                'cat':{'type':'select','title':'دسته','select':{'P':'پروژه','F':'فرایند'}}
            },
            'steps':{
                'pre':{'tasks':'cp_code,cp_name','xjobs':'dcc_dsn','title':'ثبت','app_keys':'','app_titls':'','oncomplete_act':''},#cp_code,cp_name
                's1':{'tasks':'cat,dspln,mdr_prj','xjobs':'dccm','title':'گام2','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'sm_name,alt_names','xjobs':'dcc_dsn','title':'تکمیل','app_keys':'','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'c2_prjs','xjobs':'dccm','title':'تصویب','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'cat,dspln,mdr_prj,salimi,c2_prjs','view1':'cp_code,cp_name','view2':'sm_name,alt_names,salimi,c2_prjs'},
            },
            'cols_filter':
                {'':'همه',
                'code':'شماره',
                'code,name':'شماره و موضوع',
                },
            'data_filter':{'':'همه موارد',
                'cat is Null':'نوع مشخص نشده',
                'cat = "P"':'همه پروژه ها',
                'cat = "F"':'همه فرایندها',
                },
        }
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
                'prj':{'type':'reference','width':'5','title':' پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'code':{'type':'text','title':'کد زیر پروژه','len':'3','uniq':"prj=`{{=__objs__['prj']['value']}}`"},
                'name':{'type':'text','len':'59','title':'نام زیر پروژه'},
                'code2':{'type':'auto','len':'8','auto':'{{=prj[:4].upper()}}-{code}','title':'کد کامل زیر پروژه'},
                'name2':{'type':'auto','len':'256','auto':"{{=__objs__['prj']['output_text'][5:].strip()}}-{name}",'title':'نام کامل زیر پروژه'},
                'des':{'type':'text','len':'250','title':'توضیح زیر پروژه'},
                'date':{'type':'fdate','title':'تاریخ ثبت'},
                'auth_users':{'type':'reference','width':'20','title':' افراد دارای حق دسترسی','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{m_w} {pre_n} {name} {family}'},'prop':['multiple']},
                'cat_1':{'type':'text','title':'موارد جاری'},
                'cat_2':{'type':'text','title':'دسته 2'},
                
            },
            'steps':{
                'pre':{'tasks':'prj,name,code','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'code2,name2,des,date','xjobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
                'set_auth':{'tasks':'auth_users','xjobs':'dccm','title':'دسترسی','app_keys':'','app_titls':'','oncomplete_act':''}
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
                'prj':{'type':'reference','width':'5','title':' پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'sub_p':{'type':'reference','width':'5','title':' زیر پروژه','ref':{'db':'a_sub_p','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}"'''},'prop':[]},
                'code':{'type':'text','title':'کد مرحله','len':'2'},
                'name':{'type':'text','title':'نام مرحله'},
                'date':{'type':'fdate','title':'تاریخ ثبت'},
            },
            'steps':{
                'pre':{'tasks':'prj,sub_p','xjobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
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
                'date':{'type':'text','title':'تاریخ ثبت'},
            },
            'steps':{
                'pre':{'tasks':'code,name_e,name','xjobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'n,des,date','xjobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'code,name_e,name','view1':'','view2':''}
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
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
                'code':{'type':'text','title':'کد مدرک'},
                'name':{'type':'text','title':'نام مدرک'},
                'name_e':{'type':'text','title':'doc name'},
                
            },
            'steps':{
                'pre':{'tasks':'dspln,code,lable_1','xjobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'name,name_e','xjobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
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
    'a_contact_grup':{ #db
        'a':{
            'base':{'mode':'form','title':'گروه مقابل مکاتبه','code':'103'},
            'tasks':{
                'prj':{'type':'reference','width':'5','title':' پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'sub_p':{'type':'reference','width':'5','title':' زیر پروژه','ref':{'db':'a_sub_p','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}"'''},'prop':['update']},
                'grup_code':{'type':'text','title':'کد گروه','len':'4','uniq':"prj=`{{=__objs__['prj']['value']}}`,sub_p=`{{=__objs__['sub_p']['value']}}`"},
                'grup_name':{'type':'text','title':'نام گروه'},
            },
            'steps':{
                'pre':{'tasks':'prj,sub_p,grup_code,grup_name','xjobs':'dccm','title':'تعریف اولیه','app_keys':'y','app_titls':'','oncomplete_act':''},
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
                'date_s':{'type':'fdate','title':'تاریخ شروع بهره برداری'},
                'date_e':{'type':'fdate','title':'تاریخ خاتمه بهره برداری'},
            },
            'steps':{
                'pre':{'tasks':'name,code,addres','xjobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
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
        
        'a':{
            'base':{'mode':'form','title':'نامه ها','auth':'dccm,ppr_vue','code':'901','auth_prj':'prj1','multi_app':{'0':['ks'],'1':['ks']},
            },
            'tasks':{
                'prj_id':{'type':'reference','width':'30','ref':{'db':'a_sub_p','tb':'a','key':'{id}','val':'{id:03d}-{code2}-{name2}'},'title':'پروژه','prop':['update']},
                'prj1':{'type':'auto','ref':{'db':'a_sub_p','tb':'a','key':'__0__','val':'{prj}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'کد پروژه'},
                'prj2':{'type':'auto','ref':{'db':'a_sub_p','tb':'a','key':'__0__','val':'{code2}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'کد کامل زیر پروژه'},
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
                'pre':{'tasks':'prj_id,prj1,prj2','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
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
                {'':'همه',
                'lno':'شماره',
                'lno,sbj':'شماره و موضوع',
                'lno,sbj,date_s':'شماره، موضوع، تاریخ',
                'lno,sbj,date_s,io_t':'شماره، موضوع، تاریخ، نوع',
                'lno,sbj,date_s,io_t,folder':'شماره،موضوع،تاریخ،ص-و،فایلها', 
                'lno,sbj,date_s,io_t,x_num,x_des':'ش.م.ت.ن-دستی : شماره و شرح',
                'prj,lno,sbj,date_s,io_t,x_num,x_des,act_todo,x_act_todo,x_act_rec,x_act_pey':'شماره،موضوع،تاریخ،ص-و،توضیح،اقدام (لازم،سابقه، پی گیری)',
                'folder,lno,sbj,date_s,comment,io_t,x_to_grup,act_todo,x_act_todo,x_act_rec,x_act_pey,x_act_type,x_inf,x_inf,x_des':'بررسی 1',
                'folder,lno,sbj,date_s,io_t,lv_onvan,lv_archiv,paper_num,num_x,num_link,cdate,attach,lv_per_archiv':'بررسی 2',
                'prj2,lno,sbj,date_s,io_t,lv_onvan,lv_archiv,paper_num,folder':'بررسی 3',
                'prj2,lno,sbj,date_s,io_t,lv_onvan,lv_archiv,paper_num,folder,pr_err':'بررسی 4',
                }, #table_view cols filter
                #cols_filter={'':'همه','lno,sbj':'2',}
            'data_filter':
                {'':'همه نامه ها',
                'prj_id = "112"':'پروژه صحن جامع',
                'prj_id = "110"':'مدیریت سوابق',
                'prj_id is Null':'نیاز به تعیین پروژه',
                'prj_id = "36"':'پروژه پیوندراه',
                'prj1 = "HRG1"':'پروژه گیتها',
                'prj_id = "29" AND x_des like "%L-%"':'-Lپروژه گیتها',
                'prj_id = "48"':'پروژه استاندارد سازی',
                
                'act_todo != ""':'دارای ارجاع',
                'x_act_todo != ""':'نیاز به اقدام',
                'act_pey != ""':'پی گیری',
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
            'base':{'mode':'form','title':'لیست همکاران','data_filter':'loc = "100"','code':'201',
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
                'tel_wrk':{'type':'text','title':'تلفن داخلی','len':'10','placeholder':"....-..-.."},
                'loc':{'type':'reference','title':'محل کار','ref':{'db':'a_loc','tb':'a','key':'{code}','val':'{name}'},'prop':['show_full']},
                'office':{'type':'select','select':['طراحی','نظارت','پشتیبانی','مدیریت'],'title':'بخش'},
                #'discipline':{'type':'text','title':'رسته'}
                
                'job':{'type':'text','title':'سمت','len':'50'},#,'ref':{'db':'user','tb':'job','key':'id','val':'{id}{name}'}
                'p_id':{'type':'num','len':4,'lang':'fa','title':'شماره پرسنلی','uniq':''},
                'end':{'type':'fdate','title':'تاریخ خاتمه کار'},
                'file_pic_per':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}0-pic_per','file_ext':"jpg",'path':'form,hrm,cv,{un}','title':'عکس پرسنلی'},
                'file_shnsnm':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}1-shnsnm','file_ext':"pdf",'path':'form,hrm,cv,{un}','title':'شناسنامه','auth':'dccm,#task#un,off_ens'},
                'file_mdrk_thsl':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}2-mdrk_thsl','file_ext':"pdf,jpg",'path':'form,hrm,cv,{un}','title':'آخرین مدرک تحصیلی','auth':'dccm,#task#un,off_ens'},
                'file_ot':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}3-ot','file_ext':"zip",'path':'form,hrm,cv,{un}','title':'سایر مدارک','auth':'dccm,#task#un,off_ens'},
                'file_off':{'type':'file','len':'40','file_name':'AQC0-HRM-CV-{un}4-off','file_ext':"pdf",'path':'form,hrm,cv,{un}','title':'مدارک اداری','auth':'dccm,#task#un,off_ens'},
                'login_ip':{'type':'text','title':'آی پی ورود ویژه','len':'3'},
                'auth_prj':{'type':'reference','title':'حق دسترسی به پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['multiple']},
                'file_access':{'type':'text','title':'فایل های قابل دسترس','len':'20'},
                
                'tel_mob':{'type':'text','title':'موبایل','len':'13'},
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
                },
            'steps':{
                '0':{'tasks':'m_w,pre_n,name,family,a_name,eng,office,job,un,loc','xjobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                '1':{'tasks':'file_ot,file_off','xjobs':'off_ens','title':'تکمیل','app_keys':'y,r','app_titls':'','oncomplete_act':'','auth':'dccm'},#'xjobs':'#task#un,dccm',
                '2':{'tasks':'p_id','xjobs':'off_ens','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':'',
                        'start_step':'1','start_where':"'{step_1_ap}' == 'y'",'end_where':"False",'auth':'dccm,#task#un,off_ens',},
                'b':{'tasks':'tel_wrk','xjobs':'#task#un','title':'ثبت اطلاعات توسط فرد','app_keys':'y','app_titls':'','oncomplete_act':'',
                        'name':'b','auth':'dccm,#task#un,off_ens','start_step':'1','start_where':"'{step_1_ap}' == 'y'",'end_where':"False"},
                'c1':{'tasks':'tel_mob,date,rlgn,mltr,Idc_num,shnsnme_num,father,brt_pos,mrg_case,mrg_date,n_suprt,n_child,lable_1,edu_l_cert_grade,edu_l_cert_date,edu_l_cert_pos,edu_l_cert_univ,edu_l_cert_dcpln,start_date,home_adrs,tel_home,mrf_name',
                        'xjobs':'#task#un','title':'ثبت اطلاعات توسط فرد- بخش 1','app_keys':'y','app_titls':'','oncomplete_act':'',
                        'name':'c1','auth':'dccm,#task#un,off_ens','start_step':'','start_where':"True",'end_where':"'{step_c2_ap}' == 'y'"},
                'c2':{'tasks':'file_cv,file_mdrk_thsl,file_shnsnm,file_ins_rec,idc_p1_file,idc_p2_file,file_pic_per,idc_serial',
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
                'all':{'input':'pre_n,file_pic_per,file_shnsnm,file_mdrk_thsl,file_ot,file_off,auth_prj','view1':'un,name,family','view2':'p_id','auth':'dccm'},
                },
            'cols_filter':{
                '':'همه',
                'name,family,tel_wrk':'تلفن داخلی',
                },
            'data_filter':{
                '':'همه همکاران',
                'loc = "100"':'همکاران دفتر مرکزی مشهد',
                'loc = "101"':'همکاران دفتر تهران',
                'loc = "102"':'همکاران دفتر حرم رضوی',
                },
        }
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
    'doc_num':{ #db
        'a':{
            'base':{'mode':'form','title':'شماره گذاری مدارک','help':'document_numbering','code':'401'
            },
            'tasks':{
                'prj':{'type':'reference','width':'5','title':'پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'prj_name':{'type':'auto','len':'50','auto':"{{=__objs__['prj']['output_text'][5:]}}",'title':'نام پروژه'},
                'sub_p':{'type':'reference','width':'5','title':'زیر پروژه','ref':{'db':'a_sub_p','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}"'''},'prop':['update']},
                'sub_p_name':{'type':'auto','len':'50','auto':"{{=__objs__['sub_p']['output_text'][4:]}}",'title':'نام زیر پروژه'},
                'step':{'type':'reference','width':'5','title':'مرحله','ref':{'db':'a_step','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}" AND sub_p =  "{{=__objs__['sub_p']['value']}}"'''},'prop':['update']},
                'step_name':{'type':'auto','len':'50','auto':"{{=__objs__['step']['output_text'][3:]}}",'title':'نام مرحله'},
                'dspln':{'type':'reference','width':'5','title':'دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'dspln_name':{'type':'auto','len':'50','auto':"{{=__objs__['dspln']['output_text'][3:]}}",'title':'نام دیسیپلین'},
                'doc_t':{'type':'reference','width':'5','title':'نوع مدرک','ref':{'db':'a_doc','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'doc_t_name':{'type':'auto','len':'50','auto':"{{=__objs__['doc_t']['output_text'][3:]}}",'title':'نام نوع مدرک'},
                'doc_p_code':{'type':'auto','len':'24','auto':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}','title':'پیش کد مدرک'},
                'doc_srl_code':{'type':'text','len':'4','lang':'en','title':'کد سریال مدرک','uniq':''},
                'doc_srl_name':{'type':'text','len':'250','title':'نام مدرک'},               
            },
            'steps':{
                'pre':{'tasks':'prj,prj_name,sub_p,sub_p_name,step,step_name,dspln,dspln_name,doc_t,doc_t_name','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'doc_p_code,doc_srl_code','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'doc_srl_name','xjobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'all':{'input':'prj,sub_p,step,dspln,doc_t,doc_srl_code,doc_srl_name','view1':'','view2':''},
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
                'file_edt':{'type':'file','len':'40','file_name':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}-{doc_srl_code}-{rev}-{{=date[2:4]+date[5:7]+date[8:10] if date else ""}}','file_ext':"doc,docx,xls,xlsx,ppt,pptx,dwg,zip,rar",'path':'prj,{prj},{sub_p},{step},{dspln},{doc_t}','title':'فایل نهایی با فرمت تغییر پذیر'},
                'file_fix':{'type':'file','len':'40','file_name':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}-{doc_srl_code}-{rev}-{{=date[2:4]+date[5:7]+date[8:10] if date else ""}}','file_ext':"pdf,gif,jpg,jpeg,png",'path':'prj,{prj},{sub_p},{step},{dspln},{doc_t}','title':'فایل نهایی با فرمت ثابت'},
                'snd_ppr':{'type':'text','len':'240','title':'شماره نامه های ارسال فایل'},
            },
            'steps':{
                'pre':{'tasks':'prj,sub_p,step,dspln,doc_t','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'doc_p_code,doc_srl_code,doc_srl_name','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'doc_a_code,rev,date','xjobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'file_edt,file_fix','xjobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'all':{'input':'prj,sub_p,step,dspln,doc_t','view1':'doc_p_code','view2':'doc_p_code'}
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'doc_tqm':{ #db
        'a':{
            'base':{'mode':'form','title':'اسناد مدیریت کیفیت','help':'document_for_TQM','code':'402'
            },
            'tasks':{
                'name':{'type':'text','width':'60','title':'نام مدرک'},
                'user_crt':{'type':'user','title':'تهیه کننده','prop':{'multiple'}},
                'units':{'type':'select','title':'معاونت مرتبط','select':{'D':'design-طراحی','S':'supervition-نظارت','P':'plan - برنامه ریزی و توسعه','M':'Management - مدیریت','-':'نا مشخص'},'prop':['multiple']},
                'code':{'type':'text','width':'40','title':'کد مدرک'},
                'f_code':{'type':'auto','len':'8','auto':'aqrc-tqm-{{=str(id).zfill(3)}}','title':'کد فایل'},
                'file_inc_v':{'type':'file','len':'40','file_name':'{{=f_code}}-inc-v','file_ext':"doc,docx,xls,xlsx,zip,rar",'path':'form,doc_tqm','title':'فایل ورودی'},
                'file_inc_r':{'type':'file','len':'40','file_name':'{{=f_code}}-inc-r','file_ext':"pdf",'path':'form,doc_tqm','title':'pdf - فایل ورودی'},
                'file_1cr_v':{'type':'file','len':'40','file_name':'{{=f_code}}-1cr-v','file_ext':"doc,docx,xls,xlsx,zip,rar",'path':'form,doc_tqm','title':'سند اولیه'},
                'file_1cr_r':{'type':'file','len':'40','file_name':'{{=f_code}}-1cr-r','file_ext':"pdf",'path':'form,doc_tqm','title':'pdf - سند اولیه'},
                'file_2fr_v':{'type':'file','len':'40','file_name':'{{=f_code}}-2fr-v','file_ext':"doc,docx,xls,xlsx,zip,rar",'path':'form,doc_tqm','title':'فرمت شده'},
                'file_2fr_r':{'type':'file','len':'40','file_name':'{{=f_code}}-2fr-r','file_ext':"pdf",'path':'form,doc_tqm','title':'pdf فرمت شده'},
            },
            'steps':{
                'pre':{'tasks':'name,user_crt,units,code','xjobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'f_code,file_inc_v,file_inc_r,file_1cr_v,file_1cr_r','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'file_2fr_v,file_2fr_r','xjobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'units','view1':'name,user_crt,code','view2':'code'}
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'doc_mm':{ #db
        'a':{
            'base':{'mode':'form','title':'صورت جلسه','help':'meeting minute','code':'403'
            },
            'tasks':{
                'name':{'type':'text','width':'60','title':'عنوان جلسه'},
                'date':{'type':'fdate','title':'تاریخ جلسه','prop':['update']},
                'time_st':{'type':'time_c','title':'ساعت شروع جلسه','def_value':'07:00'},
                'user_crt':{'type':'user','title':'تهیه و تنظیم','prop':{'multiple'}},
                'units':{'type':'select','title':'معاونت مرتبط','select':{'D':'design-طراحی','S':'supervition-نظارت','P':'plan - برنامه ریزی و توسعه','M':'Management - مدیریت','-':'نا مشخص'},'prop':['multiple']},
                'mm_type':{'type':'select','title':'نوع جلسه','select':{'I':'Interior-داخلی','C':'Client-کارفرما','O':'OutSource - با برون سپارها'},'prop':['update']},
                'c_prj_id':{'type':'reference','width':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update','multiple']},
                'c_prj_txt':{'type':'auto-x','width':'70','ref':'c_prj_id'},
                'code':{'type':'auto','len':'8','auto':'aqrc-_mm-{{=date[:4]+date[5:7]+date[8:10] if date else "000000"}}-{{=str(id).zfill(4)}}-{mm_type}','title':'کد فایل'},
                'file_v':{'type':'file','len':'40','file_name':'{{=code}}-vec','file_ext':"doc,docx,xls,xlsx,zip,rar",'path':'form,doc__mm','title':'فایل اصلی'},
                'file_r':{'type':'file','len':'40','file_name':'{{=code}}-ras','file_ext':"pdf",'path':'form,doc__mm','title':'pdf'},
                'des_1':{'type':'text','width':'60','title':'توضیحات'},
            },
            'steps':{
                'pre':{'tasks':'date,time_st,user_crt,units,mm_type,c_prj_id,c_prj_txt,name','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'code,file_v,file_r','xjobs':'#step#0','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'des_1','xjobs':'dccm','title':'مدیریت سوابق','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'des_1','view1':'name,date,time_st,user_crt,units,mm_type,c_prj_id,c_prj_txt','view2':'code,file_v,file_r'}
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'doc_mm2':{ #db
        'a':{
            'base':{'mode':'form','title':'صورت جلسه هوشمند - نسخه بتا','help':'meeting minute','code':'903','xform_cg_file':'doc_mm2.html'
            },
            'tasks':{
                'name':{'type':'text','width':'60','title':'عنوان جلسه'},
                'date':{'type':'fdate','title':'تاریخ جلسه','prop':['update']},
                'time_st':{'type':'time_c','title':'ساعت شروع جلسه','def_value':'07:00'},
                'user_crt':{'type':'user','title':'تهیه و تنظیم','prop':{'multiple'}},
                'units':{'type':'select','title':'معاونت مرتبط','select':{'D':'design-طراحی','S':'supervition-نظارت','P':'plan - برنامه ریزی و توسعه','M':'Management - مدیریت','-':'نا مشخص'},'prop':['multiple']},
                'mm_type':{'type':'select','title':'نوع جلسه','select':{'I':'Interior-داخلی','C':'Client-کارفرما','O':'OutSource - با برون سپارها'},'prop':['update']},
                'c_prj_id':{'type':'reference','width':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update','multiple']},
                'c_prj_txt':{'type':'auto-x','width':'70','ref':'c_prj_id'},
                'code':{'type':'auto','len':'8','auto':'aqrc-_mm-{{=date[:4]+date[5:7]+date[8:10] if date else "000000"}}-{{=str(id).zfill(4)}}-{mm_type}','title':'کد فایل'},
                'file_v':{'type':'file','len':'40','file_name':'{{=code}}-vec','file_ext':"doc,docx,xls,xlsx,zip,rar",'path':'form,doc__mm','title':'فایل اصلی'},
                'file_r':{'type':'file','len':'40','file_name':'{{=code}}-ras','file_ext':"pdf",'path':'form,doc__mm','title':'pdf'},
                'des_1':{'type':'text','width':'60','title':'توضیحات'},
                'pos':{'type':'f2f','width':'60','title':'محل جلسه','ref':{'db':'doc_mm2','tb':'pos','show_cols':['name','per']},},
                'todo':{'type':'f2f','width':'60','title':'اقدامات','ref':{'db':'doc_mm2','tb':'todo','show_cols':['p_sy','des','p_do','p_ch','dur']},},
                'note':{'type':'f2f','width':'60','title':'مذاکرات','ref':{'db':'doc_mm2','tb':'note','show_cols':['p_sy','des']},},
            },
            'steps':{
                'pre':{'tasks':'date,time_st,user_crt,units,mm_type,c_prj_id,c_prj_txt,name','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'code,pos,todo,note,file_v,file_r','xjobs':'#step#0','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'des_1','xjobs':'dccm','title':'مدیریت سوابق','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'des_1','view1':'name,date,time_st,user_crt,units,mm_type,c_prj_id,c_prj_txt','view2':'code,file_v,file_r'}
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        },
        'pos':{
            'base':{'mode':'form','title':'محل جلسه','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','width':'5','title':'فرم مبنا','ref':{'db':'doc_mm2','tb':'a','key':'{id}','val':'{date} , {c_prj_txt} , {name}'},'prop':['readonly']},
                'name':{'type':'text','width':'60','title':'نام محل'},
                'per':{'type':'text','width':'80','title':'افراد حاضر'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,name,per','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            
        },
        'todo':{
            'base':{'mode':'form','title':'اقدامات جلسه','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','width':'5','title':'فرم مبنا','ref':{'db':'doc_mm2','tb':'a','key':'{id}','val':'{date} , {c_prj_txt} , {name}'},'prop':['readonly']},
                'p_sy':{'type':'text','width':'60','title':'اعلام'},
                'des':{'type':'text','width':'80','title':'شرح اقدام'},
                'p_do':{'type':'text','width':'60','title':'انجام'},
                'p_ch':{'type':'text','width':'60','title':'پیگیری'},
                'dur':{'type':'text','width':'60','title':'زمان'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,p_sy,des,p_do,p_ch,dur','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            
        },
        'note':{
            'base':{'mode':'form','title':'مذاکرات جلسه','code':'93'
            },
            'tasks':{
                'f2f_id':{'type':'reference','width':'5','title':'فرم مبنا','ref':{'db':'doc_mm2','tb':'a','key':'{id}','val':'{date} , {c_prj_txt} , {name}'},'prop':['readonly']},
                'p_sy':{'type':'text','width':'60','title':'اعلام'},
                'des':{'type':'text','width':'80','title':'شرح'},
            },
            'steps':{
                'pre':{'tasks':'f2f_id,p_sy,des','xjobs':'*','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            
        }
    },
    #--------------------------------------------------------------------
    'person_act':{ #db
        'a':{
            'base':{'mode':'form','title':'اقدامات هر فرد','help':'person_act_manage','code':'410'
            },
            'tasks':{
                'frd_id':{'type':'auto-x','len':'4','auto':'_cur_user_id_','title':'کد همکار'},
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'نام همکار'},
                'date1':{'type':'fdate','width':'10','title':'تاریخ','prop':[]},
                'prj_id':{'type':'reference','width':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d},{cp_code},{cp_name}'},'title':'پروژه','prop':['update']},
                'cp_code':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_code}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'کد پروژه'},
                'cp_name':{'type':'auto','ref':{'db':'a_cur_subject','tb':'a','key':'__0__','val':'{cp_name}','where':'''id = "{{=__objs__['prj_id']['value']}}"'''},'title':'نام پروژه'},
                'act_des':{'type':'text','len':'255','title':'شرح اقدام'},
                'act_cat':{'type':'text','len':'35','title':'دسته اقدام'},
                'time':{'type':'time_t','title':'به مدت','def_value':'0:30'},
            },
            'steps':{
                'pre':{'tasks':'frd_id,frd_1,date1,prj_id,cp_code,cp_name,act_cat,act_des,time','xjobs':'*','title':'ورود اطلاعات','app_keys':'y','app_titls':'','oncomplete_act':''},
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
                'date':{'type':'fdate','width':'10','title':'تاریخ مراجعه'},
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
    'a_contract':{ #db
        'a':{
            'base':{'mode':'form','title':'ثبت قراردادهای شرکت','help':'','code':'120','data_filter':'','multi_app':{'0':['ks'],'1':['ks']},
            },
            'tasks':{
                'subject':{'type':'text','title':'موضوع قرارداد','len':'250'},
                'client':{'type':'text','title':'کارفرما'},
                'date':{'type':'fdate','title':'تاریخ ابلاغ قرارداد'},
                'prj_dur':{'type':'num','min':1,'max':1200,'len':'4','step':'0.1','title':'مدت قرارداد - ماه'},
                'serv_type':{'type':'select','title':'نوع خدمات','select':{'D':'design-طراحی','S':'supervition-نظارت','M':'MC-مدیریت طرح','-':'نا مشخص'},'prop':['multiple']},
                'f_cnt':{'type':'file','auth':'dcc_prj','len':'40','title':'فایل متن قرارداد امضا شده','file_name':'contract-{{=str(id).zfill(4)}}-{{=date[:4] if date else ""}}-','file_ext':"pdf",'path':'form,contract'},
                'f_cnt_ppr':{'type':'file','auth':'dcc_prj','len':'40','title':'نامه قرارداد در اتوماسیون','file_name':'contract-{{=str(id).zfill(4)}}-{{=date[:4] if date else ""}}-ppr','file_ext':"pdf",'path':'form,contract'},
                'f_cnt_1p':{'type':'file','auth':'dcc_prj','len':'40','title':'سایر اسناد مرتبط','file_name':'contract-{{=str(id).zfill(4)}}-{{=date[:4] if date else ""}}-1p','file_ext':"pdf,zip",'path':'form,contract'},
                'verify_note':{'type':'text','len':'40','title':'توضیحات بررسی کننده'},
                'des':{'type':'text','len':'250','title':'توضیح'},
                'n_contr':{'type':'text','len':'40','title':'شماره قرارداد'},
                'chlng':{'type':'text','len':'240','title':'چالش','help':'challenge'},
                'solution':{'type':'text','len':'240','title':'راهکار','help':'solution'},
                'price':{'type':'num','min':1,'max':900000,'len':'6','title':'مبلغ اولیه','title_add':'مبلغ اولیه قرارداد بدون احتساب افزایش الحاقیه بر حسب میلیون تومان','auth':'dcc_prj'},
                'price_se':{'type':'num','min':1,'max':900000,'len':'6','title':'مبلغ نهایی','title_add':'مبلغ صورت وضعیت ارسالی بر حسب میلیون تومان'},
                'date_lse':{'type':'fdate','title':'تاریخ آخرین صورت وضعیت ارسالی'},
                'frd_peygir':{'type':'reference','width':'5','title':'مسئول پیگیری','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}- {m_w} {name} {family}'},'prop':['show_full']},
                'prj_step1':{'type':'select','title':'وضعیت کلی','select':{'1':'پروپوزال','2':'در حال قرارداد','11':'جاری','21':'گذشته  و ناتمام مالی','31':'خاتمه کامل'}},
                'price_off':{'type':'num','min':0,'max':100,'len':'6','title':'درصد تخفیف'},
                'user_cord':{'type':'user','title':'مسئول هماهنگی','prop':{'multiple'}}, #cordinator
                'busn_name':{'type':'text','title':'عنوان تجاری','len':'80'},
                'pos_link':{'type':'text','title':'لینک موقعیت','len':'80','link':{'target':'_blank','text':'G','class':'btn btn-info'},},
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
                'b':{'tasks':'busn_name,chlng,solution,pos_link,ppr_name,key_words,user_cord,f_busn_id,f_exe_pic,f_rndr','xjobs':'tqm_a','title':'فراداده ها','app_keys':'y','app_titls':'','oncomplete_act':'',
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
    'suggestion':{ #db
        'a':{
            'base':{'mode':'form','title':'ثبت پیشنهاد','code':'311'
            },
            'tasks':{
                'idea':{'type':'text','title':'شرح ایده / پیشنهاد'},
                'idea_bnft':{'type':'text','title':'فایده ایده / پیشنهاد'},
                'idea_dscr':{'type':'text','title':'توضیحات لازم'},
                'vrfy_rslt':{'type':'text','title':'نتیجه بررسی'},
                'vrfy_meta':{'type':'text','title':'اقدامات انجام شده جهت بررسی'},
                'clnt_stf':{'type':'num','min':'1','max':'100', 'title':'میزان رضایت پیشنهاد دهنده از اقدامات انجام شده بر حسب درصد'},
                'clnt_stf_dscr':{'type':'text','title':'توضیحات در خصوص میزان رضایت'},
            },
            'steps':{
                's0':{'tasks':'lable_1,idea,idea_bnft,idea_dscr','xjobs':'*','title':'ثبت پیشنهاد','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'lable_2,vrfy_rslt,vrfy_meta','xjobs':'rda','title':'بررسی','app_keys':'','app_titls':'','oncomplete_act':''},
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
        }
    },
    #--------------------------------------------------------------------
    'errors':{
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
                'date':{'type':'fdate','width':'10','title':'تاریخ ابلاغ'},
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
    #--------------------------------------------------------------------time_st,time_len '"10:55","5:25"'	'auto':'{{import k_time}}{{=k_time.add("10:55","5:25")}}'},'''
    'off_morkhsi_saat':{ #db
        'a':{
            'base':{'mode':'form','title':'مرخصی ساعتی','data_filter':'f_nxt_u = "{{=_i_}}"','code':'201','multi_app':{'1':['rms'],'2':['mlk']},
            },
            'tasks':{
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'درخواست کننده'},
                'date':{'type':'fdate','width':'10','title':'تاریخ','prop':[]},
                'time_st':{'type':'time_c','title':'از ساعت','prop':['update'],'def_value':'07:00'},
                'time_len':{'type':'time_t','title':'به مدت','time_inf':{'maxTime':"03:30"},'prop':['update'],'def_value':'0:30'},
                'time_en':{'type':'auto','title':'تا ساعت','auto':'''{{import k_time}}{{=k_time.add(__objs__['time_st']['value'],__objs__['time_len']['value'])}}'''},
                'frd_modir':{'type':'reference','width':'5','title':'مدیر مربوطه','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}- {m_w} {name} {family}'},'prop':['show_full']},
                'des_0':{'type':'text','len':150,'lang':'fa','title':'توضیحات'},
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
            'cols_filter':{'':'همه',},
            'data_filter': 
                {'step_2_dt like "{{=_d_}}%"':'فرمهای نهایی شده در امروز',
                },
        }
    },
    #-------------------------------------------------------------------- 's2':{'tasks':'des_2','xjobs':'#step#0','title':'ثبت نتیجه','app_keys':'y,r,x','app_titls':['انجام شد','بازگشت جهت اصلاح','انجام نشد'],'oncomplete_act':''},
    'off_mamurit_saat':{ #db
        'a':{
            'base':{'mode':'form','title':'ماموریت ساعتی','data_filter':'f_nxt_u = "{{=_i_}}"','code':'203','multi_app':{'1':['rms'],'3':['mlk']},
            },
            'tasks':{
                'frd_1':{'type':'auto-x','len':'24','auto':'_cur_user_','title':'مامور'},
                'date':{'type':'fdate','width':'10','title':'تاریخ','prop':[]},
                'time_st':{'type':'time_c','title':'ساعت شروع ماموریت','prop':['update'],'def_value':'07:00'},
                'time_len':{'type':'time_t','title':'مدت ماموریت','time_inf':{'maxTime':"20:00"},'prop':['update'],'def_value':'0:30'},
                'time_en':{'type':'auto','title':'تا ساعت','auto':'''{{import k_time}}{{=k_time.add(__objs__['time_st']['value'],__objs__['time_len']['value'])}}'''},
                'frd_modir':{'type':'reference','width':'5','title':'مدیر مربوطه','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}- {m_w} {name} {family}'},'prop':['show_full']},
                'des_0':{'type':'text','len':700,'lang':'fa','title':'شرح ماموریت'},
                'des_modir':{'type':'text','len':150,'lang':'fa','title':'توضیح'},
                'des_2':{'type':'text','len':150,'lang':'fa','title':'توضیحات'},
                'des_off':{'type':'text','len':150,'lang':'fa','title':'توضیحات'},
                'c_prj_id':{'type':'reference','width':'30','ref':{'db':'a_cur_subject','tb':'a','key':'{id}','val':'{id:03d};{cp_code};{cp_name}'},'title':'پروژه','prop':['update','multiple']},
                'c_prj_txt':{'type':'auto-x','width':'30','ref':'c_prj_id'},
            },
            'steps':{
                's0':{'tasks':'frd_1,date,lable_2,time_st,time_len,time_en,frd_modir,lable_1,des_0,c_prj_id,c_prj_txt','xjobs':'*','title':'ثبت فرم توسط درخواست کننده','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'des_modir','xjobs':'#task#frd_modir','title':'تایید مدیر','app_keys':'y,r','app_titls':['مورد تایید است','فرم اصلاح شود'],'oncomplete_act':''},
                's2':{'tasks':'time_len,time_en,des_2,c_prj_id,c_prj_txt','xjobs':'#step#0','title':'ثبت نتیجه','app_keys':'y,r,x','app_titls':['انجام شد','بازگشت جهت اصلاح','انجام نشد'],'oncomplete_act':''},
                's3':{'tasks':'des_off','xjobs':'off_ens','title':'تطابق با ساعت دستگاه و ثبت اطلاعات','app_keys':'y,r','app_titls':['انجام شد','بازگشت جهت اصلاح'],'oncomplete_act':''}
            },
            'views':{
                'all':{'input':'frd_1,time_st,time_len,frd_modir,des_0','view1':'des_jnshin','view2':'des_modir'}
            },
            'labels':{
                'lable_1':'محل و هدف ماموریت را ذکر بفرمایید',
                'lable_2':'در مرحله اول زمان ماموریت را به صورت حدودی وارد نمایید در مرحله سوم و پس از تایید مدیر و بازگشت از ماموریت می توانیر آنرا تدقیق نمایید',
            },
            'cols_filter':{'':'همه',},
            'data_filter': 
                {'step_3_dt like "{{=_d_}}%"':'فرمهای نهایی شده در امروز',
                },
        }
    },
    #-------------------------------------------------------------------- 's2':{'tasks':'des_2','xjobs':'#step#0','title':'ثبت نتیجه','app_keys':'y,r,x','app_titls':['انجام شد','بازگشت جهت اصلاح','انجام نشد'],'oncomplete_act':''},
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
                'des':{'type':'text','title':'توضیحات','len':'250'},
            },
            'steps':{
                's0':{'tasks':'m_w,pre_n,name,family,tel_mob,tel_wrk,job,des','xjobs':'*','title':'ثبت فرم توسط درخواست کننده','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'all':{'input':'m_w,pre_n,name,family,tel_mob,tel_wrk,job,des','view1':'family','view2':'family'}
            },
            'cols_filter':{'':'همه',},
            'data_filter': {},
         }
    },
    #--------------------------------------------------------------------
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
                },
            'steps':{
                'pre':{'tasks':'subj,for_grup,tchr_name,tchr_exprt','xjobs':'edu','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'date,time_len,pos,cls_mod,cls_org,file_code','xjobs':'edu','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'user_n,usr_cmnt_file,cls_form_file,usr_cert_file,cls_lrn_file,news_link,news_file','xjobs':'edu','title':'تکمیل','app_keys':'y,r','app_titls':'','oncomplete_act':'','auth':'dccm'},#'xjobs':'#task#un,dccm',
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
    'test':{ #db
        'b':{
            'base':{'mode':'form','title':'بررسی عملکرد فیلدهای هوشمند در مرحله پیش انتشار','code':'990'
                },
            'tasks':{
                'txt':{'type':'text','len':50,'lang':'fa','title':'متن','uniq':''},#'sel=`x`'
                'n':{'type':'num','min':5,'max':15,'title':'عدد','prop':[]},
                'sel':{'type':'select','select':{'a':'طراحی','x':'نظارت'},'title':'واحد','prop':[]},
                'ref':{'type':'reference','width':'5','title':' مسئول اقدام','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{m_w} {pre_n} {name} {family}'},'prop':[]},
                'ch':{'type':'check','title':'با این موضع موافقم','prop':[]},
                'dt':{'type':'fdate','width':'10','title':'تاریخ انجام کار','prop':[]},
                'at':{'type':'auto','len':'24','auto':'{n}-{sel}-{ch}-{ref}-{dt:}','title':'کد اتوماتیک'},
                'indx1':{'type':'index','len':'4','ref':{'db':'test','tb':'b','key':'{id}','val':'{indx1}','where':''},'title':'شماره'},
                'fl':{'type':'file','len':'24','file_name':'abc-{{=int("0"+n)+25}}-{sel}-{{=dt[:4] if dt else ""}}','file_ext':"gif,jpg,jpeg,png,doc,docx,xls,xlsx,pdf,dwg,zip,rar",'path':'test,a,c,{txt}-{n}','title':'فایل نهایی'},#,'x':'{txt}-{n}-{sel}-{ch}-{ref}'
                'tt':{'type':'time_c','title':'زمان شروع'},
                'time_st2':{'type':'time_c','title':'از ساعت','def_value':'{tt}'},
                'frd_jnshin':{'type':'reference','width':'5','title':'جانشین','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}- {m_w} {name} {family}'},'prop':['show_full']},
            },
            'steps':{
                'pre':{'tasks':'txt,n,sel,indx1','xjobs':'*','title':'ثبت اطلاعات اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'ref,ch,tt,dt','xjobs':'des_eng_ar','title':'ثبت اطلاعات تکمیلی','app_keys':'y,x,r','app_titls':'','oncomplete_act':''},
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
def x_data_verify_task(obj_name,obj):
    obj['name']=obj_name
    if not 'prop' in obj:obj['prop']=[]
    if not 'width' in obj:obj['width']='10'
    if not 'title' in obj:obj['title']=obj['type']+'-'+obj_name
    if not 'def_value' in obj:obj['def_value']=''
    if not 'onchange' in obj:obj['onchange']=''
def x_data_verify(x_data): 
    #defult data_filter
    data_filter={'':'همه موارد',
                'step_0_un = "{_i_}"':'فرم های من',
                'f_nxt_u = "{{=_i_}}"':'فرمهای منتظر من',
                'f_nxt_u != "y"':'فرمهای نهایی نشده'
                }
    for db_name,db_obj in x_data.items():
        for tb_name,tb_obj in db_obj.items():
            #print(str(tb_obj))
            for obj_name,obj in tb_obj['tasks'].items():
                #for obj_name,obj in ff_o.items():
                x_data_verify_task(obj_name,obj)
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