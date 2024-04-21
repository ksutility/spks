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
    
"""
x_data_cat:{
    '1':{'titel':'ex','db':'a_prj,a_sub_p,a_step'}
}
x_data={
    
    'a_prj':{
        'a':{
            'base':{'mode':'form','title':'کد پروژه'},
            'tasks':{
                'code':{'type':'text','title':'کد پروژه','len':'4','uniq':''},
                'name':{'type':'text','title':'نام پروژه','len':'40','lang':'fa'},
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
    #--------------------------------------------------------------------lable_1,name,
    'a_sub_p':{
        'a':{
            'base':{'mode':'form','title':'زیر پروژه'},
            'tasks':{
                'prj':{'type':'reference','width':'5','title':' پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'code':{'type':'text','title':'کد زیر پروژه','len':'3','uniq':"prj=`{{=__objs__['prj']['value']}}`"},#"prj=`{{=__objs__['prj']['value']}}`"
                'name':{'type':'text','len':'140','title':'نام زیر پروژه'},
                'code2':{'type':'auto','len':'8','auto':'{{=prj[:4].upper()}}-{code}','title':'کد کامل زیر پروژه'},
                'name2':{'type':'auto','len':'256','auto':"{{=__objs__['prj']['select'][prj][5:].strip()}}-{name}",'title':'نام کامل زیر پروژه'},
                'des':{'type':'text','len':'250','title':'توضیح زیر پروژه'},
                'date':{'type':'fdate','title':'تاریخ ثبت'},
                'auth_users':{'type':'reference','width':'20','title':' افراد دارای حق دسترسی','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{m_w} {pre_n} {name} {family}'},'prop':['multiple']},
            },
            'steps':{
                'pre':{'tasks':'prj,code,name','jobs':'dcc_prj','title':'تعریف اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
                'inf':{'tasks':'code2,name2,des,date','jobs':'dcc_prj','title':'ثبت نهایی','app_keys':'','app_titls':'','oncomplete_act':''},
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
                'code':{'type':'text','title':'کد','len':'2','uniq':''},
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
            'base':{'mode':'form','title':'نامه ها','auth':'dccm'
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
                'un':{'type':'text','title':'نام کاربری','len':'3','uniq':''},
                'ps':{'type':'text','title':'پسورد','prop':['hide'],'len':'20'},
                'm_w':{'type':'select','select':['آقای','خانم'],'title':'جنسیت'},
                'pre_n':{'type':'select','select':['','مهندس','دکتر'],'title':'پیش نام'},
                'name':{'type':'text','title':'نام','len':'15'},
                'family':{'type':'text','title':'فامیل','len':'35'},
                'a_name':{'type':'text','title':'نام در اتوماسیون','len':'50'},
                'eng':{'type':'reference','title':'رسته / دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{name}'}},
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
            'base':{'mode':'form','title':'فرم سمتها','help':'document_record'
            },
            'tasks':{
                'code':{'type':'text','title':'کد سمت'},
                'title':{'type':'text','title':'عنوان سمت','lang':'fa'},
                'users':{'type':'reference','title':'لیست همکاران مرتبط','ref':{'db':'user','tb':'user','key':'{un}','val':'{name}-{family}'},'prop':['multiple']},
            },
            'steps':{
                's0':{'tasks':'code,title','jobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'users','jobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
            },
            'views':{},
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}  
        }
    },
    #--------------------------------------------------------------------
    'doc_num':{
        'a':{
            'base':{'mode':'form','title':'فرم شماره گذاری مدارک','help':'document_numbering'
            },
            'tasks':{
                'prj':{'type':'reference','width':'5','title':'پروژه','ref':{'db':'a_prj','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'sub_p':{'type':'reference','width':'5','title':'زیر پروژه','ref':{'db':'a_sub_p','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}"'''},'prop':['update']},
                'step':{'type':'reference','width':'5','title':'مرحله','ref':{'db':'a_step','tb':'a','key':'{code}','val':'{code}-{name}','where':'''prj = "{{=__objs__['prj']['value']}}" AND sub_p =  "{{=__objs__['sub_p']['value']}}"'''},'prop':['update']},
                'dspln':{'type':'reference','width':'5','title':'دیسیپلین','ref':{'db':'a_dspln','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'doc_t':{'type':'reference','width':'5','title':'دیسیپلین','ref':{'db':'a_doc','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'doc_srl_code':{'type':'text','len':'4','lang':'en','title':'کد سریال مدرک','uniq':''},
                'doc_srl_name':{'type':'text','len':'250','title':'نام مدرک'},               
            },
            'steps':{
                'pre':{'tasks':'prj,sub_p,step,dspln,doc_t','jobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'doc_srl_code','jobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'doc_srl_name','jobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'input':['prj','sub_p','step','dspln','doc_t','doc_srl_code','doc_srl_name'],
                'view1':[''],
                'view2':[''],
            },
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
                'doc_t':{'type':'reference','width':'5','title':'دسته مدرک','ref':{'db':'a_doc','tb':'a','key':'{code}','val':'{code}-{name}'},'prop':['update']},
                'doc_p_code':{'type':'auto','len':'24','auto':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}','title':'پیش کد مدرک'},
                #'test1':{'type':'auto','title':'پیش کد مدرک','auto':"{{=__objs__['doc_p_code']['value']}}"},
                'doc_srl_code':{'type':'reference','len':'4','lang':'en','title':'کد سریال مدرک','ref':{'db':'doc_num','tb':'a','key':'{doc_srl_code}','val':'{doc_srl_code}-{doc_srl_name}','where':'''doc_p_code = "{{=__objs__['doc_p_code']['value']}}"'''},'prop':['update']},#
                'doc_srl_name':{'type':'auto','len':'250','title':'نام مدرک','auto':"{{=__objs__['doc_srl_code']['select'][__objs__['doc_srl_code']['value']][5:].strip()}}"}, #"{{=__objs__['doc_srl_code']['select'][doc_srl_code]}}"
                'doc_a_code':{'type':'auto','len':'24','auto':'{doc_p_code}-{doc_srl_code}','title':'کد کامل مدرک'},
                'rev':{'type':'index','len':'2','ref':{'db':'doc_rec','tb':'a','key':'{id}','val':'{rev}','where':'doc_p_code = {doc_p_code}'},'title':'شماره','prop':['update']},
                'date':{'type':'fdate','width':'10','title':'تاریخ مدرک','prop':['update']},
                'file_edt':{'type':'file','len':'40','file_name':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}-{doc_srl_code}-{rev}-{{=date[2:4]+date[5:7]+date[8:10] if date else ""}}','file_ext':"doc,docx,xls,xlsx,ppt,pptx,dwg,zip,rar",'path':'prj,{prj},{sub_p},{step},{dspln},{doc_t}','title':'فایل نهایی با فرمت تغییر پذیر'},
                'file_fix':{'type':'file','len':'40','file_name':'{prj}-{sub_p}-{step}-{dspln}-{doc_t}-{doc_srl_code}-{rev}-{{=date[2:4]+date[5:7]+date[8:10] if date else ""}}','file_ext':"pdf,gif,jpg,jpeg,png",'path':'prj,{prj},{sub_p},{step},{dspln},{doc_t}','title':'فایل نهایی با فرمت ثابت'},
            },
            'steps':{
                'pre':{'tasks':'prj,sub_p,step,dspln,doc_t','jobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'doc_p_code,doc_srl_code,doc_srl_name','jobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'doc_a_code,rev,date','jobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''},
                's3':{'tasks':'file_edt,file_fix','jobs':'dccm','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''}
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
    'person_get':{
        'a':{
            'base':{'mode':'form','title':'فرم مشخصات افراد شناسایی شده برای جذب نیرو','help':''
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
                'pre':{'tasks':'name_f,family_f,name_e,family_e','jobs':'dcc_prj','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'code_meli,tel_mob,date,eng,eng_des,office','jobs':'dcc_prj','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'f_resume,f_form','jobs':'dcc_prj','title':'مرحله 2','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'input':['name_f','family_f','name_e','family_e','tel_mob'],
                'view1':['code_meli','date','eng','eng_des','office'],
                'view2':['f_resume','f_form'],
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'a_contract':{
        'a':{
            'base':{'mode':'form','title':'فرم ثبت قراردادهای شرکت','help':''
            },
            'tasks':{
                'subject':{'type':'text','title':'موضوع قرارداد','len':'250'},
                'client':{'type':'text','title':'کارفرما'},
                'date':{'type':'fdate','title':'تاریخ ابلاغ قرارداد'},
                'prj_dur':{'type':'num','min':1,'max':1200,'len':'4','title':'مدت قرارداد - ماه'},
                'serv_type':{'type':'select','title':'نوع خدمات','select':{'D':'design-طراحی','S':'supervition-نظارت','-':'نا مشخص'},'prop':['multiple']},
                'f_cnt':{'type':'file','len':'40','title':'فایل متن قرارداد امضا شده','file_name':'contract-{{=str(id).zfill(4)}}-{{=date[:4] if date else ""}}-','file_ext':"pdf,gif,jpg,jpeg,png",'path':'form,contract'}
            },
            'steps':{
                'pre':{'tasks':'subject,client,date,prj_dur,serv_type','jobs':'dccm','title':'ورود اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'f_cnt','jobs':'dccm','title':'تکمیل اطلاعات','app_keys':'','app_titls':'','oncomplete_act':''}
                
            },
            'views':{
                'input':['name_f','family_f','name_e','family_e','tel_mob'],
                'view1':['code_meli','date','eng','eng_des','office'],
                'view2':['f_resume','f_form'],
            },
            'cols_filter':{'':'همه',},
            'data_filter':{'':'همه',}
        }
    },
    #--------------------------------------------------------------------
    'suggestion':{
        'a':{
            'base':{'mode':'form','title':'فرم پیشنهاد'
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
                's0':{'tasks':'lable_1,idea,idea_bnft,idea_dscr','jobs':'*','title':'ثبت پیشنهاد','app_keys':'','app_titls':'','oncomplete_act':''},
                's1':{'tasks':'lable_1,vrfy_rslt,vrfy_meta','jobs':'rda','title':'بررسی','app_keys':'','app_titls':'','oncomplete_act':''},
                's2':{'tasks':'clnt_stf,clnt_stf_dscr','jobs':'#step#0','title':'نتیجه','app_keys':'','app_titls':'','oncomplete_act':''}
            },
            'views':{
                'input':['vrfy_rslt','vrfy_meta'],
                'view1':['idea','idea_bnft','idea_dscr'],
                'view2':['clnt_stf','clnt_stf_dscr'],
            },
            'labels':{
                'lable_1':'از اینکه با ارائه پیشنهادات مفید مارا در بهبود شرکت یاری می فرمایید بسیار سپاسگذاریم ',
                'lable_2':'باید تاریخ ، نام فرد و نظر فرد برای هر کدام از افراد موثر در بررسی ثبت شود',
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
                'txt':{'type':'text','len':50,'lang':'fa','title':'متن','uniq':''},#'sel=`x`'
                'n':{'type':'num','min':5,'max':15,'title':'عدد','prop':[]},
                'sel':{'type':'select','select':{'a':'طراحی','x':'نظارت'},'title':'واحد','prop':[]},
                'ref':{'type':'reference','width':'5','title':' مسئول اقدام','ref':{'db':'user','tb':'user','key':'{un}','val':'{un}-{m_w} {pre_n} {name} {family}'},'prop':[]},
                'ch':{'type':'check','title':'با این موضع موافقم','prop':[]},
                'dt':{'type':'fdate','width':'10','title':'تاریخ انجام کار','prop':[]},
                'at':{'type':'auto','len':'24','auto':'{n}-{sel}-{ch}-{ref}-{dt:}','title':'کد اتوماتیک'},
                'indx1':{'type':'index','len':'4','ref':{'db':'test','tb':'b','key':'{id}','val':'{indx1}','where':''},'title':'شماره'},
                'fl':{'type':'file','len':'24','file_name':'abc-{{=int("0"+n)+25}}-{sel}-{{=dt[:4] if dt else ""}}','file_ext':"gif,jpg,jpeg,png,doc,docx,xls,xlsx,pdf,dwg,zip,rar",'path':'test,a,c,{txt}-{n}','title':'فایل نهایی'},#,'x':'{txt}-{n}-{sel}-{ch}-{ref}'
                'tt':{'type':'time','title':'زمان شروع'},
            },
            'steps':{
                'pre':{'tasks':'txt,n,sel,indx1','jobs':'*','title':'ثبت اطلاعات اولیه','app_keys':'','app_titls':'','oncomplete_act':''},
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
