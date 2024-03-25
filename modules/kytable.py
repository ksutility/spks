#---------------------------------------------------
#kytable pack:creat table in different form
#----------------------------------------------------
kytable_ar_titel,kytable_txt,kytable_row_i='','',''
#---------------------------------------------------'
def kxtable_prepar (rows,titls,wids,sum_colomn):
    json_obj_txt=''.join([vb_2_json_object(titls,row) for row in rows])
    def vb_2_json_array(array_name,in_array_or_num):
        '''in_array_or_num can be 2 case:
            1-1 array
            2-1 number that show we need all number beatwin 0 to in_array_or_num'''
        txt="var " + array_name + " =["
        if type(in_array_or_num)==list:
            for jj in in_array_or_num:
                txt+= f'"{jj}",' 
        else:
            if array_name=="kxtable_data_cols":
                for jj in range(in_array_or_num):
                    txt+= f'"{jj}",' 
            elif array_name=="kxtable_data_width":
                for jj in range(in_array_or_num):
                    txt+= '"1",' 
        return txt[:-1] + "];\n"
    def json_object_2_array(json_objs_txt):
        txt=json_objs_txt
        if len(txt)<2: return '' #951017
        txt= txt[:-2] #remove ",chr(13)" from end of json_objs_txt
        return "var kxtable_data =[\n" + txt + "];\n"
    #-------------------------------------------
    x=['<script>','']
    x+=[json_object_2_array(json_obj_txt),
        vb_2_json_array("kxtable_data_cols",titls),
        vb_2_json_array("kxtable_data_width",wids),
        "var kxtable_sum_col='{sum_colomn}';",
        "kxtable_make_table(cookiePage);",
        '</script>']
    #print('-'*50+str(x))
    return '\n'.join(x)
def vb_2_json_object(key_array_or_num,value_array):
    txt="{\n"
    if type(key_array_or_num)==list:
        for j,k in enumerate(key_array_or_num):
            t=value_array[j]
            if type(t)==int:t=str(t)
            if not t:t=''
            if type(t)==str:
                txt += '"' + k + '" :"' + t + '", \n'
    else:
        for j in range(0,key_array_or_num):
            txt+= j + ' :"' + value_array[j] + '", \n' 
    return txt[:-2] + "},\n" 
########################################################################################################################
#-----------------------------------------------------  
def kytable_1_make_titels (titel_list):
    global kytable_ar_titel,kytable_txt,kytable_row_i
    kytable_ar_titel=titel_list.split(",")
    kytable_txt=""
    kytable_row_i=0
    
    txt="<table id='table_1' class='table_y'>\n"
    txt+="  <thead><tr>\n"
    txt+="          <th> n </th>\n"
    for title in kytable_ar_titel:
        txt+="              <th>" + title + "</th>\n"
    return txt+"</tr></thead><tbody>\n"
    #---------------------------------------------
def kytable_2_set_widths (width_list):
    return width_list.split(",")
    #---------------------------------------------
def kytable_3_make_row (row_items_ar):
    global kytable_ar_titel,kytable_txt,kytable_row_i
    kytable_txt=kytable_txt + vb_2_json_object(kytable_ar_titel,row_items_ar)
    kytable_row_i+=1
    txt="<tr>\n"
    txt+="              <td>" + kytable_row_i + "</td>\n"
    for i in range(0,ubound(kytable_ar_titel)):
        txt+="              <td>" + row_items_ar(i) + "</td>\n"
    return txt+"</tr>\n"
    
    #---------------------------------------------
def kytable_4_ending ():
    global kytable_ar_titel,kytable_txt
    txt="""
    </tbody></table>
        <input type='button' value='show/hide => simple table' id='sim_tb' name='sim_tb'  style='width:250px;height:25px;'>
    <script>
        $('#sim_tb').click(def(){$('#table_1').toggle();});
        $('#table_1').hide()
    </script>"""
    kxtable_prepar(kytable_txt,kytable_ar_titel,kytable_ar_width,"")
#######################################################################################################################

def test1():
    kytable_1_make_titels( "id,f_nexu,F_STEP,des,Update_F_nexu,Update_UCForm")
    kytable_2_set_widths( "3,3,3,15,10,10")
    kytable_3_make_row (set_ar_data(5,f_id,f_user,share.f_step,des,u1,u2,x6,x7,x8,x9,x10))
    kytable_4_ending ()             
def test2():
    n=user_ar(0,0)
    #temp_ar(10)
    h_ar="user,IP,a,first_IN,last_OUT,IN,OUT,Last_Act,DIF_L_A,Status".split(",")
    w_ar="1,1,1,1,1,1,1,1,1,1".split(",")
    txt=''
    for i in range(1,n):
        for j in range(10):temp_ar[j]=user_ar(i,j)
        txt+=vb_2_json_object(h_ar,temp_ar)
    kxtable_prepar (txt,h_ar,w_ar,"")
def test3():
    tx=[
    "1,2,3,4,<a href='https://www.w3schools.com'>Visit W3Schools.com!</a>",
    "6,7,8,9,0",
    "1,b,c,d,e",
    "1,2,4,5,6"
    ]
    h_ar="aa,ab,c,d,e".split(",")
    w_ar="2,1,1,1,1".split(",")
    txt=''
    for i in range(0,4):
        temp_ar=tx[i].split(",")
        txt+=vb_2_json_object(h_ar,temp_ar)
    return kxtable_prepar(txt,h_ar,w_ar,"")
