# -*- coding: utf-8 -*-
"""
Created on 1402/12/17 
    @author: ks
    last update 1402/12/17
"""
#k_form
def template_parser(x_template,x_dic={}):
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
            print(xx)
            print(x_dic)
            x1= template.render(content=xx,context=x_dic) 
            print(x1)
            return x1.format(**x_dic)  #remove 020926
        except Exception as err:
            from k_err import xxxprint
            xxxprint(msg=['err',err,x_template],err=err,vals=x_dic,launch=True)
            return 'error in template_parser :'+str(err)
            print('error in template_parser')
    else:
        return x_template