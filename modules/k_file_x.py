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
def read_xl(wb_path,ws_name,row_st,row_en,col_st,col_en,to_empty=True):
    import pylightxl as xl
    
    # pylightxl also supports pathlib as well
    db = xl.readxl(wb_path)
    #return (db.ws_names)
    tbl=[]
    for i in range(row_st,row_en):
        row=[]
        for j in range(col_st,col_en):
            row+=[(db.ws(ws=ws_name).index(row=i, col=j))]
        if to_empty and not row[1]:
            break
        tbl+=[row]
    #print(f'i={i}')
    return tbl
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
    
    