#path--------------------------------------------------------------------------
#---SECTION 1-----SERVER BASE------------------------------------------------
base_drive="d:\\form" 
server_folder="form-web"
server_dns="192.168.0.4"
base_path_upload=base_drive + "\form-REC"
#---SECTION 2-----------------------------------------------------
dbc_server_path="http://" + server_dns
dbc_form_prefix="00DB-FRM-" 
base_path_data_read=base_drive + "\\" + server_folder + "\\data\\"
base_path_data_bkup=base_drive + "\\" + server_folder + "\\data_bkup\\"
site_path=base_drive + "\\" + server_folder + "\\"
base_path_x=base_drive + "/" + server_folder + "/data/"
base_path_recycle_delete=base_path_upload + "\\0-recycle\\deleted"			#used=1
base_path_recycle_re_Upload=base_path_upload + "\\0-recycle\\re_Uploaded"		#used=0
base_path_import_file=base_path_upload + "\\import-file-to-form-server"		#used=0
	#where that big file copy by client to it until server move it to corect plase -this act is for upload big file- 
	#this folder shoude share
	# 	
setting_dbFile1=base_path_x + "00DB-FRM-0-SET1.mdb"
setting_dbFile2=base_path_x + "00DB-FRM-0-SET2.mdb"
setting_infFile=base_path_x + "00DB-FRM-0-inf.mdb"							#used=0	


ksf={	"user_fullaccess_from_internet":",admin,mb,bkb,ks,itm,itm2,",
		"user_reset_forms":",admin,ks,",
		"admin_set_enable":False,
		#---SECTION 1-----------------------------------------------------
		"mail_suffix":"@dbc.ir",	 #"@daryabandar.ir" "@dbc.ir"
		"debug_mode":0, #0=do not no 1=yes
		#---SECTION 2-----------------------------------------------------
		"send_email":0, #0=no 1=yes
		"shuod_fill_reject_text":False,  #false,true
		#"form_data_in_update_proccess"]:true, #true = form is in update prosess
		"run_1_step_admin_act":0} #0=do not 1=do   for spetiol task in admin_set.asp
#date--------------------------------------------------------------
kfd_tatil={"general":"0101,0102,0103,0104,0112,0113,0314,0315,1122,1229,1230", #tatilat yeksan shamsi
			1394:"0212,0226,0313,0417,0427,0428,0520,0802,0911,0921,1008,1223",#sal 94
			1395:"0302,0407,0416,0509,0622,0630,0720,0721,0830,0908,0910,0927,1021",
			1396:"0122,0205,0405,0406,0514,0618,0708,0709,0828,0906,0915,1201",
			1397:"0111,0125,0212,0316,0326,0418,0531,0628,0808,0816,0904,1120",
			1398:""}
def array_set(n1,n2):
	l1=['' for x in range(n2)] 
	return[l1 for x in range (n1)]


step_inf=array_set(16,20) # public step_inf(16,20)
task_inf=array_set(10,50) #public task_inf(10,50)#*
session_timeout=15



#--------------------------------------------------------
section_task=array_set(10,6)		#public share.section_task[10,6]


form_inf={'app_state_name':"F_NEXU"} # _" & session("form_name") #public app_form_state_name
#یک فیلد که مشخصات کلی فرم را یعنی وضعیت تکمیل را در خود نگه می دارد این فیلد برای استفاده چند گانه از یک جدول در چند فرم به جای  فیلد زیر تعریف شده است

#public
Xresult=""
html_temp_page=""
st_splite_chr1="," #جدا کننده بخش های اصلی در فایلهای تعریف هر فرم
st_splite_chr2="»"  #chr(187)-chrw(187)
								#جدا کننده در موارد زیر
										#بخشهای فرعی در فایلهای تعریف فرم
										#نام افراد مختلف در فایل شغلها
											#user_cur,job_man
										#داخل برنامه
											#user
									#task_inf[ix]['inf'],task_inf[ix]['title'],task_inf[ix]['i6'],task_inf[ix]['i7'],task_inf[ix]['i10']		
								#mail user			
									#mail_to=step_inf[next_step]['jobs_users']	
									#mail_to=step_inf[1]['s_u']
									#mail to 
st_splite_chr3=";" #برای فرستادن مقادیر مجزا به برنامه زیر 
										#sql_add_auto
								#یا سایر سلکتها برای اس کیو ال		
					#برنامه های زیر به طور مستقل از علامت سیسکالن استفاده می کنند
								#قسمتهای مخفی شده - غیر قابل اجرا
								#کدهای جاوا
								#form_update_set  ==>> html
								#xresult
st_splite_chr4="^" #جدا کننده بخشهای مختلف در 
									#list_structure
p_color_table_r1="#119999"
p_color_table_r2="#009900"
p_color1="#bbdddd"
p_color2="#99bbbb"
p_color_green="#66dd99"
p_color_orange="#f08200"
p_color_red="#dd9999" ##aaccff
p_color_yellow="#f0e68c"
p_color_blue="#55aaff"
#qq_chr=chr(34)

form={'name':"",
    'task_total':"",
    'step_total':"",
    'db_n':"",
    'tb_n':"",
    'tb_backup':"",
    'scrt_inf':"",
    'show_order':""
    }
reject_text=""
f_revn=0
f_revs=""
f_nexu=""
f_step=""





