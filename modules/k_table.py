# -*- coding: utf-8 -*-
"""
@author: ks
creat = 1402/11/17
"""
from gluon.html import *
#-------------------------------------------------------------------------------------------------------------------------------
class K_TABLE:
    def creat_htm(rows,titles,table_class="0",add_index=False,div=False):#table_type=""
        '''
            old name= htm_table
        '''
        if add_index:
            titles=['i']+titles
        if type(titles)==list:
            thead=THEAD(TR(*[TH(x) for x in titles]))#,_style="top:0;position: sticky;")
        else:  #type(titles)==dict:
            thead=THEAD(TR(*[TH(x,_width=y.get('width'),_title=y.get('title')) for x,y in titles.items()]))
        trs=[]
        if div:
            if add_index:
                for i,row in enumerate(rows):
                    trs.append(TR([i+1]+[DIV(x) for x in row]))
            else:
                for i,row in enumerate(rows):
                    trs.append(TR([DIV(x) for x in row]))
        else:
            if add_index:
                for i,row in enumerate(rows):
                    trs.append(TR([i+1]+row))
            else:
                for i,row in enumerate(rows):
                    trs.append(TR(row))
        cc='table'+ table_class if (table_class !="-1") else 'table table-sm table-hover table-responsive'
        #
        return DIV(TABLE(thead,TBODY(*trs),_class="w-auto "+cc),_class="div_table") #DIV(,_style='height:100%;overflow:auto;')