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
class C_TAG():
    
    def __init__(self,tag=''):
        import gluon
        if tag:
            tag=TAG(tag) if not type(tag) in [gluon.html.__tag_div__] else tag
            self.inf=self.tag_inf(tag)
        else :
            self.inf=''
        self.tag=tag
        self.find_tag=''
    def tag_inf(self,tag=''):
        import gluon
        if not tag:tag=self.find_tag or self.tag
        inf={x:(tag["_"+x] or '') for x in['id','name','class','style','onclick','onchange','object']}
        inf['type']='gluon.html.__tag_div__'
        inf['attr_len']=len(tag.attributes)
        inf['attr']=str(tag.attributes)
        inf['tag']=str(tag.tag)
        inf['text']=[]
        inf['el_tree']=[] #elements tree
        inf['elements']=str([x.tag for x in tag.elements()])
        inf['txt']=tag.flatten()#eval().get('value')#','.join([x[0].decode() for x in tag.elements()])
        items=[]
        for x_part in tag:
            if type(x_part) in [gluon.html.__tag_div__]:
                tip=self.tag_inf(x_part)
                items+=[tip]
                inf['text']+=[str(tip['text'])]
                inf['el_tree']+=[[tip['tag'],tip['el_tree']]]
                
            else:
                items+=[{'value':x_part,'type':'str'}]#str(type(x_part))}]
                inf['text']+=[str(x_part)]
                inf['el_tree']+=['str']
        inf['items']=items
        inf['text']=",".join([str(x) for x in inf['text'] if x])
        inf['el_tree_x']=str(inf['el_tree'])
        inf['title']=tag['_title'] if tag['_title'] else ''
        inf['str']=str(tag['value'])
        return inf
    def txt_inf(tag):
        for x in tag.elements():
            x=','.join([x[0].decode() for x in tag.elements()])
    def _find(self ,attr,tag):
        import gluon
        if attr in tag.attributes:return tag
        #res1=str(tag.attributes)+"$"+attr
        for x_part in tag:
            
            if type(x_part) in [gluon.html.__tag_div__]:
                res=self._find(attr,x_part)
                if type(res) in [gluon.html.__tag_div__]:return res
                #res1+="<br>a"+str(type(x_part))+":"+res+":"
        #return res1
    def find(self ,attr,tag=''):
        if not tag:tag=self.tag
        x=self._find(attr,tag)
        if x:return x[attr]
        #self.find_tag=
        #return self.find_tag
def report_tag(x_htm):
    import gluon,k_htm
    '''
        report all tag in str by gloun module
    '''
    
        
    ob=TAG(x_htm) if not type(x_htm) in [gluon.html.__tag_div__] else x_htm
    #yy=[y for y in ob]
    #txt_o+=["###"+str(yy)] 
    txt_o=[]
    txt_o+=[str(x_htm)]#BEAUTIFY(htm_str).xml()
    txt_o+=[C_TAG().tag_inf(ob)]
    txt_o+=[(dir(ob))]
    txt_o+=[ob.xml()]
    
    return dict(x1="x", #k_htm.val_report_prety(txt_o),
                x=k_htm.val_report(txt_o))
  
                    

            