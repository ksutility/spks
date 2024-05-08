# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 18:20:28 2021

@author: ks

last update 1400/11/14
"""
import os
import k_err 
from k_err import xxprint,xprint,xalert,xxxprint

from functools import wraps

#import eel_ui as ui
def temp_file_name(name='',ext='.txt'):
    import jdatetime #khayyam
    import time
    today=jdatetime.date.today().strftime('%y%m%d') 
    now=time.strftime("%H%M%S", time.localtime())
    return 'c:\\temp\\' + f'{today}-{now}-kspy-' + name +  ext
def check_err(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
from k_set import WEB2PY 
if WEB2PY.run:check_err=k_err.check_err
def file_count1(path):
    #os.listdir(path)
    files =[x for x in list(os.scandir(path)) if x.is_file()]
    #- print(len(files))
    #- print(files)

#onlyfiles = next(os.walk(dir))[2] #dir is your directory path as string
#print len(onlyfiles)
def list_files(path,full_name=False):
    if full_name:
        return [os.path.join(path, item) for item in os.listdir(path) if os.path.isfile(os.path.join(path, item))]
    else:
        return [item for item in os.listdir(path) if os.path.isfile(os.path.join(path, item))]
def name_correct(fname):
    '''
    010810
    اصلاح نام فایل برای سرور
    تبدیل کاراکتر های فارسی به فینگلیش
    تبدیل کلیه علائم به خط تیره
    '''
    let='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_@.'
    def sign_2_line(fname):
        for t in fname:
            if t not in let:
                fname=fname.replace(t,'-')
        return fname
    import k_finglish
    n=k_finglish.fa_to_fin(fname)
    return sign_2_line(n)        
def correct_files_name_in_folder(path):
    def add_re(re2,re3,dir_path):
        re2['changed']+=[dir_path]+re3['changed']
        re2['err']+=[dir_path]+re3['err']
    re1={'changed':[],'err':[],'same':[]}
    re2={'changed':[],'err':[],'same':[]}
    for item in os.listdir(path):
        n1=os.path.join(path, item)
        #
        n_i2=name_correct(item)
        n2=os.path.join(path, n_i2)
        if n_i2 != item:    
            try:
                os.rename(n1, n2)
                re1['changed']+=[f'{path}   |   {item}    =>    {n_i2}']
                if os.path.isdir(n2):
                    re3=correct_files_name_in_folder(n2)
                    add_re(re2,re3,n2)
            except Exception as err:
                re1['err']+=[f'{path}   |   {item}    =>    {n_i2}   |  err={err}']
        else:
            re1['same']+=[f'{item}']
            if os.path.isdir(n2):
                    re3=correct_files_name_in_folder(n2)
                    add_re(re2,re3,n2)
        
    ##------
    if re1['changed']:
        with open(path+f'\\__rename_changed.txt', 'a',encoding='utf8') as f:f.write('\n'.join(re1['changed']+['']))
    if re1['err']:
        with open(path+f'\\__rename_err.txt', 'a',encoding='utf8') as f:f.write('\n'.join(re1['err']+['']))
    ##-------        
    #print(str(re1))
    add_re(re1,re2,"-------")
    return re1
def list_folders(path):
    return [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
def file_full_name(path,file_name):
    return os.path.join(path, file_name)
def file_count(path,full_name=False):
    files=list_files(path,full_name)
    return len(files),files
    #print(files)
def dir_make(dir_path):
    # make_path #cad make_path1(path)
    '''
    Parameters
    ----------
    dir_path : string
        DESCRIPTION. 

    Returns
    -------
    None.
        check if dir_path not exist: creat it  
    
    Test
    ------
    dir_make(r'd:\temp\a\b\c')

    '''
    #print(f'dir_make:{dir_path}')
    if os.path.exists(dir_path):
        return {'ok':True,'msg':f"{dir_path} is exist"}
    d1=dir_path.rpartition('\\')[0]
    xxxprint(msg=['',d1,''])
    if d1:
        re1=dir_make(d1)
    try:
        os.mkdir(dir_path)
        if d1:
            return {'ok':re1['ok'],'msg':f" dir({dir_path}) Are created Succeccfully"+"\n"+re1['msg']}
        else:
            return {'ok':True,'msg':f" dir({dir_path}) Are created Succeccfully"}
    except Exception as err:
        return {'ok':False,'msg':f" dir({dir_path}) Not created: err= {err}"}
    
    
def downloads_path():
    from pathlib import Path
    return  str(Path.home() / "Downloads")#r"C:\Users\ks\Downloads"
@check_err
def empty_download_folder():            
    '''
        move all files frome "download" folder to "download/0"
    '''
    p1=downloads_path() 
    p2=p1 + "\\0" 
    dir_make(p2)
    for item in os.listdir(p1):
        path1=os.path.join(p1, item)
        if os.path.isfile(path1):
            path2=os.path.join(p2, item)
            #shutil.move(path1,path2)
            for i in range(2):
                if file_move(path1,path2)['ok']:
                    break
#@check_err
def file_move(base_path,des_path):
    #_path can be str or 1 tuple => ( path,filename)
    # and delete empty folder after move
    import shutil
    def pc(x):
        return x if type(x)==str else os.path.join(*x)
   
    f_inf=('x_file','file_move')
    base_path1,des_path1=[pc(x) for x in(base_path,des_path)]
    if base_path1==des_path1:
        msg1=f'error in k_file.file_move: base_path=des_path= {base_path1}'
        xxxprint(msg=['err',msg1,''])
        return {'ok':False,'msg':msg1}
    if find_path(des_path1) : file_delete_rcl(des_path1)
    des=file_name_split(des_path1)
    if not find_path(des['path']) :  dir_make(des['path'])
    if not find_path(base_path1) : 
        msg1=" file not found => "  +  base_path1
        xxxprint(msg=['err',msg1,''])
        return {'ok':False,'msg':msg1}
    rep =f"move : {base_path1} => {des_path1} "
    #try:
    shutil.move(base_path1,des_path1)
    log_to_file(f'file moved = {base_path1} => {des_path1}')
    xxprint(True,rep , "are done successfuly")
    return {'ok':True,'msg':str(rep) + " are done successfuly "}
    #except:
        # xxprint(False,rep, "not done")
        # xalert(rep + "\n not done")
        # return False
#@k_err.until_result(1,"number of file in download folder ")
def downloded_1_file_exist():
    import time
    dp=downloads_path() # r"C:\Users\ks\Downloads"
    n,files=file_count(dp)
    if n==0:
        for i in range(5):
            time.sleep(1)
            n,files=file_count(dp)
            if n>0 : break
    elif n==2:
        f0=file_name_split(files[0])
        f1=file_name_split(files[1])
        if f1['name'] in f0['name'] or f0['name'] in f1['name']:
            xalert(f"2 file is dowonload-its name is like\n{f0['name']},{f1['name']}\npro will delete => {f1['name']}")
            os.remove(os.path.join(dp,files[1]))
            return 1
    if n==1:
        path1=os.path.join(dp, files[0])
        i=0
        while i<125:
            i+=1
            if ("crdownload" not in path1) and os.access(path1, os.W_OK) and (".tmp" not in path1):
                    xprint( " ok :" + path1)
                    return 1
            else:
                xprint('sleep for file ')
                time.sleep(3)
                n,files=file_count(dp)
                if n==0:xalert(f"error:1 file not exist \n path1={path1}") 
                path1=os.path.join(dp, files[0])
        quit()
    return n    
    #return True if n==1 else False 
def file_delete(file_path,path=''):
    '''
        2 case avalabe
            1: file_path =filename(fname.ext) , path=folder
            2: file_path =fullName(folder\fname.ext),path not present
    '''
    if path !='':
        file_path=os.path.join(path,file_path)
    os.remove(file_path)
    log_to_file('File Delete = ' + file_path)
    
@check_err   
def file_delete_rcl(file_path,path='',delete_empty_folder=False,recycle_sub_folder=''):
    #move to recycle :share.base_path_recycle_delete
    #1400/10/02 ok
    '''
        recycle_sub_folder:STR
            1 folder name in recycle folder 
            for split each sum files in 1 folder
    '''
    from k_set import K_set
    rc=K_set.recycle
    if recycle_sub_folder: rc=os.path.join(rc,recycle_sub_folder)
    if path !='':
        file_path=os.path.join(path,file_path)
    rep=f'{file_path} '    
    if not os.path.exists(file_path):
        rep+=': not exist'
        xxxprint(msg=['err',rep,''])
        return rep
    #try:
    
    import k_date
    dd=k_date.ir_date("yymmdd-hhggss-")#("","yymmddhhggss",0,"","")
    ff=file_name_split(file_path)
    new_fname=dd + ff['filename']
    file_move(file_path,(rc,new_fname))
    rep+=f" => {rc} \ {new_fname} "
    if delete_empty_folder:
        folder_delete_if_empty(ff['path'])
    return rep #xxxprint(True,rep)
#---------------------------------------------------------------------------------################################     
@check_err                      
def get_downloded_file(new_path):
    '''
        get 1 file frome "download" folder and save it to new_path
    '''
    xprint(new_path)
    file_tg=file_name_split(new_path) #file_target
    dp=downloads_path()
    n=downloded_1_file_exist()
    if n:
        import time
        n,files=file_count(dp)
        path1=os.path.join(dp, files[0])
        i=0
        while i<31:
            i+=1
            if ("crdownload" not in path1) and os.access(path1, os.W_OK):
                file_dn=file_name_split(path1)
                if file_dn['ext']!=file_tg['ext']:xalert(f'error:ext of 2 file is different \n download file={file_dn["filename"]} \n target file={file_tg["filename"]}' )
                if file_move(path1,new_path)['ok']:
                    xprint(" ok ")
                    return True
            else:
                xprint('sleep for file ')
                time.sleep(4)
                n,files=file_count(dp)
                if n==0:xalert(f"error:1 file not exist \n path1={path1}") 
                path1=os.path.join(dp, files[0])
    else:
        n1,files=file_count(dp)
        xprint (f"error in get_downloded_file({new_path}>\n 1 file shoud be in download folder but <{n}> files is exist\n files={files}")
    return False
def downloads_dir_file_count()  :
    dp=downloads_path() # r"C:\Users\ks\Downloads"
    n,files=file_count(dp)
    return n
@check_err                      
def get_downloded_file1(new_path):
    '''
        get 1 file frome "download" folder and save it to new_path
    '''
    import time
    dp=downloads_path() 
    n,files=file_count(dp)
    if n==0:
        for i in range(5):
            time.sleep(1)
            n,files=file_count(dp)
            if n>0 : break
    if n==1:
    #check if file is downloading (access denided and .crdownload in end of file)
        path1=os.path.join(dp, files[0])
        i=0
        while i<31:
            i+=1
            if ("crdownload" not in path1) and os.access(path1, os.W_OK):
                if file_move(path1,new_path)['ok']:
                    k_err.xprint(f"get_downloded_file({new_path}) => ok")
                    return True
            else:
                time.sleep(2)
                n,files=file_count(dp)
                if n==0:xalert(f"error:1 file not exist \n path1={path1} \n db={dp} ") 
                path1=os.path.join(dp, files[0])
    else:
        xalert(f"error in <get_downloded_file> \n 1 file shoud be in download folder but <{n}> files is exist\n\n files=\n{files}")
    return False    
def name_append(file_path,append_str):
    f=file_path #exam  'C:\\X\\Data\\foo.txt'
    fn=os.path.basename(f) #exam 'foo.txt'
    path=os.path.dirname(f)  #exam 'C:\\X\\Data'
    ff=file_name_split(fn) #exam ('foo', '.txt')
    return path+"\\"+ff['name']+append_str+ff['ext']
def backup(file_path,bak_folder='',delete=False):
    ''' 010930 
    creat 1 backup from file_path
    INPUTS:
    ------
        delete:Bool
            delete orginal file =move file not copy
        
    '''
    
    #from datetime import datetime
    #tt=datetime.now().strftime('-%Y%m%d-%H%M%S')
    import jdatetime #khayyam
    import time
    today=jdatetime.date.today().strftime('%y%m%d') 
    now=time.strftime("%H%M%S", time.localtime())
    tt=f'-{today}-{now}'
    
    ff=file_name_split(file_path)
    if bak_folder:
        bak_folder=bak_folder.split(',')
        if bak_folder[0]=='*':
            bak_folder=os.path.join(ff['path'],*bak_folder[1:])
        else: 
            bak_folder=os.path.join(*bak_folder)
    else:
        bak_folder=ff['path']
    new_file_path=os.path.join(bak_folder,ff['name']+tt+'-bak'+ff['ext']    )
    import shutil
    dir_make(bak_folder)
    if delete:
        shutil.move(file_path, new_file_path)
    else:
        shutil.copy(file_path, new_file_path)
    return new_file_path
   
@check_err  
def read(_format,file_path):
    '''
    Parameters
    ----------
    file_path : str
    _format : str (json / text)
        data format.

    Returns
    -------
    TYPE=string or object(list/dictionary)
        DESCRIPTION.

    '''
    #try:
    
    if _format=='json':
        f = open(file_path)
        import json
        data = json.load(f)
        f.close()
    elif _format=='text':
        f = open(file_path,encoding='utf8')
        data =f.read()
        f.close()
    elif _format=='pickle':
        import pickle
        with open(file_path, 'rb') as fp:
            data = pickle.load(fp)
    return data
    '''except : 
        print("error: {error}\n in k_file.read")    
        k_err.show()
        return {}
    '''
@check_err  
def write(_format,file_path,data):
	#010618
    if _format=='json':
        import json
        with open(file_path,'w',encoding='utf8') as f:
            json.dump(data,f,indent=4)#,ensure_ascii=False)
    elif _format=='text':
        with open(file_path,'w',encoding='utf8') as f:
            f.write(str(data))
    elif _format=='pickle':
        import pickle
        with open(file_path, 'wb') as fp:
            pickle.dump(data, fp)
    #except:    
    #   print("error: {error}\n in k_file.write")   
    #   k_err.show()
def file_size(file_path):
    return os.stat(file_path).st_size  

#--------------------------------------------------------------------------------form----------------------------------
def find_path (path,sub_path=''):
    #1400/10/02 - find_file,find_dir
    p=os.path.join(path, sub_path) if sub_path!="" else path
    return os.path.exists(p)    
    '''
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return false'''
#---------------------------------------------------------------------------------################################
def find (path,sub_path=''):
    '''
    1403/01/05 - 
    goal:
        find 1 path by wildcard 
    result:
        if find:
            return first find
        else:
            return None
    '''
    import glob
    p=os.path.join(path, sub_path) if sub_path!="" else path
    re=glob.glob(p)
    if re:re=re[0]
    return re   
 #---------------------------------------------------------------------------------################################
def file_copy(base_path_filename,dest_path_filename):
    f_inf=('file','file_copy')
    if not find_path(base_path_filename): 
        return xxprint('err',"file not fond=>"+base_path_filename)
    import shutil
    rep=f'copy ({base_path_filename}) =>({dest_path_filename})'
    try:
        shutil.copy(base_path_filename ,dest_path_filename)
        return xxprint(True,rep)
    except:
         return xxprint(False,rep)
#---------------------------------------------------------------------------------################################
def folder_isempty(path):
    if not os.path.exists(path):return False
    return (len(os.listdir(path)) == 0) 
#---------------------------------------------------------------------------------################################
def folder_delete_if_empty (path): 
    if folder_isempty(path): os.rmdir(path)
#---------------------------------------------------------------------------------################################
def folderpath_maker_by_filename(filename,full_patern): 
    '''
    f( "name_1-name_2-name_3","123^23^13 ") = "name_1-name_2-name_3\name_2-name_3\name_1-name_3"
    input:
    ----------
        filename:str
            = name_1-name_2-name_3-name_n
            split chr in filename ( input) is "-"
        full_patern:str
            = pat^pat2^pat3^...^pat_n ==like==> 123^23^13 
                pat_n = (pattern to make n_th folder name ) : n1n2n3n4...nx (each n is 1 digit int) sample=143
                    nx =x_th section of filename 
                    x for the first section is=1 ?(0)
    output:
    ----------
        result:str
            = res_1 \ res_2 \ ... \ res_n  ==like==> name_1-name_2-name_3\name_2-name_3\name_1-name_3
            split chr in result( output) is "\"
            split chr in res_n is "-"
    
    '''
    fname_sec=filename.split("-")
    pats=full_patern.split("^")
    res_l=[]
    for pat in pats:
        res_l.append("-".join([fname_sec[int(t)-1] for t in pat]))
    return "\\".join(res_l)
#--------------------------------------------------------------------'
def appendstringtofile(strfile ,strnewtext ,intblankline ):
    f_inf=('file','appendstringtofile',(strfile ,strnewtext ,intblankline))
    try: 
        xfile =open(strfile,"a")# forappending
        xfile.write("\n"*intblankline)
        xfile.write(strnewtext)
        xfile.close
        return xxprint(True,'ok')
    except:
        return xxprint('err','error')
#--------------------------------------------------------------------------------
def size_easy(in_filesize):#filesize_easyread_format
    s= str(in_filesize) #in byte
    n=len(s) 
    if n in [0 ,1 ,2, 3]:
        r1=f"{s}B"
    elif n in [4]:
        r1=f"{s[0]}.{s[1:3]}K"   
    elif n in [5]:
        r1=f"{s[0:2]}.{s[2]}K"      
    elif n in [6]:
        r1=f"{s[:-3]}K"
    elif n in [7]:
        r1=f"{s[0]}.{s[1:3]}M"
    elif n in [8]:
        r1=f"{s[0:2]}.{s[2]}M"
    else:
        r1=s[:-6] + "M"
    return f'{n}:{r1}'
#---------------------------------------------------------------------------------################################
def file_name_split(file_full_path): 
    #4001004
    '''
    input
    ------
        file_full_path=file fullname by path        exam= "c:/ab/c/abname.pdf"
    output
    ------
        (path,name,ext)
        path=path of file               exam="c:/ab/c"  
        name=name section of file name  exam="abname"
        ext=ext section of file name    exam=".pdf"
    '''
    f=file_full_path #exam  'C:\\X\\Data\\foo.txt'
    fn=os.path.basename(f) #exam 'foo.txt'
    path=os.path.dirname(f)  #exam 'C:\\X\\Data'
    name,ext=os.path.splitext(fn) #exam ('foo', '.txt')
    return {'path':path,'name':name,'ext':ext,'filename':fn}

# ==================================================== xfile ===============================================
def doc2md(doc_file_path):
    '''
    input:
    ------
        doc_file_path:str
            input data
    output:
    ------    
        md_file_path:str
            output data
    '''
    f=file_name_split(doc_file_path)
    md_file_path=f['path']+"\\"+f['name']+".md"
    print("f['path']"+f['path'])
    import os
    x_cmd="D:\\ks\\ext\\WPy64-31040\\python-3.10.4.amd64\\python.exe "#, to_md {file1} {file2} ".format(file1=doc_file_path,file2=md_file_path)
    x_cmd+=os.path.join("D:\ks\I\web2py","0-need\k_word_mammoth.py")
    x_cmd+=" to_md {file1} {file2} ".format(file1=doc_file_path,file2=md_file_path)
    #print(x_cmd)
    #subprocess.call([x_cmd,''])# 'C:\\test.txt'])
    import k_os
    return k_os.run_cmd(x_cmd)  
def zip_extract(zip_path):
    from zipfile import ZipFile
    with ZipFile(zip_path, 'r') as zipObj:
        # Extract all the contents of zip file in different directory
        f=file_name_split(zip_path)
        zipObj.extractall(f['path']+"\\"+f['name'])
    return True    
def zip7_extract(zip_path,switch='x'):#rar or zip
    '''
    input:
    ------
        switch='-x' / '-e'
            '-x'= refer to 7zip switch help
            '-e'= refer to 7zip switch help
    '''
    overwrite_mode='-aoa' #Overwrite All existing files without prompt 
    f=file_name_split(zip_path)
    des_dir=f['path']+"\\"+f['name']
    x_cmd="""d:\\ks\\ext\\w2p\\7Zip\\7z.exe """ + f"""{switch} {zip_path} -o{des_dir} -r {overwrite_mode}"""
    #print(x_cmd)
    #subprocess.call([x_cmd,''])# 'C:\\test.txt'])
    import k_os
    return k_os.run_cmd(x_cmd)  

def zip_folder_to(folder_path,zip_path,delete=True):
    '''
    Parameters
    ----------
    folder_path : str
        path of folder that input files is in it
    zip_path : str 
        path of output zip file

    Returns
    -------
    zip all files in 1 folder(folder_path) to 1 file(zip_path).

    '''     
    from zipfile import ZipFile
    files = list_files(folder_path)
    xxprint('file','Following files will be zipped:')
    for file_name in files:
        xxprint('file',file_name)
     # writing files to a zipfile
    with ZipFile(zip_path,'w') as zip:
        for file in files:
            zip.write(os.path.join(folder_path,file), arcname = file)
    xxprint('file','All files zipped successfully!')    
    if delete:
        for file in files:
            os.remove(os.path.join(folder_path,file))
        xxprint('file','zip => All input files delete successfully!') 
    return True
#print(file_count("."))
#file_count1(".")

#==================================================   not used    =================================================
#--------------------------------------
'''
def file_report(x_path,d_file_name,linked):
    fp1= os.path.join(x_path,d_file_name)
    f=fp1 #pub_fs.getfile(fp1)
    fsz= filesize_easyread_format(f.size)
    # close box that shows  "download.asp" content by jquery_ajax 
    t = f''<a  href = "javascript:void(0)" onclick="j_box_hide();window.open('temp_download/{d_file_name}')"> {d_file_name}</a>'' if linked else d_file_name 
    return f''
        <hr><h2 align=center>{t}</h2>
        <br> file size = {fsz}
        <hr> file created: {iran_time(f.datecreated,"yy/mm/dd hh:gg:ss - ww",0,x_w,"t")}
        <br> file accessed: {iran_time(f.datelastaccessed,"yy/mm/dd hh:gg:ss - ww",0,x_w,"t")}
        <br> file modified: {iran_time(f.datelastmodified,"yy/mm/dd hh:gg:ss - ww",0,x_w,"t")}
    ''
#------------------------------------------------------------------------------------------------------
def listfoldercontents(path,show_folder_name,show_hlink):
    def mapurl(path): 
       #convert a physical file path to a url for hypertext links.
       rootpath = server.mappath("/")
       url = path[-len(path) + len(rootpath):]
       return url.replace("\\","/")
    #--------------------------------------------
    folder = pub_fs.getfolder(path)
    
    #display the target folder and info.
    r1="----------------------------------------------<br>\n"
    if show_folder_name : r1 += "<b>" + folder.name + "</b> - \n"
    r1 += folder.files.count + " files, \n"
    if folder.subfolders.count > 0 :
        xprint(folder.subfolders.count + " directories, \n")
    r1 += f"{round(folder.size / 1024)} kb total.\n" #'+ vbcrlf)
    r1 += "<br> list:\n" #'+ vbcrlf)
    #display a list of files.
    for item in files: #folder.files
        if show_hlink :     
            if  url1 == mapurl(item.path) :
                r1 += f'<li><a href="{url1}">{item.name}</a> - {item.size} bytes, last modified on { item.datelastmodified }.</li>\n'
        else:
            r1 += f'<li>{item.name} - {(item.size/1024)} kb, last modified on { item.datelastmodified } </li>\n'
    #display a list of sub folders.
    for item in subfolders: #folder.subfolders
        r1 += listfoldercontents(item.path,true,show_hlink)
    r1 += """</ul> 
        ----------------------------------------------<br>
        """
    return r1   
@check_err          
def move(base_path,des_path):
    return file_move(base_path,des_path)
'''
def find_sami_file(path,file_name_pattern,ext_list):
	"""
		find files 
			path = path for serch
			name_pattern = file name_pattern 
				-a pice of name like('abc*-d') 
				-or ..
			ext_list=list of acceptable ext
				- exam ['pdf','dwg','jpg']
	"""
	import glob,os
	fn=os.path.join(path,file_name_pattern)
	find=[]
	for ext in ext_list:
		#print ('fn='+fn+"."+ext)
		find+=glob.iglob(fn+"."+ext) #"/mydir/*/*.txt"): # generator, search immediate subdirectories 
	return find	
def rename(file_path,new_name_format):
    '''
        new_name_format
            sample "ab{name}e{date}-{time}.e{ext}
        file_path:str   
            exam  'C:\\X\\Data\\foo.txt'
    '''
    import k_date
    fdate=k_date.ir_date("yymmddhhggss")
    ff=file_name_split(file_path) 
    return ff['path']+"\\"+new_name_format.format(name=ff['name'],ext=ff['ext'][1:],date=fdate[:6],time=fdate[-6:])    
def launch_file(filename):
    #shell 
    import os
    os.system("start " + filename)
    '''
    import subprocess
    try:
        os.startfile(filename)
    except AttributeError:
        #subprocess.call(['open', filename])
        subprocess.call(('cmd', '/C', 'start', '', filename))
    '''
def root_split(path):
    '''
        creat 1 list of ajdad of 1 folder
    test:
        >>> print(root_split("D:\ks\I\e\pp"))
        ['D:', 'D:\\ks', 'D:\\ks\\I', 'D:\\ks\\I\\e\\pp']
    '''
    #folder slice character
    fsc="\\"
    pp=path.split(fsc)
    p0=pp[0]
    rp=[pp[0]]
    for x in pp[1:]:
        p0+=fsc+x
        rp+=[p0]
    return rp   
def log_to_file(msgs,log_path='c:\\temp\\_file_change.txt'):
    import k_date
    dd=k_date.ir_date("yymmdd-hhggss") + " "
    with open(log_path, 'a',encoding='utf8') as f:
        if type(msgs)==str:
            f.write(dd+msgs+'\n')
        elif type(msgs)==list:
            f.write('\n'.join(['-'*20+dd]+msgs+['']))
    
    
    