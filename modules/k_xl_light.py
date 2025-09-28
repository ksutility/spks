import pylightxl as xl

def read(wb_path, ws_name, row_st=1, row_en=None, col_st=1, col_en=None, empty_row='break'):
    """
    خواندن داده‌ها از یک فایل Excel با pylightxl

    Args:
        wb_path (str): مسیر فایل اکسل
        ws_name (str): نام شیت
        row_st (int): شماره سطر شروع (پیش‌فرض 1)
        row_en (int|None): شماره سطر پایان (اگر None باشد تا آخر شیت)
        col_st (int): شماره ستون شروع (پیش‌فرض 1)
        col_en (int|None): شماره ستون پایان (اگر None باشد تا آخر شیت)
        empty_row (str): رفتار با ردیف خالی 
                         ('break' → شکستن حلقه، 
                          'continue' → رد شدن از سطر خالی، 
                          'keep' → نگه داشتن سطر خالی)

    Returns:
        list[list]: لیست دوبعدی داده‌ها
    """

    # خواندن فایل اکسل
    db = xl.readxl(fn=wb_path)

    # اندازه‌ی شیت (تعداد سطر، تعداد ستون)
    size = db.ws(ws=ws_name).size

    if row_en is None:
        row_en = size[0]
    if col_en is None:
        col_en = size[1]

    tbl = []
    for i in range(row_st, row_en + 1):
        row = []
        for j in range(col_st, col_en + 1):
            val = db.ws(ws=ws_name).index(row=i, col=j)
            row.append(val)

        # بررسی خالی بودن سطر
        if all(v in (None, "", " ") for v in row):
            if empty_row.startswith('b'):   # break
                break
            elif empty_row.startswith('c'): # continue
                continue
            elif empty_row.startswith('k'): # keep
                pass

        tbl.append(row)

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