# -*- coding: utf-8 -*-
"""
Created on 1402/12/14 
    @author: ks
    last update 1402/12/14
goal :    
    manage meta data for file in '__inf.json' in txt format
    
"""
import os,k_file,k_finglish
from k_err import xxxprint
class P_JSON:
    #python json
    def append_dict(self,base_dic,add_dic):
        '''
        find in pro:
            p_json.append_dict
        '''
        for x in add_dic:
            if (x in base_dic) and type(base_dic[x])==dict :
                    if type(add_dic[x])==dict:
                        self.append_dict(base_dic[x],add_dic[x])
                    else: 
                        return False,'error change dict => none dict'
            else: #add or change
                base_dic[x]=add_dic[x]
        return True,'ok'
    def remove_dic(self,base_dic,item_name):  
        if item_name in base_dic:
            pass
        
class K_FILE_META:
    def meta_path(self,path):
        '''
            path of meta data file
        '''
        return os.path.join(path,'__inf.json')
    def read(self,path,files=[],folders=[]):#_txt
        import json
        '''
            get meta data for files & Folders form '__inf.json' in txt format
        find in pro:
            k_file_meta.read  
        output:
        ------
            retuen :meta
            
            files: update_files_inf
            
            folders: update_folders_inf
        '''
        for f in files+folders:
            for t in ['title','x']:
                f[t]=''
        f_path=self.meta_path(path) # f_path = file path
        if os.path.isfile(f_path):
            meta=k_file.read('json',f_path)
            '''
            meta={'files':{ '0-4901.pdf':{'title':'abc',
                            'x':'y'},
                '1-rec-i-4901.pdf':{'title':'qwererwe',
                                    'x':'z'}
            },
            'general':'abc'
            }
            '''
            # update_files_inf
            for f in files:
                if f['filename'] in meta['files']:
                    f.update(meta['files'][f['filename']])
            #print("###"+ str(meta['folders']))
            
            # update_folders_inf
            for f in folders:
                #print(f)
                if f['name'] in meta['folders']:
                    #print(f+' is in' )
                    f.update(meta['folders'][f['name']])
            for f in files+folders:
                f['title']=k_finglish.fin_to_fa(f['title'])
            return meta 
        else:
            return ""
    def write(self,f_path,meta):
        xxxprint(msg=['f_path',f_path,''],vals=meta)
        k_file.write('json',f_path,meta)
        return (f'<hr> write=> ok<br>{f_path}<hr>{str(meta)}')
    #-----------------------------------------------------------------
    def append(self,path,f_name,f_case,append_dic):#_txt
        import json
        '''
        goal:
            add or change file titels in '__inf.json' in txt format
            if file not exist creat it
        find in pro:
            k_file_meta.append
            
        inputs
        ------
            path :str
                path of '__inf.json' folder 
            f_name:str
                name of file or folder 
            f_case:
                "files" / "folders"
            append_dic:dict 
                meta inf of file
                {file_name1:file_title1,...}
        '''
        append_dic_2={f_case:{f_name:append_dic}}
        f_path=self.meta_path(path)# file path
        p_json=P_JSON()
        try:
            if os.path.isfile(f_path): # if file exist 
                meta=k_file.read('json',f_path)
                p_json.append_dict(meta,append_dic_2)
                return self.write(f_path=f_path,meta=meta)
                #k_file.write('json',f_path,meta)
                #return (str(meta)+'<br>append ok<br> '+f_path)
            else: # creat file
                meta={ "files": {},
                       "folders": {},
                       "general": "abc"}
                ok,msg=p_json.append_dict(meta,append_dic_2)
                if ok:
                    return "<hr> creat ok" + self.write(f_path=f_path,meta=meta)
                    #k_file.write('json',f_path,meta)       
                    #return (str(meta)+'<br>creat ok<br> '+f_path)
                else:
                    return msg
        except Exception as err:
            xxxprint(err=err)
            return ('<hr> error in <br> k_file_meta.append <br> '+f_path)
    #-----------------------------------------------------------------  
    def change_key(self,path,old_key_in_dict,new_key):#_txt
        import json
        '''
        exam
            input:
                abc.inf={'file':{'a':'a'},'folder':{'x':'x_t'}  }
                k_file_meta.change_key('abc.inf',{'folder':{'x':'x_t'},'y')
            result:
                abc.inf={'file':{'a':'a'},'folder':{'y':'x_t'} }
        find in pro:
            k_file_meta.change_key
        inputs:
        ------
            f_path=file path
            old_key_in_dict=dict
            new_key:str
                new nemae for last key in old_key_in_dict in this exam ='x'
        '''
        def change_dic_key(base_dic,old_key_in_dict,new_key):
            for x in old_key_in_dict:
                if (x in base_dic):
                    if type(old_key_in_dict[x])==dict: #if type(base_dic[x])==dict :
                        return change_dic_key(base_dic[x],old_key_in_dict[x],new_key)
                    else :
                        base_dic[new_key]=base_dic[x]
                        del base_dic[x]
                        return True,'ok'
                else: 
                    return False,'error change dict => none dict'                
        #----------------------------------------------------------    
        f_path=self.meta_path(path)
        #try:
        if os.path.isfile(f_path):
            meta=k_file.read('json',f_path)
            ok,msg=change_dic_key(meta,old_key_in_dict,new_key)
            if ok:
                return "change_key ok<br>" + self.write(f_path=f_path,meta=meta)
                #k_file.write('json',f_path,meta)
                #return (str(meta)+'<br>change_key ok<br> '+f_path)
            else:
                return msg
        #except:
        #    return ('error in <br> k_file_meta.change_key <br> '+f_path)
    def move(self,path1,path2,f_name):
        '''
            move meta inf of a file or folder (f_name) from '__inf.json' in folder1(path1) to '__inf.json' in folder2(path2)
        inputs:
        ------
            path1:str
                path of folder 1
                where 1st "__inf.json" is there
            path2:str
                path of folder 2
                where 2th "__inf.json" is there
            f_name:str
                file or filder name
        '''
        meta=self.read(path1)
        xxxprint(msg=['meta',f_name,path1+" | " + path2],vals=meta)
        print('-')
        if meta:
            for f_case in ['folders','files']:
                if f_name in meta[f_case]:
                    f_data=meta[f_case].pop(f_name)
                    re1= "<hr> k_file_meta.move ok" 
                    re1+=self.write(f_path=self.meta_path(path1),meta=meta)
                    xxxprint(msg=[f_case,f_name,path1+" | " + path2],vals=f_data)
                    re1+=self.append(path=path2,f_name=f_name,f_case=f_case,append_dic=f_data)
                    return f"<div style='backgroundColor:#f90'>{re1}</div>"
        return "error k_file.move not done"
    #-------------------------------------------------------------------
    def list_unused_json_item(self,files,folders,meta):
        '''
            make list of unused json item in meta file ="__inf.json"
        '''
        try:
            #- print('unused')
            files_list=[f['name']+f['ext'] for f in files]
            folders_list=[f['name'] for f in folders]
            files_un=[f for f in meta['files'] if not f in files_list] #files_unused
            folders_un=[f for f in meta['folders'] if not f in folders_list] #folders_unused
            #- print(files_list)
            #- print(folders_list)
            #- print(files_un)
            #- print(folders_un)
        except Exception as err:
            print('err in unused_json_item \n'+ str(err))