debug=False
import time,k_err
class Cornometer():
    def __init__(self,name,pre_text='',tik_print=False,):
        self.start=time.time()
        self.name=name
        self.tik_print=tik_print
        self.rec=[]
        self.last=self.start
        self.pre_text=pre_text
    def tik(self,msg):
        ct=time.time()
        x={'time':(ct-self.last),'msg':msg,'name':self.name}
        self.last=ct
        self.rec+=[x]#.insert(x)
        if self.tik_print:k_err.xprint(f'k_time.tik ({self.name})'+str(x)) 
    def records(self,msg='end'):
        self.tik(msg)
        total=self.last-self.start
        return [{'name':self.name,'start':self.start,'total':total}]+self.rec
    def report(self):
        k_err.xprint('k_time.report='+str(self.records()))
    def print(self,msg):
        if debug:
            en=time.time()
            st=self.last
            self.last=en
            print ('{} {:.4f} : {:.4f} - {:.4f} , {} , msg = {}'.format(self.pre_text,en-st,st % 1000,en % 1000,self.name,msg))
class C_TIME():
    def __init__(self,txt_time="0:0"):
        xx=txt_time.split(":")
        self.hh=int(xx[0])
        self.gg=int(xx[1])
        self.ss=int(xx[2]) if len(xx)>2 else 0
        self.sss=self.ss+self.gg*60+self.hh*3600
    def add(self,x_c_time):
        self.sss=self.sss+x_c_time.sss
        self.sss_to_time()
        return self
    def dif(self,x_c_time):
        self.sss=self.sss-x_c_time.sss
        self.sss_to_time()
        return self
    def sss_to_time(self):
        sss=self.sss
        hh=int(sss /3600)
        gg= int((sss-hh*3600) / 60)
        ss= sss-hh*3600-gg* 60
        self.hh,self.gg,self.ss,self.sss=hh,gg,ss,sss
    def out(self,format="hh:gg"):
        return format.replace('hh',str(1000+self.hh)[-2:]).replace('gg',str(1000+self.gg)[-2:]).replace('ss',str(1000+self.ss)[-2:])
    def to_minute(self):
        return self.hh*60+self.gg
def add(time1,time2,output_format="hh:gg"):
    '''
    output_format:
        hh:gg
        hh:gg:ss
    '''
    return C_TIME(time1).add(C_TIME(time2)).out(output_format)
def dif(time1,time2,output_format="hh:gg"):
    '''
    output_format:
        hh:gg
        hh:gg:ss
    '''
    return C_TIME(time1).dif(C_TIME(time2)).out(output_format) 
def sum_times(time_list):
    '''
    time_list=list of "hh:dd"
        sample ["10:15","14:20","02:50"]
    '''
    hh,mm=0,0
    for x_time in time_list:
        h1,m1=x_time.split(":")
        hh+=int(h1)
        mm+=int(m1)
    h2,m2=divmod(mm, 60)#hh=hh+mm\60
    return str(hh+h2).zfill(2)+":"+str(m2).zfill(2)
    #return round((hh+mm/60),1)
def time_2_num(x_time):
    h1,m1=x_time.split(":")[:2]
    return round(int(h1)+int(m1)/60,1)    
def time_2_min(x_time):
    h1,m1=x_time.split(":")[:2]
    return (int(h1)*60+int(m1))        
def time_div(x_time,n_div):
    gg=C_TIME(x_time).to_minute()
    gg2=int(gg/n_div)
    gg3=gg-gg2*(n_div-1)
    ggt2=min_2_time(gg2)
    ggt3=min_2_time(gg3)
    return [ggt2]*(n_div-1)+[ggt3]  
def min_2_time(x_gg,z_text=''):
    if x_gg==0 :return z_text
    h2,m2=divmod(x_gg, 60)#hh=hh+mm\60
    return str(h2).zfill(2)+":"+str(m2).zfill(2)
    
if __name__ == "__main__":
    print(add("10:20","5:55","hh:gg:ss"))
    print(dif("10:20","5:55","hh:gg:ss"))
    print(add("12:43","5:55","hh:gg"))
            