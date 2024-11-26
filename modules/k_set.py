# k-set = setting file of ks
import os
class WEB2PY:
    run=True if os.getcwd().split('\\')[-1]!='web2py' else False
    path=r'C:\pro\prog' if os.environ['COMPUTERNAME']=='DESKTOP-IDTS8DD' else r'D:\ks\I'
    #DESKTOP-IDTS8DD = Home laptop
    app_path=path+r'\web2py\applications'
class K_set:  
    recycle=r'c:\temp\recycle' #share.base_path_recycle_delete}
    dropbox_py_path=r'C:\Users\Ksaadati\Dropbox\1-my-data\0-py\0-ok'
    #report_html_path=dropbox_py_path+r'\lib\report\report_inf.htm'
    report_html={'path':'c:\\temp\\report\\',
                'name':'report_inf',
                'ext':'.htm'}
    report_html['fullname']=report_html['path']+report_html['name']+report_html['ext']
    report_html['htm_report_fullname']=report_html['path']+"htm_rep_"+report_html['name']+report_html['ext']
    share_inf={ 'share':'اشتراک فایل',
            'paper;pre':'محل پیش نویس نامه ها'}
    def report_err_fname_crt(self,ext="htm"):
        import k_date
        return self.report_html['path']+"err-report__"+k_date.ir_date("yy-mm-dd__hh-gg-ss")+"."+ext
'''
x_dic={'a':'b',
    'c':'d'}
class x_class:
    a1='b1'
    c1='d1'
use:

from k_set import x_dic
from k_set import x_class
    x=x_dic['a']
    b=x_class.a1    
'''
#----
def xpath(file_name=''):
    xpath='d:\\ks\\0-file\\' #or xpath=os.getcwd()+"\\file"
    #xpath=os.getcwd()+"\\"+path if not ':' in path else path
    from gluon import current
    session=current.session
    request=current.request
    if session["admin"] or 'share_for_all' in file_name:
        if request.vars['drive']:
            xpath= request.vars['drive'] + ':\\'
        elif request.vars['xpath']:
            xpath= request.vars['xpath'] + '\\'
    #print('xpath =>xpath ='+xpath)         
    return xpath.replace('/','\\')