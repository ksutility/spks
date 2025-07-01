from gluon import current
from gluon.html import *
import k_user

class FILES_X_TOOLS1():
    def __init__(self):
        import re,k_set
        args=current.request.args
        r_vars=current.request.vars
        # chak adrees is send to form from adress input
        if 'input_adr' in r_vars:
            path=r_vars['input_adr']
            del r_vars['input_adr']
            args=path.split('\\')
            #if path:
            xpath=args[0]
            #r_vars['xpath']=xpath
            #p1=path.replace(xpath,'')
            args=args[1:]
            #return xpath," | ",p1," | ",path
        else:
            xpath=k_set.xpath()
            path=xpath+'\\'.join(args)
        x_path=";"+path.lower().replace("\\",";")+";"
        #file_change_access-----------------------------
        fc_access=folder_w_access(x_path=x_path)['ok']
        self.x_path=x_path
        self.path=path
        self.args=args
        self.fc_access=fc_access
        self.r_vars=r_vars
    def set_out_val(self):
        return self.x_path,self.path,self.fc_access,self.args
    def link_delete(self):
        return A('Delete',_title='حذف فایل',_class='btn btn-danger',_href=URL(f='delete',args=self.args,vars=self.r_vars)) if self.fc_access else '' #_target="x_frame"
    def link_rename(self):
        return A('Refine File Name',_title='اصلاح نام فایل',_class='btn btn-warning',_href=URL(f='name_correct',args=self.args,vars=self.r_vars),_target="x_frame") if self.fc_access  else ''     
    def link_ren2(self):
        return A('Refine ALL Files Name in Folder',_title='اصلاح نام کلیه فایلها داخل فلدر',_class='btn btn-warning',_href=URL(f='correct_files_name_in_folder',args=self.args,vars=self.r_vars),_target="x_frame") if self.fc_access  else ''     
    def link_rename_title2(self,f_title='{}',vals={},tit=''):#,case,f_name,f_title):
        #if not f_title:f_title='-'
        #vars='f_name':f_name,'f_title':f_title,'case':case}
        vals.update(dict(self.r_vars))
        f_title=f_title.format(vals['f_title'])
        tit=tit if tit else vals['tit'] if 'tit' in vals else f_title
        return A("r",_href=URL(f='file_meta_edit',args=self.args,vars=vals),_target="",_class='btn') if self.fc_access else '' #f_title
        # k_htm.a(_target="box")
        #return A(f_title,_href=URL(f='file_meta_edit',args=self.args,vars={'f_name':f_name,'f_title':f_title,'case':case}.update(dict(self.r_vars))),_target="x_frame") if self.fc_access else f_title 
    def link_comp(self):
        return A("compare",_href=URL('xfile','tools',args=self.args,vars=self.r_vars),_title="مقایسه")
    def link_move(self):
        #DIV(A('Move',_title='Move',_class='btn btn-warning',_href='javascript:void(0)',_onclick=f"""j_box_show("{URL(f='move',args=args+[fname],vars=r_vars)}",true)""")),
        return A('Cut',_title='CUT',_class='btn btn-warning',_href=URL(f='move_x',args=['cut']+self.args,vars=self.r_vars)
        #DIV(A('Copy',_title='COPY',_class='btn btn-warning',_href='javascript:void(0)',_onclick=f"""j_box_show("{URL(f='move_x',args=['copy']+args+[fname],vars=r_vars)}",true)"""))
        ) if self.fc_access else '' #_target="x_frame"
    def link_edit(self):#,x_file,link_txt,link_title='Edit'):  
        ext=x_file['ext'][1:]
        if ext in ['md','mm','json','csv','txt','ksm','mermaid','mermaid2']:#files that can edit by edit_r page
            return A(link_txt,_href=URL('xfile','edit_r',args=args+[x_file['filename']],vars=r_vars),_target="x_frame",_title=link_title)
        return ''   
def folder_w_access(args=[],x_path=''):
    '''
    old name=fca
    بررسی امکان تغییر یک فلدر توسط یک نفر
    folder_w_access=folder_write_access
        بررسی می کند که آیا یک فلدر توس ط کاربر جاری قابل دسترسی نوشتن و موارد مشابه مثل حذف و جابجایی است یا خیر
    input
    ------
        session["file_access"]=> set by user.py on login
        session["my_folder"]=> set by user.py on login
            سسشن های فایل_اکسس و مای_فلدر در داخل برنامه یوزر.پای در زمان لاگین کردن فرد تنظیم می شود
            
    '''
    session=current.session
    request=current.request
    from k_set import C_SET
    share_inf=C_SET().share_inf
    # if not x_path:
    if not args:args=current.request.args
    x_path=(x_path or (';'.join(args))) +";"
    def list_match(pt_list,st):
        import re
        import k_err
        k_err.xxxprint(vals={'pt_list':pt_list,'st':st})
        st=st.lower()
        for pt in pt_list:
            if re.findall(pt.lower(),st):
                return True
    #------------------------    
    import k_err
    #k_err.xxxprint(msg=['a','b','c'],vals={'session':[session["file_access"],session["my_folder"]]})
    if session["file_access"]:
        fc_list=(session["file_access"].split(",") if type(session["file_access"])==str else [])+session["my_folder"] #[f';{session["my_folder"]};']
    else:
        fc_list=session["my_folder"]
    if session["admin"] or x_path[:-1] in share_inf or (list_match(fc_list,x_path)) or request.vars['from']=='form': #file_change_access: user have file_change_access for this folder 
        return {'ok':True}  
    else:
        import k_err
        k_err.xxxprint(vals={'fc_list':fc_list,'share_inf':share_inf,'x_path':x_path,'args':args,'args1':current.request.args})
        return {'ok':False,'msg':f'you can not do this action-path={x_path} <br> share_inf={share_inf} <br> fc_list={str(fc_list)} '}         