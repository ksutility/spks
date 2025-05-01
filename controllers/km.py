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
    
    db1=DB1(db_name)
    res=db1.count(tb_name)
    trs=[[x,str(y)] for x,y in res.items()]
    from k_table import K_TABLE
    return dict(table=K_TABLE.creat_htm(trs, titles=['name','value'],table_class="1"))
               
def test_user():
    import k_htm
    return dict(h1=k_htm.val_report(k_user.ALL_USERS().inf),h2='')
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
        db1=DB1(db_name)

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
            db1=DB1(db_name)
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
def test4():
    return request.env.HTTP_HOST.partition(":")[0]
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
def test_pivot():
    file_path=r"C:\Users\XMART\Desktop\temp\test\x3.csv"
    set1="""{
            rows: ["name"], 
            cols: ["prj"],
            vals: ["time"],
            aggregatorName: "Sum",
            rendererName: "Bar Chart",
            renderers: $.extend(
                $.pivotUtilities.renderers, 
              $.pivotUtilities.plotly_renderers
            )
            }"""
    import k_file_x
    data1="""a,b,c
1,2,3
4,5,6
7,8,9"""
    data1=k_file_x.read_csv(file_path)
    htm1=f"""
    <html><head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>pivot</title>
            <script type="text/javascript" src="{URL('static','js/pivot/plotly-basic-latest.min.js')}"></script>
            <script type="text/javascript" src="{URL('static','js/pivot/jquery.min.js')}"></script>
            <script type="text/javascript" src="{URL('static','js/pivot/jquery-ui.min.js')}"></script>
            <script type="text/javascript" src="{URL('static','js/pivot/papaparse.min.js')}"></script>
            <!-- PivotTable.js libs from ../dist -->
            <link rel="stylesheet" type="text/css" href="{URL('static','js/pivot/pivot.css')}">
            <script type="text/javascript" src="{URL('static','js/pivot/pivot.js')}"></script>
            <script type="text/javascript" src="{URL('static','js/pivot/plotly_renderers.js')}"></script>
            <style>
                
            </style>
            <!-- optional: mobile support with jqueryui-touch-punch -->
            <script type="text/javascript" src="{URL('static','js/pivot/jquery.ui.touch-punch.min.js')}"></script>

            <!-- for examples only! script to show code to user 
            <script type="text/javascript" src="{URL('static','js/pivot/show_code.js')}"></script>-->
            <link rel="stylesheet" type="text/css" href="{URL('static','js/pivot/color-brewer.min.css')}">
            <link rel="stylesheet" type="text/css" href="{URL('static','js/pivot/css')}">
    </head>
    <body style="">
    """
    """
           <script type="text/javascript">
    // This example loads the "Canadian Parliament 2012"
    // dataset from a CSV instead of from JSON.

    $(function(){
        data1=[
                {color: "blue", shape: "circle"},
                {color: "red", shape: "triangle"}
            ];

        setting1={
                rows: ["color"],
                cols: ["shape"]
            };
        //$("#output").pivot(data1,setting1);
        $("#output").pivotUI(
            data1,setting1
        );
     });
        
    </script>
    """
    htm1+="""
    <script type="text/javascript">
        function ar2d_2_objar(ar){
            //alert(ar.length);
            const obj_ar = [];
            for (let i = 1; i < ar.length; i++) {
                const obj_i = {};
                for (let j = 0; j < ar[i].length; j++) {
                    
                    obj_i[ar[0][j]]=ar[i][j];
                }
                //alert(JSON.stringify(obj_i));
                obj_ar.push(obj_i)
            }
            return obj_ar
        }
        $(function(){
            csvString=`%%%1`;
            results = Papa.parse(csvString);
            //alert(JSON.stringify(results.data));
            obj_ar=ar2d_2_objar(results.data);
            //alert(JSON.stringify(obj_ar));
            
            var derivers = $.pivotUtilities.derivers;
            var renderers = $.extend($.pivotUtilities.renderers,
                $.pivotUtilities.plotly_renderers);
            $("#output").pivotUI(obj_ar,%%%2);
        });
    </script>
    """ .replace("%%%1",data1).replace("%%%2",set1)
    htm1+="""
        <div id="output" style="margin: 30px;"><div>
    </body></html>
    """    
    return htm1
def test_mermaid():
    style='''
    .center {
        width:"100%";
        margin: auto;
        text-align: center;
    }
    .container {
      display: flex;
      justify-content: center;
    }
    '''
    """
        <script type="text/javascript" src="{URL('static','js/pivot/jquery.min.js')}"></script>
        <script type="text/javascript" src="{URL('static','js/pivot/jquery-ui.min.js')}"></script>
        <script src="{URL('static','js/bootstrap.bundle.min.js')}"></script>
        <script src="{URL('static','js/web2py-bootstrap4.js')}"></script>
        <link rel="stylesheet" href="{URL('static','css/bootstrap.min.css')}"/>
        <link rel="stylesheet" href="{URL('static','css/web2py-bootstrap4.css')}"/>
    """
    htm1=f'''
    <html><head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>mermaid</title>
        
        <script src="{URL('static','js/mermaid/mermaid.min.js')}"></script>

        <style>
        {style}
        </style>
    </head>
    <body >
        <div class="container1">
            <div class="center">
                <h1 class="center">
                    چارت سازمانی شرکت مشاور قدس
                </h1>
                <hr>
                <div>
                    <pre class="mermaid">
                        graph TD
                        A[مدیر عامل] --> B1[معاون طراحی]
                        A --> B2[معاون اجرایی]
                        A --> B3[معاون برنامه ریزی]
                        B1 --> C[سرپرست معماری]
                        B1 --> D[سرپرست شهرسازی]
                    </pre>
                </div>
            </div
        </div>
    </body>
    '''
    return htm1
def test_ipgrid():
    sh={'inf':{'cols_n':'9','rows_n':'20'},
        'col_widths':'10,5,3,3,5,20,15,30,5',
        'col_titels':['نام و نام خانوادگی',
                      'سال','ماه','روز','روز هفته',
                      'نام پروژه','موضوع','اقدامات','زمان']
      }
    if 'col_widths' in sh:
        table_width=1200
        cw_ts=sh['col_widths'].split(',')
        cw_ns=[int(x) for x in cw_ts]
        cw_sum=sum(cw_ns)
        sh['col_widths']=[int(x*table_width/cw_sum) for x in cw_ns]
    col_titels=[{'name':'id','width':'1'}]+[{'name':sh['col_titels'][i],'width':sh['col_widths'][i]} for i in range(len(sh['col_titels']))]  
    import json
    data=request.vars['data']
    if data:
        style=XML("""
        <style>
            th, td {
              border-bottom: 1px solid #ddd;
            }
        </style>
        """)
        data=json.loads(data)
        if 'table' in data:
            #return style+TABLE(data['table'])
            return _aqc_report_daily_updata(data['table'],col_titels)
    style='''
    <style>
        body {
            font-family: Arial;
            color: white;
            background-color: #3d3d3d;
            margin: 0;
            padding: 10px;
            position: relative;
        }

        a {
            color: #46b3ff;
            text-decoration: dotted;
        }

        .gridContainer {

            position: relative;
            width: 100%;
            height: 700px;
        }
        #jqs {

            width: 100%;
            height: 100%;
        }
    </style>
    '''
    #$('#jqs').on('ip_CellInput', function (event, args) {
    #alert(JSON.stringify(table));
    if 'col_widths' in sh:
        col_widths="\n".join([f"$('#jqs').ip_ResizeColumn({{ columns: [{i}], size: {x} }});" for i,x in enumerate(sh['col_widths'])])
    if 'col_titels' in sh:
        col_titels="\n".join([f"$('#jqs_q2_columnSelectorCell_{i} div').text('{x}');" for i,x in enumerate(sh['col_titels'])])
    clipboard1="""
        $('#bt_clp').on('change', function () {
            alert('change');
            txt=$('#bt_clp').val();
            var rows = txt.split('\\n');
            alert (rows.length);
            for (const x in rows) {
                row=rows[x];
                var cels = row.split('\\t');
                for (const xc in cels) {
                    alert(x+" , "+xc+" : "+cels[xc] + " => "+report(cels[xc]));
                }
            }
       });
    """
    clipboard="""
        $('#bt_clp').on('selectionchange', function () {
            txt=$('#bt_clp').val();
            if (txt=='') {return; };
            var rows = txt.split('\\n');
            for (const r in rows) {
                row=rows[r];
                var cels = row.split('\\t');
                for (const c in cels) {
                    $('#jqs').ip_CellInput({ valueRAW:cels[c], row: r, col: c })
                    //alert(r+" , "+c+" : "+cels[c] + " => "+report(cels[c]));
                }
            }
            $('#bt_clp').val('')
       });
    """
    script='''
    <script>
        function report(txt){
            var tt=''
            for(let i = 0; i < txt.length; i++){
                tt+= txt.charAt(i) + " : " + txt.charCodeAt(i) + " : " + txt.codePointAt(i)+" , " ;
            }
            return tt
        }
        function get_table_data(){
            table=[]
            for (let ir = 0; ir < 20; ir++) {
                row=[ir]
                for (let ic = 0; ic < 9; ic++) {
                    row.push($('#jqs').ip_CellData(ir,ic).value); 
                }
                table.push(row);
            }
            return table
            //alert(JSON.stringify($('#jqs').ip_CellData(1,1)));
        }
        $( document ).ready(function() {
            //alert("b");
            $('#jqs').ip_Grid({ rows: % rows_n %, cols: % cols_n %});
            % col_titels %
            $('#jqs').ip_ResizeRow({ rows: [-1], size: 50 }); 
            % col_widths %
            % clipboard %
            $('#bt_send').on('click', function (event, args) {
                data={table:get_table_data()};
                var dataString = JSON.stringify(data);
                var dataStringBase64Safe = encodeURIComponent(dataString); //dataStringBase64
                var url = '/spks/km/test_ipgrid?data=' + dataStringBase64Safe;
                window.open(url,'popUpWindow','height=400,width=600,left=10,top=10,scrollbars=yes,menubar=no'); 
                return false;
            });
            $('#bt_x').on('click', function (event, args) {
                
                table=get_table_data()
                alert(JSON.stringify(table));
                return
                var columnData = [];

                // یافتن همه سلول‌های ستون دوم
                $('#jqs').each(function() {
                    columnData.push(JSON.stringify($(this)));
                });
                // تبدیل آرایه به یک رشته برای نمایش
                var dataString = columnData.join(', ');

                alert(dataString);
                /*
                myObject=$('#jqs')
                for (let property in myObject) {
                    if (typeof myObject[property] === 'function') {
                        console.log(property + " یک تابع است.");
                    } else {
                        console.log(property + " یک متغیر است.");
                    }
                }
                */
                

            });
            
        });
    </script>
    '''.replace('% rows_n %',sh['inf']['rows_n']).replace('% cols_n %',sh['inf']['cols_n']).replace('% col_widths %',col_widths).replace('% col_titels %',col_titels)
    script=script.replace('% clipboard %',clipboard)
    htm1=f'''
    <html><head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>ipgrid</title>
        
        <script src="{URL('static','js/ipgrid/jquery_min_2_1_3.js')}"></script>
        <script src="{URL('static','js/ipgrid/jquery_ui_min_1_13_2.js')}"></script>
        <script src="{URL('static','js/ipgrid/ip.grid.js')}"></script>
        <link href="{URL('static','js/ipgrid/ip.grid.css')}" rel="stylesheet" />
        {script}
        {style}
        
    </head>
    <body >
           <div class="gridContainer" >
                <div id="jqs">
                </div
            </div>
        <button id="bt_send" type="button">send</button>
        <button id="bt_x" type="button">x</button>
        <textarea id="bt_clp" rows="1" cols="50"></textarea>
    </body>
    '''
    return htm1   
    
    archiv1_test="""
                $('#bt_send').on('click', function (event, args) {
                //alert("aaa");
                table=[]
                $('#jqs_q4_table_tbody').children().each(function () {
                    row=[]
                    $(this).children().each(function () {
                        row.push($(this).text()); // "this" is the current element in the loop
                    });
                    table.push(row);
                });
                data={table:table};
                var dataString = JSON.stringify(data);
                var dataStringBase64Safe = encodeURIComponent(dataString); //dataStringBase64
                var url = '/spks/km/test_ipgrid?data=' + dataStringBase64Safe;
                window.open(url,'popUpWindow','height=400,width=600,left=10,top=10,scrollbars=yes,menubar=no'); 
                return false;
            });
            $('#bt_x').on('click', function (event, args) {
                alert(JSON.stringify($('#jqs').ip_CellData(1,1)));
                return
                var columnData = [];

                // یافتن همه سلول‌های ستون دوم
                $('#jqs').each(function() {
                    columnData.push(JSON.stringify($(this)));
                });
                // تبدیل آرایه به یک رشته برای نمایش
                var dataString = columnData.join(', ');

                alert(dataString);
                /*
                myObject=$('#jqs')
                for (let property in myObject) {
                    if (typeof myObject[property] === 'function') {
                        console.log(property + " یک تابع است.");
                    } else {
                        console.log(property + " یک متغیر است.");
                    }
                }
                */
                

            });
    """
    
def test_kytable():
    import k_file_x
    titles=['id','x','y','z','a']
    rows=[
        ['1','5','6','55','45'],
        ['2','8','10','55','45'],
        ]
    
    widths=['3','5','6','5','6']        
    return k_file_x.kytable_make(rows,titles)#,widths)
    htm1=f'''
<!DOCTYPE html> 
    <html lang="fa">
    <style type="text/css" id="dark-mode-custom-style"></style>
    <head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>   kx table </title>
            <meta http-equiv="Cache-control" content="no-cache">
            <!-- kxtable -->
                <script src="{URL('static','kxtable/jquery-1.8.2.min.js')}" type="text/javascript"></script>
                
                <link rel="stylesheet" href="{URL('static','kxtable/jquery-ui.css')}">
                <script src="{URL('static','kxtable/jquery-ui.js')}"></script>
                
                <link rel="stylesheet" href="{URL('static','kxtable/kxtable.css')}">
                <script src="{URL('static','kxtable/kxtable-21.js')}"></script>
                
                <link rel="stylesheet" href="{URL('static','kxtable/jquery.contextMenu.css')}" type="text/css">
                <script src="{URL('static','kxtable/jquery.contextMenu.js')}" type="text/javascript"></script>
            <!-- /kxtable -->   
                

    </head>
   <body bgcolor="#888888">
   <div id='output' style='width:100%' >
    ...
    </div>
    '''
    import kytable
    ttls2=['id','x','y','z','a']
    wids2=['3','5','6','5','6']
    rows2=[
        ['1','5','6','55','45'],
        ['2','8','10','55','45'],
        ]
    return XML(htm1+kytable.kxtable_prepar(rows2,ttls2,wids2,""))
def test_xl():
    import k_file_x,k_xl_light
    #path1=r'\\192.168.88.196\share data\AQC\DES-AR\REPORT-DAILY-R03-030402.xlsm'
    path1=r'\\192.168.88.196\share data\AQC\DES-AR\OTHER\KS\REPORT-DAILY-R03-030402_test.xlsm'
    tbl=k_xl_light.read(wb_path =path1,
                    ws_name='daily-report',
                    row_st=2,row_en=100000,col_st=1,col_en=10,empty_row='b')
    #return (str(tbl))
    set1="""{
        rows: ["نام و نام خانوادگی"], 
        cols: ["روز"],
        vals: ["زمان"],
        aggregatorName: "Sum",
        rendererName: "Table"}"""
    import json
    tb2=json.dumps(tbl)
    return (k_file_x.pivot_make_free(tb2,set1))  

    
def test_xl_old():
    import k_xl_light
    k_xl_light.read(wb_path,ws_name,row_st,row_en,col_st,col_en)
    xl_path = r'C:\temp\test.xlsx'
    import pylightxl as xl
    
    # pylightxl also supports pathlib as well
    db = xl.readxl(xl_path)
    #return (db.ws_names)
    tbl=[]
    for i in range(3):
        row=[]
        for j in range(7):
            row+=[(db.ws(ws='a12').index(row=i+1, col=j+1))]
        tbl+=[row]
    return (str(tbl))

def test_kytable1():
    return '''
    
<!DOCTYPE html> 
    <html lang="fa">
    <style type="text/css" id="dark-mode-custom-style"></style>
    <head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>   kx table </title>
            <meta http-equiv="Cache-control" content="no-cache">
            <!-- kxtable -->
                <script src="/spks/static/kxtable/jquery-1.8.2.min.js" type="text/javascript"></script>
                
                <link rel="stylesheet" href="/spks/static/kxtable/jquery-ui.css">
                <script src="/spks/static/kxtable/jquery-ui.js"></script>
                
                <link rel="stylesheet" href="/spks/static/kxtable/kxtable.css">
                <script src="/spks/static/kxtable/kxtable-21.js"></script>
                
                <link rel="stylesheet" href="/spks/static/kxtable/jquery.contextMenu.css" type="text/css">
                <script src="/spks/static/kxtable/jquery.contextMenu.js" type="text/javascript"></script>
            <!-- /kxtable -->   
                

    </head>
   <body bgcolor="#888888">
   <div id='output' style='width:100%' >
    ...
    </div>
    <script>

var kxtable_data =[
{
"id" :"1008", 
"نام و نام خانوادگی" :"آیدا صباغیان طوسی", 
"سال" :"1403", 
"ماه" :"5", 
"روز" :"10", 
"روز هفته" :"4 شنبه", 
"پروژه" :"امور روزانه و ستادی", 
"موضوع" :"", 
"اقدامات" :"",},
{
"id" :"1009", 
"نام و نام خانوادگی" :"آیدا صباغیان طوسی", 
"سال" :"1403", 
"ماه" :"5", 
"روز" :"11", 
"روز هفته" :"5 شنبه", 
"پروژه" :"امور روزانه و ستادی", 
"موضوع" :"توضیح و هم اندیشی در خصوص نواقص", 
"اقدامات" :"هم اندیشی در خصوص نواقص زمانبر در گروه ", 
"زمان" :"1",},
{
"id" :"1010", 
"نام و نام خانوادگی" :"آیدا صباغیان طوسی", 
"سال" :"1403", 
"ماه" :"5", 
"روز" :"11", 
"روز هفته" :"5 شنبه", 
"پروژه" :"ارتقا توانمندی ها و جایگاه شرکت", 
"موضوع" :"تحقیق و توسعه ", 
"اقدامات" :"پیگیری از دکتر بهروزفر - پیرو نامه مهندس سعادتی ",}];

var kxtable_data_cols =["id","نام و نام خانوادگی","سال","ماه","روز","روز هفته","پروژه","موضوع","اقدامات","زمان"];

var kxtable_data_width =["1","1","1","1","1","1","1","1","1","1"];

var kxtable_sum_col='{sum_colomn}';
kxtable_make_table(cookiePage);
</script>
    '''
def test_muti_row_approve():
    import k_form
    from k_htm import C_TABLE
    from x_data import x_data_verify_task
    
    data=[
    ['a','a1',1],
    ['b','b2',2],
    ['c','c3',3],
    ['a','a1',4],
    ['b','b2',5],
    ['c','c3',6],
    ['a','a1',1],
    ['b','b2',2],
    ['c','c3',3],
    ['a','a1',4],
    ['b','b2',5],
    ['c','c3',6],
        ]
    if request.vars:
        rows_ch={}
        for i in range(len(data)):
            rows_ch[i] = True if (request.vars[f'row_{i}']) else False 
        return str(rows_ch)    
    data1=[]
    for i,row in enumerate(data):
        obj_inf={'type':'check'}
        nn=f'checkbox_{i}'
        x_data_verify_task(f'row_{i}',obj_inf)
        xh=k_form.obj_set(i_obj=obj_inf,x_dic={},x_data_s={}, need=['input'])['input']
        
        xh=k_htm.checkbox(name=nn)
        #print (str(xh))
        row1=[xh]+row
        data1.append(row1)
    tbl=C_TABLE(['c','x','y','z'],data1).creat_htm()
    return dict(t=k_htm.form(inner_html=tbl))

def test_tag():
    #030528
    import k_s_dom
    tt0="abcd"
    tt1="abc<div id='id-a1' class='class1'>div_text</div>"
    tt2="""<div >
                <a class="btn btn-info" title='مشاهده فایل AQC0-HRM-CV-fbg4-off.pdf' href = 'javascript:void(0)' onclick='j_box_show("/spks/file/download/auto/form/hrm/cv/fbg/AQC0-HRM-CV-fbg4-off.pdf",false);'>F</a>
            </div>"""
    tt3="""<div>
    <a class="btn btn-primary" href="/spks/form/xform.csv/user/user/133" title="open form 133">133</a>,
    <a  title="خانم">خانم</a>,
    <a  title="مهندس">مهندس</a>,فاطمه,برزوی گلستانی,-,
    <a  title="شهر سازی">UR</a>,
    <a  title="طراحی">طراحی</a>,کارشناس شهرسازی,fbg,دفتر مرکزی مشهد- سجاد,y,
            <div >
                
            </div> ,
            <div >
                
            </div> ,
            <div >
                
            </div> ,
            <div >
                
            </div> ,
            <div >
                <a class="btn btn-info" title='مشاهده فایل AQC0-HRM-CV-fbg4-off.pdf' href = 'javascript:void(0)' onclick='j_box_show("/spks/file/download.csv/auto/form/hrm/cv/fbg/AQC0-HRM-CV-fbg4-off.pdf",false);'>F</a>
            </div></div>
    """
    
    return dict(at2=k_s_dom.report_tag(tt2),
                at1=k_s_dom.report_tag(tt1),
                at0=k_s_dom.report_tag(tt0),
                aa=str(k_s_dom.C_TAG(tt2).find('_title')))#.tag_inf())
def test_ppr():
    import k_file,os
    x_cmd="D:\\ks\\ext\\WPy64-31040\\python-3.10.4.amd64\\python.exe "#, to_md {file1} {file2} ".format(file1=doc_file_path,file2=md_file_path)
    #x_cmd+=os.path.join("D:\ks\I\web2py","0-need\k_word_mammoth.py")
    #x_cmd+=" to_md {file1} {file2} ".format(file1=doc_file_path,file2=md_file_path)
    
    #x_cmd="D:\\ks\\ext\\WPy64-3850\\python-3.8.5.amd64\\python.exe "
    #x_cmd+=os.path.join("D:\ks","I","Dropbox","00-PRO","0-py","0-base","AQC_paper_playwright.py")
    x_cmd+=os.path.join("D:\ks\I\web2py","0-need\k_q_atm_playwright.py.py")
    x_cmd+=" 2266" 
    import k_os
    return k_os.run_cmd(x_cmd) 
    '''
    import subprocess
    try:
        os.startfile(filename)
    except AttributeError:
        #subprocess.call(['open', filename])
        subprocess.call(('cmd', '/C', 'start', '', filename))
    k_file.launch_file(x_cmd)
    '''
    return x_cmd
def test_ppr1():
    from k_q_atm_playwright import C_Q_ATM_PR
    c_q_atm_pr=C_Q_ATM_PR()
    c_q_atm_pr.run_pp("2266")
    return ("2266")
def set_ppr():
    def paper_num_min(papaer_num):
        '''
        goal:
        ------
            تهیه شماره مختصر برای هر نامه از روی شماره ثبت شده در اتوماسیون روان
        '''
        import re
        num_list=re.findall("\d+", papaer_num)
        pnm=num_list[0] #pnm=paper_num_min
        if len(num_list)>1 and len(num_list[1])>3 and (not num_list[1] in ["1404","1403","1402","1401","1400"]):
            pnm=num_list[1]
        return pnm
    if not 'lno' in request.vars:return "lno not in vars"
    papaer_num=request.vars['lno'] #request.args[0] 
    #from k_q_atm_ppi import C_PAPER
    pp_num_min=paper_num_min(papaer_num) #C_PAPER().
    import k_file
    f_name='c:\\temp\\x_export\\paper_num.txt'
    k_file.write('text',f_name,pp_num_min+",",append=True)
    new_list=k_file.read('text',f_name)
    return f"<h2>ok</h2>{pp_num_min}<br> saved to => <br>{f_name}<hr>new list=<hr>{new_list}"
def reports():
    import k_htm #k_err
    #return k_err.htm_dict(session['reports'])
    return k_htm.val_report(session['reports'])


def auth_of_form():
    '''
    db_name='person_act'
    tb_name='a'
    x_data_s=x_data[db_name][tb_name]
    tasks=x_data_s['tasks']
    for task in tasks:
        if 'auth' in task:
            
        else:
    '''
    
def need_links():
    links=['']
    #AND end IS NULL
    #loc = 100
    prm={"_class":"btn btn-outline-primary text-center text-wrap rounded"}
    prm1={"_target":"",**prm}
    prm2={"_target":"","_dir":"ltr",**prm}
    rows=[
        [
            '',
            [k_htm.a("تلفن همکاران دفتر مرکزی",**prm1,
                _href=URL('form','xtable',args=['user','user'],vars={'data_filter':'(end IS NULL OR end =0) AND loc LIKE "01%"','cols_filter':'name,family,tel_wrk,tel_mob',
                        'table_class':2,'data_page_n':1,'data_page_len':40})         
                )],
            [k_htm.a("همکاران قدیمی",**prm1,
                _href=URL('form','xtable',args=['user','user'],vars={'data_filter':'(end IS NOT NULL AND end != 0)','cols_filter':'name,family,end',
                    'table_class':2,'data_page_n':1,'data_page_len':40})
                )],
            [k_htm.a("آمار فراداده ها",**prm1,_href=URL('form','list_0_mr')
                )],
            [k_htm.a("اطلاعات پروژه ها",**prm2,_href=URL('form',"prj_inf")
                )],
            '',
        ],
        [
            '',
            [k_htm.a("حاظران",**prm2,_href=URL('tmsh',"hazeran")
                )],
            '',
            '',
            '',
            '',
        ]
    ]
    #rows=[links]
    if session["admin"]:
        links=[k_htm.a("papers=>todo !=''",**prm2,
                    _href=URL('data','xtable',args=['paper','a'],vars={'data_filter':"todo !=''",
                        'table_class':2,'data_page_n':1,'data_page_len':40})),
                k_htm.a("p date",**prm2,_href=URL('form','date_picker')),
                k_htm.a("لیست فیلد های لینک شده",**prm2,_href=URL('data','rc',args=('find_linked_target_fields'))),
                k_htm.a("ریست پسورد همکاران",**prm2, _href=URL('user','reset_password')),
                k_htm.a("مشخصات و اطلاعات ارتباط",**prm2,_href=URL('data','inf')),
                k_htm.a("همکاران وارد شده به سیستم",**prm2,_href=URL('data','user_inf')),

            ]
        rows+=[links+["","","","",""]]
    else:
        rows+=[["","","","","","",""]]
    lnk,trs,f_l='','',''
    xx00={    
    "papers=>todo !=''":lnk+"""data/xtable/paper/a?data_filter=act_todo+%21%3D%22%22&cols_filter=&table_class=2&data_page_n=1&data_page_len=20""",
    "papers=>نامه ها- پیگیری":lnk+"""data/xtable/paper/a?data_filter=act_pey+%21%3D%22%22&cols_filter=&table_class=2&data_page_n=1&data_page_len=20""",
    "papers=>ALL":lnk+"""data/xtable/paper/a""",
    "papers=>GGA-Layouts":lnk+"""data/xtable/paper?data_filter=%22prj%22%3D%2229%22+AND+%22des%22+like+%22%25L-%25%22&cols_filter=&table_class=1""",
    "papers=>standard":lnk+"""data/xtable/paper?data_filter=%22prj%22%3D%2248%22""",
    "-----------":"", 
    "spks help":lnk+"""file/f_list?xpath=D:\ks\I\web2py\Applications\spks\help""",
    "km":lnk+"""file/f_list/ks/i/dropbox/01-KM/1-ACT?xpath=d%3A """,
    "TimeSHeet":lnk+"""xfile/read/ks/i/dropbox/01-KM/1-ACT/11-KS/Timesheet/TMST-NNNN-AQC.mm?xpath=d%3A""",
    "------------":"",
    "form":lnk+"""form/xform/test/b/1""",
    "form-table":lnk+"""data/table/test/b"""
    }
    rem={
    "home":lnk+"""data/index""",
    "spks-file-index":lnk+"""file/index""",
    }
    
    if session["admin"]:
        """
        trs+=[TR(*[TH(f_l+x) for x in ['0','x','kx','sp','select']])]#[TR(TH(f_l+'0'),TH(f_l+'X'),TH(f_l+'KX'),TH(f_l+'SP'),TH('update'))]
        for arg in [['a_sub_p','a'],['paper','a'],['a_dspln','a'],['user','user'],['job','a']]:#,'a'),('eng','a'),('user','user')]:
            trs+=[TR(*[A(ff[arg[0]],_href=URL(xtbl,args=(arg)))   for xtbl in ['table','xtable','kxtable','sptable','select']])]
        t1=DIV(DIV(A('admin',_href=URL('spks','default','admin'))),
              DIV(A('xxprint_reset_html',_href=URL('spks','data','_xxprint_reset_html'),_target="x_frame"))
              )
        
        t2="<hr>"      
        t2+='<br>'.join([f"<a href={links[x]} > {x} </a>" for x in links])  
        
        
        """
        t2=f"""<br><div class="row">
            <div class="col">
                <a class='btn btn-primary' href={URL('rc',args=('copy_table_inf','do-x'))}>edit (data.py) def(rc) line 1048 : کپی اطلاعات 1 جدول به جدول دیگر </a>
            </div>
            <div class="col">
                <a class='btn btn-primary' href={URL('km','test_ipgrid')}>test_ipgrid</a>
            </div>
        </div>
            """
   
    return dict(htm=TABLE(['']+rows+[''],_id="table_A1"))
def test_xdata():
    import x_data_test as xx
    return xx.main_test()
def test_pass():
    import k_user
    pss=['abcd@12A','ab','123456789','abcd!12B']
    res=''
    for ps in pss:
        res+=ps+ " = " +str(k_user.pass_is_safe(ps)) + "<br>"
    return res
def test_mob():
    url=URL('static','jq_mob')
    return f"""
    <!DOCTYPE html>
<html class="ui-mobile"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8"><!-- base href="http://demos.jquerymobile.com/1.4.5/pages-single-page/index.html" -->
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Single page</title>
	<link rel="stylesheet" href="{url}/jquery.mobile-1.4.5.min.css">
	<link rel="stylesheet" href="{url}/jqm-demos.css">
	<link rel="shortcut icon" href="http://demos.jquerymobile.com/1.4.5/favicon.ico">
	<script src="{url}/jquery.js"></script>
	<script src="{url}/index.js"></script>
	<script src="{url}/jquery.mobile-1.4.5.min.js"></script>
</head>

<body style="" class="ui-mobile-viewport ui-overlay-a">

<div data-role="page" data-url="/1.4.5/pages-single-page/index.html" tabindex="0" class="ui-page ui-page-theme-a ui-page-active" style="min-height: 775px;">

	<div data-role="header" role="banner" class="ui-header ui-bar-inherit">
		<h1 class="ui-title" role="heading" aria-level="1">Single page</h1>
	</div><!-- /header -->

	<div role="main" class="ui-content">
		<p>This is a single page boilerplate template that you can copy to 
build your first jQuery Mobile page. Each link or form from here will 
pull a new page in via Ajax to support the animated page transitions.</p>
		<p>Just view the source and copy the code to get started. All the CSS 
and JS is linked to the jQuery CDN versions so this is super easy to set
 up. Remember to include a meta viewport tag in the head to set the zoom
 level.</p>
		<p>This template is standard HTML document with a single "page" container inside, unlike a <a href="http://demos.jquerymobile.com/1.4.5/pages-multi-page/" data-ajax="false" class="ui-link">multi-page template</a>
 that has multiple pages within it. We strongly recommend building your 
site or app as a series of separate pages like this because it's 
cleaner, more lightweight and works better without JavaScript.</p>
<a href=http://demos.jquerymobile.com/1.4.5/> ***</a>
	</div><!-- /content -->

	<div data-role="footer" role="contentinfo" class="ui-footer ui-bar-inherit">
		<h4 class="ui-title" role="heading" aria-level="1">Footer content</h4>
	</div><!-- /footer -->

</div><!-- /page -->



<div class="ui-loader ui-corner-all ui-body-a ui-loader-default"><span class="ui-icon-loading"></span><h1>loading</h1></div></body></html>
    """
    return """
    <!doctype html>
    <html>
    <head>
        <title>My Page</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        
        <link rel="stylesheet" href="https://code.jquery.com/mobile/1.4.0/jquery.mobile-1.4.0.min.css">
        
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
        <script src="https://code.jquery.com/mobile/1.4.0-rc.1/jquery.mobile-1.4.0-rc.1.min.js" ></script>
    </head>
    <body>
        <div data-role="page">
     
            <div data-role="header">
                <h1>My Title</h1>
            </div><!-- /header -->
     
            <div role="main" class="ui-content">
                <p>Hello world</p>
            </div><!-- /content -->
     
            <div data-role="footer">
                <h4>My Footer</h4>
            </div><!-- /footer -->
     
        </div><!-- /page -->
    </body>
    </html>
    """
