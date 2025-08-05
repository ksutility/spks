def xxx():
    def save(text_app):
        def get_vv(f_nxt_s,f_nxt_s_new):
            steps=x_data_s['steps']
            step=steps[list(steps.keys())[f_nxt_s]]
            step_flds=step['tasks'].split(',')
            rv=list(request.vars)
            #breakpoint()
            vv={t:request.vars[t] for t in rv if t in step_flds }
            vv.update({ f'step_{f_nxt_s}_un':session['username'],
                        f'step_{f_nxt_s}_dt':k_date.ir_date('yy/mm/dd-hh:gg:ss'),
                        f'step_{f_nxt_s}_ap':request.vars['text_app'],
                        'f_nxt_s':str(f_nxt_s_new),
                        'f_nxt_u':''
                        })
            return vv
        def update(text_app):
            xi,r1,rows_num='','',''
            if text_app=='r': 
                xi,r1,rows_num=db1.row_backup(tb_name,xid)
                f_nxt_s_new=f_nxt_s-1
            elif text_app=='x':
                pass
            elif text_app=='y':
                f_nxt_s_new=f_nxt_s+1
            vv=get_vv(f_nxt_s,f_nxt_s_new)    
            xu = db1.update_data(tb_name,vv,{'id':xid})
            rr=f"{db1.path}<br> UPDATE: "+str(xu)+"<hr> backup<br>xi="+str(xi)+"<br> r1="+str(xi)+ "<br> rows_num="+str(rows_num)
            #+"<brr>vv"+str(vv)+"<br>vars:"+str(list(request.vars))+"<br>titels:"+str(titles)
            return rr
        def insert():
            vv=get_vv(0,1)
            xi,r1=db1.insert_data(tb_name,vv.keys(),vv.values())
            rr=f"{db1.path}<br> INSERT:result="+str(r1)+" => "+str(xi)+" | "+str(r1) #+"<hr>"+str(vv)
            return rr
        #--------------------------------    
        if xid==-1:
            r1=insert()
        else:
            r1=update(text_app)
        return DIV(XML(r1))
def wday():
    import k_date
    return k_date.ir_weekday(name=True)
def json1():
    """test/json1"""
    json_str1='''
    {
    "k8":"http://192.168.88.179/spks/",
    "doc_STKH_002":"[سند چارچوب ارزش افزایی ذی‌نفعان در فرایند توسعه]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/STKH-002-00.md)",
    "doc_RADAR" : "[سند چهار چوب تهیه اسناد شرکت بر اساس منطق رادار]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/AQRC-TQM-IN-RADAR.md?xpath=D%3A%5Cks%5C0-file&pre_case=a)",
    "doc_TQM_WB_4A4_VAL_HSE_SCE" :"[سند چارچوب جامع مدیریت HSE-SCE برای ارزش‌آفرینی پایدار]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM_WB_4A4_VAL_HSE_SCE.md)",
    "doc_TQM_WB_4A1_SDV":"[سند چهار چوب مدیریت ارزش متمایز پایدار شرکت]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM_WB_4A1_SDV.md?xpath=D%3A%5Cks%5C0-file)",
    "doc_TQM_EVT":"[لیست حضور سازمان در رویدادهای تأثیرگذار@@]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM-EVT.md?xpath=D%3A%5Cks%5C0-file)",
    "doc_TQM_SCMF":"[چهارچوب مدیریت زنجیره تأمین]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM-SCMF.md?xpath=D%3A%5Cks%5C0-file)",
    "doc_TQM_SEIA":"[چهار چوب کاهش اثرات اجتماعی و زیست محیطی پروژه های شرکت]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM-SEIA.md?xpath=D%3A%5Cks%5C0-file)",
    "apr_4A3":"[رویکرد توسعه هدفمند سبد محصولات و خدمات بر مبنای فلسفه وجودی و نیازهای مشتریان  ]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/M4/4-A-3.ksml)",
    "doc_RADAR_SEC_R_old":"مطابق روش اصلاح کلی در {{=doc_RADAR}}",
    "doc_RADAR_SEC_A_old":"مطابق روش ارزیابی کلی در {{=doc_RADAR}}",
    "doc_RADAR_SEC_DOC_old":"مطابق شواهد موجود کلی در {{=doc_RADAR}}",
    "k8_km_a":"[فرم ثبت دانش]({{=k8}}form/xtable/km/a)",
    "k8_doc_tqm_a":"[فرم اسناد تعالی و مدیریت کیفیت]({{=k8}}form/xtable/doc_tqm/a)",
    "k8_doc_mm_a":"[فرم صورت جلسه]({{=k8}}form/xtable/doc_mm/a)"

    }
    '''
    json_str="""{
'k8':'''http://192.168.88.179/spks/''',
'doc_STKH_002':'''[سند چارچوب ارزش افزایی ذی‌نفعان در فرایند توسعه]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/STKH-002-00.md)''',
'doc_RADAR':'''[سند چهار چوب تهیه اسناد شرکت بر اساس منطق رادار]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/AQRC-TQM-IN-RADAR.md?xpath=D%3A%5Cks%5C0-file&pre_case=a)''',
'doc_TQM_WB_4A4_VAL_HSE_SCE':'''[سند چارچوب جامع مدیریت HSE-SCE برای ارزش‌آفرینی پایدار]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM_WB_4A4_VAL_HSE_SCE.md)''',
'doc_TQM_WB_4A1_SDV':'''[سند چهار چوب مدیریت ارزش متمایز پایدار شرکت]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM_WB_4A1_SDV.md?xpath=D%3A%5Cks%5C0-file)''',
'doc_TQM_EVT':'''[لیست حضور سازمان در رویدادهای تأثیرگذار@@]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM-EVT.md?xpath=D%3A%5Cks%5C0-file)''',
'doc_TQM_SCMF':'''[چهارچوب مدیریت زنجیره تأمین]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM-SCMF.md?xpath=D%3A%5Cks%5C0-file)''',
'doc_TQM_SEIA':'''[چهار چوب کاهش اثرات اجتماعی و زیست محیطی پروژه های شرکت]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM-SEIA.md?xpath=D%3A%5Cks%5C0-file)''',
'apr_4A3':'''[رویکرد توسعه هدفمند سبد محصولات و خدمات بر مبنای فلسفه وجودی و نیازهای مشتریان  ]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/M4/4-A-3.ksml)''',
'doc_RADAR_SEC_R_old':'''مطابق روش اصلاح کلی در {{=doc_RADAR}}''',
'doc_RADAR_SEC_A_old':'''مطابق روش ارزیابی کلی در {{=doc_RADAR}}''',
'doc_RADAR_SEC_DOC_old':'''مطابق شواهد موجود کلی در {{=doc_RADAR}}''',
'k8_km_a':'''[فرم ثبت دانش]({{=k8}}form/xtable/km/a)''',
'k8_doc_tqm_a':'''[فرم اسناد تعالی و مدیریت کیفیت]({{=k8}}form/xtable/doc_tqm/a)''',
'k8_doc_mm_a':'''[فرم صورت جلسه]({{=k8}}form/xtable/doc_mm/a)''',
'doc_RADAR_SEC_A':'''
* $$1

* دریافت بازخورد از ذی‌نفعان کلیدی در خصوص

        * سطح رضایت از "اثر بخش بودن فرایند در راستای هدف "

        * سطح رضایت از کیفیت اقدامات

        * سطح رضایت از تحلیل ها ، اسناد تهیه شده و شاخص ها

* ارزیابی مشارکت ذی‌نفعان کلیدی''',
'doc_RADAR_SEC_A1':'''
* $$1

* جمع آوری و تحلیل نظر همکاران ، مدیران و اعضا هیات مدیره بر روی سند قبلی - در دوره های 1 ساله به منظور تشخیص نیاز به بازنگری سند
''',
'doc_RADAR_SEC_R':'''
* $$1

* بازنگری سالانه مدارک بر اساس نتایج  و یا به صورت موردی حسب عدم تطابقهای مهم

* مستند سازی درس‌آموخته‌ها و تجربیات در بانک دانش سازمانی  و به کار گیری در برنامه ریزی آینده

* بازنگری سیاست‌ها  ،فرایند ها ، دستور العملها ، فرمها و چک لیستها ی مرتبط حسب مورد

''',
'doc_RADAR_SEC_DOC':'''
* $$1

* سند ساپارتا

* سامانه مدریت دانش - دانش هشتم

        * {{=k8_km_a}}

        * {{=k8_doc_tqm_a}}

        * {{=k8_doc_mm_a}}

* باز خورد ذی نفعان در پرس لاین

* {{=doc_RADAR}}
''',
'doc_RADAR_SEC_KPI':'''
* $$1

* سطح رضایت ذی‌نفعان کلیدی از :

        *  "اثر بخش بودن فرایند در راستای هدف "

        *  کیفیت اقدامات

        *  تحلیل ها ، اسناد تهیه شده و شاخص ها

* نرخ به‌روزرسانی تحلیل‌ها و اسناد در بازه 2 ساله

* نرخ به‌روزرسانی فرایند در بازه 2 ساله
''',
'doc_RADAR_SEC_KPI_1':'''
* $$1

* نرخ به‌روزرسانی تحلیل‌ها و اسناد در بازه 2 ساله

* نرخ به‌روزرسانی فرایند در بازه 2 ساله
''',
}"""
    """{
'k8':'http://192.168.88.179/spks/',
'doc_STKH_002':'[سند چارچوب ارزش افزایی ذی‌نفعان در فرایند توسعه]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/STKH-002-00.md)',
'doc_RADAR':'[سند چهار چوب تهیه اسناد شرکت بر اساس منطق رادار]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/AQRC-TQM-IN-RADAR.md?xpath=D%3A%5Cks%5C0-file&pre_case=a)',
'doc_TQM_WB_4A4_VAL_HSE_SCE':'[سند چارچوب جامع مدیریت HSE-SCE برای ارزش‌آفرینی پایدار]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM_WB_4A4_VAL_HSE_SCE.md)',
'doc_TQM_WB_4A1_SDV':'[سند چهار چوب مدیریت ارزش متمایز پایدار شرکت]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM_WB_4A1_SDV.md?xpath=D%3A%5Cks%5C0-file)',
'doc_TQM_EVT':'[لیست حضور سازمان در رویدادهای تأثیرگذار@@]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM-EVT.md?xpath=D%3A%5Cks%5C0-file)',
'doc_TQM_SCMF':'[چهارچوب مدیریت زنجیره تأمین]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM-SCMF.md?xpath=D%3A%5Cks%5C0-file)',
'doc_TQM_SEIA':'[چهار چوب کاهش اثرات اجتماعی و زیست محیطی پروژه های شرکت]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/2-DOCS/TQM-SEIA.md?xpath=D%3A%5Cks%5C0-file)',
'apr_4A3':'[رویکرد توسعه هدفمند سبد محصولات و خدمات بر مبنای فلسفه وجودی و نیازهای مشتریان  ]({{=k8}}xfile/read_xx/prj/AQRC/AQRC-DOC/2-TQM/1-EXST-ezharname/M4/4-A-3.ksml)',
'doc_RADAR_SEC_R_old':'مطابق روش اصلاح کلی در {{=doc_RADAR}}',
'doc_RADAR_SEC_A_old':'مطابق روش ارزیابی کلی در {{=doc_RADAR}}',
'doc_RADAR_SEC_DOC_old':'مطابق شواهد موجود کلی در {{=doc_RADAR}}',
'k8_km_a':'[فرم ثبت دانش]({{=k8}}form/xtable/km/a)',
'k8_doc_tqm_a':'[فرم اسناد تعالی و مدیریت کیفیت]({{=k8}}form/xtable/doc_tqm/a)',
'k8_doc_mm_a':'[فرم صورت جلسه]({{=k8}}form/xtable/doc_mm/a)',
'doc_RADAR_SEC_A':'''
* $$1
\n* دریافت بازخورد از ذی‌نفعان کلیدی در خصوص 
\n	* سطح رضایت از "اثر بخش بودن فرایند در راستای هدف "  
\n	* سطح رضایت از کیفیت اقدامات
\n	* سطح رضایت از تحلیل ها ، اسناد تهیه شده و شاخص ها
\n* ارزیابی مشارکت ذی‌نفعان کلیدی''',
'doc_RADAR_SEC_A1':'''
* $$1
\n* جمع آوری و تحلیل نظر همکاران ، مدیران و اعضا هیات مدیره بر روی سند قبلی - در دوره های 1 ساله به منظور تشخیص نیاز به بازنگری سند
''',
'doc_RADAR_SEC_R':'''
* $$1
\n* بازنگری سالانه مدارک بر اساس نتایج  و یا به صورت موردی حسب عدم تطابقهای مهم
\n* مستند سازی درس‌آموخته‌ها و تجربیات در بانک دانش سازمانی  و به کار گیری در برنامه ریزی آینده
\n* بازنگری سیاست‌ها  ،فرایند ها ، دستور العملها ، فرمها و چک لیستها ی مرتبط حسب مورد
\n''',
'doc_RADAR_SEC_DOC':'''
* $$1
\n* سند ساپارتا
\n* سامانه مدریت دانش - دانش هشتم
\n	* {{=k8_km_a}}
\n	* {{=k8_doc_tqm_a}}
\n	* {{=k8_doc_mm_a}}
\n* باز خورد ذی نفعان در پرس لاین
\n* {{=doc_RADAR}}
''',
'doc_RADAR_SEC_KPI':'''
* $$1
\n* سطح رضایت ذی‌نفعان کلیدی از :
\n	*  "اثر بخش بودن فرایند در راستای هدف "  
\n	*  کیفیت اقدامات
\n	*  تحلیل ها ، اسناد تهیه شده و شاخص ها
\n* نرخ به‌روزرسانی تحلیل‌ها و اسناد در بازه 2 ساله
\n* نرخ به‌روزرسانی فرایند در بازه 2 ساله
''',
'doc_RADAR_SEC_KPI_1':'''
* $$1
\n* نرخ به‌روزرسانی تحلیل‌ها و اسناد در بازه 2 ساله
\n* نرخ به‌روزرسانی فرایند در بازه 2 ساله
''',
}"""
    import k_diff
    xdic=eval(json_str)
    #print(xdic['k8'])
    ttt="\n".join([f"'{x}':'''{y}'''," for x,y in xdic.items()])
    ttt="{\n"+ttt+"\n}"
    #print(str(xdic))
    print(ttt)
    return k_diff._diff_txt(ttt.split('\n'),json_str.split('\n'),'ttt','json_str')

    #print(ttt==json_str)

