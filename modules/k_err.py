# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 14:47:02 2021

@author: ks
update 1400/11/19
"""
import sys
import traceback
from functools import wraps
from k_set import K_set
k_set=K_set()
report_html=k_set.report_html
#from k_ui import input
#import eel_ ui as ui
def _func_inf(inspect_n=0,trace_n=0):
    '''
        USE IN (Service to) : xxprint(),xxxprint()
    '''    
    def trace_step_parser(trace_step):
        func={
            'file':trace_step[1].rpartition('\\')[2].partition('.')[0],
            'name':trace_step[3],
            'args':trace_step[0].f_code.co_consts,
            'line':trace_step[2]}
        func["inf"]='{} #{} . {} () >>> '.format(trace_step[1],func['line'],func['name'],func['args']) 
        func["inf_mini"]='{}#{}.{}()'.format(trace_step[1].split("\\")[-1],func['line'],func['name'],func['args'])
            #[4][:-1]]}
        return func
    ## -----------------------------
    
    import inspect
    
    #called_fun
    #try:
    if True:
        sts=inspect.stack()
        sts1=sts[:inspect_n+1]
        sts2=sts[inspect_n+1:]
        # for s in st:
            # print(str(s[1:3]))
            # print(str(s[3:]))

        #called_function_inf:func  
        st=sts[inspect_n]
        ## -----------------------------
        func=trace_step_parser(sts[inspect_n+1])
        n=min(len(sts2),trace_n+inspect_n)
        func["xtrace_title"]=str(len(sts2))+'>'+'-'.join('{file}:{line}({name})'.format(**trace_step_parser(sts2[x])) for x in range(n+1))
        func["xtrace_v"]=str(len(sts2))+'+'*(len(sts2)-5)
        #func_inf=file name- ,func name)
        ## -------
        #func["inf"]='{} #{} : {} () =>'.format(func['file'],func['line'],func['name'],func['args'])
        #func['all']='\n'.join([f'{i} ** {x[1]} - {x[3]} - {x[2]}' for i,x in enumerate(sts2)])
        func['all']='\n'.join([f'{i} ** '+trace_step_parser(x)["inf"] for i,x in enumerate(sts2)]+[''])
        '''exam output of all=>
            0 ** D:\Dropbox\1-my-data\0-py\Lib\k_err.py - func_inf - 195
            1 ** D:\Dropbox\1-my-data\0-py\Lib\k_err.py - xxprint - 215
            2 ** D:\Dropbox\1-my-data\0-py\Lib\k_selenium.py - wait_for - 125
            3 ** D:\Dropbox\1-my-data\0-py\Lib\k_selenium.py - wait_click - 63
            4 ** D:\Dropbox\1-my-data\0-py\Lib\aqc_paper.py - go_login - 79
            5 ** D:\Dropbox\1-my-data\0-py\Lib\aqc_paper.py - <module> - 687
            6 ** <frozen importlib._bootstrap> - _call_with_frames_removed - 219
            7 ** <frozen importlib._bootstrap_external> - exec_module - 783
            8 ** <frozen importlib._bootstrap> - _load_unlocked - 671
            9 ** <frozen importlib._bootstrap> - _find_and_load_unlocked - 975
            10 ** <frozen importlib._bootstrap> - _find_and_load - 991
            11 ** D:\Dropbox\1-my-data\0-py\0-base\0_aqc_paper-ui.py - <module> - 24
            12 ** D:\pro\ext\WPy64-3850\python-3.8.5.amd64\lib\idlelib\run.py - runcode - 548
            13 ** D:\pro\ext\WPy64-3850\python-3.8.5.amd64\lib\idlelib\run.py - main - 155
            14 ** <string> - <module> - 1
        '''
        return func #,xtrace_title,xtrace_v,func_inf
        
    else:
        #except:
        return {'file':'','line':-1,'name':'','all':''},'','',''
def trace(func):
    "not ok yet"
    @wraps(func)
    def wrapper(*args, **kwargs):
        import sys
        import trace
        # create a Trace object, telling it what to ignore, and whether to
        # do tracing or line-counting or both.
        tracer = trace.Trace(
            ignoredirs=[sys.prefix, sys.exec_prefix],
            trace=0,
            count=1)
        # run the new command using the given tracer
        tracer.runfunc(func, *args, **kwargs)
        # make a report, placing output in the current directory
        r = tracer.results()
        r.write_results(show_missing=True, coverdir=".")
    return wrapper
def _show_old():
    traceback.print_exc()
    print('-'*25+'\n')
    x=input('show traceback_with_variables? n=no / else=yes')
    if x and x=='n':return
    import logging
    import k_date
    from traceback_with_variables import print_cur_tb,print_exc, LoggerAsFile
    xd=k_date.ir_date('yymmdd-hhggss')
    f1,f2=["c:\\temp\\log\\{}-trace_with_var-{}-log.py".format (xd,i) for i in (1,2)]
    
    xprint("-"*30+'tracetrace_with_var2-----start')

    try:
        with open(f2,"w",encoding='utf8') as f:
            print_exc(file_=f)
        xprint (f'File "{f2}", line 1')
        print('-'*25+'\n')
        x=input('countinue?')
    except:
        xxprint("err"," ### error in traceback_with_variables-var2:fun(print_exc)")
        print_exc()
        xprint("err","### error in ( print_exc=> file)=")
        traceback.print_exc()
    xprint("-"*30+'tracetrace_with_var2----end')
    
    xprint("-"*30+'tracetrace_with_var1-----start')
    try:    
        with open(f1,"w",encoding='utf8') as f:
            print_cur_tb(file_=f)
        xprint (f'File "{f1}, line 1"')
        print('-'*25+'\n')
        x=input('countinue?')
        #print_cur_tb()
    except:
        xxprint("err","### error in traceback_with_variables-var1:fun(print_cur_tb)")
        print_cur_tb()
        xxprint("err","### error in ( print_cur_tb=> file)=")
        traceback.print_exc()
    xprint("-"*30+'tracetrace_with_var1----end')
    xprint("-"*30)
    
def _show(msg=['']):
    hh="""
        <html><head>
            <link rel="stylesheet" href="need/do_report.css">
            <script src="need/jquery-3.7.1.min.js"></script>
            
            <link rel="stylesheet" href="need/bootstrap4/css/bootstrap.min.css">
            <script src="need/bootstrap4/js/bootstrap.min.js" ></script>
            <script>
            $(document).ready(function(){
                $(".contents").hide()
            });
            </script>
        </head>
        <body>
        <div class='container-fluid'><pre>
    """
    he="""
       </pre></div></div></body></html> 
    """
    def xxd(n):
        return(f'''</pre></div><div class="bg-primary w-100 text-light" onclick="$('#{n}').toggle();">{n}</div><div id="{n}" class"contents"><pre>''')
    from traceback_with_variables import print_cur_tb,print_exc
    traceback.print_exc()
    fname=k_set.report_err_fname_crt()
    func=_func_inf()
    with open(fname,'a',encoding='UTF8') as file:
        file.write(hh)
        #traceback.print_exc(file_=file)
        file.write(xxd("exec"))#-------
        print_exc(file_=file)
        file.write(xxd("msg"))#-------
        for x in msg:
            #file.write(str(x))
            #file.write('<hr>')
            file.write(val_report(x))
            file.write('<hr>')
        file.write(xxd("trace"))#-------
        file.write(_er_chk(func["xtrace_title"])) 
        file.write('<hr>')
        file.write(_er_chk(func["all"])) 
        file.write(xxd("cur_tb"))#-------
        print_cur_tb(file_=file)
        file.write(he)
    import k_file
    k_file.launch_file(fname)
    return fname
def show(msg=''): #old => check
    _show()
    return x_ask_retry(msg)
def check_err(func):
    'check for error in function'
    @wraps(func)
    def wrapper(*args, **kwargs):
        #return func(*args, **kwargs)
        def func_inf(func,args,kwargs):
            args_repr = [repr(a) for a in args]                   # 1
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
            signature = ", ".join(args_repr + kwargs_repr)           # 3
            return f"{func.__name__}({signature})"
        func_inf1=func_inf(func,args,kwargs)
        while True:
            try:
                xxxprint(cat=['##'],msg=['@check_err','start - func','',func_inf1],inspect_n=2)  
                result = True
                result = func(*args, **kwargs)
                xxxprint(cat=['##'],msg=['@check_err','end - func','-'*20 ,func_inf1],inspect_n=2)
                break
            except:
                result = False
                #debug
                fname=_show(msg=[func_inf1])
                print('#err | check_err | func='+func_inf1)
                if not x_ask_retry(msg=func_inf):break
        return result
    return wrapper
def until_result(result,act_goal_msg):
    def decorator_until(func):
        'check for result(func)=True '
        @wraps(func)
        def wrapper(*args, **kwargs):
            r1=False
            while True:
                f_result = func(*args, **kwargs)
                if f_result==result:
                    r1=f_result
                    break
                else:
                    #debug
                    args_repr = [repr(a) for a in args]                   # 1
                    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
                    signature = ", ".join(args_repr + kwargs_repr)           # 3
                    act={"go-retry":" = play from here - countinue from this",
                         "next-jump after err" : " err = play from next - return False-countinue from next",
                         "breakpoint":"breakpoint()",
                          "end":"quit()"}
                    import tk_ui as ui
                    tx=f"""repeat until true:","one act do not act correctly and need repeat it again!
                        Calling     :{func.__name__}({signature})
                        goal is     :{act_goal_msg}
                        goal result :{result}
                        func result :{f_result}
                    """
                    xxxprint(msg=['err','try again',tx])
                    b=[x for x in act]
                    a=ui.ask(tx,b)
                    if a=="go-retry":pass 
                    elif a=="next-jump after err":return False
                    elif a=="breakpoint":
                        breakpoint()
                        xxx=1
                    elif a=="end":quit()
                    
            return r1
        return wrapper
    return decorator_until
def x_ask_retry(msg):
    '''
        retry?
    '''
    xxxprint(msg=["err",msg,''],trace_n=4)
    while True:
        print("-"*50 + "\n")
        x=input('r=retry / c=cancel & countinu / v=show traceback vars / e=end ?')
        if x=="c":return False
        elif x=="r":return True
        elif x=="v":traceback.print_exc()
        elif x=="e":sys.exit()
def end(msg=''):#ending program for 1 error
    m="به دلیل مشکل زیر برنامه نمی تواند ادامه پیدا کند و متوقف می شود"
    xprint(m+"\n"+msg)  
    quit()
def quit():
    pass
    #web2py
    #x=1/0
    #sys.exit()
    #raise Exception("an error occurred", "unexpected value", 42)   
def xalert(message):
    #use=k_file
    xxprint('alert', message,inspect_n=2)
    from k_ui import alert
    alert(message)
def xprint(message):
    ''' trace for detect err'''
    xxprint('-', message,inspect_n=2)
def xxprint(x_case='-',msg='',msg2='',add_msgs='',inspect_n=1,trace_n=1):
    return xxxprint(out_case=3,cat=[x_case,'-','-'], msg=[msg,msg2,add_msgs],vals={},inspect_n=inspect_n+1,trace_n=trace_n)
    '''
    input:
    ------
        x_case:str
            error/act result(True/False)
        add_msgs:str or list or dict
            program show str(add_msgs)
            (additional msg's that shout be write to file_output no to screen_output 
    '''
def xxxprint(out_case=1,cat=['-','-','-'], msg=['-','-','-'],vals={},vals2={},args=[],err='',inspect_n=1,trace_n=1,_slice=False,launch=False,reset=False,session_report=False):
    '''
    WIP:
    
    input:
    ------
        out_case:int = 1,2,3
            مشخص کردن خروجی اطلاعات : اصلاعات به کدام خروجی ها فرستاده شود
            1:out to report file
            2:out to screen
            3:out to report_file(all data) + Screen
        cat:list len=(3) :3 itme list for ctaegory =>['cat1','cat2','cat3']
            cat1:str =category base =(level 1)
            cat2:str =sub category  =(level 2)
            cat3:str =sub sub category  =(level 3)
        msg:list len=(3) :3 itme list for messegegs =>['msg1','msg2','msg3']  
            msg1:str =short message = subject of happend
            msg2:str =medium message = why happend
            msg3:str =long  message = detail of var and ....
        (additional msg's that shout be write to file_output no to screen_output 
    '''
    vals=vals.copy()#km: for unchange input data
    vals2=vals2.copy()#km: for unchange input data
    if reset:xxprint_reset_html()
    def xxd(n):
        return(f'''</div><div class="bg-primary w-100 text-light border" onclick="$('#{n}').toggle();">{n}</div><div id="{n}" class"contents">''')
        
    def htm_file(file_path):
        return  '<a href={0}>{0}</a>'.format(file_path)
    #-----------------
    def htm_list(args):
        if type(args)==list:
            tt=''
            for i,y in enumerate(args):
                if type(y)==dict:
                    x=htm_dict(y)
                elif type(y)==list:
                    x=htm_list(y)
                else:
                    x=str(y)
                tt+='<div class="row border"><div class="col-1 bg-info">{}:</div><div  class="col-11">{}</div></div>'.format(i,_er_chk(x))
            return tt
        return ""
    #-----------------
    def htm_dict(vals):
        tt=''
        if vals and type(vals)==dict:
            for x in vals:
                y=vals[x] 
                if type(y)==dict:
                    y=htm_dict(y)
                elif type(y)==list:
                    y=htm_list(y)
                else:
                    y=str(y)
                try:
                    if 'file' in x:
                        y=htm_file(y)
                except:
                    pass
                tt+='<div class="row border"><div class="col-2 bg-info">{}:</div><div  class="col-10">{}</div></div>'.format(x,_er_chk(y))
        return tt
    #-----------------
 
    
    #---
    def html_out(func,cat,msg,err):
    	# 020905
        #t=('''
        t="<div class='container-fluid'>\n <div class='row border '>\n"
        t+=_htm_b('col-1 trace',func["xtrace_v"],func["xtrace_title"])
        t+=_htm_b('col-1 x_case',cat[0],func['all'])
        t+=_htm_b('col-1 time',xtime[-8:],xtime)
        t+=_htm_b('col-1 func_file',func['file']+" : "+str(func['line']))
        #t+=_htm_b('col-1 func_line',)
        t+=_htm_b('col-1 func_name',func['name'])
        t+=_htm_b('col-1 msg1',msg[0])
        t+=_htm_b('col-5 msg2',msg[1])#,_prop=""" onclick='$(this).siblings(\":last\").text($(this).text())' """)
        t+="        <div class='col-1 buttom'>##2</div>\n"
        t+="    </div>\n"
        #t+=_htm_b('row msg32',msg[1],'',""" onclick='$(this).siblings(":last").text($(this).text())' """)
        t+=_htm_b('row msg3',msg[2],'')#,""" onclick='$(this).siblings(":last").text($(this).text())' """) # >##1</div>\n"
        t+="    <div class='row border '>\n"  
        t+=_htm_b('col vals',msg[3],'') # ></div>\n"
        t+="    </div>\n" 
        t+="    <div class='row border '>\n"  
        t+=_htm_b('col args',msg[4],'') # ></div>\n"
        t+="    </div>\n"         
        if err:
            ee={}
            for x in dir(err):
                try:
                    ee[x]=eval('err.'+x)
                except:
                    ee[x]="!!! error read err obj "
            t+="    <div class='row border '>\n" 
            t+=_htm_b('col err',htm_list([ee]),'') # ></div>\n"
            t+="    </div>\n"
        t+="</div>\n" 
        t=t.replace('##1',msg[3])#t_add_msgs)
        b1='<button class="btnx1" onclick="$(this).parent().parent().next().toggle();">msg2</button>\n' if msg[2] else ''
        b2='<button class="btnx1" onclick="$(this).parent().parent().next().next().toggle();">vals</button>\n' if msg[3] else ''
        b3='<button class="btnx1" onclick="$(this).parent().parent().next().next().next().toggle();">args</button>\n' if msg[4] else ''
        b4='<button class="btnx1" onclick="$(this).parent().parent().next().next().next().next().toggle();">err</button>\n' if err else ''
        t=t.replace('##2',b1+b2+b3+b4)
        return t
    #----------------------------------------------------------------------------
    import k_date
    xtime=k_date.ir_date('yy/mm/dd-hh:gg:ss')
    cat[0]=cat[0] or "-"
    func=_func_inf(inspect_n,trace_n)


    msg+=['','','','']#msg[3]
    vals.update(vals2)
    msg[3]=htm_dict(vals)
    msg[4]=htm_list(args)
    

    if out_case in [1,3]:
        ttt=html_out(func,cat,msg,err)  
        if _slice:
            ttt=xxd(msg[0])+ttt
            print ('\n'+' = '*5+msg[0]+' = '*5, end='')
        print ('.',end='')
        with open(report_html['fullname'],'a',encoding='UTF8') as file:
            file.write(ttt)
    if out_case in [2,3]:
        x_case=cat[0]
        xc=str(x_case) if x_case else ''
        print('\n'+xtime[-8:]+xc+f'-{func["inf_mini"]} >>> {x_case} : {msg[0]},{msg[1]}')#,end=''
        #if msg[1]:print(f'msg2={msg[1]}')
    
    if session_report:

        from gluon import current
        if not 'reports' in current.session:current.session['reports']={}
        
        rep=current.session['reports']
        if not msg[0] in rep:rep[msg[0]]={}
        rep0=rep[msg[0]]
        if not func["inf_mini"] in rep0:rep0[func["inf_mini"]]={}
        if not msg[1] in rep0[func["inf_mini"]]:rep0[func["inf_mini"]][msg[1]]=0
        rep0[func["inf_mini"]][msg[1]]+=1


        pass
    if cat[0]=='err' or msg[0]=='err':
        import k_ui 
        #k_ui.var_report(
        print("\nerr > "+" | ".join ([str(x) for x in [xtime[-8:],func["xtrace_title"],out_case,msg[0],msg[1],msg[2]]]))
        return False
    if launch:
        import k_file
        k_file.launch_file(report_html['fullname'])  
        
    return True 
def _er_chk(x):
    #import sys 
    #sys.path.insert(0, r"D:\ks\I\web2py")
    try:
        import gluon as html #_html
        h1=html.XML(x)
        return str(h1)
    except Exception as err:
        #x=str(x)
        #for t in ['"',"'"]:
        #    x=x.replace(t,"|")
        print("er_chek err"+ str(err))
        return x
def _htm_b(_class,_txt,_title='',_prop=''):
        #if len(str(_txt))>20 :_title,_txt=_txt ,str(_txt)[:20]    
        _txt=f"<a title='{_er_chk(_title)}'>{_er_chk(_txt)}</a>" if _title else _er_chk(_txt)
        return f"        <div class='{_class} border' {_prop}>{_txt}</div>\n"    
def xxprint_reset_html(last_file_add=''):
    import k_date
    import k_file
    k_file.file_move(report_html['fullname'],r'c:\temp\report\report_inf_{}{}.htm'.format(k_date.ir_date('yymmdd-hhggss'),last_file_add))
    with open(report_html['fullname'],'w',encoding='UTF8') as file:
        file.write('''
        <html><head>
            <link rel="stylesheet" href="need/do_report.css">
            <script src="need/jquery-3.7.1.min.js"></script>
            
            <link rel="stylesheet" href="need/bootstrap4/css/bootstrap.min.css">
            <script src="need/bootstrap4/js/bootstrap.min.js" ></script>
            <script>
            $(document).ready(function(){
                $(".contents").hide();
                $(".btnx1").click();
                $(".func_name").on( "click", function() {
                    $(".func_name").removeClass("bg-primary")
                    $('.func_name:contains("$(this).text()")').addClass("bg-primary")
                    alert( $(this).text() );
                    } );
              
            });
            </script>
        </head>
        <body>
            <div class="head"> 
                <button onclick="$('.msg3').toggle();">msg 3</button>
                <button onclick="$('.vals').toggle();">vals</button>
                <button onclick="$('.args').toggle();">args</button>
            </div><hr>
            <div class='container-fluid'>
        ''')
    return 'xxprint_reset_html done successfully'

#---- test:
#print (1)
def xreport_var(x_var_list,reset=False):
    import k_date
    import k_file,k_htm
    br="<br>" #"\n"
    hr="<HR>"
    ttt=k_date.ir_date('yy/mm/dd-hh:gg:ss')+br
    lunch=True
    nl="\n"
    for i,x_var in enumerate(x_var_list):
        ttt+="="*3+f" {i} "+"-"*50+br+nl
        
        if not x_var:
            ttt+='----- emplty value'+"-"*20+br+nl
            ttt+=f"val = {x_var}"+br+nl
        elif type(x_var)== dict:
            ttt+=f'---- dict:len={len(x_var)}'+"-"*20+br+nl
            ttt+=br.join([f"{x} : { x_var[x]}" for x in x_var]+[''])+nl
            ttt+="++++"+br+nl
            ttt+=val_report(x_var)
        elif type(x_var)== list:
            ttt+=f'---- list:len={len(x_var)}'+"-"*20+br+nl
            ttt+=br.join([f"{x}" for x in x_var]+[''])+nl
            ttt+="++++"+br+nl
            ttt+=val_report(x_var)
        else:
            ttt+='---- else type'+"-"*20+br+nl
            ttt+=br+f"{x_var}"+nl
    func =_func_inf(inspect_n=1,trace_n=1)
    ttt+=k_htm.x_toggle(br.join([x+":"+str(func[x])+nl for x in ["name","line","xtrace_title","xtrace_v","inf"]]))
    ttt+=k_htm.x_toggle("all:<br>"+br.join([x+nl for x in func["all"].split('\n')]))

    # ('w' if reset else 'a')
    fname='c:\\temp\\report\\var_report-'+k_date.ir_date('yymmdd-hhggss')+'.htm'
    import os.path
    if not os.path.isfile(fname):
        ttt="""
            <html><head>
                <link rel="stylesheet" href="need/do_report.css">
                <script src="need/jquery-3.7.1.min.js"></script>
                
                <link rel="stylesheet" href="need/bootstrap4/css/bootstrap.min.css">
                <script src="need/bootstrap4/js/bootstrap.min.js" ></script>
            </head>
            <body>
            """+ttt
    with open(fname,'a' ,encoding='UTF8') as file:
        file.write(k_htm.x_toggle(ttt))
    if lunch:
        k_file.launch_file(fname)
    print("------------")
    return True
#------------------------------------
def val_report(xv):
    import k_htm
    tt=''
    if type(xv)==dict:
        for x in xv:
            y=xv[x] 
            #if 'file' in x:y=htm_file(y)
            tt+='<div class="row border"><div class="col-2 bg-info">{}:</div><div  class="col-10">{}</div></div>'.format(x,val_report(y))
        return k_htm.x_toggle(tt)
    elif type(xv)==list:
        for i,y in enumerate(xv):
            tt+='<div class="row border"><div class="col-2 bg-info">{}:</div><div  class="col-10">{}</div></div>'.format(i,val_report(y))
        return k_htm.x_toggle(tt)
    else: 
        tt+="type="+type(xv).__name__+"<br>"+str(xv)
    return tt
#-------------------------------------    

