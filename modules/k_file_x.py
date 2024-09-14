# -*- coding: utf-8 -*-

"""
Created on 1403/04/31

@author: ks

last update 1403/04/31
"""
from gluon.html import *

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
    