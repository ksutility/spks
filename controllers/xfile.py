# -*- coding: utf-8 -*-
# ver 1.00 1401/08/14 
# -------------------------------------------------------------------------
"""
body {
+    padding:50px 50px 0 0px;
 }
@media print {
-  h1 {page-break-before: always;}
+  h1:not(:first-child) {page-break-before :always;}
+  h1:first-child {page-break-before: avoid;}
 }
h1 {
-    margin:4px;
+    margin:10px 0 0 0;
+    padding:50px 10px 0px 0px;
 } 
"""
def htm_head(print_mode=1):
    xr=f"""
    <head>
    <script type="text/javascript" src="{URL('static','js/datepicker/jquery-1.8.2.min.js')}"></script>
    <script type="text/javascript" src="{URL('static','js/jquery.tablesorter.js')}"></script>
    <link rel="stylesheet" href="{URL('static','css/fonts_b.css')}"/>
    """
    xr+="""
    <style>
    body {
        counter-reset: c_h1;
        /* background-color: #ffe; */
        direction:rtl;
        font-family: BBadr;
        font-size: 20px;
        /* padding:50px 50px 0 0px; */
        
    }"""
    if print_mode==1:
        xr+="""
        @media print {
          h1:not(:first-child) {page-break-before :always;}
          h1:first-child {page-break-before: avoid;}
        }"""
    else:
        xr+="""
        @media print {
          h1 {padding:0px 0px 0px 0px;}
        }"""
    xr+="""
    h1:before {
        content: counter(c_h1)") ";
        counter-increment: c_h1;
    }
    h1 {
        counter-reset: c_h2;
        background-color: #fbb;
        margin:10px 0 0 0;
        font-family: BTitrBold,Tahoma, sans-serif;
        font-size: 24px;
        padding:50px 20px 0px 0px;
    }
    h2:before {
        content: counter(c_h1)"." counter(c_h2)") ";
        counter-increment: c_h2;
    }
    h2 {
        text-indent: 40px;
        background-color: #eef;
        counter-reset: c_h3;
        margin:2px;
        font-family: BTitrBold,Tahoma, sans-serif;
        font-size: 20px;
    }
    h3:before {
        content: counter(c_h1)"." counter(c_h2)"." counter(c_h3)") ";
        counter-increment: c_h3;
    }
    h3 {
        text-indent: 60px;
        background-color: #eed;
        margin:2px;
        font-family: BTitrBold,Tahoma, sans-serif;
        font-size: 16px;
    }
    h4 {
        text-indent: 80px;
        background-color: #ccc;
        margin:2px;
        font-family: BTitrBold,Tahoma, sans-serif;
        font-size: 18px;
    }
    /* ---------------------------------------------------------- */
    table {
      font-family: Arial, Helvetica, sans-serif;
      border-collapse: collapse;
      width:100%
      
    }

    table td, table th {
      border: 2px solid #ddd;
      padding: 8px;
    }
    .title1 {
        background-color: #523e6b;
        color: #edebc5; 
        text-align: center;
        font-size: 40px;
        font-family: BTitrBold,Tahoma, sans-serif;
        padding:100px;
    }
    .title2 {

        color: #523e6b; 
        text-align: center;
        font-size: 20px;
        font-family: BTitrBold,Tahoma, sans-serif;
        padding:30px;
    }
    .menu {
        font-size: 14px;
        text-align: center;
    }
    table tr:nth-child(odd){background-color: hsl(220, 90%, 95%);}
    table tr:nth-child(even){background-color: hsl(220, 90%, 90%);}
    table thead tr td,
    table tfoot tr td {background-color:#fff;color:#fff}
    table tr:hover {background-color: #fdd;}

    table th {
      padding-top: 12px;
      padding-bottom: 12px;
      background-color: hsl(220, 90%, 85%);
    }
    table td {text-align: center;}
    /* ----------------------------------------------------------blockquote =>  */
    blockquote {
       
       background-color:rgba(250, 200, 130, 0.5);
       font-family: BYekan,Tahoma, sans-serif;
       text-indent: 20px;
       font-size: 18px;
       width: 90%;
       margin: 5 auto;
    }
    blockquote h1 {
       font-size: 4rem;
    }
    blockquote p {
       font-style: italic;
       margin-bottom: 0;
    }

    blockquote p::before,
    blockquote p::after {
       content: "“";
       font-family: Georgia;
       font-size: 1rem;
       margin: 0 -1rem 0 0 ;
       position: absolute;
       opacity: 0.5;
    }

    blockquote p::after {
       content: "”";
       margin: +0rem +1rem 0 0;
    }

    blockquote cite {
       font-size: 1.5rem;
    }
    textarea {
        background-attachment: local;
        background-repeat: no-repeat;
        padding-left: 35px;
        padding-top: 10px;
        border-color:#ccc;
    }
    /* ---------------------------------------------------------- */
    ul,li{
        direction:rtl;
        font-family:BNazanin,BYekan,BRoya,BTitrBold,BMehrBold,arial, sans-serif;
        font-size: 18px;
        margin:2px;
    }   
    pre {direction:ltr;}
    code {
      font-family: Consolas,"courier new";
      color: crimson;
      background-color: #f1f1f1;
      padding: 2px;
      font-size: 14px;
    }
    </style>
    <script>
    $(document).ready(function(){
        $("table").tablesorter();
        $("h1").click(function(e) {
            if (e.ctrlKey) {
                $(this).nextUntil("h1").show();
            } 
            else if (e.altKey){
                $(this).nextUntil("h1").hide();
                $(this).nextAll("h2").show();
            }
            else {
                $(this).nextUntil("h1").hide();
            }
        });
        $("h1").dblclick(function(e){
            $(this).nextUntil("h1").show();
        });
        $("h2").click(function(e){
            if (e.ctrlKey) {
                $(this).nextUntil("h1,h2").show();
            } 
            else if (e.altKey){
                $(this).nextUntil("h1").hide();
                $(this).nextAll("h2").show();
                $(this).nextAll("h3").show();
            }
            else {
                $(this).nextUntil("h1,h2").hide();
            }
        });    
        $("h2").dblclick(function(e){
            $(this).nextUntil("h1,h2").show();
        });
        $("h3").click(function(e){
            if (e.ctrlKey) {
                $(this).nextUntil("h1,h2,h3").show();
            } 
            else if (e.altKey){
                
            }
            else {
                $(this).nextUntil("h1,h2,h3").hide();
            }
        });  
        $("h3").dblclick(function(e){
            $(this).nextUntil("h1,h2,h3").show();
        });
    });
    </script>
    </head>
    """
    return XML(xr)
#---------------------------------------------------------------------
#e.shiftKey   if (e.ctrlKey) altKey
#import share_value as share
#xpath=share.xpath()

def _x_file(def_file=''):
    '''
        dedicate file from args
    '''
    msg=''
    import os,sys,k_file
    import share_value as share
    import k_set
    xpath=request.vars['xpath'] or k_set.xpath()
    #if xpath[-1] !='\\' :xpath+='\\'
    #xpath=share.xpath()
    args=request.args
    f_name='\\'.join((request.args)) if args else request.vars['file_path'] or def_file
    if not f_name:msg='error :file not spesified'
    #f_name=os.path.join(xpath,f_name) if f_name else xpath
    f_name=xpath + "\\" + f_name if f_name else xpath
    #print(f_name,xpath,share.xpath(),"-")
    file_inf=k_file.file_name_split(f_name)
    
    #print("file_inf" + str(file_inf))
    return f_name,msg,file_inf

#---------------------------------------------------------------------------------------------------------------------------------------------------------
    
def index():
    xinf=['read_m','read_csv']
    tt1=[INPUT(_value=request.vars['file_path'],_name='file_path'),
        INPUT(_type='submit')]
    tt2=[A(x,_href=URL(x,vars=request.vars)) for x in xinf ]
        
    return FORM(TABLE(*tt1,*tt2))
def py2json():
    '''
        convert a dic_obj form py file to json file
        dict_name=x_data
    '''
    path0='D:\\pro\\ext\\web2py\\0-file'
    import os,sys,csv,k_file
    args=request.args
    f_name='\\'.join((request.args)) if args else os.path.join('test','x_data.py')
    f_name=os.path.join(path0,f_name)
    import f_name
    ff=k_file.file_name_split(f_name)
    f_name2=os.path.join(ff['path'],ff['name']+'.json')
    #k_file.write('json',f_name2,x_data)
    return 'ok - coverted inf from py to json<br>{}<br>{}'.format(f_name,f_name2)
def testj1():
    import os,k_file
    f_path2=os.path.join("0-file",'xxx1.json')
    k_file.write('json',f_path2,fildes)
    return 'ok'
def json_read():
    def json_p(name,data,n_idn,par='_',t_idn=' '*8,br='<br>'):
        def h_a(val,tit): #html a
            return f"""<a title='{tit}'>{val}</a>"""
        #br=break line par=parent
        pt=t_idn*n_idn #pre text
        d=data
        if type(data)==str:
            return f'<input name="{name}" id="{name}" value="{d}" class="input1">'+br
        elif type(data)==int:
            return f'<input name="{name}" id="{name}" value="{d}" class="input1" type="number">'+br
        elif type(data)==dict:
            if len(data)==0:
                return "{}"+br
            return "{"+br+ pt+pt.join([f'{h_a(x,name+";"+x)} : {json_p(name+";"+x,data[x],n_idn+1,x)} ' for x in data]) +pt+"}"+br
        elif type(data)==list:
            if len(data)==0:
                return "[]"+br
            return "["+br+ pt+pt.join([f'{json_p(name+f";{i}",x,n_idn+1)}' for i,x in enumerate(data)])+pt+"]"+br
    import os,k_file,json
    f_name,f_msg,file_inf=_x_file()
    if not f_name:return f_msg
    meta=k_file.read('json',f_name)
    style1="""
       .input1{
       height:20px;
       width:500px
       } 
    """
    return dict(style=style1,
            k_json=XML(json_p("-",meta,0)),
            json_dump=XML(json.dumps(meta,indent=4)),
            json_str=str(meta)) #<div class=''>+"</pre>"  
def read_xl():
    try:
        f_name,f_msg,file_inf=_x_file()
        if not f_name:return f_msg
        import kxl
        wb=kxl.wb(f_name)
        return (wb.sheetnames)
    except:
        return "error in xfile.py => def(read_xl)"
def _read_csv(f_name):
    import k_file_x
    data=k_file_x.read_csv(f_name,'list')
    if len(data)>5 and 'error'==data[:5]:
        return data #'error in encoding file'   
    #return TABLE([TR([TD(XML(x)) for x in row]) for row in data],_class='table2')#XML()
    x_head=TAG.thead([TH(XML(x)) for x in data[0]]) #THEAD([TH(XML(x)) for x in data[0]])
    return TAG.table(x_head,TBODY([TR([TD(XML(x)) for x in row]) for row in data[1:]]),_class='table2')#XML()
    #return TABLE(x_head,TBODY([TR([TD(XML(x)) for x in row]) for row in data[1:]]),_class='table2')#XML()
def read_csv():
    f_name,f_msg,file_inf=_x_file()
    if not f_name:return f_msg
    return dict(t=_read_csv(f_name))
def read_csv1():
    f_name,f_msg,file_inf=_x_file()
    if not f_name:return f_msg
    return _read_csv(f_name)
def read_csv2():
    f_name,f_msg,file_inf=_x_file()
    if not f_name:return f_msg
    return dict(x_table = _read_csv(f_name))
def read_mermaid():
    f_name,f_msg,file_inf=_x_file()
    with open(f_name,'r',encoding='utf8') as file: 
        lines = [line for line in file]
    def mermaid_2_html(head,mermaid_base): 
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
                    <h1 class="center">
                        {head}
                    </h1>
                    <hr>
                    <div>
                        <pre class="mermaid">
                            {''.join(mermaid_base)}
                        </pre>
                    </div>
                </div
            </div>
        </body>
        '''
        
    #--------------
    ext=file_inf['ext'][1:]
    #return ext
    if ext=="mermaid2":
        return mermaid_2_html(lines[0],lines[1:]) 
    if ext=="mermaid":
        return mermaid_2_html("abc",lines) 
    pass
def read(): #read all markup
    f_name,f_msg,file_inf=_x_file()
    ext=file_inf['ext'][1:]
    if ext in ['md','mm','ksm']:
        return _read_markup(ext)
    #elif ext in[""]
    #xd={'json':'json_read','csv':'read_csv','md':'read_m','mm':'read_m','ksm':'read_m','ipt2win':'read_ipt2win'}    
    return str(file_inf) 
def read_ipt2win():
    #return 'abc'
    import autocad_persian_ipt as acp
    f_name,f_msg,file_inf=_x_file()
    if not f_name:return f_msg
    with open(f_name,'r',encoding='utf8') as file: 
        #lines = [line.rstrip() for line in file]
        lines = [line for line in file]
    style="""
    <style>
    tr:nth-child(even) {
        background-color: #D6EEEE;
        }
    table {width:100%}    
    </style>
    """
    #return [acp.kateb_2_win(line.rstrip()) for line in lines]
    return XML(style)+TABLE([TR(acp.kateb_2_win(line.rstrip()),line) for line in lines])
    #return "<br>".join([acp.kateb_2_win(line.rstrip()) for line in lines])

def _read_markup(mm_case):
    f_name,f_msg,file_inf=_x_file()
    if not f_name:return f_msg
    import k_s_dom,k_file
    #from gluon.ks import markdown
    #return x.xx()
    def file_2_htm(data,ext):
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
    def _r_mm(data):
        return file_2_htm(data,'mm')
    def _r_md(data):
        return file_2_htm(data,'md')
    def _r_ksm1(f_name):
        d2=""
        with open(f_name) as file: #open(f_name,'r',encoding='utf8')
            lines = [line.rstrip() for line in file]
        if lines[0][1]=="SET ":
            pass
        for f_name in files[1:]:
            with open(files[0]+f_name,'r',encoding='utf8') as f:
                d1=f.read()
            d2+=d1 #<br>+f_name    
        return _r_mm(d2) #d2    #
    def _r_ksm(f_name):
        d2=""
        from gluon import template
        with open(f_name,'r',encoding='utf8') as file: 
            #lines = [line.rstrip() for line in file]
            lines = [line for line in file]
            lines_rs = [line.rstrip() for line in lines]
        #return str(lines)   
        if "---" in lines_rs:
            n=lines_rs.index('---')
            try:
                xdic=eval(''.join(lines_rs[:n]))
            except Exception as err:
                import traceback
                tb = traceback.format_exc()
                return f'ERROR<br>خطا در محتوای داخل فایل <br> در قسمت دیکشنری تعریف متغرها در بالای فایل قبل از 3 دش<hr>file={f_name}<hr>{tb}'
            #return (str(xdic))
            xlines=lines[n+1:]
            xlines=[template.render(content=x,context=xdic) for x in xlines]
            #return (str(xlines))
        else :
            xlines=lines
        ml_mode='md'
        line_sum=''
        for line in xlines:
            if len(line)>6 and line[:6]=='%%read':
                f_name=line[7:].rstrip()
                f_name1=k_file.find (f_name)
                if not f_name1:
                    return DIV(H1("ERROR: file not found"),HR(),H2(f_name))
                ext=k_file.file_name_split(f_name1)['ext'][1:]
                if ext in ['mm','md']:
                    with open(f_name1,'r',encoding='utf8') as f:
                        d1=f.read()
                    d2+=file_2_htm(d1,ext)
                elif ext=='csv':
                    d2+=_read_csv(f_name1)
            elif len(line)>3 and line[:2]=='%%':
                if line_sum:
                    d2+=file_2_htm(line_sum,ml_mode)
                    line_sum=''
                x_act=line[2:].strip().lower()
                if x_act in ['md','mm','htm']:
                    ml_mode=x_act
                    #print (x_act)
                else:
                    print(f"error : {line} => {x_act}")
            else:
                line_sum+=line
                #d1=file_2_htm(line,ml_mode)
            #d2+=d1 #XML(d1) #<br>+f_name    
        d2+=file_2_htm(line_sum,ml_mode)
        return d2 #_r_mm(d2) #d2    #
            
    def html_visible(html):
        return html.replace('<','^').replace('\n','/n').replace('\t','/t')
    # /def - 1 -------------------------------------    
    def _dir_x(html):
        """
            چر چین کردن : چپ چین و یا راست چین کردن یک بخش از متن و یا فقط یک خط
            با استفاده از علامتهای $$l,$$r
            اگر علامت در یک خط خالی باشد محدوده علامت تا علامت بعدی چر چین  می شود
            اگر علامت در یک خط دارای متن باشد ( بهتر است اول خط باشد- جهت خانایی) فقط خط مورد نظر چر چین میشود
            add <div dir='ltr'></div> or <div dir='ltr'></div> to txt:

                convert :   '<p> txt_line \n ... \n txt_1 $$lr txt_2                        \n text_line \n ... <\p>' 
                      to:   '<p> txt_line \n ... \n <<divx>>txt_1 text_2 <<\divx>> $$lr txt \n text_line \n ... <\p>' 

                convert :                   ' <p> txt_line \n ... \n $$lr    \n text_line \n ... <\p>' 
                      to:   '<<\divx>><<divx>><p> txt_line \n ... \n         \n text_line \n ... <\p>' 

                            $$lr =$$r or $$l
                            <<divx>> = <div dir='ltr'> or  <div dir='rtl'> 
        """
        import re
        def repl(x):
            '''
                x=find item
                xb=item befor of x
            '''
            tag_name=x[1]
            m=list(x[3].partition('$$'))
            dd=m[2][0]
            dirx='ltr' if dd in ['l','L'] else 'rtl'
            m[2]=m[2][1:] # omit r / l ($$r,$$l)
            if dd in ["l","r"]:
                return f"<{tag_name}><div dir='{dirx}'>{m[0]}{m[2]}</div></{tag_name}>"
            elif dd in ["L","R"]:
                ou=f"</div><div dir='{dirx}'>"
                if m[0]:ou=f"<{tag_name}>{m[0]}</{tag_name}>"+ou 
                if m[2]:ou=ou+f"<{tag_name}>{m[2]}</{tag_name}>"   
                return ou
        # /def - 2 ---------------------------------
        h_o=TAG(html)
        
        fnd=k_s_dom.find_item(h_o,'$$')
        for x in fnd:
            rp=XML(repl(x))
            k_s_dom.tag_set_by_jad_list(tag=h_o,jad=x[2],html=rp)
        return str(h_o)
    # /def - 1 -------------------------------------    
    with open(f_name,'r',encoding='utf8') as f:
        data0=f.read()
    # slice -----------------    
    
    #data='\n# '.join(data0.split('\n# ')[0:2])
    
    #data1='\n# '+ data0.split('\n# ')[0]
    #data='\n## '+ data1.split('\n## ')[1]
    
    data=data0
    # \slice----------------- 
    if mm_case=='mm':
        html_1=_r_mm(data)  
    elif mm_case=='md':
        html_1=_r_md(data) 
    elif mm_case=='ksm':
        html_1=_r_ksm(f_name) 
        data=""
    html_2=_dir_x(html_1)    
    def report(data,html_1,html_2):
        if not request.vars.debug: return ''
        '''
        use: url+     
            ?debug=1
            &debug=1
        -----------------------------------
        print("#"*30+" data")
        print(data)
        print("="*30+" html_2")
        print (html_2)
        print("="*30+" html_1")
        print (html_1)
        print("="*30+"html_1 sanitize=True")
        print (XML(html_1, sanitize=True))
        '''
        def tbl0(data):
            trs=[TR(TD(i),TD(A(tag,_title=html_visible(tag)))) for i,tag in enumerate(data.split('\n'))]
            return XML(TABLE(*trs ,_style='direction:ltr;width:100%'))
        def tbl(html):
            tags=k_s_dom.tags_list(html)
            trs=[TR(TD(i),TD(A(tag,_title=html_visible(tag)))) for i,tag in enumerate(tags)]
            return XML(TABLE(*trs ,_style='direction:ltr;width:100%'))
            #hs=html.split('<')
            #return XML(TABLE(*[f'<{x}' for x in hs[1:]] ,_style='direction:ltr'))
        def r2(html):
            return XML(DIV(html_visible(html),_style='direction:ltr'))
            #:return XML(DIV(html.replace('<','^').replace('\n','/n').replace('\t','/t'),_style='direction:ltr'))
        #return '<hr><div style="width:100%><div style="width:45%;float: left;">data'+tbl0(data)+'</div><div style="width:45%;float: left;>html_1'+tbl(html_1)+'</div></div>html_2'+tbl(html_2)+'<hr>html_2<br>'+r2(html_2)+'<hr>data<br>'+r2(data)
        return '<hr>data'+tbl0(data)+'<hr>html_1'+tbl(html_1)+'<hr>html_2'+tbl(html_2)+'<hr>html_2<br>'+r2(html_2)+'<hr>data<br>'+r2(data)
    list_link=f"<a title='سیستم مدیریت محتوا' href={URL('file','f_list',args=request.args[:-1],vars=request.vars)}>SPKS </a> | "
    file_name=f"<a title={f_name} href={URL('edit_r',args=request.args,vars=request.vars)}> {file_inf['name']}.{file_inf['ext']} </a><hr>"
    return htm_head(print_mode=0)+DIV(XML(list_link+file_name),_class="menu")+ html_2 + report(data,html_1,html_2)
    #return "----"+ html_1
    #return dict(xml=XML(view_link+list_link+html_2)+ report(data,html_1,html_2)
    #return dict(htm_head=htm_head,xml=XML(html),htm1=rr(html))
def _save_file(f_name,file_txt,encode_n='utf8'):
    ''' creat=1401/10/14
    '''
    import k_file
    bak_file=k_file.backup(f_name,"*,bak")
    file_txt1=file_txt.split('\n')
    # error debuge : python file write add new line when write all lines with other (like f.write(file_content))
    with open(f_name,'w',encoding=encode_n) as f:
        for line in file_txt1:
            f.write(line)
    return bak_file
def edit_r():

    ''' creat=1401/         edit:1401/10/20
    options request.vars
    -------
    
    '''
    if not session["admin"]:
        redirect(URL('file','_access_denied_msg'))
    f_name,f_msg,file_inf=_x_file()
    if not f_name:return f_msg
    file_txt=request.vars['file_txt']
    save_t=bak_file=''
    dir_x='rtl' if not 'dir' in request.vars else 'ltr' 
    enc_list=('utf8','utf-16','','BOM','BOM_BE','BOM_LE','BOM_UTF8','BOM_UTF16','BOM_UTF16_BE','BOM_UTF16_LE','BOM_UTF32','BOM_UTF32_BE','BOM_UTF32_LE')
    for enc in enc_list:
        try:
            with open(f_name,'r',encoding=enc) as f:
                data=f.read()
                encode_n=enc
            break    
        except:
            print ('error: file format !='+enc)
    else:
        return 'error in find encoding of file'
    # save data    
    if file_txt and file_txt != data and request.vars['save_chek']:
        dif_t='' #_diff_txt(data,file_txt)
        bak_file=_save_file(f_name,file_txt,encode_n)
        data=file_txt
        save_t=dif_t+f"<hr>save=ok --- <hr> write to file:{f_name}<hr><pre>{file_txt}</pre>"    
    comp='backup='+bak_file + _diff_files(from_file_path=bak_file,to_file_path=f_name,fromdesc="Old",todesc="New",encoding=encode_n) if bak_file else ''

    on='file_txt'
    lines_num=len(data.split('\n'))
    vars={'xpath':request.vars['xpath']}
    file_name=f"<a title={f_name}> {file_inf['name']}.{file_inf['ext']} </a>"
    o1=XML(f"""
                <a id='view_but' href={URL('read',args=request.args,vars=vars) }>view</a> | {file_name} |  
                {enc}
                {lines_num}
                <input type='hidden' name='textarea_top' id='textarea_top' onchange='file_txt.scrollTop=textarea_top.value;' value='{request.vars['textarea_top']}'>
                <input type='hidden' name='save_chek' id='save_chek' >
                """)
    btn= INPUT(_type='submit',_name="save_but",_id="save_but",_value="Save changed",_style='width:100%,color:#ff00ff' )
    o2= XML(f"""
                <textarea name={on} id={on} rows='50' style='direction:{dir_x};width:100%;height:700px' onclick='textarea_top.value=file_txt.scrollTop;' 
                onchange="text_changed();" scrollTop="{request.vars['textarea_top']}">{data}</textarea>
                """)
    ''
    ''
    #view_link=f"<hr>"-hidden
    '''  $("#save_but").prop('disbled', true);
        var textarea_init=""
        if (textarea_init != document.getElementById("file_txt").value)
        $(document).ready(function(){
            textarea_init=document.getElementById("file_txt").value;
    '''
    script1=(f"""<head><title>+{file_inf['name']}</title></head>"""+
        f"""<script type="text/javascript" src="{URL('static','js/datepicker/jquery-1.8.2.min.js')}"></script> """ +
        """ 
        <script> 
        function text_changed() {
                $("#save_but").css("background-color","red");
                $("#save_chek").val("1")
                $("#save_but").show();
                $("#view_but").hide();
        }
        $(document).ready(function(){
            $("#save_but").hide()
            var textarea = document.getElementById('file_txt');
            var tt = document.getElementById('textarea_top');
            textarea.scrollTop = tt.value;
        });
        </script>
    """)
    return dict(scr= XML(script1),
        mnu=o1,
        btn=btn,
        bdy=o2,
        cmp=XML(comp),
        txt=XML(save_t) )#_action=URL('edit_s',args=request.args,vars=request.vars)
def edit_r2():
    ''' creat=1401/10/21
       برای تغییر یک بخش خاص از فایل
    options request.vars
    -------
    
    '''
    f_name,f_msg,file_inf=_x_file()
    if not f_name:return f_msg
    file_txt=request.vars['file_txt']
    save_t=bak_file=''
    dir_x='rtl' if not 'dir' in request.vars else 'ltr' 
    with open(f_name,'r',encoding='utf8') as f:
        data0=f.read()
    # slice -----------------    
    
    #data='\n# '.join(data0.split('\n# ')[0:2])
    
    #data1='\n# '+ data0.split('\n# ')[0]
    #data='\n## '+ data1.split('\n## ')[1]    
    
    if file_txt and file_txt != data:
        dif_t='' #_diff_txt(data,file_txt)
        bak_file=_save_file(f_name,file_txt)
        data=file_txt
        save_t=dif_t+f"<hr>save=ok --- <hr> write to file:{f_name}<hr><pre>{file_txt}</pre>"    
    comp='backup='+bak_file + _diff_files(from_file_path=bak_file,to_file_path=f_name,fromdesc="Old",todesc="New") if bak_file else ''

    on='file_txt'
    lines_num=len(data.split('\n'))
    o1=[XML(f"<textarea name={on} id={on} rows='50' style='direction:{dir_x};width:100%'>{data}</textarea>{lines_num}"),
        INPUT(_type='submit',_value="Save changed",_style='width:100%,background-color:#ff00ff' )]
    return "<head><title>x</title></head>"+FORM(*o1)+XML(comp+"<hr>"+save_t) #_action=URL('edit_s',args=request.args,vars=request.vars)    
def edit_s():
    ''' creat=1401/         edit:1401/10/14
    با توجه به تغییرات edit_r فعلا استفاده نمیشود
    according to change of (edit_r) not used now (1401/10/14)
    '''
    f_name,f_msg,file_inf=_x_file()
    if not f_name:return f_msg

    file_txt=request.vars['file_txt']
    _save_file(f_name,file_txt)
    vars=request.vars
    vars['file_txt']=''
    return f"<head><title>x</title></head>save=ok --- <a href={URL('edit_r',args=request.args,vars=request.vars)}>edit</a><hr> write to file:{f_name}<hr><pre>{file_txt}</pre>"     
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------    
def edit_view():
    ''' creat=1401/10/14
    '''
    return dict(read_link=URL("read_mm",args=request.args,vars=request.vars),
                edit_link=URL("edit_r",args=request.args,vars=request.vars))
    return dict(frame1=XML(f'<iframe id="f_frame" name="f_frame" src="{URL("read_mm",args=request.args,vars=request.vars)}" height="1000" width="800" title="file previw"></iframe>'),
    frame2=XML(f'<iframe id="f_frame2" name="f_frame2" src="{URL("edit_r",args=request.args,vars=request.vars)}" height="1000" width="800" title="file previw"></iframe>'))
#--------------------------------------------------------------------------------------------------------------------------------------------------------
def _diff_files(from_file_path,to_file_path,fromdesc="Original",todesc="Modified",dif_file_path='',encoding='utf8'):
    ''' creat=1401/10/14
    '''
    from difflib import HtmlDiff
        
    f1 = open(from_file_path, "r",encoding=encoding).readlines()
    f2 = open(to_file_path, "r",encoding=encoding).readlines()   #f2 = "cdef"
    difference = HtmlDiff(tabsize=2)
    html_0 = difference.make_file(fromlines=f1, tolines=f2, fromdesc=fromdesc, todesc=todesc,
            context=True, numlines=1)
    html=html_0.replace("&nbsp;"," ").replace('nowrap="nowrap"',' ')
    if dif_file_path:
        with open(dif_file_path, "w",encoding=encoding) as f:
            f.write(html)
    return html
def _diff_txt(fromlines,tolines,fromdesc="Original",todesc="Modified"):
    ''' creat=1401/10/14
    '''
    from difflib import HtmlDiff
    difference = HtmlDiff(tabsize=2)
    html_0 = difference.make_file(fromlines=fromlines, tolines=tolines, fromdesc=fromdesc, todesc=todesc,
            context=False, numlines=5)
    html=html_0.replace("&nbsp;"," ").replace('nowrap="nowrap"',' ')
    return html    
def diff_files():
    import k_file,os,k_htm
    ''' creat=1401/10/21
        بررسی تغییرات یک فایل با نسخه  ها بک آپ آن در فلدر 
        bak
    '''
    base_file=request.vars.file #or request.vars.file #r'D:\0-file\test\markmin.mm'#
    #- print ('base_file')
    #- print (base_file)
    f1_select1,f1_select2='',''
    dif='-'
    #f_name2
    if base_file:
        #try:
        if True:
            ff=k_file.file_name_split(base_file)
            b_path=os.path.join(ff['path'],'bak')
            files=k_file.find_sami_file(path=b_path,file_name_pattern=ff['name']+'*bak',ext_list=[ff['ext'][1:]])
            if files:
                files.sort(reverse=True)
                f1_select2=k_htm.select(_options=files,_name='file2')#,_value='')#,_onchange=onact_txt,can_add=("can_add" in obj['prop']))
            else:    
                f1_select2='File not have bakup in '+b_path
            f1_select1=k_htm.select(_options=[base_file]+files,_name='file1')
            
        #except:
            #t1='file not valid'
        f_name1=request.vars.file1
        f_name2=request.vars.file2
        if f_name2:
            dif=_diff_files(from_file_path=f_name2,to_file_path=f_name1,
            fromdesc="Original - "+f_name2, todesc="Modified - "+f_name1,dif_file_path='')
    return DIV(FORM(
        TABLE(
            TR('NEW (Modified) File =',f1_select1),#XML(f'''<input name="file2" type="text" value={f_name2} style="width:100%">''')),
            TR('OLD (Original) File =',f1_select2),_style='width:100%;'),
        #XML(''' <input name="file" type="file" size="60"> '''),
        INPUT(_value='Compare',_type='submit')),XML("<HR>"),DIV(XML(dif)))
def tools(): 
    ''' creat=1401/10/21
       انتخاب یک عمل برای اعمال روی فایل
    options request.vars
    -------
    '''
    f_name,f_msg,file_inf=_x_file()
    if not f_name:return f_msg       
    return XML(f'''<input name="file" type="text" value={f_name} style="width:100%">
        <a href={URL('diff_files',vars={'file':f_name})}> comp diff by bak </a>''')
        #<button onclick="$('#input_adr').val('{os.path.join(*args,x['filename'])}');alert('ok')">Copy</button>''')
def diff_files_test():
    ''' creat=1401/10/14
    '''
    path='D:\\ks\\0-file\\test\\bak\\'
    f0='test-20230102-'
    fe='-bak.md'
    f1_n=f0+"120133"+fe
    f2_n=f0+"123920"+fe
    return _diff_files(from_file_path=f1_n,to_file_path=f2_n,
        fromdesc="Original - "+f1_n, todesc="Modified - "+f2_n,dif_file_path=path+"diff.html")
#---------------------------------------------------------------------------------
def test_r():
    t=''
    for i in range (1,70):
        l=''
        for j in range(0,9):
            n=i*10+j
            l+=f'{n}:{chr(n)} ,'
        t+=l+'\n'
    on='file_txt'
    lines_num=len(t.split('\n'))
    txt=request.vars['txt']
    tt=''
    if txt:
        tt=','.join([str(ord(x)) for x in txt])
    o1=[XML(f"<textarea name={on} id={on} rows='{lines_num}' style='direction:rtl;width:100%'>{t}</textarea>{lines_num}"),
        INPUT(_name='txt'),
        tt,
        INPUT(_type='submit',_value="Save changed",_style='width:100%,background-color:#ff00ff' )]
    return FORM(*o1)    
    
    
def test():
    import time
    for i in range(2):
        time.sleep(0.5)
        response.write(i)
    response.menu=[['civilized',True,URL('civilized')],
                   ['slick',False,URL('slick')],
                   ['basic',False,URL('basic')]]    
    response.flash=T("Hello World in a flash!")    
    return dict(x='ok')
def test1():
    import gluon.contrib.pyrtf as q
    doc=q.Document()
    section=q.Section()
    doc.Sections.append(section)
    section.append('Section Title')
    section.append('web2py is great. '*100)
    response.headers['Content-Type']='text/rtf'
    return q.dumps(doc)    
            