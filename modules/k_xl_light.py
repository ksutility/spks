import pylightxl as xl
def read(wb_path,ws_name,row_st,row_en,col_st,col_en,empty_row='break'):
    # pylightxl also supports pathlib as well
    db = xl.readxl(wb_path)
    size=db.ws(ws=ws_name).size
    if not row_en :row_en = size[0] 
    #print(f" xl sixze={size}")
    #return (db.ws_names)
    tbl=[]
    for i in range(row_st,row_en+1):
        row=[]
        for j in range(col_st,col_en):
            row+=[(db.ws(ws=ws_name).index(row=i, col=j))]
        if not row[1]:
            if empty_row[0] =='b':
                break
            elif empty_row[0] == 'c':
                continue    
        tbl+=[row]
    #print(f'i={i}')
    return tbl
def size(wb_path,ws_name):
    db = xl.readxl(wb_path)
    size=db.ws(ws=ws_name).size
    return size
def write(wb_path,ws_name,new_rows):
    import k_file
    db = xl.readxl(wb_path)
    ws=db.ws(ws=ws_name)
    end_row=ws.size[0]
    for i,row in enumerate(new_rows):
        for j,cell in enumerate(row):
            ws.update_index(row=end_row+i+1, col=j+1, val=cell)
    k_file.backup(wb_path)
    xl.writexl(db=db, fn=wb_path)