# -*- coding: utf-8 -*-
"""
Created on 1402/12/17 
    @author: ks
    last update 1402/12/17
"""
#k_form
def template_parser(x_template,x_dic={},do_format=True):
    '''
    use in kswt:ok 020905
    rename:021126 - old name=format_parser
    func type : simple 
    goal:
    ------
        out_source template_parser =to=> web2py>gluon>template
        help:
            https://web2py.readthedocs.io/en/latest/template.html
    input:
    ------
        x_template:str
            input template str 
            python str by internal code in {{}} =like=> 'abc {{=x}} de{{=y[2]}}f'
        x_dic=dict
            {VAR1:VAL1,...} = var set dict  
                
    ------
    Usage examples:
    >>> template_parser("""abc-{{=a}}""",{'a':'abc'})
    abc-abc
    >>> template_parser("""abc-{{=a.upper()}}""",{'a':'abc'})
    abc-ABC
    >>> template_parser("""abc-{{=a[2].upper()}}""",{'a':'abc'})
    abc-C
    '''
    #return x_template.format(task=task_inf,step=form['steps'],session=session,**x_dic)
    if type(x_template)==str:
        try:
            xx=x_template.strip()
            from gluon import template
            #print(xx)
            #print(x_dic)
            x1= template.render(content=xx,context=x_dic) 
            #print(x1)
            if do_format:
                return x1.format(**x_dic)  #remove 020926
            else:
                return x1
        except Exception as err:
            from k_err import xxxprint
            xxxprint(msg=['err',err,x_template],err=err,vals=x_dic,launch=True)
            return 'error in template_parser :'+str(err)
            #print('error in template_parser')
    else:
        return x_template
from k_err import xxprint,xprint
def end_with(txt,ew):
    n=len(ew)
    return (txt[-n:]==ew)
def compare_2_str(str1,str2):
    '''
    compare 2 str and make 1 brif report
    '''
    str1=str1.strip().replace(" ",".")
    str2=str2.strip().replace(" ",".")
    #res={'dif_n':0}
    if str1!=str2:
        l1=len(str1)
        l2=len(str2)
        cm1=''
        cm2=''
        dif_n=0
        l=l1 if l1<l2 else l2
        for i in range(l):
            if str1[i]==str2[i]:
                cm1+="_"
                cm2+="_"
            else:
                dif_n+=1
                cm1+=str1[i]
                cm2+=str2[i]
        if l1==l2:
            return (f'(dif={dif_n}, len={l1},{l2} : {cm1} != {cm2})')
        elif l==l1:
            return (f'(dif={dif_n}+, len={l1},{l2} ,ex = {str2[l:]} : {cm1} != {cm2}{str2[l:]})')
        else:
            return (f'(dif={dif_n}+, len={l1},{l2} ,ex = {str1[l:]}:  {cm1}{str1[l:]} != {cm2} )')
    else:
        return '='
def do_compare_2_str():
    while True:
        x=ui.input([['str1',''],['str2','']])
        if not x:break
        xprint(compare_2_str(x['str1'],x['str2']))
#----------------------------------------------------------------------------
def correct_fa(str1):
    r1='ي'
    r2='ي'
    str1=str1.replace(r2,r1)
    r2='ك'
    r1='ک'
    str1=str1.replace(r2,r1)
    '''
    if r1 in str1:print ('r1:'+str(list_all_index(str1,r1)))
    if r2 in str1:print ('r2:'+str(list_all_index(str1,r2)))
    str1=str1.replace(r2,r1)
    print('-'*10+' replced ')
    if r1 in str1:print ('r1:'+str(list_all_index(str1,r1)))
    if r2 in str1:print ('r2:'+str(list_all_index(str1,r2)))
    '''
    return str1
def do_correct_fa():
    res=''
    while True:
        x=ui.input([['result',res],['new_str','']])
        if not x:break
        res=correct_fa(x['new_str'])
def list_all_index(str_base,chr_search):
    return [i for i,t in enumerate(str_base) if t==chr_search]
if __name__ == "__main__":
    import tk_ui as ui
    while True:
        x=ui.input([['pro',['correct_fa','compare_2_str'],'c']])
        if not x:break
        xx='do_'+x['pro']+'()'
        #print(xx)
        exec(xx)