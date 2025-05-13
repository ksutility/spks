import time

class C_XL_MS():
    def __init__(self,filename='',sheet_name=''):
        import win32com.client as win32
        self.excel = win32.gencache.EnsureDispatch('Excel.Application')
        #excel = win32.Dispatch('Excel.Application')
        #excel = win32com.client.Dispatch("Excel.Application")
        if filename:
            self.filename=filename
            self.open(filename)
            if sheet_name:
                self.ws=self.wb.Worksheets(sheet_name)
                self.sheet_name=sheet_name
    def open(self,filename):
        # try except for file / path
        self.filename=filename
        try:
            self.wb = self.excel.Workbooks.Open(filename)
            return self.wb
        except com_error as e:
            if e.excepinfo[5] == -2146827284:
                print(f'Failed to open spreadsheet.  Invalid filename or location: {filename}')
            else:
                raise e
            sys.exit(1)
    def sheet(self,sheet_name):     
        self.ws=self.wb.Worksheets(sheet_name)
        self.sheet_name=sheet_name
        return self.ws
    def sheet_append_data(self,data,sheet_name='',st_row=0):
        t1=[time.time()]
        if sheet_name:
            self.sheet(sheet_name)
        t1+=[time.time()-t[0]]     
        if not st_row:st_row=self.max_row()  
        t1+=[time.time()-t[0]]   
        print(f"st_row={st_row}")  
        end_row=2000
        for i,row in enumerate(data):
            for j,cell in enumerate(row):
                self.ws.Cells(i+end_row,j+1).Value=cell
        t1+=[time.time()-t[0]]        
        print (f"time1={t1[1:]}")
        return self  
    def max_row(self,filename='',sheet_name=''):
        if not filename:filename=self.filename
        if not sheet_name:sheet_name=self.sheet_name
        import k_xl_light
        return k_xl_light.size(filename,sheet_name)[0]
    def max_row_x(self,n_empty_row=9,start_row=2,do_n=1):
        if do_n>7:return start_row
        for i in range(start_row,100000):
            if not self.ws.Cells(i,1).Value:
                break
        max_r=i-1
        print(f"max_r={max_r}")
        for i in range(max_r+1,max_r+n_empty_row+1):
            if self.ws.Cells(i,1).Value:
                break
        print(f"i={i},max_r={max_r} , n_empty_row={n_empty_row}")
        if i<max_r+n_empty_row:
            print("i<max_r+n_empty_row")
            return self.max_row(n_empty_row=9,start_row=i,do_n=do_n+1)
        return i    
    def save(self,filename=''):
        if filename:
            self.wb.SaveAs(filename)
        else:
            self.wb.Save() 
        return self    
    def close(self):
        self.wb.Close(SaveChanges=False)
        self.excel.Quit()
 
def append(wb_path,sheet_name,new_rows):
    t=[time.time()]
    c_xl_ms=C_XL_MS(wb_path,sheet_name)
    t+=[time.time()-t[0]]   
    c_xl_ms.sheet_append_data(new_rows)
    t+=[time.time()-t[0]]   
    c_xl_ms.save()
    t+=[time.time()-t[0]]   
    c_xl_ms.close() 
    t+=[time.time()-t[0]]   
    print (f"time={t[1:]}")
def report_1():
    print(excel.ActiveWorkbook.FullName)
    print(excel.ActiveWorkbook.ActiveSheet.Name)

    excel.Application.Visible = True
    _ = input("Press ENTER to quit:")

    print(len(excel.Application.ActiveWorkbook.Worksheets))
    #excel.Application.Quit()
    
    # excel can be visible or not
    excel.Visible = True  # False
    
    

    # get worksheet names        
    sheet_names = [sheet.Name for sheet in wb.Sheets]
        
    wb.Close(True)
    
    
def _val(x_str):
    try:
        return float(x_str)
    except:
        return 0
def read_row(i_row,n=0):
    sh=excel.ActiveWorkbook.ActiveSheet
    ic=0
    x_row=[]
    if n==0:
        while True:
            ic+=1
            txt=sh.Cells(i_row,ic).Value
            if txt and txt!=None:
                #print(txt)
                x_row+=[txt]
            else:
                return x_row
    else:
        for i in range(n):
            txt=sh.Cells(i_row,i+1).Value
            x_row+=[txt]   
        return x_row         
def pdd_sum_in_check_area_list():
    sh=excel.ActiveWorkbook.ActiveSheet
    last_r=['','']
    s_area=0
    for i in range(1,1080):
        rr=read_row(i,6)
        area=rr[5]
        if last_r[0]!=rr[0] or last_r[1]!=rr[1]:
            s_area=area
        else:
            if rr[2]==999:
                print (f'{round(s_area-area,3)} | {rr[0]} | {rr[1]} | {s_area}  => {area}')
            else:
                #print (s_area,rr[2])
                s_area+=_val(area)
        #print(rr)
        #print(i,sh.Cells(i,1))
        last_r=list(rr)
  