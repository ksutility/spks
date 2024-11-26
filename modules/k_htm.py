from gluon.html import *
def html_form(data,url):
    '''
    data={label1:[def_val1,[options1],label2:[def_val2,[options2]...}
    data = list(list(label,def_value,list(case_values)))
            [[label,def_val,[case1,case2,...]]..]
    '''
    i=0
    wid=30
    page=DIV()
    for xx in data:
        x=data[xx]
        if not isinstance(x, list):x=[x] 
        i = i+ 1
        lb1 = LABEL(xx,_width=wid)
        lb2 = LABEL(x[0],_width=wid)
        if i%2: lb2['style']='background-color:coral;'
        if len(x)==1:
            #x is a input
            en = INPUT(_value= x[0], _name=xx, _width=wid)  
        else:
            #x is a select and x[2] is options
            en = SELECT(*x[1], value=x[0])
        d=DIV(lb1,lb2,en) 
        page.append(d)
    return FORM(page,INPUT(_type='submit'),_action=URL(url),_method='post')
def htm(tag,html_txt,attributs=''):
    return "<{0} {2}>{1}</{0}>".format(tag,html_txt,attributs)    
def test1():
    return A('abc',_href=URL('index'))
def val_report(xv):
    p=A("+",_onclick="$(this).next().toggle()",_class='toggle')
    if type(xv)==dict:
        #return DIV(p,TABLE(THEAD(TR(TH('key'),TH('val'))),TBODY(*[TR(x,val_report(y)) for x,y in xv.items()]),_class="table"))
        return DIV(p,TABLE(TBODY(*[TR(x,val_report(y)) for x,y in xv.items()]),_class="table"))
    elif type(xv)==list:
        #return DIV(p,TABLE(THEAD(TR(TH('key'))),TBODY(*[TR(val_report(x)) for x in xv]),_class="table"))  
        return DIV(p,TABLE(TBODY(*[TR(val_report(x)) for x in xv]),_class="table"))
    elif type(xv)==bool:
        if xv==True:
            return DIV(str(xv),_class="bg-success")
        elif xv==False:
            return DIV(str(xv),_class="bg-danger")
    elif type(xv)==str:
        if xv.lower().strip()=='true':
            return DIV(xv,_class="bg-success")
        elif xv.lower().strip()=='false':
            return DIV(xv,_class="bg-danger")
    return xv
def val_report_prety(xv):
    
    #make tree type : exam =>['list','list'] or ['list','dict'] or ['dict','dict'] or dict,list,list
    def make_tree_type(xv):
        if type(xv) in [dict,list]:
            mtt=[{type(xv)}]
            for x in xv:
                mtt_n=make_tree_type(x)
                if len(mtt_n)+1>len(mtt):
                    for ii in range(len(mtt),len(mtt_n)):mtt+=[{}]
                for i in range(len(mtt_n)-1):
                    mtt[i+1]=mtt[i+1]|mtt_n[i]
        else:
            mtt=[]
        return mtt
    #------------------------------------------------------------------------
    return make_tree_type(xv)
    if type(xv)==dict:
        #return DIV(p,TABLE(THEAD(TR(TH('key'),TH('val'))),TBODY(*[TR(x,val_report(y)) for x,y in xv.items()]),_class="table"))
        return DIV(p,TABLE(TBODY(*[TR(x,val_report(y)) for x,y in xv.items()]),_class="table"))
    elif type(xv)==list:
        #return DIV(p,TABLE(THEAD(TR(TH('key'))),TBODY(*[TR(val_report(x)) for x in xv]),_class="table"))  
        return DIV(p,TABLE(TBODY(*[TR(val_report(x)) for x in xv]),_class="table"))
    elif type(xv)==bool:
        if xv==True:
            return DIV(str(xv),_class="bg-success")
        elif xv==False:
            return DIV(str(xv),_class="bg-danger")
    elif type(xv)==str:
        if xv.lower().strip()=='true':
            return DIV(xv,_class="bg-success")
        elif xv.lower().strip()=='false':
            return DIV(xv,_class="bg-danger")
    return xv    
def dict_2_table(i_dict,_class='table'):
    return TABLE(THEAD(TR(TH('key'),TH('val'))),TBODY(*[TR(x,y) for x,y in i_dict.items()]),_class=_class)
#---------------------- not use
def table_4_diclist(i_diclist,base_cols=[]):#,id_col):
    if len(base_cols)==0:  base_cols=[x for x in i_diclist[0]]
    d=i_diclist[0]
    #tt=TABLE()
    #d1=DIV()
    rr=htm('TH','id')#id_col
    for x in base_cols: #d:
        rr+=htm('TH',x)
    tt=htm('TR',rr)
    for d in i_diclist:
        rr=htm('TD','-') #id_col,'href=#{}'.format(d[id_col]))))
        ##dd=htm('DIV'(_id=d[id_col],_style="float: none;display: block;" )
        # make table row
        for x in base_cols: #d:
            rr+=htm('TD',d[x])
        # make linked div    
        #for x in d:
        #    if x not in base_cols:
                ##dd.append(DIV(d[x],_style="float: left; border: 1px solid gray;margin :1px; padding:1px;"))
        tt+=htm('TR',rr)
        tb=htm('table',tt)
        #d1.append(dd)
        #d1.append(BR())
    return tb #DIV(tt,d1)
def table_4_diclist_glon(i_diclist,base_cols,id_col):
    if len(base_cols)==0:  base_cols=[x for x in i_diclist[0]]
    d=i_diclist[0]
    tt=TABLE()
    d1=DIV()
    rr=TR(TH(id_col))
    for x in base_cols: #d:
        rr.append(TH(x))
    tt.append(rr)
    for d in i_diclist:
        rr=TR(TD(A(d[id_col],_href='#{}'.format(d[id_col]))))
        dd=DIV(_id=d[id_col],_style="float: none;display: block;" )
        # make table row
        for x in base_cols: #d:
            rr.append(TD(d[x]))
        # make linked div    
        for x in d:
            if x not in base_cols:
                dd.append(DIV(d[x],_style="float: left; border: 1px solid gray;margin :1px; padding:1px;"))
        tt.append(rr)
        d1.append(dd)
        d1.append(BR())
    return DIV(tt,d1)
class C_TABLE:
    """
    @author: ks
    creat = 1402/11/17
    """
    def __init__(self,heads,rows):
        '''
        inputs:
        ------
            heads:list of dict / list / dict :(titles)
                list of dict:
                    [
                        {'name':'name_val','title':'title_val','width':'width_val','class':'class_val'} #col0
                        {'name':'name_val','title':'title_val','width':'width_val','class':'class_val'} #col1
                        ...
                    ]
                list:
                    ['col0','col1','col2',...]
                dict
                    {
                    'col_name':{'title':'title_val','width':'width_val','class':'class_val'},
                    'col_name':{'title':'title_val','width':'width_val','class':'class_val'},
                    }
                    
            rows:list of list of dict / list of list
                list of list of dict:
                    [
                        [
                            {'value':'x_val','title':'title_val','class':'class_val'} #row0_col0
                            {'value':'x_val','title':'title_val','class':'class_val'} #row0_col1
                            ,...
                        ],
                        [
                            {'value':'x_val','title':'title_val','class':'class_val','style':'style_val'} #row1_col0
                            {'value':'x_val','title':'title_val','class':'class_val','style':'style_val'} #row1_col1
                            ,...
                        ]
                    ...
                    ]
                list of list:
                    [
                        [row0_col0,row0_col1,row0_col2,...],
                        [row1_col0,row1_col1,row1_col2,...],
                        ...    
                    ]
        '''
        self.rows=rows
        self.heads=heads
    def export_csv(self,folder_name):
        import gluon,k_s_dom,os
        rows=self.rows
        heads=self.heads
        trs=[]
        
        #creat thead of table
        if type(heads)==list:
            tds=[]
            for col in heads:
                if type(col)==dict:
                    tds+=[col['name']]#,_title=col.get('title',''),_width=col.get('width',''))]
                elif type(col)==str:
                    tds+=[col]
                else:
                    tds+=["error"]
                    #print('k_form.C_table =err=> type(cell)='+str(type(cell)))
        
            
        elif type(heads)==dict:
            tds=[x for x in heads]
        trs+=[tds]
        
        att_files=set() # set for store
        
        def _tag_pars(tag):
            c_tag=k_s_dom.C_TAG(tag)
            tag_inf=c_tag.tag_inf()
            #vv=vv+":::"+str(tag_inf['elements'])+":::"+str(tag_inf['text'])+":::"+tag_inf['onclick']
            onclick=c_tag.find('_onclick')
            if onclick and 'j_box_show' in onclick:#file link
                #help => j_box_show("%%",false)
                v1=onclick[12:-9].split("/")
                file_path=v1[4:-1]
                file_name=v1[-1]
                file_inf=os.path.join(*file_path,file_name)
                att_files.add(file_inf)
                vv=file_name
            #tag=k_s_dom.C_TAG().tag_inf(tag)
            #if tag_inf['tag']=='a' and tag_inf['onclick']:#file link
            #    vv=tag_inf['onclick']
            elif tag_inf['tag']=='a' and 'value' in tag_inf['items'][0] :
                vv="A:"+tag_inf['items'][0]['value']+tag_inf['titele']
            else:
               vv=tag.flatten()#tag_inf['text']
            return vv
            
        def export_files(att_files):
            if not att_files:return
            import k_file
            dest_folder=os.path.join("C:",os.sep,"temp","x_export",folder_name)
            k_file.dir_make(dest_folder)
            for file_path in att_files:
                ff=k_file.file_name_split(file_path)
                base_file=os.path.join("D:",os.sep,"ks","0-file",file_path)
                dest_file=os.path.join(dest_folder,ff['filename'])
                k_file.file_copy(base_file,dest_file)
            
        #creat tbody of table
        for row in rows:
            tds=[]
            for i,cell in enumerate(row):
                
                if type(cell)==dict:
                    vv=cell['value']
                elif type(cell) == str:
                    vv=cell
                elif type(cell) in [float,int]:
                    vv=cell
                elif type(cell) in [gluon.html.XML]:
                    vv=_tag_pars(cell)
                else:
                    vv="error"
                vv=str(vv)
                tag=TAG(vv)
                if "<" in vv or (('elements' in tag)):# and  len(tag['elements'])>1):
                    vv=_tag_pars(tag)
 
                tds+=[vv.replace("\n","")]    
            trs+=[tds]
        
        #preper export
        tt="\ufeff" # BOM
        export_files(att_files)
        return tt+'\n'.join([','.join([str(cel) for cel in row]) for row in trs])
        #return trs
        
    def creat_htm(self,table_class="0",table_type="",_id="table_c",titels=[],div_class="div_table"):
        import gluon
        '''
            old name= htm_table
        '''
        rows=self.rows
        if titels:
            if type(titels)==list:
                heads=titels
            elif type(titels)==str:
                heads=titels.split(",")
        else:
            heads=self.heads
        #heads=self.heads
        
        #creat thead of table
        if type(heads)==list:
            tds=[]
            for col in self.heads:
                if not col in heads:continue
                if type(col)==dict:
                    tds+=[TH(col['name'],_title=col.get('title',''),_width=col.get('width',''))]
                elif type(col)==str:
                    tds+=[TH(col)]
                else:
                    print('k_form.C_table =err=> type(cell)='+str(type(cell)))
        
            thead=THEAD(TR(*tds))#,_style="top:0;position: sticky;")
        elif type(heads)==dict:
            thead=THEAD(TR(*[TH(x,_width=y.get('width'),_title=y.get('title')) for x,y in heads.items()]))
        
        
        #creat tbody of table
        trs=[]
        for row in rows:
            tds=[]
            for i,cell in enumerate(row):
                if not self.heads[i] in heads:continue
                if type(cell)==dict:
                    _class_l=[heads[i]['class']] if 'class' in heads[i] else []
                    _class_l+=[cell['class']] if 'class' in cell else []
                    _class=",".join(_class_l)
                    
                    _style=cell['style'] if 'style' in cell else ''
                    tds+=[TD(cell['value'],_class=_class,_title=cell.get('title',''),_style=_style)]
                elif type(cell) in [str,int,float,gluon.html.XML]:
                    try:
                        _class=heads[i]['class'] if 'class' in heads[i] else ''
                    except:  
                        _class=''
                    tds+=[TD(cell,_class=_class)]
                else:
                    print('type(cell)='+str(type(cell)))
            trs.append(TR(*tds))

        #creat table
        class_table='table'+ table_class if (table_class !="-1") else 'table table-sm table-hover table-responsive'
        #import k_err    
        #k_err.xreport_var([heads,rows,thead,trs])  
        #class_table='table'+class_table if class_table else 'table2'
        return DIV(TABLE(thead,TBODY(*trs),_class="w-auto "+class_table,_dir="rtl",_id=_id,_name=_id),_class=div_class)
def table_x_not_used(cols,rows,class_table=''):
    import gluon
    '''
    inputs:
    ------
        cols:list of dict / list (titles)
            list of dict:
                [
                    {'name':'name_val','title':'title_val','width':'width_val','class':'class_val'} #col0
                    {'name':'name_val','title':'title_val','width':'width_val','class':'class_val'} #col1
                    ...
                ]
            list:
                ['col0','col1','col2',...]
        rows:list of list of dict / list of list
            list of list of dict:
                [
                    [
                        {'value':'x_val','title':'title_val','class':'class_val'} #row0_col0
                        {'value':'x_val','title':'title_val','class':'class_val'} #row0_col1
                        ,...
                    ],
                    [
                        {'value':'x_val','title':'title_val','class':'class_val','style':'style_val'} #row1_col0
                        {'value':'x_val','title':'title_val','class':'class_val','style':'style_val'} #row1_col1
                        ,...
                    ]
                ...
                ]
            list of list:
                [
                    [row0_col0,row0_col1,row0_col2,...],
                    [row1_col0,row1_col1,row1_col2,...],
                    ...    
                ]
    '''
    tds=[]
    for col in cols:
        if type(col)==dict:
            tds+=[TH(col['name'],_title=col.get('title',''),_width=col.get('width',''))]
        elif type(col)==str:
            tds+=[TH(col)]
        else:
            print('k_form.table_x =err=> type(cell)='+str(type(cell)))
        
    #tds=[TH(col['name'],_title=col.get('title',''),_width=col.get('width','')) for col in cols]
    thead=THEAD(TR(*tds))
    trs=[]
    for row in rows:
        tds=[]
        for i,cell in enumerate(row):
            
            if type(cell)==dict:
                _class_l=[cols[i]['class']] if 'class' in cols[i] else []
                _class_l+=[cell['class']] if 'class' in cell else []
                _class=",".join(_class_l)
                
                _style=cell['style'] if 'style' in cell else ''
                tds+=[TD(cell['value'],_class=_class,_title=cell.get('title',''),_style=_style)]
            elif type(cell) in [str,int,float,gluon.html.XML]:
                try:
                    _class=cols[i]['class'] if 'class' in cols[i] else ''
                except:  
                    _class=''
                tds+=[TD(cell,_class=_class)]
            else:
                print('type(cell)='+str(type(cell)))
        trs.append(TR(*tds))
    #import k_err    
    #k_err.xreport_var([cols,rows,thead,trs])  
    class_table='table'+class_table if class_table else 'table2'
    return TABLE(thead,TBODY(*trs),_class=class_table,_dir="rtl")
 #---------------------------------------
def select(_options,_name,_title='',_width='100%',_multiple=False,_value='',_onchange='',can_add=False,add_empty_first=True,remember=True):#k_htm.select
    ''' (_options=_select,_name=_name,_value=_value.split(',') if _multiple else _value 
        make 1 select html object
        update 01/08/09 ks
        _options:list or dict
    INPUTS:
    -------
        remember:bool
            remember last select value
    '''
    #convert _options :list to dict
    _dict={x:x for x in _options} if type(_options)==list else _options
    vs=''
    #if not _value:
    if remember:
        from gluon import current
        _value=current.request.post_vars[_name] or current.request.vars[_name] or _value
        #import k_err
        #k_err.xxxprint(msg=["err-s","current.request.vars[_name]="+str(current.request.vars[_name]),''],vals={'name':_name,'value':_value})
    if _value:
        vs=_value if type(_value)==list else _value.split(",")
    opts=[]
    if add_empty_first:
        opts+=[OPTION("-",_value="-")]
    for v in _dict:
        value=_dict[v]
        if type(value)==dict:value=value['value'] 
        op=OPTION(value,_value=v)
        if vs and v in vs:op['_selected']='selected'
        opts+=[op]
    sel=TAG.SELECT(*opts,_id=_name,_name=_name,_style="width:100%;",_onchange=XML(_onchange))
    ##import k_err
    ##k_err.xreport_var([vs,_dict,opts,sel])
    if _multiple:
        sel['_multiple']='multiple'#_multiple
        #print ("multiple"+str(_multiple))
    if can_add:sel['_class']="can_add"
    if not _title:
        return DIV(sel)#,str(vs),type(vs),str("2" in vs))
    else:
        if _title=='#':_title=_name
        sel['_style']="width:90%;"
        return DIV(LABEL(_title,_style="width:10%;"),sel)
#----------------------------------------------------------------------------- 
def select_x1(select_base_list,select_describ_list,onact_txt):
    '''
        old selct
        use= htm_select_x1(select_base_list,select_describ_list,onact_txt)
    '''
    t1="\n" + "<select " + _n + " style='width:99%;'" + onact_txt + ">" + "\n"
    if select_base_list:
        t="<option value='...'>...</option>"+ "\n"
        #call correct_fa_str(t_des)
        ti_val=select_base_list
        ti_des=select_describ_list
        if not ti_des: 
            ti_des=select_base_list
        else:
            ti_des=vb.len_set(ti_des,len(ti_val))
        for i,v in enumerate(ti_val):
            _select="' selected='selected" if v.lower() == def_val.lower() else ""
            t+= "<option value='" + v + _select + "'>" + ti_des[i] + "</option>"+ "\n"
        h_code1=t1 + t + "</select>" + "\n"
    else:
        h_code1=t1 +  "</select>" + "\n"
    return h_code1
def a(txt,_href,_target="frame",_title='',_class='btn btn-primary'):
    if _target=="frame":
        return A(txt,_title=_title,_class=_class,_href=_href,_target="x_frame") 
    elif _target=="box":   
        return A(txt,_title=_title,_class=_class,_href='javascript:void(0)',_onclick=f"""j_box_show("{_href}",true)""") 
    else:
        return A(txt,_title=_title,_class=_class,_href=_href,_target="")
def xtd(td_list):#
    rep=""
    for td_obj in td_list:
        if type(td_obj)==list: 
            rep+=f"""
                <div class="col-{td_obj[1]}">
                    {td_obj[0]}
                </div> 
            """
        else:
            rep+=f"""
                <div class="col">
                    {td_obj}
                </div> 
            """
    return f"""
        <div class="row">
            {rep}
        </div>
    """
def x_toggle(txt):
    return  f"""<div><a onclick="$(this).parent().next().toggle()" class="btn btn-primary " >+</a></div>\n
                <div style='border:2px outset red;margin:0 0 0 10px;'>\n
                {txt}\n
                </div>\n
            """
def x_toggle_s(txt,head='+',color='warning'):#s=small
    js="""
        <script>
            $( document ).ready(function() {
            $(".a_toggle_hide").click();})
            </script>
        </div>\n
    """
    return  f"""<div class="text-center">
                <a onclick="$(this).parent().next().toggle()" class="btn btn-{color} btn-sm a_toggle_hide" 
                    style="width:5%">{head}</a>\n
                </div>
                <div class="text-center">\n
                {txt}\n
                </div>\n
            """
def x_toggle_h(head,txt):#s=head dar
    return  f"""<div><a onclick="$(this).parent().next().toggle()" class="btn btn-primary a_toggle_hide" >{head}</a>\n
                </div>
                <div>\n
                {txt}\n
                </div>\n
            """
def tabs(cat_dict,content_dict,x_active=''):
    head=''
    body=''
    for x,y in cat_dict.items():
        _class=' active' if x==x_active else ''
        head+=f'''<li class="nav-item" >
                    <a class="nav-link{_class}" data-toggle="tab" href="#tab_{x}">{y}</a>
                </li>'''
        _class='active' if x==x_active else 'fade'
        body+=f"""
            <div id="tab_{x}" class="tab-pane container {_class}">\n
                {content_dict[x]}\n
            </div>\n
        """
    return  f"""
                <!-- Nav tabs -->
                <ul class="nav nav-tabs justify-content-center" >
                    {head}
                </ul>\n
                
                <!-- Tab panes -->
                <div class="tab-content">
                    {body}
                </div>
   """
def checkbox(name):
    '''
        creat checkbox in html page
    inputs:
    ------ 
        name:str
            name of object
            
            
            <div class="form-check-inline">
            </div>
            
    '''
    from gluon import current
    _value=current.request.vars[name]
    #xprint(f"checkbox {name} = {vv}")
    checked="checked" if _value=="1" else ""
    return XML(f"""<input name='{name}' id='{name}' value=1 type="checkbox" {checked} class='largercheckbox'
                style='width: 50px;height: 30px;transform: scale(1.01);
                margin: 0px;color:#hca;background color:#a00;' >""")
  
    '''
    xh=XML(f"""
                <input name='{nn}' id='{nn}' type="hidden" value=0 >
                <input style='width: 50px;height: 30px;transform: scale(1.01);margin: 0px;color:#hca;background color:#a00;' 
                    class='largercheckbox' type='checkbox' value='1' onchange="this.previousSibling.value=this.checked ?'1':'0' ">
            """)
    '''        
def form(inner_html,action=''):
    bt_a=DIV(INPUT(_type='submit',_value='تایید',_class='btn btn-primary w-50'),_class="text-center")#,_style='width:100%,background-color:#ff00ff' )
    action='action='+action if action else ''
    #URL(url),_method='post'
    return XML(f"""<form {action}>{inner_html}<br>{bt_a}</form>""")
    