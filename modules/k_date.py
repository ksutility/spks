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
def ir_date(xformat):
    xf=xformat
    today=jdatetime.date.today().strftime('%Y-%m-%d')
    yyyy,mm,dd=today.split('-')
    yy=yyyy[-2:]
    now=time.strftime("%H:%M:%S", time.localtime())
    hh,gg,ss=now.split(':')
    ll={'yyyy':yyyy,'yy':yy,'mm':mm,'dd':dd,
        'hh':hh,'gg':gg,'ss':ss}
    for x in ll:
        xf=xf.replace(x,ll[x])
    return xf
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
    #print(str(t3))
    for x in t3:
        t3[x]=f"000{t3[x]}"[-len(x):]
    #print(str(t3))   
    return out_in_format(t3,out_format)
#print (ir_date('yy-mm-dd-hh-gg-ss'))
#print (i_date())
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
    #print(out_format)   
    for x,y in dt_obj.items():
        out_format=out_format.replace(x,y)
    return out_format

#print (date_dif('01/09/18 16:45','01/08/19 17:55','yy/mm/dd hh:gg'))
