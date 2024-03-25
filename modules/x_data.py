# -*- coding: utf-8 -*-
# ver 1.00 1401/09/24 
# -------------------------------------------------------------------------
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
steps.jobs= list of name of jobs 
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
"""
x_data={
    
    'a_prj':{
        'a':{
            'base':{'mode':'form','title':'کد پروژه'},
            'tasks':{
                'code':{'type':'text','title':'کد پروژه','len':'4','prop':['uniq']},
                'name':{'type':'text','title':'نام پروژه','lang':'fa'},
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
                'pre':{'tasks':'lable_1,name,per,date,code,code_hlp','jobs':'dcc_prj','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'cnt_name,cmn_name,client,client_mn,client_pr,prj_dur,date,serv_type','jobs':'dcc_prj','title':'اطلاعات کلی','app_keys':'','app_titls':'','oncomplete_act':''},
                'sbt':{'tasks':'code,code_hlp,name,serv_type,date','jobs':'dccm','title':'ثبت نهایی','app_keys':'y,x,r','app_titls':'','oncomplete_act':''},
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
    #--------------------------------------------------------------------
    'a_sub_p':{
        'a':{
            'base':{'mode':'form','title':'زیر پروژه'},
            'tasks':{
                'prj':{'type':'reference','width':'5','title':' پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':[]},
                'code':{'type':'text','title':'کد زیر پروژه','len':'3','prop':['uniq']},
                'name':{'type':'text','title':'نام زیر پروژه'},
                'code2':{'type':'auto','len':'8','auto':'{{=prj[:4].upper()}}-{code}','title':'کد کامل زیر پروژه'},
                'name2':{'type':'auto','len':'256','auto':"{{=__objs__['prj']['select'][prj][5:].strip()}}-{name}",'title':'نام کامل زیر پروژه'},
                'des':{'type':'text','title':'توضیح زیر پروژه'},
                'date':{'type':'fdate','title':'تاریخ ثبت'},
                'auth_users':{'type':'reference','width':'20','title':' افراد دارای حق دسترسی','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{m_w} {pre_n} {name} {family}'},'prop':['multiple']},
            },
            'steps':{
                'pre':{'tasks':'prj,code,name','jobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'code2,name2,des,date','jobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
                'auth':{'tasks':'auth_users','jobs':'dccm','title':'دسترسی','app_keys':'','app_titls':'','oncomplete_act':''},
            },  
            'views':{
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'a_step':{
        'a':{
            'base':{'mode':'form','title':'کد مرحله'},
            'tasks':{
                'prj':{'type':'reference','width':'5','title':' پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'sub_p':{'type':'reference','width':'5','title':' زیر پروژه','ref':{'db':'a_sub_p','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}"'''},'prop':[]},
                'code':{'type':'text','title':'کد مرحله','len':'2'},
                'name':{'type':'text','title':'نام مرحله'},
                'date':{'type':'fdate','title':'تاریخ ثبت'},
            },
            'steps':{
                'pre':{'tasks':'prj,sub_p','jobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'date,code,name','jobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'a_dspln':{
        'a':{
            'base':{'mode':'form','title':'کد دیسیپلین'},
            'tasks':{
                'code':{'type':'text','title':'کد','len':'2','prop':['uniq']},
                'name_e':{'type':'text','title':'DECIPLINE NAME'},
                'name':{'type':'text','title':'نام دیسیپلین'},
                'n':{'type':'text','title':'ترتیب'},
                'des':{'type':'text','title':'توضیح'},
                'date':{'type':'text','title':'تاریخ ثبت'},
            },
            'steps':{
                'pre':{'tasks':'code,name_e,name','jobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'n,des,date','jobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                'input':['code','name_e','name'],
                'view1':[],
                'view2':[]
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    #'eng'
    #--------------------------------------------------------------------
    'a_doc':{
        'a':{
            'base':{'mode':'form','title':'کد نوع مدرک'},
            'tasks':{
                'dspln':{'type':'reference','width':'5','title':' دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':[]},
                'code':{'type':'text','title':'کد مدرک'},
                'name':{'type':'text','title':'نام مدرک'},
                'name_e':{'type':'text','title':'doc name'},
                
            },
            'steps':{
                'pre':{'tasks':'dspln,code,lable_1','jobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'name,name_e','jobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
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
    'a_loc':{
        'a':{
            'base':{'mode':'form','title':'نام و آدرس دفاتر'
            },
            'tasks':{
                'name':{'type':'text','title':'نام دفتر'},
                'code':{'type':'text','title':'کد دفتر'},
                'addres':{'type':'text','title':'آدرس دفتر'},
                'date_s':{'type':'fdate','title':'تاریخ شروع بهره برداری'},
                'date_e':{'type':'fdate','title':'تاریخ خاتمه بهره برداری'},
            },
            'steps':{
                'pre':{'tasks':'name,code,addres','jobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'date_s','jobs':'dccm','title':'تکمیل','app_keys':'','app_titls':'','oncomplete_act':''},
                'st2':{'tasks':'date_e','jobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #-----------------------------------------------------------------------
    'paper':{
        'a':{
            'base':{'mode':'form','title':'نامه ها'
            },
            'tasks':{
                'prj':{'type':'reference','width':'30','ref':{'db':'prj','tb':'a','key':'{id}','val':'{id:03d}-{name}'},'title':'پروژه'},
                'prj1':{'type':'auto','ref':{'db':'prj','tb':'a','key':'__0__','val':'{prj}','where':'''id = "{{=__objs__['prj']['value']}}"'''},'title':'کد کامل زیر پروژه'},
                'man_crt':{'type':'reference','width':'5','title':'تهیه کننده','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{family}'},'prop':['read']},#,'prop':['read']
                'man_ar_mng':{'type':'reference','width':'5','title':'مسئول طرح معماری','ref':{'db':'user','tb':'user','key':'{id}','val':'{un}-{family}'}},#,'prop':['read']
                'folder':{'type':'text','width':'20','title':'محل فایلها','link':{'url':['spks','file','f_list_sd'],'args':['pp','{folder}'],'vars':{}},'prop':[]},#'hide']},
                
                'lno':{'type':'text','width':'10','title':'شماره نامه','prop':['read']},
                'lno_t':{'type':'num','width':'10','title':'شماره پیشنویس','prop':[]},
                'sbj':{'type':'text','width':'50','title':'موضوع نامه','prop':['read']},
                'date_s':{'type':'fdate','width':'10','title':'تاریخ اولین ارجاع','prop':[]},
                'date_e':{'type':'fdate','width':'10','title':'تاریخ آخرین ارجاع','prop':['read']},
                'comment':{'type':'text','width':'30','title':'خلاصه','prop':['read']},
                'cdate':{'type':'fdate','width':'10','title':'تاریخ ثبت','prop':['read']},#'prop':['hide']
                'io_t':{'type':'text','width':'5','title':'نوع','prop':['read']},
                'outbox':{'type':'text','width':'5','title':'ارسالی','prop':['read']},
                'x_des':{'type':'text','width':'20','title':'توضیح دستی'},#,'prop':['read']
                'x_num':{'type':'text','width':'5','title':'شماره دستی'},#,'prop':['read']
                'paper_num':{'type':'text','width':'6','title':'شماره کوچک','prop':[]},
                'attach':{'type':'text','width':'10','title':'ضمایم','prop':['hide']},
                'act_todo':{'type':'text','width':'150','title':'ارجاع نامه','prop':[]},
                'x_act_todo':{'type':'text','width':'150','title':'اقدامات لازم','prop':[]},
                'x_act_rec':{'type':'text','width':'150','title':'اقدامات انجام شده','prop':[]},
                'x_act_pey':{'type':'text','width':'150','title':'پیگیری','prop':[]},                 
                 #,'get_inf':{'type':'xlink','width':'20','title':'دانلود','link':{'pro':['ksw','aqc','import_paper_inf'],'args':['{lno}']},'prop':['hide']}                
            },
            'steps':{
                'pre':{'tasks':'prj,sbj','jobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                'd1':{'tasks':'prj1','jobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'input':['prj','man_crt','x_num','x_des','x_act_todo','x_act_rec','x_act_pey','act_todo'],
                'view1':['lno','lno_t','sbj'],
                'view2':['comment','date_s','date_e','cdate','io_t','outbox','man_ar_mng','paper_num','attach','folder'],
            },
            'cols_filter':
                {'':'همه',
                'lno':'شماره',
                'lno,sbj':'شماره و موضوع',
                'lno,sbj,date_s':'شماره، موضوع، تاریخ',
                'lno,sbj,date_s,io_t':'شماره، موضوع، تاریخ، نوع',
                'lno,sbj,date_s,io_t,folder':'شماره،موضوع،تاریخ،ص-و،فایلها', 
                'lno,sbj,date_s,io_t,x_num,x_des':'ش.م.ت.ن-دستی : شماره و شرح',
                'prj,lno,sbj,date_s,io_t,x_num,x_des,act_todo,x_act_todo,x_act_rec,x_act_pey':'شماره،موضوع،تاریخ،ص-و،توضیح،اقدام (لازم،سابقه، پی گیری)'}, #table_view cols filter
                #cols_filter={'':'همه','lno,sbj':'2',}
            'data_filter':
                {'':'همه نامه ها',
                'prj is Null':'نیاز به تعیین پروژه',
                'prj = "36"':'پروژه پیوندراه',
                'prj = "29"':'پروژه گیتها',
                'prj = "29" AND x_des like "%L-%"':'-Lپروژه گیتها',
                'prj = "48"':'پروژه استاندارد سازی',
                'act_todo != ""':'دارای ارجاع',
                'x_act_todo != ""':'نیاز به اقدام',
                'act_pey != ""':'پی گیری',
                'lno like "%xxxx%"':'جستجوی نامه'},
            'order':'date_s'    
                
        },#,
    },
    #--------------------------------------------------------------------
    'prj':{
        'a':{
            'base':{'mode':'form','title':'پروژه های KS'
            },
            'tasks':{
                'name':{'type':'text','title':'نام پروژه'},
                'des':{'type':'text','title':'توضیحات'},
                'cat_1':{'type':'text','title':'موارد جاری'},
                'prj':{'type':'reference','width':'5','title':' پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':[]},
                'sub_p':{'type':'reference','width':'5','title':' زیر پروژه','ref':{'db':'a_sub_p','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}"'''},'prop':[]},
            },
            'steps':{
                'pre':{'tasks':'name,des,cat_1,prj,sub_p','jobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                'd1':{'tasks':'prj,sub_p','jobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'input':['prj,sub_p'],
                'view1':['name','cat_1'],
                'view2':['des'],
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'user':{
        'user':{
            'base':{'mode':'form','title':'لیست همکاران'
                },
            'tasks':{
                'un':{'type':'text','title':'نام کاربری','len':'3','prop':['uniq']},
                'ps':{'type':'text','title':'پسورد','prop':['hide'],'len':'20'},
                'm_w':{'type':'select','select':['آقای','خانم'],'title':'جنسیت'},
                'pre_n':{'type':'select','select':['','مهندس','دکتر'],'title':'پیش نام'},
                'name':{'type':'text','title':'نام','len':'15'},
                'family':{'type':'text','title':'فامیل','len':'35'},
                'a_name':{'type':'text','title':'نام در اتوماسیون','len':'50'},
                'eng':{'type':'reference','title':'رسته / دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{name_f}'}},
                #'tel_mob':{'type':'text','title':'موبایل','len':'13','placeholder':"0...-...-....",'data-slots':"."},#,'data-accept':"\d"
                #'tel_mob':{'type':'text','title':'موبایل','len':'13','placeholder':"0...-...-....",'pattern':"0[0-9]{{3}}-[0-9]{{3}}-[0-9]{{4}}"},
                'tel_mob':{'type':'text','title':'موبایل','len':'13'},
                #'tel_wrk':{'type':'text','title':'تلفن','len':'10','placeholder':"....-..-..",'data-slots':".",'data-accept':"\d"},
                'tel_wrk':{'type':'text','title':'تلفن','len':'10','placeholder':"....-..-.."},
                'loc':{'type':'reference','title':'موقعیت','ref':{'db':'a_loc','tb':'a','key':'{code}','val':'{name}'}},
                'office':{'type':'select','select':['طراحی','نظارت','پشتیبانی','مدیریت'],'title':'بخش'},
                #'discipline':{'type':'text','title':'رسته'}
                'job':{'type':'text','title':'سمت','len':'50'}#,'ref':{'db':'user','tb':'job','key':'id','val':'{id}{name}'}
                },
            'steps':{
                'pre':{'tasks':'m_w,pre_n,name,family,a_name,eng,office,job,un','jobs':'dccm','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'tel_mob,tel_wrk','jobs':'#task#un','title':'تکمیل','app_keys':'y,r','app_titls':'','oncomplete_act':''},
                'st2':{'tasks':'job','jobs':'dccm','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{
                },
            'cols_filter':{'':'همه',},
            'data_filter':{
                '':'همه همکاران',
                'loc = "100"':'همکاران دفتر مرکزی مشهد',
                },
        }
    },
    #--------------------------------------------------------------------
    'job':{
        'a':{ 
            'tasks':{
                'code':{'type':'text','title':'کد سمت'},
                'title':{'type':'text','title':'عنوان سمت','lang':'fa'},
                'users':{'type':'reference','title':'لیست همکاران مرتبط','ref':{'db':'user','tb':'user','key':'{un}','val':'{name}-{family}'},'prop':['multiple']},
            },
            'views':{},
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}  
        }
    },
    #--------------------------------------------------------------------
    'doc_rec':{
        'a':{
            'base':{'mode':'form','title':'فرم دریافت مدارک','help':'document_record'
            },
            'tasks':{
                'prj':{'type':'reference','width':'5','title':'پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'sub_p':{'type':'reference','width':'5','title':'زیر پروژه','ref':{'db':'a_sub_p','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}"'''},'prop':['update']},
                'step':{'type':'reference','width':'5','title':'مرحله','ref':{'db':'a_step','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}" AND sub_p =  "{{=__objs__['sub_p']['value']}}"'''},'prop':['update']},
                'dspln':{'type':'reference','width':'5','title':'دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'doc_t':{'type':'reference','width':'5','title':'دیسیپلین','ref':{'db':'a_doc','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'doc_p_code':{'type':'auto','len':'24','auto':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}','title':'پیش کد مدرک'},
                'doc_srl_code':{'type':'text','len':'4','lang':'en','title':'کد سریال مدرک','prop':['uniq']},
                'file_pdf':{'type':'file','len':'24','file_name':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}-{doc_srl_code}','file_ext':"gif,jpg,jpeg,png,doc,docx,xls,xlsx,pdf,dwg,zip,rar",'path':'{prj},{sub_p},{step},{dspln},{doc_t}','x':'{txt}-{n}-{sel}-{ch}-{ref}','title':'فایل نهایی'},
            },
            'steps':{
                'pre':{'tasks':'prj,sub_p,step,dspln,doc_t','jobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'doc_p_code,doc_srl_code','jobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'file_pdf','jobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'input':['prj','sub_p','step','dspln','doc_t'],
                'view1':['doc_p_code'],
                'view2':['doc_p_code'],
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'test':{
        'b':{
            'base':{'mode':'form','title':'فرم بررسی عملکرد فیلدهای هوشمند در مرحله پیش انتشار'
                },
            'tasks':{
                'txt':{'type':'text','len':50,'lang':'fa','title':'متن','prop':['uniq']},
                'n':{'type':'num','min':5,'max':15,'title':'عدد','prop':[]},
                'sel':{'type':'select','select':{'a':'طراحی','x':'نظارت'},'title':'واحد','prop':[]},
                'ref':{'type':'reference','width':'5','title':' مسئول اقدام','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{m_w} {pre_n} {name} {family}'},'prop':[]},
                'ch':{'type':'check','title':'با این موضع موافقم','prop':[]},
                'dt':{'type':'fdate','width':'10','title':'تاریخ انجام کار','prop':[]},
                'at':{'type':'auto','len':'24','auto':'{n}-{sel}-{ch}-{ref}-{dt:}','title':'کد اتوماتیک'},
                'fl':{'type':'file','len':'24','file_name':'abc-{{=int("0"+n)+25}}-{sel}-{{=dt[:4] if dt else ""}}','file_ext':"gif,jpg,jpeg,png,doc,docx,xls,xlsx,pdf,dwg,zip,rar",'path':'test,a,c','x':'{txt}-{n}-{sel}-{ch}-{ref}','title':'فایل نهایی'},
                'tt':{'type':'time','title':'زمان شروع'},
            },
            'steps':{
                'pre':{'tasks':'txt,n,sel','jobs':'*','title':'ثبت اطلاعات اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'ref,ch,tt,dt','jobs':'des_eng_ar','title':'ثبت اطلاعات تکمیلی','app_keys':'y,x,r','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'at,fl,tt','jobs':'#step#0','title':'ثبت فراداده ها','app_keys':'y,x,r','app_titls':'','oncomplete_act':''},
                's4':{'tasks':'dt,at,fl,tt','jobs':'#task#ref','title':'بررسی اطلاعات','app_keys':'y,x,r','app_titls':'','oncomplete_act':''},
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
    if 'prop' not in obj:obj['prop']=[]
    if 'width' not in obj:obj['width']='10'
    if 'title' not in obj:obj['title']=obj['type']+'-'+obj_name
    if 'def_value' not in obj:obj['def_value']=''
    if 'onchange' not in obj:obj['onchange']=''
def x_data_verify(x_data):    
    for db_name,db_obj in x_data.items():
        for tb_name,tb_obj in db_obj.items():
            #print(str(tb_obj))
            for obj_name,obj in tb_obj['tasks'].items():
                #for obj_name,obj in ff_o.items():
                x_data_verify_task(obj_name,obj)
            if 'views' not in tb_obj:tb_obj['views']={}  
            if not tb_obj['views']:
                tb_obj['views']={
                    'input':list(tb_obj['tasks'].keys()),
                    'view1':{},
                    'view2':{}
                }
            if 'base' not in tb_obj:tb_obj['base']={}  
            if 'labels' not in tb_obj:tb_obj['labels']={} 
            #--------------------
            if 'mode' not in tb_obj['base']:tb_obj['base']['mode']='table'  
            tb_obj['base']['tb_name']=tb_name
            tb_obj['base']['db_name']=db_name
            #--------------------
            if 'order' not in tb_obj:tb_obj['order']='id'    
            if 'cols_filter' not in tb_obj:tb_obj['cols_filter']:{'':'همه',}
            if 'data_filter' not in tb_obj:tb_obj['data_filter']:{'':'همه',}  
            if 'steps' in tb_obj:
                i=-1
                for step_name,step in tb_obj['steps'].items():
                    i+=1
                    if 'app_keys' not in step or not step['app_keys']:
                        step['app_keys']='y,x,r' if i>0 else 'y,x'
                    if 'app_titls' not in step or not step['app_titls']:
                        step['app_titls']=[{'x':'حذف فرم','y':'تایید این مرحله','r':'بازگشت به مرحله قبل'}[x] for x in step['app_keys'].split(',')]
                    step['app_keys']=step['app_keys'].split(',')
                    #'app_kt'=app dict from keys and titels
                    step['app_kt']=dict(zip(step['app_keys'],step['app_titls']))
                    step['i']=i
                    #{x:step['app_titls'][i] for i,x in enumerate(step['app_keys'].split(',').reverse())} 
                #tt=','.join[step['tasks']+['step' for sn,step in tb_obj['steps'].items() ]
                #tb_obj['cols_filter']['a']=[
#------------------------------------------------------------------------------
x_data_verify(x_data)
#import k_err
#k_err.xxxprint(vals=x_data,launch=True)
