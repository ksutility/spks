#010929
import jdatetime #khayyam
import time
today=jdatetime.date.today().strftime('%y-%m-%d') #khayyam.JalaliDate.today().strftime('%y-%m-%d')
now=time.strftime("%H%M%S", time.localtime())
from datetime import date
def i_date():
        x = date.today()
        m = x.month-2
        mt ='0123456789abc'[m]
        d = x.day-21
        if d<1:d+=30
        dt = '{:0>2}'.format (d)
        return {'d':d,'m':m,'iso':mt + dt}
def ir_date(xformat='',add=0):
    date_obj=jdatetime.date.today()+jdatetime.timedelta(days=add)
    date_txt=(date_obj).strftime('%Y-%m-%d')
    yyyy,mm,dd=date_txt.split('-')
    yy=yyyy[-2:]
    now=time.strftime("%H:%M:%S", time.localtime())
    hh,gg,ss=now.split(':')
    w,ww,www=ir_weekday(in_time=date_obj,w_case=4)
    ll={'yyyy':yyyy,'yy':yy,'mm':mm,'dd':dd,
        'hh':hh,'gg':gg,'ss':ss,
        'w':str(w),'ww':ww,'www':www}
    if xformat:  
        for x in ll:
            xformat=xformat.replace(x,ll[x])
        return xformat
    else:
        return ll
def date_dif(time2,time1,in_format,out_format="DDD+hh:gg"):
    t1=split_by_format(time1,in_format,int_str='int')
    t2=split_by_format(time2,in_format,int_str='int')
    t3={}
    for x in t1:
        t3[x]=t2[x]-t1[x]
        #difference of date in minutes
    if t3['ss']<0:t3['ss']+=60;t3['gg']-=1
    if t3['gg']<0:t3['gg']+=60;t3['hh']-=1
    if t3['hh']<0:t3['hh']+=8;t3['dd']-=1
    if t3['dd']<0:t3['dd']+=30;t3['mm']-=1
    if t3['mm']<0:
        t3['mm']+=12
        if t3['yy']:
            t3['yy']-=1
        else:
            t3['yyyy']-=1
    t3['DDD']=(t3['yy']+t3['yyyy'])*365+t3['mm']*30+t3['dd']

    for x in t3:
        t3[x]=f"000{t3[x]}"[-len(x):]
  
    return out_in_format(t3,out_format)
#xprint (ir_date('yy-mm-dd-hh-gg-ss'))
#xprint (i_date())
#------------------------------------------------------------
def split_by_format(in_time,in_format,int_str='int'):
    #return a k_datetime obj
    yyyy=yy=mm=dd=hh=gg=ss=''
    in_format=in_format.lower()
    t={} #get values
    ll=['yyyy','yy','mm','dd','hh','gg','ss']
    if int_str=='int':
        for x in ll:
            t[x]=int(in_time[in_format.index(x):][:len(x)]) if x in in_format else 0
    else: #str
        for x in ll:
            t[x]=in_time[in_format.index(x):][:len(x)] if x in in_format else ""
    return t
#---------------------------------------------------------------------    
def change_format(in_time,in_format,out_format):
    #old name =date_change_format
    dt=split_by_format(in_time,in_format,'str') #dt=k_datetime obj
    return out_in_format(dt,out_format)
def out_in_format(dt_obj,out_format):
    #dt =date_time dict format ['yyyy','yy','mm','dd','hh','gg','ss' + 'DDD']
    #out_format=out_format.lower()
    #xprint(out_format)   
    for x,y in dt_obj.items():
        out_format=out_format.replace(x,y)
    return out_format

#xprint (date_dif('01/09/18 16:45','01/08/19 17:55','yy/mm/dd hh:gg'))
def ir_weekday(in_time=jdatetime.date.today(),in_format='yyyy/mm/dd',w_case=0):
    import datetime
    if type(in_time)==tuple:
        in_time=jdatetime.date(in_time)
    elif type(in_time)==str:
        ids=ir_date_split(in_time,in_format)
        #print(str(ids))
        in_time=jdatetime.date(ids['yyyy'],ids['mm'],ids['dd'])
    wd_e=in_time.togregorian().weekday()
    wd_f=(wd_e+2) % 7
    w_days=[[0,1,2,3,4,5,6],
            ['ش','1ش','2ش','3ش','4ش','5ش','ج'],
            ['شنبه','1 شنبه','2 شنبه','3 شنبه','4 شنبه ','5 شنبه ','جمعه']]
    if w_case==4:
        return w_days[0][wd_f],w_days[1][wd_f],w_days[2][wd_f] 
    elif w_case==3:
        t1,t2=w_days[1][wd_f],w_days[2][wd_f]  
        return f"<a title='{t2}' class='btn btn-light'>{t1}</a>"
    else:
        return w_days[w_case][wd_f] 
    
    #x=datetime.date(2008, 6, 24).weekday()
    #xprint(x1,x2)
    #x=datetime.date(2008, 6, 24).weekday() 0=monday,6=sunday
def site_time():
    #=k_date.ir_date('yy/mm/dd-hh:gg:ss')}}-
    ird=ir_date() #irdate
    t0,t1,t2=ir_weekday(w_case=4)
    xcs="class='btn btn-light mx-n1 px-2' style='background-color:#429bca;color:#fff'"
    xs1="style='color:#f55;'"#margin:3px
    return f"""<h5 dir="lrt">
                <i title='{t2}' {xs1}>{t1}</i>
                 
                {ird["hh"]}:{ird["gg"]}
                {ird["yy"]}/{ird["mm"]}/<i {xs1}>{ird["dd"]}</i> 
                <h5>
                """
    return f"""
                <a title='{t2}' {xcs}>{t1}</a>
                <a title='{ird["hh"]}:{ird["gg"]}:{ird["hh"]}' {xcs}>{ird["hh"]}:{ird["gg"]}</a>
                <a title='{ird["yyyy"]}/{ird["mm"]}/{ird["dd"]}' {xcs}>{ird["dd"]}</a>
                
                """
    return f"""<div dir="rtl" class="row ">
                <div title='{t2}' class='col  btn btn-light mx-auto p-1'>{t1}</div>
                <div title='{ird["hh"]}:{ird["gg"]}:{ird["hh"]}' class='col  btn btn-light mx-0 p-1'>{ird["hh"]}:{ird["gg"]}</div>
                <div title='{ird["yyyy"]}/{ird["mm"]}/{ird["dd"]}' class='col  btn btn-light mx-0 p-1'>{ird["dd"]}</div>
                
                
            </div>"""
def ir_date_split(in_time,in_format='yyyy/mm/dd',x_mode='int'):
    l=len(in_time)
    r_o={}
    for x in ['yyyy','mm','dd']:
        n=in_format.index(x)
        xx=in_time[n:n+len(x)]
        r_o[x]=int(xx) if x_mode=='int' else xx
    return r_o
    
class C_IR_DATE():
    def from_en_strptime(self,en_strptime,strptime_format='%m/%d/%y %H:%M:%S'):
        import datetime
        inputDate = datetime.datetime.strptime(en_strptime,strptime_format )
        self.from_timestomp(inputDate.timestamp())
        return self
    def from_timestomp(self,timestomp):
        self.date_obj=jdatetime.datetime.fromtimestamp(timestomp)
        return self
    def out(self,xformat):
        date_obj=self.date_obj.strftime('%Y-%m-%d')
        date_txt=date_obj
        yyyy,mm,dd=date_txt.split('-')
        yy=yyyy[-2:]
        now=time.strftime("%H:%M:%S", time.localtime())
        hh,gg,ss=now.split(':')
        w,ww,www=ir_weekday(in_time=date_obj,w_case=4)
        ll={'yyyy':yyyy,'yy':yy,'mm':mm,'dd':dd,
            'hh':hh,'gg':gg,'ss':ss,
            'w':str(w),'ww':ww,'www':www}
        if xformat:  
            for x in ll:
                xformat=xformat.replace(x,ll[x])
            return xformat
        else:
            return ll

#-----------------
#print(C_IR_DATE().from_en_strptime("2024-03-24","%Y-%m-%d").out('yyyy-mm-dd'))
def tatil_mode(x_date,out_case='num'):
    iw=ir_weekday(x_date)
    ids=ir_date_split(x_date,x_mode='str')
    a_tatil={
        'all':'0101,0102,0103,0104,0112,0113,0314,0315,1122,1229,1230',
        '1403':'0122,0123,0215,0328,0405,0425,0426,0604,0612,0614,0622,0631,0915,1025,1109,1126',
    }
    b_tatil={
        '1403':'0302,0303,0507,0518,0925,0926,0927,1022,1120,1121,1123'
        #.split(','),
    }
    xx=ids['mm']+ids['dd']
    #print(str(ids) +" ---- " + xx )
    rr=0
    if iw==6:
        rr= 1
    elif (xx in a_tatil['all']) or (xx in a_tatil['1403']):
        rr= 2
    elif (xx in b_tatil['1403']):
        rr= 3
    #print(str(ids) +" ---- " + xx + " *** " + str(rr) )
    if out_case=='color':
        return ['#efe','#f00','#fa5','#f5a'][rr]
    else:
        return rr
    #yy,mm,dd
def ir_mon_len(yy_n,mm_n):
    if mm_n < 7:
        return 31 
    if mm_n < 12 :
        return 30
    if yy_n in [1403]:
        return 30
    return 29
def st_date(yyyy,mm,dd):
    return str(yyyy)+"/"+("0"+str(mm))[-2:]+"/"+("0"+str(dd))[-2:]