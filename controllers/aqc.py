# -*- coding: utf-8 -*-

#from gluon.custom_import import track_changes; track_changes(True)
#import aqc_paper as gods
def import_paper_inf():
    paper=request.args(0)
    #gods.import_paper_inf(paper,'yes','io')
    import os
    p1='D:\\pro\\ext\\WPy64-3850\\IDLEX.exe'
    f1='C:\\Users\\Ksaadati\\Dropbox\\1-my-data\\0-py\\0-ok\\0-base\\0_aqc_paper-ui.py'
    pp=p1+' -r '+ f1 + " 'import_paper_inf({})'".format(paper)
    os.system(pp)
    return repr(pp)+'\n=>done'