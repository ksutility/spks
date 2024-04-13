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
 #---------------------------------------
def select(_options,_name,_title='',_width='100%',_multiple=False,_value='',_onchange='',can_add=False,add_empty_first=True):
    '''
        make 1 select html object
        update 01/08/09 ks
        _options:list or dict
    '''
    #convert _options :list to dict
    _dict={x:x for x in _options} if type(_options)==list else _options
    vs=''
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
    if _multiple:
        sel['_multiple']='multiple'#_multiple
        print ("multiple"+str(_multiple))
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