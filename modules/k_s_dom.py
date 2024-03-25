# -*- coding: utf-8 -*-
# ver 1.00 1401/10/10 
"""
    web2py server dom object help 
    
    >>> a = DIV(SPAN('a', 'b'), 'c')
    >>> print a
    <div><span>ab</span>c</div>
    >>> del a[1]
    >>> a.append(B('x'))
    >>> a[0][0] = 'y'
    >>> print a
    <div><span>yb</span><b>x</b></div>
    
    Attributes of helpers can be referenced by name, and helpers act as dictionaries with respect to their attributes:

    >>> a = DIV(SPAN('a', 'b'), 'c')
    >>> a['_class'] = 's'
    >>> a[0]['_class'] = 't'
    >>> print a
    <div class="s"><span class="t">ab</span>c</div>
"""
from gluon.html import *
# -------------------------------------------------------------------------
def tag_name(tag):
    import re
    '''
    input:
    ------
        tag:web2py server dom object 
    '''
    return re.search('</\s*(\w*)\s*>',str(tag)).group(1)
def tags_list(html):
    '''
    input:
    ------
        html:str
            html in text format
    '''
    tags=html.split('<')
    return [f'<{x}' for x in tags[1:]] 
def tag_set_by_jad_list(tag,jad,html):
    '''
    input:
    ------
        tag:web2py server dom object 
        jad:list    
            list of born_number for each ajdad of person
            born_number=index number for each child in 1 h
        html:str
            html in text format
    '''
    indx=''.join([f'[{i}]' for i in jad])
    rp=XML(html)
    exec(f'tag{indx}=rp')
def find_item(h_o,txt,jad=[]):
    """
    input:
    ------
        h_o:web2py server dom object 
            =html_object
            target for search in it
        txt:str
            match text= search for find like it
        jad:list    
            list of born_number for each ajdad of person
            born_number=index number for each child in 1 h
    output:
    ------
        find_list=[[obj,name,jad,content],...]
        بعد از استفاده از این تابع برای مقدار دهی به عبارات پیدا شده به ترتیب زیر عمل می کنیم 
            برای مقدار دهی به مقدار متنی شی پدا شده
            for change text of finds object =>
                find_list[i][0][0]='newtext' 
                    i:indx in find_list
                    0=obj in find_list[i]
                    0=text ib find_list[i][0]
            for change object tag=>
                k_s_dom.tag_set_by_jad_list(tag=h_o,jad=find_list[i][2],html=XML(html))
    """
    def x_len(tag):
        try:
            return len(tag)
        except:
            return 0
    ff=[]
    for i,tag in enumerate(h_o):
        #print(f"{len(tag)}--{tag}") 
        if type(tag)!='bytes': # 'gluon.html.__tag_div__': #
            tag_e_n=x_len(tag)
            #print(f"tag_e_n={tag_e_n}--tag={tag}") 
            if tag_e_n==1:
                if txt in str(tag):
                    name=tag_name(tag)
                    #print (f'name={name}')
                    #h_o[i]=DIV(TAG[name]('==='))
                    ff+=[[h_o[i],name,jad+[i],tag[0].decode("utf-8")]]
            elif tag_e_n>1:
                #print (f'tag={tag}')
                ff+=find_item(tag,txt,jad+[i])
    return ff
def test():
    for i,x in enumerate(h_o.elements()):
        print (f"{i} - {len(x.elements())} --: {x}")
        if len(x.elements())==1:
            if '$$' in str(x):
                print("*"*70)
                x[0]='*'*20
    #-------------------------------
"""
    xx=h_o.elements(find='step') => xx=[]
    
    -----------------------------------------
    x1=re.sub('<p>(.*)\$\$l(.*)</p>',r"</div><div dir='ltr'>\1 \2",html) 
    x2=re.compile('<p>(.*)\$\$([r,l])(.*)</p>', flags=re.S).sub(repl,html)#r"</div><div dir='rtl'>\1 \2",x1)
    return "<div>"+x2+"</div>"    
    return "<div>"+html.replace('<p>$$l</p>',"</div><div dir='ltr'>").replace('<p>$$r</p>',"</div><div dir='rtl'>")+"</div>"   
    
"""    


            