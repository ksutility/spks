# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
from gluon.custom_import import track_changes; track_changes(True)
from datetime import datetime
from k_sql import DB1
import kytable
now = datetime.now().strftime("%H:%M:%S")

db1=DB1('example2.db')
style='''
        <style>
            table {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              width: 100%;    }

            table td, #customers th {
              border: 1px solid #ddd;
              padding: 8px; }

            table tr:nth-child(even){background-color: #f2f2f2;}

            table tr:hover {background-color: #ddd;}

            table th {
              padding-top: 12px;
              padding-bottom: 12px;
              text-align: left;
              background-color: #04AA6D;
              color: white; }
        </style>
      '''
def f_cod(s1, enc_st='09377953310'):
    return s1
    s2=enc_st*5
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])
def set_table(db_name):

    db1.define_table("paper1", fields_txt='''
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lno TEXT NOT NULL,
                    prj TEXT NOT NULL,
                    sbj TEXT NOT NULL,
                    i_per TEXT NOT NULL,
                    i_des TEXT NOT NULL,
                    i_end TEXT,
                    i_date TEXT,
                    table_name TEXT,
                    fill_date,
                    UNIQUE(lno, sbj,i_per,i_des,i_date)''')
    db1.define_table("paper", fields_txt='''
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lno TEXT NOT NULL,
                    prj TEXT NOT NULL,
                    fill_date''')
    db1.define_table("prj", fields_txt='''
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    des TEXT NOT NULL''')
    db1.define_table("user", fields_txt='''
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    un TEXT NOT NULL,
                    ps TEXT NOT NULL,
                    job TEXT,
                    full_name TEXT NOT NULL''')
    db1.define_table("job", fields_txt='''
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL''')
def set_table_4_fildes(db_name,fildes):
    for table in fildes:
        t1="id INTEGER PRIMARY KEY AUTOINCREMENT,"
        for itm in fildes[table]:
            t1+=f"{itm['name']} TEXT,"
        t2=t1[:-1]
        db1.define_table(table, fields_txt=t2)


fildes={'paper':[{'name':'lno','type':'text','title':'شماره نامه','disabled':1},
                 {'name':'sbj','type':'text','title':'موضوع نامه','disabled':1},
                 {'name':'x_date','type':'text','title':'تاریخ ارجاع','disabled':1},
                 {'name':'comment','type':'text','title':'خلاصه','disabled':1},
                 {'name':'prj_x','type':'text','title':'پرژ'},
                 {'name':'prj','type':'reference prj name','title':'پروژه'}],#,
                 #{'name':'fill_date','type':'fdate','title':'تاریخ تکمیل'}],
        'prj':[{'name':'name','type':'text','title':'نام پروژه'},
               {'name':'des','type':'text','title':'توضیحات'}],
        'user':[{'name':'username','type':'text','title':'نام کاربری'},
                {'name':'password','type':'text','title':'پسورد'},
                {'name':'name_add','type':'text','title':'پیش نام'},
                {'name':'fullname','type':'text','title':'نام کامل'},
                {'name':'job','type':'reference job name','title':'سمت'}],
        'job':[{'name':'name','type':'text','title':'سمت'}]

       }

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def index():
    redirect(URL('spks','user','login',args=['go']))
    response.flash = T("سیستم مدیریت محتوا")
    im_url=URL('spks','static','images/AQC-entrance-web-page-030401.jpg')
    login_ulr=URL('spks','user','login')
    x_url=URL('spks','static','images/AQC-')
    html=f"""
        <body style="background-image: url('{im_url}');">
        <div>سیستم مدیریت محتوا</div>
        </body>
    """
    url2=URL('spks','form','list_0')
    url3=URL('spks','user','login',args=['go'])
    return dict(im_url=im_url,login_ulr=login_ulr,x_url=x_url,m1=T('سیستم مدیریت محتوا'),m2=T('-'),m3=T('Kind Smart Web Tools'),
        link=A('ورود', _href=url3,_class="btn btn-primary"))
def index1():
    t=[ A('جداول اطلاعات',_href=URL('data','index')),
        A('ویرایشگر اتوکد',_href=URL('acpe','index'))
        ]
    if session["admin"]:
        t+=[HR(),
            A('set_tables',_href=URL('set_tables')),
            HR(),
            A('test2',_href=URL('test2')),
            A('admin',_href=URL('admin')),
            DIV(f_cod(f_cod('kurosh')))
        ]
    return dict(m=TABLE(*t))
def admin():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))
def set_tables():
    set_table(db_name)
    return 'tables created'
def prj3():
    """ this controller returns a dictionary rendered by the view
        it lists all wiki prjs
    >>> index().has_key('prjs')
    True
    """
    #prjs = db().select(db.prj.id,db.prj.title,db.prj.des,orderby=db.prj.title)
    grid = SQLFORM.grid(db.prj,deletable=False)#, linked_tables=['post'])
    #form = SQLFORM(db.prj).process(next=URL('prj'))
    #return dict(prjs=prjs,grid=grid,form=form)
    return dict(grid=grid)
def prj1():
    """ this controller returns a dictionary rendered by the view
        it lists all wiki prjs
    >>> index().has_key('prjs')
    True
    """
    prjs = db().select(db.prj.id,db.prj.title,db.prj.des,orderby=db.prj.title)
    #grid = SQLFORM.grid(db.prj,deletable=True)#, linked_tables=['post'])
    #form = SQLFORM(db.prj).process(next=URL('prj'))
    #return dict(prjs=prjs,grid=grid,form=form)
    return dict(prjs=prjs)
def sub_prj1():
    tb=db.sub_prj
    grid = SQLFORM.grid(tb,deletable=False,fields=[tb.id,tb.title,tb.des,tb.prj_id])#, linked_tables=['post'])
    return dict(grid=grid)

def table():
    return dict(table=data_show_simple(db_name))
def test2():
    t0=",".join([x+"="+str(request.vars[x]) for x in request.vars ])  if request.vars["a"] else ""
    t1= '''
        <div class='div_t'><input type='text' id='xDATE1' name='xDATE1' class='in_a' value='1400/07/01'>از تاریخ</div>
        <div class='div_t'><input type='text' id='xDATE2' name='xDATE2' class='in_a' value='1400/08/01'>تا تاریخ</div>
    '''
    '''
        <select name="states2" multiple="multiple" style="width:900px">
          <option value="AL">Alabama</option>
          <option value="xx">xxxx</option>
          <option value="WY">Wyoming</option>
        </select><br>
        <select name="states" style="width:900px">
          <option value="AL">Alabama</option>
          <option value="xx">xxxx</option>
          <option value="WY">Wyoming</option>
        </select><br>
    '''
    s1=htm_select(_options={'AL':'Alabama','xx':'xxxx','WY':'Wyoming'},_name='state2',_title='#',_multiple="multiple",_value=request.vars['state2'])
    s2=htm_select(_options={'AL':'Alabama','xx':'xxxx','WY':'Wyoming'},_name='state1',_title='#',_value=request.vars['state1'])
    t2=htm_select(_options=['1','2','3'],_name='a1',_title='#')#SELECT('1','2','3',_name="b",_style="width:900px")
    t3=DIV(INPUT(_name="a",_class='fDATE',_value='1400/07/01'),'از تاریخ')
    #t3=XML('''<div class='div_t'><input type='text' id='xDATE1' name='xDATE1' class='in_a' value='1400/07/01'>از تاریخ</div>''')
    #return dict(txt=style+str(t1)+"<hr>"+str(table)+str(t2)+str(t3))
    ss=htm_select(_options={'1':'a','2':'b'},_name='abc',_title='#')
    su=INPUT(_type='submit')
    ff=FORM(XML(t1),s1,s2,t2,t3,ss,su, _action='', _method='post')
    return dict(t0=t0,ff=ff)


@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

# controllers/default.py
folder = r'''D:\ks\0-file\AUTO\form\image''' #+'\\' 
# 'D:/external_images/'

def serve_external_image():
    import os
    from gluon.contenttype import contenttype

    filename = request.args(0)
    full_path = os.path.join(folder, filename)

    if not os.path.isfile(full_path):
        raise HTTP(404, "File not found")

    response.headers['Content-Type'] = contenttype(full_path)
    return response.stream(full_path)

# در همان کنترلر
def image_list():
    import os
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return dict(files=files)
