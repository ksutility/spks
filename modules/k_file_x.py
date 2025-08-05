# -*- coding: utf-8 -*-

"""
Created on 1403/04/31

@author: ks

last update 1403/04/31
"""
from gluon.html import *
from k_err import xreport_var

def read_csv(f_name,out_form='str'):
    enc_list={'utf8':',','utf-16':'\t'}
    for enc in enc_list:
        try:
            with open(f_name,'r',encoding=enc) as csvfile:
                if out_form=='str':    
                    data='/n'.join(csvfile)
                elif out_form=='list':
                    data=[row.split(enc_list[enc]) for row in csvfile]
            break    
        except:   
            pass
    else:
        data= 'error in encoding file'
    #import k_err    
    #k_err.xxxprint(msg=['err','',''],args=data,launch=True) 
    return data

def pivot_make(data,set1,htm0=''):  
    '''
    sample input:
        set1:{
            rows: ["name"], 
            cols: ["prj"],
            vals: ["time"],
            aggregatorName: "Sum",
            rendererName: "Bar Chart"}
            
            
            data1="""a,b,c
1,2,3
4,5,6
7,8,9"""
    data1=k_file_x.read_csv(file_path)
            
    '''
    set2=set1[:-1]+""",
            renderers: $.extend(
                $.pivotUtilities.renderers, 
              $.pivotUtilities.plotly_renderers
            )
            }"""
    data1=data        
    import k_file_x
    
    htm1=f"""
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
            //csvString=`%%%1`;
            //results = Papa.parse(csvString);
            ////alert(JSON.stringify(results.data));
            //obj_ar=ar2d_2_objar(results.data);
            //alert(JSON.stringify(obj_ar));
            
            var derivers = $.pivotUtilities.derivers;
            var renderers = $.extend($.pivotUtilities.renderers,
                $.pivotUtilities.plotly_renderers);
            $("#output").pivotUI(%%%1,%%%2);
        });
    </script>
    """ .replace("%%%1",data1).replace("%%%2",set2)
    htm1+=htm0+"""
        <div id="output" dir="ltr" style="margin:2px;font-family: Arial, Helvetica, sans-serif;"><div>
    """    
    return htm1
def pivot_make_free(data,set1,htm0=''):  
    '''
    sample input:
        set1:{
            rows: ["name"], 
            cols: ["prj"],
            vals: ["time"],
            aggregatorName: "Sum",
            rendererName: "Bar Chart"}
            
            
            data1="""a,b,c
1,2,3
4,5,6
7,8,9"""
    data1=k_file_x.read_csv(file_path)
            
    '''
    set2=set1[:-1]+""",
            renderers: $.extend(
                $.pivotUtilities.renderers, 
              $.pivotUtilities.plotly_renderers
            )
            }"""
    data1=data        
    import k_file_x
    
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
            //csvString=`%%%1`;
            //results = Papa.parse(csvString);
            ////alert(JSON.stringify(results.data));
            //obj_ar=ar2d_2_objar(results.data);
            //alert(JSON.stringify(obj_ar));
            
            var derivers = $.pivotUtilities.derivers;
            var renderers = $.extend($.pivotUtilities.renderers,
                $.pivotUtilities.plotly_renderers);
            $("#output").pivotUI(%%%1,%%%2);
        });
    </script>
    """ .replace("%%%1",data1).replace("%%%2",set2)
    htm1+=htm0+"""
        <div id="output" style="margin: 30px;"><div>
    </body></html>
    """    
    return htm1   
def kytable_make(rows,titles,widths='',sum_colomn=''):
    '''
    sample use:
        () or ()
        
        titles=['id','x','y','z','a']
        rows=[
            ['1','5','6','55','45'],
            ['2','8','10','55','45'],
            ]
        
        widths=['3','5','6','5','6']        
        res=kytable_make(rows,titles,widths) 
        
        (or):
        
        res=kytable_make(rows,titles) 
    '''


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
    if not widths:widths=["1" for x in titles]
    if type(widths)==str:widths=widths.split(',')
    import kytable
    return XML(htm1+kytable.kxtable_prepar(rows,titles,widths,sum_colomn))
def ipgrid_make(grid_inf):
    '''
    030613
    
    grid_inf={'inf':{'cols_n':'9','rows_n':'20'},
        'col_widths':'10,5,3,3,5,20,15,30,5',
        'col_titels':['نام و نام خانوادگی',
                      'سال','ماه','روز','روز هفته',
                      'نام پروژه','موضوع','اقدامات','زمان']
      }
    '''  
    data=request.vars['data']
    
    if 'col_widths' in grid_inf:
        table_width=1200
        cw_ts=grid_inf['col_widths'].split(',')
        cw_ns=[int(x) for x in cw_ts]
        cw_sum=sum(cw_ns)
        grid_inf['col_widths']=[int(x*table_width/cw_sum) for x in cw_ns]
    col_titels=[{'name':'id','width':'1'}]+[{'name':grid_inf['col_titels'][i],'width':grid_inf['col_widths'][i]} for i in range(len(grid_inf['col_titels']))]  
    import json
    
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
    if 'col_widths' in grid_inf:
        col_widths="\n".join([f"$('#jqs').ip_ResizeColumn({{ columns: [{i}], size: {x} }});" for i,x in enumerate(grid_inf['col_widths'])])
    if 'col_titels' in grid_inf:
        col_titels="\n".join([f"$('#jqs_q2_columnSelectorCell_{i} div').text('{x}');" for i,x in enumerate(grid_inf['col_titels'])])
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
    '''.replace('% rows_n %',grid_inf['inf']['rows_n']).replace('% cols_n %',grid_inf['inf']['cols_n']).replace('% col_widths %',col_widths).replace('% col_titels %',col_titels)
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
    
def mermaid_2_html(mermaid_base,head=''): 
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
    head=f'''
                <h1 class="center">
                    {head}
                </h1>
                <hr>
    ''' if head else ''
    return f'''
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
                {head}
                <div>
                    <pre class="mermaid">
                        {''.join(mermaid_base)}
                    </pre>
                </div>
            </div>
        </div>
    </body>
    '''
    
#--------------
def cg_form(tmplt_fname,json_data,url1):
    '''
        goal:show 1 form in grafical form
        use : 
            - form.xform_cg
            - ksml
    '''
    import os,k_file,json
    cur_dir=os.getcwd() #D:\ks\I\web2py-test
    file_dir=cur_dir+r"\applications\spks\static\xform_cg"+"\\"+ tmplt_fname
    x_file=k_file.read(file_dir,'text')
    x_file1=x_file.replace('link_url',str(URL('static','xform_cg/link_url')))
    
    x_file1=x_file1.replace('link_server',url1) 
    if tmplt_fname[-8:]!='-st.html': #vue mode
        
        #xreport_var([{'json_data':json_data}])
        
        json_txt=json.dumps(json_data,indent=4,ensure_ascii=False)
        #xreport_var([{'json_data':json_data,'json_txt':json_txt}])
        #'json_txt':json.dumps(htm_form['body_json'],indent=4,ensure_ascii=False) }#,TABLE([str(y) for x,y in htm_form['body_json'].items()])
        #return x_file1
        
        x_file2=x_file1.replace("{'date':'0000/00/00','time':'00:00',}",json_txt)
        script2=""" 
        document.getElementById('help_div').style.display = "none"
        document.getElementById('bt_writetext').style.display = "none"
        """
        x_file2=x_file2.replace("//script2_inject",script2)
        #return x_file2
        return XML(x_file2)
    else:                              #python mode
        import k_tools,k_str
        #--------------------
        x_dic=k_tools.dict2obj(json_data)
        #return json.dumps(x_dic,indent=4,ensure_ascii=False)
        x_file1=k_str.template_parser(x_file1,x_dic,do_format=False)
        return XML(x_file1)
#------------------------------------------------------------------------------
def markup_2_htm(data,ext): # oldname =file_2_htm
    if ext=='mm':
        from gluon.contrib.markmin.markmin2html import markmin2html
        """
        from gluon.contrib.markmin.markmin2latex import markmin2latex
        latex=markmin2latex(data)
        from gluon.contrib.markmin.markmin2pdf import markmin2pdf
        pdf=markmin2pdf(data)  # requires pdflatex 
        """
        return markmin2html(data)#[2:-2]
    elif ext=='md1':
        """
            module\mistune3\
        """
        import mistune3
        return mistune3.html(data)
    elif ext=='md':
        """
            module\mistune.py
        """
        import mistune 
        renderer = mistune.Renderer(escape=False, hard_wrap=True)
        markdown = mistune.Markdown(renderer=renderer)
        return markdown(data)
    elif ext=='htm':
        return data
    elif ext=='mermaid': 
        from k_file_x import mermaid_2_html
        lines= data.split("/n")
        return mermaid_2_html(lines)
#--------------------------------------------------------------------------------------
def ksml_to_html(file,list_url,file_url,pre_case=''): # ksml_to_html(f_name):   
    xdic={}
    f_name=''
    import k_file,k_str
    from gluon import template
    from k_err import xxxprint,xprint
    def read_global_ksml(f_name):
        #  read global ksml in self folder

        xdic2={}
        if f_name:
            folder=k_file.file_name_split(f_name)['path']
            ksml_file=folder+"\\00.ksml"
            import os
            if os.path.exists(ksml_file):
                with open(ksml_file,'r',encoding='utf8') as file: 
                    lines = [line for line in file]
                lines_rs = [line.rstrip() for line in lines] 
                try:
                    json_str=''.join(lines_rs)
                    xdic2=eval(json_str)   
                except Exception as err:
                    xxxprint(msg=['err',err,''],err=err,vals={'lines_rs':lines_rs},launch=True)
                    xprint ('error in template_parser :'+str(err))
   
                xk=list(xdic2.keys())
                for x in xk:
                    xdic2[x]=k_str.template_parser(xdic2[x],xdic2)  
                #xdic.update(xdic2)
 
                return xdic2
            xprint(ksml_file + " => not exist")
        xprint(" ** f_name is epmty")    
        return {}
    #-----------------------------------            
    if type(file)==str:
        f_name=file
        with open(f_name,'r',encoding='utf8') as file: 
            #lines = [line.rstrip() for line in file]
            lines = [line for line in file]
    else: #type(file)==list:
        lines=file 

    lines_rs = [line.rstrip() for line in lines]
    #return str(lines)   
    if "---" in lines_rs:
        n=lines_rs.index('---')
        try:
            json_str=''.join(lines_rs[:n])
            xdic=eval(json_str)
            #xreport_var([{'json_str':json_str,'xdic':xdic}])
        except Exception as err:
            import traceback
            tb = traceback.format_exc()
            return f'ERROR<br>خطا در محتوای داخل فایل <br> در قسمت دیکشنری تعریف متغرها در بالای فایل قبل از 3 دش<hr>file={f_name}<hr>{tb}'
        #return (str(xdic))
        xlines=lines[n+1:]
        file_ns=k_file.file_name_split(f_name)
        xdic['__path__']=file_ns['path']+"\\"
        xdic['__filename__']=file_ns['name']
        
        xdic2=read_global_ksml(f_name)
        xdic.update(xdic2)
        
        xlines=[template.render(content=x,context=xdic.copy()) for x in xlines]
        #return (str(xlines))
    else :
        xlines=lines
    
    
        
    if pre_case:
        xdic['cg_form']={'1':'a01-st.html','2':'a02-st.html','3':'a03-st.html','4':'a04-st.html','a':'a10-pr-wip-st.html'}.get(pre_case,'a04-st.html')
        
    d1=""  #line in base format
    d2=""  #convert md to html 
    d3="" #contet of 1th read file
    ml_mode='md'
    line_sum=''
    for line in xlines:
        if len(line)>6 and line[:6]=='%%read':
            if line_sum: # output lasrt read content of cur file 
                d1+=line_sum+"\n"
                d2+=str(markup_2_htm(line_sum,ml_mode))
                line_sum=''
            f_name=line[7:].rstrip()
            f_name1=k_file.find (f_name)
            if not f_name1:
                return DIV(H1("ERROR: file not found"),HR(),H2(f_name))
            ext=k_file.file_name_split(f_name1)['ext'][1:]
            if ext in ['mm','md','mermaid']:
                with open(f_name1,'r',encoding='utf8') as f:
                    f_t=f.read()
                d3=str(markup_2_htm(f_t,ext))
                d1+=f_t+"\n"
                d2+=d3
            elif ext=='csv':
                d1+="CSV\n"
                d2+=str(_read_csv(f_name1))
        elif len(line)>3 and line[:2]=='%%':
            if line_sum:
                d1+=line_sum+"\n"
                d2+=str(markup_2_htm(line_sum,ml_mode))
                line_sum=''
            x_act=line[2:].strip().lower()
            if x_act in ['md','mm','htm']:
                ml_mode=x_act
                #print (x_act)
            else:
                print(f"error : {line} => {x_act}")
        else:
            line_sum+=line
            #d1=markup_2_htm(line,ml_mode)
        #d2+=d1 #XML(d1) #<br>+f_name    
    d1+=line_sum+"\n"
    d2+=str(markup_2_htm(line_sum,ml_mode))
    def first_text_line(lines):
        '''
        برگرداندن اولین خط متنی 
        خط متنی یعنی با کد های اچ تی ام ال شروع نمی شود
        '''
        xlines=lines.split("\n")
        #import k_err
        #k_err.xreport_var([xlines])
        for line in xlines:
            ll=line.strip()
            if ll and ll[0]!="<":
                return ll
    #-------------------------------
    if 'cg_form' in xdic :
        import k_date
        xdic['__text__']=DIV(XML(d2),_id='_t_',_style="direction:rtl")
        if not 'text_list_color' in xdic:xdic['text_list_color']='1'
        
        if not 'rev' in xdic:xdic['rev']='00'
        #----------------------------
        if not 'app' in xdic:
            xdic['app']='''
                - تهیه :
                - 
                - 
                - تایید :
                - 
                - 
                - تصویب :
                - 
                - 
                '''
        ap=xdic['app'].split("-")+['']*9
        print (str(ap))
        xdic['app1']=ap[1:4]
        xdic['app2']=ap[4:7]
        xdic['app3']=ap[7:10]
        if not 'date' in xdic:
            xdic['date']=k_date.ir_date(xformat='yyyy/mm/dd')
        xdic['__trace__']=f_name+"|"+k_date.ir_date(xformat='yy/mm/dd-hh:gg:ss')
        xdic['list_url']=list_url
        xdic['file_url']=file_url
        #if not 'code' in xdic:
        xdic['code']= (xdic.get('code') or k_file.file_name_split(f_name)['name'])
        if not 'title' in xdic or (not xdic['title']):
            xdic['title']=first_text_line(d1).replace("#","")
        print(xdic)    
        return cg_form(tmplt_fname=xdic['cg_form'],json_data=xdic,url1='')
    else:
        return d2 #markup_2_htm(d2,'mm') #d2    #