# -*- coding: utf-8 -*-
# ver 1.00 1402/09/12
# -------------------------------------------------------------------------
''' value help
    x_data :# all form "extra data" that read from x_data.py file
        ساختار اطلاعات کل فرمها که از فایل مربوطه خوانده می شود
    x_data_s :# selected x_data = x_data for <select db_file><select table>    
'''
from gluon.custom_import import track_changes; track_changes(True)
from k_sql import DB1
import k_htm
import k_form
from k_err import xxprint,xprint,xalert,xreport_var
from x_data import x_data ,x_data_verify_task
import k_date
now = k_date.ir_date('yy/mm/dd-hh:gg:ss')
# import datetime
# now = datetime.datetime.now().strftime("%H:%M:%S")

debug=False # True: for check error
db_path='applications\\spks\\databases\\'
import k_user
#----------------------------------------------------------------------------------------------------------
def get_init_data():
    '''
    اطلاعات مورد نیاز را حسب آدرس صفحه از اطلاعات ساختاری جدول مورد نظر استخراج می کند
    output:
    -------
    return down inf according args in 1 url page
        x_data_s :#
        db_name:str
        tb_name:str    
    '''
    #global: x_data
    args=request.args
    if len(args)>0:
        if args[0] not in x_data:
            return f'error: >  "{args[0]}" not defined in Fieldes'
        db_name=args[0]
        #print (db_name)
        if len(args)<2:args+=['a']
        tb_name=args[1]# if len(args)>1 else 'a'

        if not db_name in x_data:return False,'','','error : "{}" not in ( x_data )'.format(db_name)
        x_data_s1=x_data[db_name]#x_data_select

        if not tb_name in x_data_s1:return False,'','','error : "{}" not in ( x_data["{}"] )'.format(tb_name,db_name)
        x_data_s=x_data_s1[tb_name]
        return x_data_s,db_name,tb_name,'ok'
    return False,'','','error : args not set correctly'
#---------------------------------------------------------------------------------------------------------- 
def err_reset():
    #reset report file for err
    import k_err
    k_err.xxprint_reset_html()
    return ('<h1>err report are reset : <h1>'+now)
#----------------------------------------------------------------------------------------------------------       
def test_count_row():  
    #sample=   spks/form/test_count_row/test/b_backup
    if len(request.args)<2 :
        return "err: arg number send to fun(count_row) is < 2"
    #breakpoint()
    x_data_s,db_name,tb_name,msg=get_init_data()
    
    db1=DB1(db_path+db_name+'.db')
    res=db1.count(tb_name)
    trs=[[x,str(y)] for x,y in res.items()]
    from k_table import K_TABLE
    return dict(table=K_TABLE.creat_htm(trs, titles=['name','value'],table_class="1"))
               
def test_user():
    import k_htm
    return dict(h1=k_htm.val_report(k_user.a_users),h2=k_htm.val_report(k_user.all_users.inf))
def test_parser():
    import k_form
    return k_form.template_parser("{a}+{{=b+','.join([x for x in 'abc'])}}",x_dic={'a':'1','b':'2'})
def testx():
    x="""
     <!-- Nav tabs -->
<ul class="nav nav-tabs">
  <li class="nav-item">
    <a class="nav-link active" data-toggle="tab" href="#home">Home</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" data-toggle="tab" href="#menu1">Menu 1</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" data-toggle="tab" href="#menu2">Menu 2</a>
  </li>
</ul>

<!-- Tab panes -->
<div class="tab-content">
  <div class="tab-pane container active" id="home">123</div>
  <div class="tab-pane container fade" id="menu1">...</div>
  <div class="tab-pane container fade" id="menu2">...</div>
</div>
    """
    return dict(x=XML(x))
def test_uniq_old2():
    #sample=   spks/form/test_uniq/paper/a/lno
    args=request.args
    x_val=request.vars['x_val'] or ''
    xhtm=[DIV('--')]
    if x_val and len(args)>2:
        x_data_s,db_name,tb_name,msg=get_init_data()
        db1=DB1(db_path+db_name+'.db')

        x_field=args[2]
        is_uniq,like_list=db1.chek_uniq(tb_name,x_field,uniq_where='',uniq_value=x_val)
        xhtm+=[DIV(x_val)]+[DIV('--')]
        xhtm+=[DIV(str(is_uniq))]+[DIV('--')]
        xhtm+=[DIV(x) for x in like_list]+[DIV('--')]
    return dict(f=DIV(
        FORM(INPUT(_value=x_val,_id='x_val',_name='x_val',_onkeyup='submit();'),INPUT(_type='submit'),_action=URL('test_uniq',args=args))
        ,DIV(xhtm)
        ))      
#---------------------------------------------------------------------------------------------------------- =================      
def test_uniq_old1():      
    scr1='''
    <script>
        function ajax_chek_uniq(){
            var code = $("#x_val").val();
            url ="''' + URL('km','uniq_inf.json',args=['paper','a','lno']) + '''/"+code;
            $.ajax({
                url :url,
                method : 'POST',
                data : {code:code},
                success : function(echo){
                    $('#x_val').val(echo.uniq);
                    $('#x_val_div').text(echo.like_list);
                    alert("like:"+ echo.like_list)
                }
            });
        }
    </script>
    '''
    #    +$("#x_val").val()
    return dict(f=DIV(
        XML(scr1),
        INPUT(_value="",_id='x_val',_name='x_val',_onchange='ee1("")'),
        DIV("",_id='x_val_div'),
        ))   
#--------------------        
def chek_uniq():  
    #sample=   spks/km/chek_uniq/paper/a/lno
    args=request.args
    scr1='''
    <script>
        function ajax_chek_uniq(db,tb,field_name,target,target_hlp=""){
            /*
                goal:
                    check that dom.input(target).value  is uniq in file(db).table(tb).filed(field_name)
                output:
                    alert like/sami value in  file(db).table(tb).filed(field_name)
                        values in  file(db).table(tb).filed(field_name) that is like to dom.input(target).value 
                    if not uniq: (dom.input(target).value is in  file(db).table(tb).filed(field_name))
                        delete dom.input(target).value
            */
            var code = $(target).val();
            url ="''' + URL('km','uniq_inf.json') + '''/"+db+"/"+tb+"/"+field_name+"/"+code;
            
            $.ajax({
                url :url,
                method : 'POST',
                data : {code:code},
                success : function(echo){
                    $(target).val(echo.uniq);
                    if (target_hlp!="") { $(target_hlp).text(echo.like_list);}
                    var msg="like: \\n" + echo.like_list
                    alert(msg)
                    $(target).attr('title', msg);
                }
            });
        }
    </script>
    '''
    #    +$("#x_val").val()
    return dict(f=DIV(
        XML(scr1),
        INPUT(_value="",_id='x_val',_name='x_val',_onchange=f"ajax_chek_uniq('{args[0]}','{args[1]}','{args[2]}','#x_val');"),#,'#x_val_div'
        DIV("",_id='x_val_div'),
        ))   
def ajax_val_get():
    '''
    goal:
        use in ajax for get 1 value from server
    args:
        0:session / request /
        1:value name
    test:
        /spks/km/ajax_val_get/test/a/txt
    '''
    args=request.args
    try:
        if len(args)>1:
            return {'val':session[arg[1]],'msg':'ok'}
        msg='shoud len(args)>2'
    except Exception as err:
        msg='err='+str(err)
    return {'val':'','msg':msg}    
      
#--------------------
def uniq_inf():
    '''
    goal:
        use uniq_inf.json for ajax from ks-form.js>ajax_chek_uniq()
    test:
        /spks/km/uniq_inf.json/test/a/txt
    '''
    args=''
    x_dic=''
    n='1'
    try:
        args=request.args
        x_dic=request.vars
        if len(args)>2:
            x_data_s,db_name,tb_name,msg=get_init_data()
            x_field=args[2]
            uniq_value=x_dic['uniq_value'] #args[3]
            uniq_where=x_dic['uniq_where']
            db1=DB1(db_path+db_name+'.db')
            n='2'
            is_uniq,like_list=db1.chek_uniq(tb_name,x_field,uniq_where=uniq_where,uniq_value=uniq_value)
            n='3'
            return {'uniq':uniq_value if is_uniq else '','is_uniq':'Y' if is_uniq else '','like_list':like_list,'msg':str(x_dic)}
        msg='shoud len(args)>2'
    except Exception as err:
        msg='err='+n+"|"+str(err)
    #return dict(x={'uniq':'err','is_uniq':'','like_list':'','msg':f"error in form.py/def(uniq_inf){msg}\n-args="+str(args)+"\n,vars="+str(request.vars)})  
    return {'uniq':'error','is_uniq':'','like_list':'','msg':str(x_dic),'err':f" - error in form.py/def(uniq_inf)\n - {msg}\n - args="+str(args)+"\n - vars="+str(x_dic)}
#---------------------------------------------------------------------------------------------------------- =================     
def test_ajax():
    scr1='''
    <script>
        function ee1(){
            var code = $("#x_val").val();
            $.ajax({
                url :"''' + URL('km','test_json') + '''.json",
                method : 'POST',
                data : {code:code},
                success : function(echo){
                    $('#x_val').val(echo.a);
                    $('#x_val_div').text(echo.b);
                }
            });
        }
    </script>
    '''
    #
    return dict(f=DIV(
        XML(scr1),
        INPUT(_value="",_id='x_val',_name='x_val',_onchange='ee1("")'),
        DIV("",_id='x_val_div'),
        ))       
def test_json():
    return {'a':'abc','b':'cde'}        
#----------------------------------------------------------------------------------------------------------   
def test_uniq1():
    d1=LOAD('form', 'test_uniq.load', ajax=True, args=['paper','a','lno'])# , vars={'reload_div':'map'})
    d2=DIV('hello WORLD')
    return dict(d=DIV(d1,d2))
    #return DIV(d1,d2)
def test1():
    return str(INPUT(_name='a',_required=True))
def test2():
    #from zipfile import ZipFile
    import zipfile
    def dir_prop(obj):
        t=''
        for p in dir(obj):
            t+=p+':'+str(eval("obj."+p))+'<br>'
        return t
    #return (zipfile.__version__)
    return dir_prop(zipfile)+"<hr>"+dir_prop(zipfile.ZipFile)
    return zipfile.LZMA_VERSION
    return str(dir(zipfile))
def test3():
    #sample=   spks/km/test3
    #return 1
    #import subprocess
    #import os
    #subprocess.call(['D:\ext\pro\FSViewerPortable\FSViewerPortable.exe',''])# 'C:\\test.txt'])
    #os.system(r'C:\temp\7Zip\7z.exe x C:\temp\need.zip -oc:\temp\7z * -r')
    '''C:\temp\7Zip\7z.exe e C:\temp\need.zip -oc:\temp\7z * -r',''])'''
    #return 6
    import k_file
    path=r'C:\temp\need.zip'
    re1=k_file.zip7_extract(path)
    return (f'<br> unzip_7 done successfully <br> {path} <hr> inf= {re1["inf"]} <hr> ok= {re1["ok"]}')
#-------------------------------------------------
def rar_extract(rar_path):#rar or zip
    from unrar import rarfile
    rar = rarfile.RarFile(rar_path)
    f=file_name_split(rar_path)
    rar.extractall(f['path']+"\\"+f['name'])
    return True        
def test_stdout_redirect():
    # <set_stdout_to_string>
    from io import StringIO
    import sys
    old_stdout = sys.stdout
    mystdout = StringIO()
    sys.stdout = mystdout
    # </set_stdout_to_string>
    print("hellow")
    sys.stdout = old_stdout # reset <set_stdout_to_string>
    return {'ok':True,'inf':x_cmd+"<hr>"+mystdout.getvalue()}
def test_kform_template_parser():
    import k_form
    return k_form.template_parser("""abc-{{=a[2].upper()}}""",{'a':'abc'})
    abc-C
    