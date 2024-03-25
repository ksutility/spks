#tk_ui ver=1.03 1401/07/09 
'''     
        label (input[0])=> name (input[0]) , label(input[3]) : (for each var)
    1.03 1401/07/09
        add dict type input to input function   
'''
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
g_row=0 #global row
width=50
res=''
def _set_row(row):
    global g_row
    if row==-1:
        row=g_row
    g_row +=1
    return row
def _out_label(app,label,row):
    #CREAT 1 LABEL CELL IN LEFT OF A UI OBJECT 
    label_o = tk.Label(app,text = label,width=30,anchor='w')
    label_o.grid(column=0, row=row, sticky=tk.W)
def _add_report_2cell(app,label,report='',row=-1):  
    row=_set_row(row)
    _out_label(app,label,row)
    report_o = tk.Label(app,text = report,width=width,anchor='w')
    report_o.grid(column=1, row=row, sticky=tk.W)
def _add_input(app,label,defult='',row=-1):
    row=_set_row(row)
    _out_label(app,label,row)
    i_string = tk.StringVar()
    input_o= tk.Entry(app, width=width, textvariable=i_string)
    i_string.set(defult)
    input_o.grid(column=1, row=row) #, padx=10)#.pack()
    return i_string
def _add_text(app,label,defult='',row=-1):
    row=_set_row(row)
    _out_label(app,label,row)
    i_string = tk.StringVar()
    i_string= tk.Text(app, width=width)#, textvariable=i_string)
    #i_string.set(defult)
    i_string.insert(tk.INSERT,defult)
    i_string.grid(column=1, row=row) #, padx=10)#.pack()
    return i_string
def _add_combobox(app,label,values,defult='',row=-1):
    row=_set_row(row)
    #values=list of vlue  ==excam=>["J","e","d"] 
    _out_label(app,label,row)
    i_string = tk.StringVar()
    combobox = ttk.Combobox(app,values=values,width=width-5,textvariable=i_string)
    combobox .grid(column=1, row=row)
    if type(defult) is int:
        combobox .current(defult)
    #combobox .bind("<<ComboboxSelected>>", callbackFunc)
    #def callback():
    #   print(combobox .current(), combobox .get()
    return i_string,combobox 
def _add_ok_buttom(app,row=-1,colspan=2):
    def res_1(res_v):
        global res
        res= res_v #.cget('text')
        app.destroy()
    row=_set_row(row)
    Button = tk.Button(app, text ='cancel',width=30,command=lambda:res_1('cancel'))#command=app.destroy,width=width
    Button.grid(column=0, row=row, pady=10)# columnspan=colspan,sticky=tk.W
    Button = tk.Button(app, text ='ok',width=30,command=lambda:res_1('ok'))#command=app.destroy,width=width
    Button.grid(column=1, row=row, pady=10 )#columnspan=colspan,sticky=tk.W
    Button.focus_set() 
def _add_chekbox(app,label,values,defult='',row=-1):
    row=_set_row(row)
    _out_label(app,label,row)
    res=[]
    for v in values:
        chkValue = tk.BooleanVar() 
        #chkValue.set(True)
        chk = tk.Checkbutton(app, text=v, var=chkValue) 
        chk.grid(column=1, row=row)
        res.append(chkValue)
    return res
class _Checkbar(tk.Frame):
    def __init__(self, parent=None, label='', picks=[]):#, side=tk.LEFT, anchor=tk.W):
        tk.Frame.__init__(self, parent)
        self.vals=picks
        self.vars = []
        for index,pick in enumerate(picks):
            row=_set_row(-1)
            if index==0:_out_label(parent,label,row)
            var = tk.IntVar()
            chk = tk.Checkbutton(parent, text=pick, variable=var)
            chk.grid(column=1, row=row,sticky=tk.W)
            #.pack(side=side, anchor=anchor, expand=tk.YES)
            self.vars.append(var)
    def get(self):
        vv=list(map((lambda var: var.get()), self.vars))
        res=[]
        for index,v in enumerate(vv):
            if v==1:
                res.append(self.vals[index])
        return res
    #{v.get for v in self.vars} #list(map((lambda var: var.get()), self.vars))

def input(x_list,result_case="dic"):
    import k_err
    '''
    Parameters
    ----------
    x_list : list of v_list
        DESCRIPTION 
                    structure= list of list
                             :  [ ['name_n','default_n','case_n','help txt_n'],...] 
                    sample =  [ ['titel1','str1','','val_name1']            #input     :  ['name','default','','help txt'] 
                                ['titel2','str1','r',],                     #report    :     
                                ['titel3',list ,'c','val_name3'],           #combobox
                                ['titel4',list ,'','val_name4'],            #_Checkbar
                                ]
            val_names can be omit,titel will be copiedefult for it 
    result_case : string , optional , (1="dic"(dictionary) 2="tup"/"tuple")
        DESCRIPTION. The default is "dic".

    Returns
    -------
    dictionary or tuple
        DESCRIPTION. according to result_case
    '''
    #x_list= list of data(labels,defults,options) for each input
    global g_row
    g_row=0
    def result(result_case):
        if res=='cancel':return False
        if result_case=="dic":
            return {v:vals[v].get() for v in vals if v!='category'}
        else:
            return [vals[v].get() for v in vals]
    def import_json_from_file():
        import json
        try:
            f = open(r'c:\temp\ui_records.txt')
            data = json.load(f)
            f.close()
            return data
        except :    
            print("error: {error}\n in import_json_from_file")  
            #k_err.show()
            #export_json_to_file({})
            return {}
    @k_err.check_err
    def export_json_to_file(data):
        import json
        f = open(r'c:\temp\ui_records.txt','w')
        json.dump(data,f)
        f.close()
    def import_records():
        u_recs = import_json_from_file()
        new_rec_name="|".join([x[0] for x in x_list])
        return u_recs.get(new_rec_name,[''])
    def export_records():
        new_rec_name="|".join([x for x in vals])
        new_rec_val="|".join([str(vals[x].get()) for x in vals if x!='category'])
        u_recs = import_json_from_file()
        if new_rec_name in u_recs:
            if new_rec_val in u_recs[new_rec_name]:
                return
            else:
                u_recs[new_rec_name].insert(0,new_rec_val)
        else: 
            u_recs[new_rec_name]=[new_rec_val]
        
        export_json_to_file(u_recs)
    def reset_vals(x):
        print (x)
        text_vals=recbox.get()+"|"*len(vals)
        tvs=text_vals.split("|")
        for i,t in enumerate(vals):
            vals[t].set(tvs[i])
    app = tk.Tk() #app=window
    #import record
    recs=import_records()
    if recs!=[] :
        rec,recbox=_add_combobox(app,'record',recs,0)
        recbox.bind('<Double-1>', reset_vals)
        recbox.config({"background": "blue"})


    vals={}
    #for index,l in enumerate(labels):
    for x in x_list:
        if type(x) is not list: x=[x]
        x+=['','',''] # defults can be omit in call
        name=x[0]
        defult=x[1]
        option=x[2]
        label=x[3]
        combo_objs={}
        if label=='' :label=name
        
        if type(defult) is dict:
            kk=list(defult.keys())
            def sync_combo_child(event): #*args):
                name,default,combo_child_obj=vals['category']
                selected=event.widget.get()
                '''
                print('sync_combo_child')
                print(name+'-cat')
                print(str(default))
                print(selected)
                print(str(default[selected]))
                print(str(combo_objs.keys()))
                '''
                combo_child_obj['values']=default[selected]
                #defult[event.widget.get()] #vals[vals['cat']+'-cat'].get()]
                combo_child_obj.current(0)
            #if type(defult[0]) is list:
            
            vals[name+'-cat'],combo_cat_obj=_add_combobox(app,label+'-cat',kk,0)
            vals[name],combo_child_obj=_add_combobox(app,label,defult[kk[0]],0)
            combo_cat_obj.bind("<<ComboboxSelected>>", sync_combo_child)
            vals['category']=[name,defult,combo_child_obj]
            
        elif type(defult) is list:
            if option=='c': #combobox
                vals[name],xx1=_add_combobox(app,label,defult,0)
            else:           #chekbox
                vals[name]=_Checkbar(app,label,defult)
                #_add_chekbox(app,l,d,0)
        else:
            if option=='r': #report
                _add_report_2cell(app,label,defult)
            if option=='t': #report
                vals[name]=_add_text(app,label,defult)
            else:   
                vals[name]=_add_input(app,label,defult)
    _add_ok_buttom(app)

    app.geometry('550x{}'.format((g_row)*25+20))
    #app.focus_force()
    app.after(1, lambda: app.focus_force())
    app.mainloop()
    export_records()
    return result(result_case)
def msg(message,act='ok',titel='--'):
    message=trans_msg(message)
    app = tk.Tk()
    #app.focus_force()
    app.after(1, lambda: app.focus_force())
    if act=='ok':
        m=messagebox.showinfo(titel, message)
    elif act=='yesno':
        m=messagebox.askyesno(titel, message)
    elif act in['okcancel','+cancel']:
        m=messagebox.askokcancel(titel, message)        
    app.destroy()
    return m
def ask(message,buttoms=['ok'],case='r',titel='--'):
    message=trans_msg(message)
    app = tk.Tk()
    #app.focus_force()
    app.after(1, lambda: app.focus_force())
    tk.Label(app, text=message+"\n\n"+("-"*20),
              justify = tk.CENTER,
              padx = 20).pack()
    if case in ['b','buttom']:
    
        def res_1(res_v):
            global res
            res= res_v #.cget('text')
            app.destroy()
            
        for b in buttoms:
            tk.Button(text=b,width = 20, command=lambda:res_1(b)).pack()
            
    elif case in ['r','radio']:
        v = tk.IntVar()
        v.set(-1)  # initializing the choice, i.e. Python
    
        def ShowChoice():
            global res
            x=v.get()
            app.destroy()
            res=buttoms[x]
    
        for i,b in enumerate(buttoms):
            tk.Radiobutton(app, 
                text=b,
                indicatoron = 0,
                width = 20,
                padx = 20, 
                variable=v, 
                command=ShowChoice,
                value=i).pack(anchor=tk.CENTER)
    else:
        print(f"error in ask \n '{case}' => shoud be radio / buttom")
        quit()      
    app.mainloop()
    return res
def table(data):
    n=len(data)
    m=len(data[0])
    app = tk.Tk() #app=window
    for i_r,r in enumerate(data):
        tk.Label(app,text = f'{i_r+1}').grid(column=0, row=i_r, sticky=tk.W)
        for i_c,c in enumerate(r):
            tk.Label(app,text = c).grid(column=i_c+1, row=i_r, sticky=tk.W)
    app.geometry('{}x{}'.format(m*200,n*22+50))
    _add_ok_buttom(app,n,m)
    app.mainloop()
def _active_tk():
    import pygetwindow as gw
    tk_win = gw.getWindowsWithTitle('tk')[0]
    tk_win.activate()   
def trans_msg(msg1):
    r1=str(msg1).replace("<hr>","\n"+"-"*30+"\n")
    return r1
'''
select=tk.ttk.Combobox(values=["a","b"])
select.pack()

def callbackFunc():
    resultString.set("{} - {} - {}".format(landString.get(),cityString.get(),c_String.get()))
resultString=tk.StringVar()
resultLabel = tk.Label(app, textvariable=resultString)
resultLabel.grid(column=1, row=4, padx=10, sticky=tk.W)
'''
'''
usage:
import tk_ui
tk_ui.input(param)

    param=
        - input_label
        - [input1_label,input2_label,...]
        - [[select_opt1,select_opt2,select_opt3,...]]
        - [input1_label,input2_label,[select1_opt1,select1_opt2,select1_opt3,...],input3_label,[select2_opt1,select2_opt2,select2_opt3,...],...]
        - [<input1_inf>,<input2_inf>,...]
        <input_inf>={name:{prop_name:prop_value}}
            - {'text':{'label':'abcd','defult':'abcd'}}
            - {'select':{'label':'abcd','options':['op1','op2','op3'],'defult':'op1'},'mode':<mode>}
            <mode> =
                'radio'
                'checkbox'
                'combobox'
                ''
'''                
            
            
        
