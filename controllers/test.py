def xxx():
    def save(text_app):
        def get_vv(f_nxt_s,f_nxt_s_new):
            steps=x_data_s['steps']
            step=steps[list(steps.keys())[f_nxt_s]]
            step_flds=step['tasks'].split(',')
            rv=list(request.vars)
            #breakpoint()
            vv={t:request.vars[t] for t in rv if t in step_flds }
            vv.update({ f'step_{f_nxt_s}_un':session['username'],
                        f'step_{f_nxt_s}_dt':k_date.ir_date('yy/mm/dd-hh:gg:ss'),
                        f'step_{f_nxt_s}_ap':request.vars['text_app'],
                        'f_nxt_s':str(f_nxt_s_new),
                        'f_nxt_u':''
                        })
            return vv
        def update(text_app):
            xi,r1,rows_num='','',''
            if text_app=='r': 
                xi,r1,rows_num=db1.row_backup(tb_name,xid)
                f_nxt_s_new=f_nxt_s-1
            elif text_app=='x':
                pass
            elif text_app=='y':
                f_nxt_s_new=f_nxt_s+1
            vv=get_vv(f_nxt_s,f_nxt_s_new)    
            xu = db1.update_data(tb_name,vv,{'id':xid})
            rr=f"{db1.get_path()}<br> UPDATE: "+str(xu)+"<hr> backup<br>xi="+str(xi)+"<br> r1="+str(xi)+ "<br> rows_num="+str(rows_num)
            #+"<brr>vv"+str(vv)+"<br>vars:"+str(list(request.vars))+"<br>titels:"+str(titles)
            return rr
        def insert():
            vv=get_vv(0,1)
            xi,r1=db1.insert_data(tb_name,vv.keys(),vv.values())
            rr=f"{db1.get_path()}<br> INSERT:result="+str(r1)+" => "+str(xi)+" | "+str(r1) #+"<hr>"+str(vv)
            return rr
        #--------------------------------    
        if xid==-1:
            r1=insert()
        else:
            r1=update(text_app)
        return DIV(XML(r1))
def wday():
    import k_date
    return k_date.ir_weekday(name=True)
            