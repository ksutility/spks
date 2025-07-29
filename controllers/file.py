# -*- coding: utf-8 -*-
'''
امکانات:
    اصلاح نام فایل ورودی
        تبدیل فارسی به فینگلیش
        تبدیل کاراکترها به خط فاصله
    نشان دادن تاریخ فارسی برای فایلها
    نشان دادن  میزان قدیمی بودن فایل به دقیقه
'''

import os,time
from jdatetime import datetime
import k_file,k_file_w2p
from k_file_meta import K_FILE_META 
k_file_meta=K_FILE_META()
import k_finglish
import k_err,k_user,k_htm
k_user.how_is_connect('file')
from k_file_w2p import FILES_X_TOOLS1
import k_set #share_value as share
xpath=k_set.xpath()
from k_set import C_SET
share_inf=C_SET().share_inf

def _access_denied_msg():
    link=URL('user','login')
    r0='''
        <h2> وارد سیستم شوید تا حق دسترسی شما بررسی شود</h2>
        <BR><a href='javascript:void(0)' onclick="j_box_show('{}',true)"><h3> ورود به سیستم </h3></a>
    '''.format(link) if not session['username'] else ''
    r1='''
        <div align="center">
        <h1>شما اجازه دسترسی به این صفحه را ندارید</h1>
        {}
        </div>
    '''.format(r0)
    return dict(x=XML(r1))
def _login_check():
    if not session["username"]: 
        return _access_denied_msg()    #redirect(URL('_access_denied_msg'))
def _ftime(x):
    return datetime.utcfromtimestamp(x).strftime("%Y/%m/%d - %H:%M:%S")#%a, %b
def _dif_time(x):
    import time
    now = time.time()
    d = now-x 
    mm = int(d / 60) #minutes
    h,g=divmod(mm,60)#g=dgige
    d,h=divmod(h,24)
    m,d=divmod(d,30)
    y,m=divmod(m,12)
    st=f'{d:03d}D,{h:02d}H'
    isi=f'Y-{y:02d}' if y else f'M-{m:02d}' if m  else f'D-{d:02d}' if d else 'D-00'#isi=asan
    isi_min=''
    if isi=='D-00':isi_min=f'{h: 2d} H' if h else f'{m: 2d} M' 
    return {'m':mm,'st':st,'isi':isi}
def _list_files(path,full_name=False):
    #path=file full_path(path/name.ext) 
    showall =True if request.vars.showall else False
    files,folders=[],[]
    if not os.path.exists(path):
        return files,folders
    for item in os.listdir(path):
        if not showall and item[:2]=='__':continue
        pp=os.path.join(path, item)
        if os.path.isfile(pp):
            #if not os.path.getsize(pp):break:#omit zero size file
            if full_name:
                files+= [pp]
            else:
                ff=k_file.file_name_split(item)
                file_sz=k_file.size_easy(os.path.getsize(pp))
                file_mt=os.path.getmtime(pp)
                files+= [{  'name':ff['name'],'size':file_sz,'size_min':XML(A(file_sz[0],_title=file_sz[2:])),
                            'fname':k_finglish.fin_to_fa(ff['name']),'ext':ff['ext'],'filename':ff['filename'],
                            'mtime':_ftime(file_mt),'mtime_min':XML(A(_dif_time(file_mt)['isi'],_title=_ftime(file_mt))),
                            'ctime':_ftime(os.path.getctime(pp)),
                            'm_dif_time':_dif_time(file_mt)
                        }]
        else:
            folders+=[{'name':item,'fname':k_finglish.fin_to_fa(item)}]
    return files,folders

#-----------------------------------------------------------------      
def upload_file():
    # این تابع فایل را دریافت و ذخیره می‌کند
    fwa=k_file_w2p.folder_w_access()
    if not fwa['ok']:return fwa['msg']
    if 'file' in request.vars:
        import os
        # دریافت اطلاعات فایل
        filename_base = request.vars.file.filename
        filename_goal =request.vars.filename
        fn_obj =k_file.file_name_split(filename_base)#.replace(" ", "")
        xdata={    
            'user_filename':k_file.name_correct(fn_obj['name']),
            'un':session["username"]}
        filefullname=filename_goal.format(**xdata) or xdata['user_filename']
        filefullname+=fn_obj['ext']
    
        #input_file_name= file.filename
        #ou=str(file.file.read())
        
        #ou+=str(file.filename)
        #ou+='<br>'+ str(file_b)
        res={}
        if filefullname:
            
            session['uploaded_name']=filefullname
            path1=xpath+'\\'.join(request.args) #join((*request.args,filefullname))
            # تنظیم مسیر ذخیره‌سازی
            filepath=path1+'\\'+filefullname
            session['uploaded_path']=filepath
            session['uploaded_time']=time.time() #now
            response.flash=T("File Upload started!")
            if not os.path.exists(path1):k_file.dir_make(path1)
            msgs=[k_file.file_delete_rcl(filepath,recycle_sub_folder=request.args[0])]  
            

            
            #file_b=file.file.read() #file contents in byte format
            #with open(filepath, 'wb') as f:f.write(file_b)
            
            # ذخیره فایل با امکان ردیابی پیشرفت
            with open(filepath, 'wb') as f:
                while True:
                    chunk = request.vars.file.file.read(65536)  # 64KB chunks
                    if not chunk:
                        break
                    f.write(chunk)    
                
            
            msgs+=['File Upload Succesfully',f'filename={filepath}',f'args={request.args}','uploaded_time = '+ str(time.time()-session['uploaded_time']),'-'*25]
            
            if request.vars.todo :
                msgs+=_update_todo(request.vars.todo,filefullname)
           
            msg='<br>'.join(msgs) #"<h2>فایل با موفقیت آپلود شد</h2><hr>"+
            res={'status': 'success', 'filename': filepath,'msg':msg}
        else:
            msg=f'File Not Found <br> filename={path}'
            res={'status': 'error','msg':msg}
    else:
        res={'status': 'error','msg':'file not set'}
    return response.json(res) #return msg
        

def _update_todo(todo,filefullname):
    '''
        todo=request.vars.todo
        filefullname:str    
            input file full name (name +ext)
    '''
    import json
    msgs=[]
    todo=todo.replace("$filefullname$",filefullname)
    todo= json.loads(todo)
    if todo['do']=='sql':                 
        from k_sql import DB1
        db1=DB1(todo['db'])
        xu=db1.update_data(table_name=todo['tb'],set_dic=todo['set_dic'],x_where=todo['where']) #tb_name=sq[1]
        msgs+=['update db is done =>'+ str(xu)]
    return msgs
def mdir():
    args=request.args
    if args:
        path=xpath+'\\'.join(args)
        
        return str(k_file.dir_make(path))
def upload():
    """ 010825
        input by request.vars
            filepicker (auto by <input tyep='file' id,name='filepicker'>
            file_ext
            filename
            todo    = action that do after file upload
                sql;<db_name;<table_name>;<id>;<field_name>
    """
    fwa=k_file_w2p.folder_w_access()
    if not fwa['ok']:return fwa['msg']
    
    args=request.args
    file_ext=request.vars.file_ext #"jpg,gif" #"gif,jpg,jpeg,png,doc,docx"
    #if type(file_ext)!=list:file_ext=[]
    file_ext_list=file_ext.split(",")
    file_ext_tit=','.join([f' {x} ' for x in file_ext_list])
    file_ext_li=','.join([f'"{x}"' for x in file_ext_list])
    file_ext_dot=','.join([f'.{x}' for x in file_ext_list])  #".gif,.jpg,.jpeg,.png,.doc,.docx"
    link=XML(URL(f='upload_file',args=args,vars=request.vars))#upload_file # action='j_box_show("{}");'
    return dict( link=link,
                args=str(args)+"<br>"+str(request.vars),
                file_ext_tit=file_ext_tit,
                file_ext_list=XML(file_ext_li),
                file_ext_dot=file_ext_dot )
def download():#ownload
    #return response.download(request,db,download_filename=xpath+'per.xlsx')
    args=request.args
    xpath=k_set.xpath(args[-1]) # check for access to files with "share_for_all"
    if args:
        path=xpath+'\\'.join(args)
        if not os.path.exists(path):
            return DIV(H2('فایل مورد نظر وجود ندارد'),DIV(path))
        #fn=args[0] if len(args)>0 else 'per.xlsx'
        #path=xpath+fn
        return response.stream(open(path,'rb'),chunk_size=4096)
def serve_external_image():
    import os
    from gluon.contenttype import contenttype
    args=request.args
    xpath=k_set.xpath(args[-1]) # check for access to files with "share_for_all"
    if args:
        full_path=os.path.join(xpath, *args) #xpath+'\\'.join(args)
        if not os.path.exists(full_path): #if not os.path.isfile(full_path)
            #return DIV('path not exist'+full_path)
            raise HTTP(404, "File not found : "+full_path)
        response.headers['Content-Type'] = contenttype(full_path)
        return response.stream(full_path)
def unzip():
    args=request.args
    if args:
        path=xpath+'\\'.join(args)
        ok=k_file.zip_extract(path)
        if ok: return (f'<br> unzip done successfully <br> {path} <hr>')
    return (f'Error in unzip\n{path}')
def unzip7():
    '''
        unzip 1 selected *.zip file with external_cmd to 7zip
    '''
    args=request.args
    if args:
        path=xpath+'\\'.join(args)
        re1=k_file.zip7_extract(path,'e')
        if re1['ok']: return (f'<br> unzip_7 done successfully <br> {path} <hr> inf= {re1["inf"]}')
    return (f'Error in unzip_7 <br> {path} <hr> inf= {re1["inf"]}')   
def doc2md():
    '''
        convert 1 selected *.docx file to *.md file with external_cmd
    '''
    args=request.args
    if args:
        path=xpath+'\\'.join(args)
        re1=k_file.doc2md(path)
        if re1['ok']: 
            bak_file=k_file.backup(path,"*,bak",delete=True)
            return (f'<br> doc_2_md done successfully <br> {path} <hr> inf= {re1["inf"]}<hr>File move to => {str(bak_file)}')
        return (f'<br> doc_2_md : args = true ==> but <br> {path} <hr> inf= {re1["inf"]}<hr>args={args}') 
    return (f'Error in doc_2_md <br> path={path} <hr> inf= {re1["inf"]}<hr>args={args}')        
def zip():
    args=request.args
    if args:
        folder=xpath+'\\'.join(args)
        r_file=folder+'.zip' #xpath+'\\'.join(args[:-1]+[''])
        msg=k_file.zip_folder_to(folder,r_file)
        return (msg)        
def delete():
    fwa=k_file_w2p.folder_w_access(args=request.args[:-1])
    if not fwa['ok']:return fwa['msg']
    args=request.args
    def _delete(args):
        from k_set import C_SET
        xp=os.path.join(xpath,*args)
        k_file.file_delete_rcl(xp,recycle_sub_folder=args[0])
        msgs=['Delete  Done Successfully','move to recycle:',f'===>   {C_SET().recycle})','fome:',f'<=== {xp}']
        if request.vars.todo :
            msgs+=_update_todo(request.vars.todo,'')
        return "<br><h2>فایل /  فلدر با موفقیت پاک شد</h2><hr>"+'<br>'.join(msgs)
    if args:
        if args[0]=='del':
            args=args[1:]
            return (_delete(args))
        else:
            ok_do=request.vars['ok_do']
            if ok_do=='y' :
                return (_delete(args))
            else:    
                xp=os.path.join(xpath,*args)    
                ok_do_htm=INPUT(_name='ok_do',_id='ok_do',_value=ok_do ,_style="width:90%")
                b_s=INPUT(_type='submit',_value='حذف فایل')
                return XML(f'''
                    <form action="" method="post">
                    <div class="container" dir="rtl">
                        <div class="row">
                            <div class="col-2">شما در حال حذف یک فایل یا فلدر هستید</div>
                            <div class="col-8">{xp}</div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-2">در صورت اطمینان عبارت y را تایپ کنید</div>
                            <div class="col-8">{ok_do_htm}</div>
                        </div>
                        <div class="well">{b_s}</div>
                    </div></form>''')
    return 'error : args is empty'
def move():
    '''
        move 1 file frome path1 to path2 &
            move its metadata form __inf
    exam:
        http://127.0.0.1/spks/file/move?path1=c:\temp&path2=d:\ks\0-file\lib\0-Refrence\1-mogararat-meli&f_name=mabhas-13-1395.pdf
    INPUTS:
    ------
        path1=vals['path2'] or args[:-1]
        path2=vals['path2']
        f_name=vals['f_name'] or args[-1]
    '''
    re0,re1="",""
    fwa=k_file_w2p.folder_w_access(args=request.args[:-1])
    if not fwa['ok']:return fwa['msg']
    path1=request.vars['path1']
    f_name=request.vars['f_name']
    if not path1:
        args=request.args
        if args:
            path1=os.path.join(xpath,*args[:-1])
        f_name=args[-1]
    if path1:        
        path2=request.vars['path2']
        if path2:
            '''
                path2 format='<s><n>*<text>'
                   <s> = ['+','-']  : 1X
                   <n> = [0..9]     : 1X
            '''
            if len(path2)>2 and path2[2]=='*' and path2[0] in '-+' and path2[1] in '0123456789':
                x_root=k_file.root_split(path1)  
                path2=x_root[int(path2[0:2])]+path2[3:]
            #path2={{=root[+1]}}\b&
            #import k_str
            #path2=k_str.template_parser(path2,x_dic={'root':x_root})#path2.format(root=x_root)
            re0=_move_1_file(path1,path2,f_name)
            if re0['ok']:
                return re0['report']
    #return f'error in file.move() : <br> path1 ={path1}<br>path2={path2}<br>f_name={f_name}<hr>{str(re0)}<hr>{re1}'
    
    
    p1=INPUT(_name='path1',_id='path1',_value=path1 ,_style="width:90%")
    p2=INPUT(_name='path2',_id='path2',_value=request.vars['path2'] ,_style="width:90%")
    b_s=INPUT(_type='submit')
    return XML(f'''
    <form action="" method="post">
    <div class="container">
        <div class="row">
            <div class="col-2">path1=</div>
            <div class="col-8">{p1}</div>
        </div>
        <div class="row">
            <div class="col-2">path2=</div>
            <div class="col-8">{p2}</div>
        </div>
        <div class="well">{b_s}</div>
    </div></form>''')
def _move_1_file(path1,path2,f_name):
    re0=k_file.file_move((path1,f_name),(path2,f_name))
    if re0['ok']:
        re1=k_file_meta.move(path1,path2,f_name)
        re0['report']=(f"""<br><h2>گزارش اقدامات انجام شده</h2>
                    <br> MOVE:<br>{"-"*5} path1={path1}<br>{"-"*5} path2={path2}<br>{"-"*5}f_name={f_name})
                    <br> MOVE  Done - Report = {str(re0)}<br>{re1}""")
    else:
        re0['report']=(f"""<br><h2>Error in</h2> 
                    <br> MOVE:<br>{"-"*5} path1={path1}<br>{"-"*5} path2={path2}<br>{"-"*5}f_name={f_name})
                    """)
    return re0
def move_x():
    '''
        cut 1 file for move it from past_location
            + move its metadata form __inf
    exam:
        use by pro 
        external use is not ok
    INPUTS:
    ------
        request.args:
            [0]='cut' / 'copy'
            [...] =path
            [-1]= filename (by .ext)
    '''
    re0,re1="",""
    fwa=k_file_w2p.folder_w_access(args=request.args[:-1])
    if not fwa['ok']:return fwa['msg']
    if not session['move_files']:
        session['move_files']=[]
    if not request.args in session['move_files']:
        session['move_files']+=[request.args]
    return (DIV(*[DIV(str(x)) for x in session['move_files']]))
def move_p(): 
    '''
        past 1 file (move it from cut_location)
            + move its metadata form __inf
    exam:
        use by pro 
        external use is not ok
    INPUTS:
    ------
        request.args:
            [0]='cut' / 'copy'
            [...] =path
            [-1]= filename (by .ext)
    '''
    rep=''
    path2=''
    if session['move_files']:
        path2=os.path.join(xpath,*request.args)
        for x_args in session['move_files']:
            path1= os.path.join(xpath,*x_args[1:-1])
            f_name=x_args[-1]
            if path1!=path2:
                rep+=_move_1_file(path1,path2,f_name)['report']
            else:
                rep+=f"""مبدا و مقصد با هم یکسان هستند : 
                    {path1},{f_name}"""
    rep1=DIV("path2="+path2,HR(),DIV(*[DIV(str(x)) for x in session['move_files']],HR(),XML(rep)))
    session['move_files']=[]
    return (rep1)
def new_file(): 
    if request.vars['file_name'] :
        f_name=request.vars['file_name']
        path=os.path.join(xpath,*request.args+[f_name])
        return k_file.new_file(path)
    else:
        p1=INPUT(_name='file_name',_id='file_name',_value=request.vars['file_name'] ,_style="width:90%")
        b_s=INPUT(_type='submit')
        return XML(f'''
        <form action="" method="post">
        <div class="container">
            <div class="row">
                <div class="col-6">filename</div>
                <div class="col-6">{p1}</div>
            </div>
            <div class="well">{b_s}</div>
        </div></form>''')
def file_tools(): 
    files_x_tools=FILES_X_TOOLS1()
    return DIV(
        DIV("args="+str(files_x_tools.args)),
        DIV(files_x_tools.link_comp()),
        DIV(files_x_tools.link_move()),
        HR(),
        DIV(files_x_tools.link_rename()),
        HR(),
        DIV(files_x_tools.link_rename_title2(f_title="rename {} =>")), #'files',x_file['filename'],x_file['title'])),
        HR(),
        DIV(files_x_tools.link_delete()),
        )
def folder_tools(): 
    files_x_tools=FILES_X_TOOLS1()
    return DIV(
        DIV("args="+str(files_x_tools.args)),
        DIV(files_x_tools.link_move()),
        HR(),
        DIV(files_x_tools.link_rename()),
        HR(),
        DIV(files_x_tools.link_ren2()),
        HR(),  
        DIV(files_x_tools.link_rename_title2(f_title="rename {} =>")), #'files',x_file['filename'],x_file['title'])),
        HR(),
        DIV(files_x_tools.link_delete()),
        )        
def name_correct():
    args=request.args
    if args:
        xp=os.path.join(xpath,*args[:-1])
        n1=args[-1]
        n2=k_file.name_correct(n1)
        re1=k_file.file_move((xp,n1),(xp,n2))
        return '{3} : {0}\\{1}<br>    {0}\\{2}<br>'.format(xp,n1,n2,str(re1)) 
def correct_files_name_in_folder():
    args=request.args
    if args:
        xp=os.path.join(xpath,*args)
        re1=k_file.correct_files_name_in_folder(xp)
        return XML('<hr>'.join(['-'*20 + x +'<br>'.join(['']+re1[x]) for x in re1]))
def manage():
    args=request.args
    path=os.path.join(xpath,*args)
    files,folders=_list_files(path)
    
    return dict(a=A('upload new file',_href=URL(f='upload',args=args,vars=request.vars)),
    files=TABLE(*[TR(A(x['name'],_href=URL(f='download',args=args+[x['name']])),x['size'],x['mtime'],x['ctime']) for x in files],_class='table2'),
    folders=TABLE(*[A(x,_href=URL(args=args+[x])) for x in folders],_class='table2'))

def f_list_sd():    #sd=sade
    return f_list()
def f_list_set():
    path=request.vars['path']
    return path
def f_list():#file_browser=file.index
    files_x_tools=FILES_X_TOOLS1()
    r1=False #_login_check()
    if r1:return dict(address='',m_dir='',upload='',path='',a='',files=XML(r1),folders='',js='')
    '''
    use:
    ----------
        url?del=1
    '''
    import re
    r_vars=request.vars
 
    x_path,path,fc_access,args=files_x_tools.set_out_val()
    #print(f"x_path={x_path},args={request.args}")
    #xxxprint('curren user file_change_access='+ str(fc_access)+ '  | on floder ='+x_path)
    #xprint(f'f_list : file_access -{fc_access}-{session["file_access"]}-{x_path}')
    args=request.args
    #add_folder_access
    def add_my_folder(x_path):
        def afa():
            
            '''
                بررسی اینکه آیا در فلدر جاری می تواند برای شخص جاری فلدر بسازد یا خیر
            '''
            x_match=r";prj;prj;\w*;\w*;\B"
            if re.findall(x_match,x_path):
                path=xpath+'\\'.join(args+[str(session["my_folder"])])
                if not os.path.exists(path):
                    return True
        #------------------------------------        
        #   re1 = True if session["admin"] or (re.findall(x_match,x_path)) else False
        #    print(f'f_list : add-folder -{re1}-{x_match}-{x_path}')
        #    return re1
        if afa():
            link1=XML(URL(f='mdir',args=args+[session["my_folder"]],vars=r_vars))
            return XML('''<a  href = 'javascript:void(0)' onclick='j_box_show("{}",true);' title='{} ساخت پوشه تحت مدیریت من با نام :'   > + MY Folder </a>'''.format(link1,session["my_folder"]))
        return ''
    #--------------------------------------------    
    
    files,folders=_list_files(path)
    meta=k_file_meta.read(path,files,folders)
    #print(f'path={path} ,fiels len={len(files)}')
    def x_ext(x_file):
        x_file['ext']=x_file['ext'].lower()
        if x_file['ext']=='.zip':
            return DIV(A('+zip',_title='unzip in this folder',_href=URL(f='unzip',args=args+[x_file['filename']],vars=r_vars),_target="x_frame")
                ,A('+7z',_title='unzip7 in this folder',_href=URL(f='unzip7',args=args+[x_file['filename']],vars=r_vars),_target="x_frame")) if fc_access else ''
        elif x_file['ext'] in ['.docx','.doc']:
            return DIV(A('+md',_title='doc=>md in this folder',_href=URL(f='doc2md',args=args+[x_file['filename']],vars=r_vars),_target="x_frame")) if fc_access else ''
        
        else:
            return x_file['ext']
            #f=k_file.file_name_split(fname)
            
            #return link_unzip(x_file['filename'])
    def link_doc2md(fname):#c:\temp
        f=k_file.file_name_split(fname)
        
    def link_unzip(fname):
        pass

    def link_view(x_file,link_txt,link_title='View'):
        xd={'json':'json_read','csv':'read_csv','md':'read_xx','mm':'read_xx','ksm':'read_xx','ksml':'read_xx','ipt2win':'read_ipt2win',
            'mermaid':'read_xx','mermaid2':'read_mermaid'}
            #'xls':'read_xl','xlsx':'read_xl','xlsm':'read_xl'}
        ext=x_file['ext'][1:]
        link_txt=link_txt[:100] if len(link_txt)>100 else link_txt
        if ext in xd:
            return A(link_txt,_href=URL('xfile',xd[ext],args=args+[x_file['filename']],vars=r_vars),_target="x_frame",_title=link_title)
        return link_download(x_file,link_txt,link_title)    
    def link_file_tools(x_file,link_title,vars):    
        vars.update(r_vars)
        #args=args+[x_file['filename']]
        return  A(link_title,_href='javascript:void(0)',_onclick=f"""j_box_show("{URL('file_tools',args=args,vars=vars)}",true)""",_target="x_frame",_title='tools'
            ) if fc_access else link_title     
    def link_folder_tools(x_dir,link_txt,link_title='Tools'):        
        return  A(link_txt,_href='javascript:void(0)',_onclick=f"""j_box_show("{URL('folder_tools',args=args+[x_dir['name']],vars=r_vars)}",true)""",_target="x_frame",_title=link_title
            ) if fc_access else ''      
    def link_edit(x_file,link_txt,link_title='Edit'):  
        ext=x_file['ext'][1:]
        if ext in ['md','mm','json','csv','txt','ksm','ksml','mermaid','mermaid2']:#files that can edit by edit_r page
            return A(link_txt,_href=URL('xfile','edit_r',args=args+[x_file['filename']],vars=r_vars),_target="x_frame",_title=link_title)
        return ''   
    def link_download(x_file,link_txt,link_title='download'):
        return A(link_txt,_href=URL(f='download',args=args+[x_file['filename']],vars=r_vars),_target="x_frame",_title=link_title)
    #def list(path):
    copyclip_func='''<script>
                          function copyToClipboard(copyText) {
                             navigator.clipboard.writeText(copyText).then(() => {
                                // Alert the user that the action took place.
                                alert("Copied to clipboard");
                            });
                          }
                        </script> '''   
    copyclip_func=''
    '''<script>var $temp = $("<input>");
            $("body").append($temp);
            $temp.val($(element).text()).select();
            document.execCommand("copy");
            $temp.remove();
            </script>'''                        
    xp=XML(path.replace(',','\\'))
    #onchange="window.location.replace('{URL('f_list_set')}')"
    list_view_mod=XML(SELECT('1','2',_id='list_view_mod',_name='list_view_mod', value=r_vars['list_view_mod']))
    x_setting=f'''
    <div class="row">
        <div class="col-2"> نحوه نمایش لیست </div>
		<div class="col-2">{list_view_mod}</div>
        <div class="col-6">-</div>
        <div class="col-2"><input type="submit" /></div>
    </div>
    '''
    x_cmd_address=f'''
    <div class="row">
        <div class="col-10"><input id="input_adr" name="input_adr" type="text" value="{xp}" style="width:100%" onchange="this.form.submit()" /></div>
        <div class="col-2"><button id="copy">Copy</button></div>
    </div>
    <script>
        function copy() {{
            var copyText = document.querySelector("#input_adr");
            copyText.select();
            document.execCommand("copy");
        }}
        
        document.querySelector("#copy").addEventListener("click", copy);
    </script>
    '''
    xx1=f'<div onclick="navigator.clipboard.writeText(\'{xp}\');alert(\'ok\')">{xp}</div>'
    def address(name,args,titel=''):
        return DIV(' \\ ',A(name,_href=URL(args=args,vars=r_vars),_style='background-color:#ffddcc;margin:0px 10px 0px 10px;padding:0px 10px 0px 10px'),_style='float:left; ',_title=titel)
    def x_class(ext): 
        '''
           در جدول به ردیف هر نوع از فایلها یک کلاس اختصاص می دهد تا بتوان با سی.اس.اس گرافیک آنرا تنظیم کرد
            تنظیمات گرافیک در فایل زیر می باشد
            ks.css 
        '''
        xx={'folder':['older'],
            'pic':['jpg','png'],
            'pdf':['pdf'],
            'txt':['txt'],
            'zip':['zip'],
            'ml':['md','mm','ksl']
            }
        #  
        for x in xx:
            if ext[1:].lower() in xx[x]:
                t=x
                break
        else:
            t='general'
        return 'file_'+ t
    def add_file():
        return DIV(
            k_htm.a('+upload File',_target="box",_href =URL(f='upload',args=request.args,vars={**r_vars,'filename':'','file_ext':""}),_title='بارگزاری فایل'),
            "-",
            k_htm.a('+past',_target="box",_href =URL(f='move_p',args=request.args,vars={**r_vars})
                ,_title='چسباندن فایل'+"\n"+"\n".join(str(x) for x in session['move_files'])) if session['move_files'] else '' ,
            "-",
            k_htm.a('+new file',_target="box",_href =URL(f='new_file',args=request.args,vars={**r_vars}),_title='فایل جدید'),   
            ) if fc_access else ''
    def files_list(list_view_mod=1):
        
        if list_view_mod==1:
            return TABLE(THEAD(TR(*[TH(x) for x in ['n','Title','Name','E_1','E_2','Size','Date','-','-','-']])),
                        TBODY(  *[TR((i+1),
                                    A(f"<{x_dir['title']}>",_href=URL(args=args+[x_dir['name']],vars=r_vars),_title=x_dir['fname']),
                                    A(f"<{x_dir['name']}>",_href=URL(args=args+[x_dir['name']],vars=r_vars),_title=x_dir['fname']),
                                    '<>',
                                    link_folder_tools(x_dir,'_F'),
                                    files_x_tools.link_rename_title2(vals={'f_name':x_dir['name'],'f_title':x_dir['title'],'case':'folders'}),#'folders',x_dir['name'],x_dir['title']),
                                    #'',#files_x_tools.link_rename(),#x_dir['name']),
                                    '',#files_x_tools.link_ren2(),#x_dir['name']),
                                    '',#files_x_tools.link_delete(),#x_dir['name']),
                                    '',
                                    '',
                                    _class=x_class('folder')
                                    ) for i,x_dir in enumerate(folders)],
                                *[TR((i+1),
                                    link_view(x_file,x_file['title'],link_title=x_file['fname']+'\n'+x_file['ext']),
                                    link_view(x_file,x_file['name'],link_title=x_file['fname']+'\n'+x_file['ext']),
                                    #A(x_file['name'],_href=URL(f='download',args=args+[x_file['filename']],vars=r_vars),_target="x_frame",_title=x_file['fname']+'\n'+x_file['ext']),
                                    x_file['ext'][1:],
                                    DIV(link_download(x_file,'d'),"|",
                                        link_file_tools(x_file,'*',vars={'f_name':x_file['filename'],'f_title':x_file['title'],'case':'files'}),"|",
                                        link_edit(x_file,'e'),"|",
                                        files_x_tools.link_rename_title2(vals={'f_name':x_file['filename'],'f_title':x_file['title'],'case':'files'}),#'files',x_file['filename'],x_file['title']),),
                                        ),
                                    x_file['size'],
                                    x_file['mtime'],
                                    x_ext(x_file),
                                    '',#files_x_tools.link_delete(x_file['filename']),
                                    '',#files_x_tools.link_rename(),#x_file['filename']),
                                    _class=x_class(x_file['ext'])
                                    ) for i,x_file in enumerate(files)],
                             ),
                _class='table_file')
        elif list_view_mod==2: #'simple'
            return TABLE(THEAD(TR(*[TH(x) for x in ['n','عنوان',A('T',_title='نوع فایل + ابزارها'),A('S',_title='حجم فایل بر اساس لگاریتم 10'),A('D',_title='زمام فایل')]])),
                        TBODY(  *[TR((i+1),
                                    A(f"<{x_dir['title'] or x_dir['name']}>",_href=URL(args=args+[x_dir['name']],vars=r_vars),_title=x_dir['fname']),
                                    link_folder_tools(x_dir,'_F'),
                                    files_x_tools.link_rename_title2(vals={'f_name':x_dir['name'],'f_title':x_dir['title'],'case':'folders','tit':'r'},tit='r'),
                                    '',
                                    ) for i,x_dir in enumerate(folders)],
                                *[TR((i+1),
                                    link_view(x_file,x_file['title'] or x_file['name'],
                                            link_title=(x_file['name']+x_file['ext']+'\n'+'\n'.join(f'{xi} : {x_file[xi]}' for xi in ('fname','s_code','s_date','valid_org') if xi in x_file))),
                                    link_file_tools(x_file,x_ext(x_file),vars={'f_name':x_file['filename'],'f_title':x_file['title'],'case':'files'}),                                    
                                    x_file['size_min'],
                                    x_file['mtime_min'],
                                    
                                    ) for i,x_file in enumerate(files)],
                             ),
                _class='table table-hover ')
    #k_file_meta.list_unused_json_item(files,folders,meta)
    return dict(js=XML(copyclip_func),
    m_dir=add_my_folder(x_path),
    upload=add_file(),
    setting=(XML(x_setting)), #(XML(x_setting)  if fc_access else ''),
    cmd_address=(XML(x_cmd_address) if session["admin"] else ''),
    #a=DIV(*[DIV(' \\ ',A(args.get(i),_href=URL(args=args[:(i+1)]),_style='background-color:#ddddff'),_style='float:left') for i in range(-1, len(args))],DIV(' : ')) ,
    address=DIV(address('..',[]),*[address(args[i],args[:i+1],k_finglish.fin_to_fa(args[i])) for i in range(len(args))]," : ") ,
    files=files_list(list_view_mod=1 if r_vars['list_view_mod']=='1' else 2),
    
    folders=TABLE(THEAD(TR(*[TH(x) for x in ['n','Folder Name','-','-']])),
                  TBODY(*[TR((i+1),
                        A(x['name'],_href=URL(args=args+[x['name']],vars=r_vars),_title=x['fname']),
                        files_x_tools.link_rename(),#x['name']),
                        files_x_tools.link_ren2(),#x['name'])
                        ) for i,x in enumerate(folders)]),
        _class='table_file'),
    frame=XML('<iframe id="f_frame" name="f_frame" src="" height="1000" width="1740" title="file previw"></iframe>')
    )
def socket_x():
    from gluon.contrib.websocket_messaging import websocket_send
    websocket_send('http://127.0.0.1:8888', 'Hello World', 'mykey', 'mygroup')
    return 'ok'
"""
index temp    
    $('#wait').ajaxStart(function() {{
                $(#wait).show();
                $(#file_form).hide();
            }}).ajaxComplete(function() {{
                $(#wait).hide();
                $(#file_form).show();
    --------------------------------------
    ajaxStart(function() {{
                $('#wait').show();
                $('#file_form').hide();
            }}).ajaxComplete(function() {{
                $('#wait').hide();
                $('#file_form').show();
            }});
            $('#x_frame').attr("src", "{1}");
                r"http:/10.36.1.200:8000"+
    ------------------------------------
        <div name="wait" id="wait">Please wait</div>
        <script>
            function loadIframe(iframeName, url) {{
                var $iframe = $('#' + iframeName);
                if ( $iframe.length ) {{
                    $iframe.attr('src',url);    // here you can change src
                    return "A";
                }}
                document.getElementById(iframeName).src=url;
               
                //$iframe.attr('src',url)
                return "2";
            }}
            
            $('#wait').hide();
            alert("{1}");
            //alert(loadIframe("x_frame", "{1}"));
            $('#file_form').submit(function( event ) {{
                loadIframe("x_frame", "{1}")
                return;
            }});    
        </script>  
    .format(link,URL(f="wait"))),        
----------------------
    link=XML(URL(f='upload_file',args=['share']))#upload_file    
    upload=XML('''
        <form name="file_form" id="file_form" method="post" enctype="multipart/form-data" action="{0}" target="x_frame">
             <input name="file" type="file" size="60">
             <input type="Submit" value="Upload">
        </form> 
    '''.format(link)),
    
"""    
def index1():
    '''
    share folder
    '''
    args=['share']
    path=xpath+'\\'.join(args)
    files,folders=_list_files(path)
    def myFunc(file):
        return file['mtime']
    files.sort(reverse=True,key=myFunc)
    def link_delete(fname):
        return A('Del',_href=URL(f='delete',args=['share',fname],vars=request.vars),_target="x_frame") #if request.vars['del'] else ''
    link=XML(URL(f='upload_file',args=['share'],vars=request.vars))#upload_file
    #<input name="file" type="file" size="60" maxlength="10000000">

    return dict(
    x_farme=1,
    upload=XML('''
        <form name="file_form" id="file_form" method="post" enctype="multipart/form-data" action="{0}" target="x_frame">
             <input name="file" type="file" size="60">
             <input type="Submit" value="Upload">
        </form> 
    '''.format(link)),
    files=TABLE(THEAD(TR(*[TH(x) for x in ['n','Name','Size','Date','Age','-']])),
                TBODY(*[TR((i+1),
                    A(x['filename'],_href=URL(f='download',args=args+[x['filename']],vars=request.vars),_target="x_frame",_title=x['fname']),
                    x['size'],x['mtime'],x['m_dif_time']['isi'],link_delete(x['filename'])
                        ) for i,x in enumerate(files)]),
                _class='table6'),
    )
  
def index():
    #r1=_login_check()
    '''
        share folder
    '''
    args=request.args or ['share']
    
    fwa=k_file_w2p.folder_w_access(args=args)
    if not fwa['ok']:return fwa['msg']
    
    path='\\'.join(args)
    x_title=share_inf[path]
    path=xpath+path
    files,folders=_list_files(path)
    def myFunc(file):
        return file['mtime']
    files.sort(reverse=True,key=myFunc)
    j_box_txt='''<div ><a  href = 'javascript:void(0)' title='{2}' onclick='j_box_show("{0}",true);'> {1}</a></div>'''
    def link_delete(fname):
        # return A('Del',_href=URL(f='delete',args=['share',fname]),_target="x_frame") #if request.vars['del'] else ''
        return XML(j_box_txt.format(URL(f='delete',args=[*args,fname],vars=request.vars),'X','Delete file')) #A('Del',_href='javascript:void(0)',_onclick=f"""j_box_show("{URL(f='delete',args=['share',fname])}",true)""") #_target="x_frame"
    link1=XML(URL(f='upload',args=args,vars={**request.vars,'filename':'{user_filename}',
        'file_ext':"csv,gif,jpg,jpeg,png,doc,docx,xls,xlsx,pdf,dwg,zip,rar,ppt,pptx,mp4,mkv,mp3,m4a,htm,html"}))
    '''samplemple : 
    link1=XML(URL(f='upload',args=args,vars={**request.vars,'filename':'{un}-{user_filename}','file_ext':"txt,gif,jpg,jpeg,png,doc,docx,xls,xlsx,pdf,dwg,zip,rar,ppt,pptx,md,ksml,ksm,mm"}))
    '''
    #<input name="file" type="file" size="60" maxlength="10000000">
    return dict(
    x_title=x_title,
    x_farme=1,
    upload1=XML(j_box_txt.format(link1,'+ File','Uload File (بارگزاری فایل)')),
    
    files=TABLE(THEAD(TR(*[TH(x) for x in ['n','-','Size','Age','Name','Date',]])),
                TBODY(*[TR((i+1),
                    link_delete(x['filename']),
                    x['size'],x['m_dif_time']['isi'],
                   
                    A(x['filename'],_href=URL(f='download',args=args+[x['filename']],vars=request.vars),_target="x_frame",_title=x['fname']),
                    x['mtime']
                        ) for i,x in enumerate(files)]),
                _class='table0'),
    )    
def file_meta_edit():
    def file_meta_save(f_name,f_title,x_dic={}):
        if f_name:
            x_dic.update({'title':k_finglish.fa_to_fin(f_title)})
            #append_dic={request.vars['case']:{f_name:x_dic}}
            return (k_file_meta.append(path=xpath+'\\'.join(request.args),
                    f_name=f_name,
                    f_case=request.vars['case'],
                    append_dic=x_dic)
                )  
        return 'save not done'
    def file_meta_change(f_name1,fname2):
        x_dic={request.vars['case']:{f_name1:''}}
        return (k_file_meta.change_key(xpath+'\\'.join(request.args),
            old_key_in_dict=x_dic,new_key=fname2))
    def file_meta_read(path,f_name,case):   
        meta=k_file_meta.read(path)
        if meta and case in meta:
            xlist=meta[case]
            if f_name in xlist:
                return xlist[f_name]
        return {}
    #------------------------------URL('file_meta_save',args=args,vars=request.vars)
    k_err.xxprint_reset_html()
    args=request.args
    path=xpath+'\\'.join(args)
    vars=request.vars
    inf_list0=['s_date','s_code','valid_org']#s=sabt ,v_co=validate organization
    inf_list=['title']+inf_list0 
    ou=''
    xdic= file_meta_read(path,vars['f_name'],vars['case'])
    for xx in inf_list:
        if not xx in xdic:
            xdic[xx]=''
    xdic['title']=k_finglish.fin_to_fa(xdic['title'])      
    if vars['f_name2']:
        for xx in inf_list:
            if (vars[xx+'2'] or xdic[xx] ) and xdic[xx] !=vars[xx+'2']:
                ou+=file_meta_save(vars['f_name'],vars['title2'],{xi:vars[xi+'2'] for xi in inf_list0 })
                break
    if vars['f_name2'] and vars['f_name'] !=vars['f_name2']:
        import os
        f1=os.path.join(path, vars['f_name'])
        f2=os.path.join(path, vars['f_name2'])

        os.rename(f1,f2)
        ou+=file_meta_change(vars['f_name'],vars['f_name2'])
    if ou:return ou 
    #else
    f_n =INPUT(_name='f_name2',_id='f_name2',_value=vars['f_name2'] or vars['f_name'] ,_style="width:90%")
    t2=''
    for xx in inf_list:
        t1=INPUT(_name=xx+'2',_id=xx+'2',_value=vars[xx+'2'] or xdic[xx],_style="width:90%")
        t2+=f'''
            <div class="row">
                <div class="col-2">{xx}=</div>
                <div class="col-8">{t1}</div>
            </div>'''
    b_s=INPUT(_type='submit')
    return XML(f'''
    <form action="" method="post">
    <div class="container">
        <div class="row">
            <div class="col-2">name=</div>
            <div class="col-8">{f_n}</div>
        </div>
        {
        t2
        }
        <div class="well">{b_s}</div>
    </div></form>''')

    #FORM(DIV(f_n,f_t),, _action='', _method='post'))

def file_meta_edit1():
    def file_meta_save(f_name,set_dict):
        args=request.args
        #path=xpath+'\\'.join(args)
        if f_name:
            #append_dic={request.vars['case']:{f_name:{'title':k_finglish.fa_to_fin(f_title)}}}
            #return (str(append_dic))
            return (k_file_meta.append(path=xpath+'\\'.join(args),
                    f_name=f_name,
                    f_case=request.vars['case'],
                    append_dic={'title':k_finglish.fa_to_fin(f_title)})
                )  
            #(k_file_meta.append(path,append_dic))  
        return 'save not done'
    #------------------------------URL('file_meta_save',args=args,vars=request.vars)
    args=request.args
    rr=['name','title','title2','title_fa']
    #dict(request.vars)
    #rr.pop('case')
    path=xpath+'\\'.join(args)
    f_name=request.vars['f_name']
    f_title=request.vars['f_title']
    for x in rr:
        if request.vars[x+'2'] and request.vars[x] !=request.vars[x+'2']:
            return file_meta_save(f_name,rr)
    else: 
        xx=[INPUT(_name=x+'2',_id=x+'2',_value=request.vars[x+'2'] or request.vars[x]) for x in rr]
        return XML(FORM(DIV(*xx),INPUT(_type='submit'), _action='', _method='post'))

def wait():
    return "please wait"
def test():
    return dict(x=response.toolbar())
def test1():
    import mammoth
    doc_path="d:/test/"
    doc_name="test.docx"
    with open(doc_path+doc_name, "rb") as docx_file:
        result_html = mammoth.convert_to_html(docx_file)
        html = result_html.value # The generated HTML
        messages = result_html.messages # Any messages, such as warnings during conversion
        
        result_txt = mammoth.extract_raw_text(docx_file)
        text = result_txt.value # The raw text
        messages = result_txt.messages # Any messages
    #- print(text)