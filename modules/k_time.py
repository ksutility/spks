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