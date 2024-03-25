//940120
//help on smart_num_list.bas
//-----------------------------------------------------------------------------------------------------------------
function smart_num_list_add(in_smart_num_list, new_num) { 
	//931213
	//make a new smart_num_list by add new_num to in_smart_num_list
    in_smart_num_list = smart_num_list_correct(in_smart_num_list);	
    var sn_ar = in_smart_num_list.split(",");
    var re = "" ;
    var x_find = false ;
	var i,st,stn,c_num;
	for (i = 0; i < sn_ar.length; i++) {
		if ( x_find == true ) {
			re += "," + sn_ar[i];
		} else {
            st = sn_ar[i].split("-");
            stn = st.length-1;
			c_num=new_num * 1;
			switch ( true ) {
				case (c_num + 1  < (st[0] *1)) :
					re += "," + new_num + "," + sn_ar[i];
                    x_find = true;
					break;
				case (c_num + 1 == (st[0] *1)) :
					re += "," + new_num + "-" + st[stn];
                    x_find = true;
					break;
				case (c_num - 1 == (st[stn] *1)):
					re += "," + st[0] + "-" + new_num;
                    x_find = true;
					break;	
				case (c_num - 1 > (st[stn] *1)):
					re += "," +  sn_ar[i];
 					break;					
				default: 
					re += "," + sn_ar[i];
					 x_find = true;
			}
		}
    }
	if ( x_find == false ) {re += "," + new_num;}
    return re.slice(1,re.length);
}
//-----------------------------------------------------------------------------------------------------------------
function smart_num_list_correct(in_smart_num_list) {
	//931213
	//if 2 sections in smart_num_list can be a section , this pro do it
	//for exampe 
		//input=		1-5,6-7,9,10-12
		//output=	1-7,9-12
   var sn_sec = in_smart_num_list.split(",");
   var re = "";
   var x_find = false;
   var sec1 = sn_sec[0],sec1_ar;
   for (i = 1; i < sn_sec.length ; i++ ) {
		sec1_ar = sec1.split("-");
        sec2_ar = sn_sec[i].split("-");
        if (sec1_ar[sec1_ar.length-1] * 1 == sec2_ar[0] - 1) {
            sec1 = sec1_ar[0] + "-" + sec2_ar[sec2_ar.length-1];
         } else {
            re += "," + sec1; 
            sec1 = sn_sec[i];
        }
    }
    re += "," + sec1; 
	return re.slice(1,re.length);
}
//-----------------------------------------------------------------------------------------------------------------
function index_key(obj_n,smart_num_list,def,can_omit) {
		var ss2 
		ss2=smart_num_list_correct(smart_num_list);
		obj=document.getElementById(obj_n);
		var t=obj.value;
		var v=Number(t);
		if ((can_omit==true) && (t=="-")) 
			{
				re=true;	
				
				//alert(" ok ")
			}		
		else if (!(t==v))
			{
			obj.value= def;
			//alert("لطفا يک عدد جدید با توجه به لیست اعداد موجود وارد کنيد");re=false;
			alert(" Please inter a number ");re=false;
			}
		else 
			{
			var ss=smart_num_list_add(ss2, v);
			if  ( ss == ss2)
				{obj.value= def;
				alert(" Please inter a new number with look at list Of exist numbers \n" +"لطفا يک عدد جدید با توجه به لیست اعداد موجود وارد کنيد" );re=false;
				}
			else {	}	
			}
	}
//------------------------------------------------------------------------------------------------------------
function txt_key(obj_n,n) {
	//این بخش یک تابع داخل صفحه وب برای کابر ایجاد می کند که وظیفه آن اینست که
	//متن ورودی را برای خطای زیر بررسی کند
	//مقدار کاراکتر باقی مانده برای تایپ را محاسبه نموده و در لیبل مربوطه نشان دهد
		t=document.getElementById(obj_n).value;
		//document.getElementById(obj_n).value=fa_coreect(t);
		document.getElementById("label" + obj_n).innerHTML  = n-t.length;
		}
//------------------------------------------------------------------------------------------------------------
function fa_coreect(str) {
	// 	1740=i fa 1610=shift+i fa   
		var i,t;t="";
		for (i=0;i<str.length;i++) {
				if (str.charCodeAt(i)==1610) {
				str=str.replace(str.charAt(i),String.fromCharCode(1740));
				}
			}
		return str;
		}
//------------------------------------------------------------------------------------------------------------
function fa_coreect_obj(obj_name) {
	// 	
		//alert (obj_name);
		var t=document.getElementById(obj_name).value;
		document.getElementById(obj_name).value=fa_coreect(t);
		}		
//---------------------------------------------------------------------------------------------------------------------------
function num_key(obj_n,minv,maxv) 	{
	
		obj=document.getElementById(obj_n);
		t=obj.value;
		if (!(t*1) && !(t==0))
			{obj.value= minv*1;
			alert("لطفا يک عدد در بازه تعيين شده وارد کنيد");re=false;
			}
		else 
			{
			n=t*1
			if (minv != "" && n < minv*1)	{obj.value= minv*1;	}
			if (maxv !="" && n > maxv*1) 	{obj.value= maxv*1;	}
			}
		}
//---------------------------------------------------------------------------------------------------------------------------		
function date_key1(obj_n,def) {
//	alert("input date is not correct");	
	obj=document.getElementById(obj_n);
	var t=obj.value;var re1;
	var re=false;	
	if ((t.length == 6) && !(isNaN(t)))  {
		var yy=t.substr(0,2);
		var mm=t.substr(2,2) ;
		var dd=t.substr(4,2) ;
		if ( !(isNaN(yy)) && !(isNaN(mm)) && (mm.valueOf()  < 13) && !(isNaN(dd)) &&  (dd.valueOf() < 32) )  { 
			//alert("input date is correct :" + yy + "/" + mm + "/" +dd);	
			if (( dd.valueOf() != 31) || ( mm.valueOf() < 7)) {re=true }
		}
		}
	if ( re == true ) {
		//alert("input date is correct :" + yy + "/" + mm + "/" +dd);	
	}
	else {
		obj.value= def;
		alert("input date is not correct :" + yy + "/" + mm + "/" +dd);	
	}
}
//---------------------------------------------------------------------------------------------------------------------------
function findStrRe(baseStr,xformat,findStr) {
	var tt = "00" ;
	var xLen=findStr.length;
	var n = xformat.search(findStr);
	if (n > -1) {tt = baseStr.substr(n , xLen);}
	tt=tt.match(/[0-9]+/i);
	if ( (tt == null) || (tt == "")) {tt="000".substr(0,xLen);}
	//alert("baseStr="+baseStr+ "\n format="+ xformat + "\n xLen="+xLen+"\n findStr=" + findStr + "\n n=" + n + "\n tt=" +tt +"\n" + "/"+findStr +"/i" );
	return tt ;
}
function findSign(baseStr,xformat,findStr) {
	var tt= "" ;
	//alert("findStr=" + findStr);
	var xLen=findStr.length;
	var n = xformat.search("#");
	//alert("n=" + n );
	if (n > -1) {tt = baseStr.substr(n , xLen);}
	//alert("tt=" + tt );
	if (tt != "-") {tt = "+" ;}
	//alert("tt=" + tt );
	return tt ;
}
//
function isLikeFormate(str,xformat) {
	//alert("isLikeFormate 1=" +str+ " || 2= " + xformat);
	var tt,res,i,sum=0;
	for (i=0;i < xformat.length;i++) {
		tt= xformat.substr(i,1);
		res = tt.search(/\W/i);
		if (res == -1){	
			if (tt != str.substr(i,1)) {alert("input date is not correct format like :" + xformat);return false;}
		}
	}	
	return true;
}
//
function fixLenDigit(strDigit,xlen) {
	var t1="0000000000" +strDigit;
	return t1.slice(-xlen);
}
//---
function outStrByFormat(xout,xsearch,xrep,xlen) {
	xrep = fixLenDigit(xrep,xlen);
	return xout.replace( xsearch,xrep );
}
//---
function limitcontrol(baseVal,upLevelValObj,xLimit){
	//alert ("baseVal=" + baseVal + " | upLevelValObj=" + upLevelValObj.v + " | Limit=" + xLimit); 
	var bagi=(baseVal % xLimit); 
	upLevelValObj.v = (baseVal-bagi)/xLimit;
	return bagi; 
}
//
function date_key(obj_n,def,format) {
//	alert("input date is not correct");	
	var obj=document.getElementById(obj_n);
	var xstr=obj.value;
	var re1,temp
	var tObj={v:0};
	var xout=format;
	var re=false;	
	// در صورتی که فرمت با یک علامت شروع می شود ولی عدد وارد شده علامت ندارد یک فاصله برای علامت خالی می گذارد
	// این فاصله در ادامه برنامه به علامت مورد نظر تبدیل می شود
		if ((format.substr(0,1)=="#") && (xstr.substr(0,1).search(/\d/i)!=-1)) {xstr =" " + xstr;}
	//format.length
	//if ( isLikeFormate(xstr,format) == true )  {
		//alert("ok like");
		var yy=findStrRe(xstr,format,"yy");
		var mm=findStrRe(xstr,format,"mm") ;
		var dd=findStrRe(xstr,format,"dd") ;
		var DD=findStrRe(xstr,format,"DD") ;// a sum day
		var DDD=findStrRe(xstr,format,"DDD") ;// a sum day by 3 digit
		var hh=findStrRe(xstr,format,"hh") ;
		var H=findStrRe(xstr,format,"H") ;// saat edari < 8
		var HH=findStrRe(xstr,format,"HH") ;// a sum houe that can be more than 23
		var HHH=findStrRe(xstr,format,"HHH") ;// a sum houe that can be more than 23 by 3 digit
		var gg=findStrRe(xstr,format,"gg") ;
		var ss=findStrRe(xstr,format,"ss") ;
		var sign=findSign(xstr,format,"#") ;
		
		if ( ss.valueOf() > 59) {alert("Second is >59");ss = limitcontrol(ss,tObj,60);gg= tObj.v + (gg*1)}	
		//alert ("gg=" + gg + " | ss=" + ss); 
		if ( gg.valueOf() > 59) {alert("Minut is >59");gg=limitcontrol(gg,tObj,60);hh=hh*1+tObj.v;HH=HH*1+tObj.v;H=H*1+tObj.v;HHH=HHH*1+tObj.v}
		if ( hh.valueOf() > 23) {alert("hour shoud be < 24");hh=limitcontrol(hh,tObj,24);dd=dd*1+tObj.v;DD=DD*1+tObj.v;}
		if ( H.valueOf() > 7) {alert("hour(office) shoud be < 8");H=limitcontrol(H,tObj,8);dd=dd*1+tObj.v;DD=DD*1+tObj.v;}	
		if ((dd.valueOf() == 31) && ( mm.valueOf() > 6)) {alert("According to mount number day shoud be < 31"); dd="30";}
		if ( dd.valueOf() > 31) {alert("day is >31");dd= "31";}
		if ( mm.valueOf() > 12) {alert("mount is >12");mm="12";}
	
		
		xout = outStrByFormat(xout, "yy" , yy ,2 );
		xout = outStrByFormat(xout, "mm" , mm ,2 );
		xout = outStrByFormat(xout, "dd" , dd ,2 );
		xout = outStrByFormat(xout, "DDD" , DDD ,3 );
		xout = outStrByFormat(xout, "DD" , DD ,2 );
		xout = outStrByFormat(xout, "hh" , hh ,2 );
		xout = outStrByFormat(xout, "HHH" , HHH ,3 );
		xout = outStrByFormat(xout, "HH" , HH ,2 );
		xout = outStrByFormat(xout, "H" , H ,1 );
		xout = outStrByFormat(xout, "gg" , gg ,2 );	
		xout = outStrByFormat(xout, "ss" , ss ,2 );
		xout = xout.replace( "#",sign );
		//}
		
	/*if ( re == true ) {
		//alert("input date is correct :" + yy + "/" + mm + "/" +dd);	
	}
	else {
		obj.value= def;
		alert("input date is not correct :" + format);	
	}
	*/
	obj.value = xout;
}
//---------------------------------------------------------------------------------------------------------------------------
function app_key(t) {
		re=false;
		if (t=="R") {if (isvalid_re()==true) { re=confirm("Form RETURN  - ARE You Sure ? \n \n" + "فرم بازگشت داده شود ؟") }
					}	
		else {	if (t=="X") 
				{ 	var msg =	"آیا مطمئن هستید که می خواهید این فرم را   عدم تایید   نمایید؟ "
									msg	+= "\n" + "ARE You Sure ? \n \n"
									msg += "\n" + "توجه :با این کار کلیه فایلهای الحاق شده به این فرم  پاک می شود"
									msg += "\n" +"with this action all file in this form will delete"
									if (confirm(msg) == true) {
									var msg =	"برای انجام این کار کدد زیر را وارد نمایید "
										msg	+= "\n" + "Please enter this code:"
										msg	+= "\n \n \n" + "code= db"
										var ikey = prompt(msg, "");
										if (ikey == "db") {re=true;}
									}
        
							}
				else { if ( isvalid()==true) { re = confirm("ARE You Sure2 ? \n \n" + "آیا مطمئن هستید ؟" );	} 	
				}
			}		
		if (re == true) 
			{
			document.getElementById("text_app").value=t;
			document.getElementById("form1").submit();
			document.getElementById("maindiv").innerHTML="<h2>" + "فرم تکمیل شده توسط شما به سرور ارسال شد" + "<br>" + "لطفا برای مشاهده نتیجه منتظر بمانید" + "</h2>";
			document.getElementById("histortdiv").innerHTML="";
			}
		}
//------------------------------------------------------------------------------------------------------------
	function jdownload(file,Pfolder,patern) {
		path = "download.asp?file=" + file + "&Pfolder=" + Pfolder + "&patern=" + patern;
		document.getElementById('subwin1_body').innerText='فایل در حال آماده سازی می باشد '+'\n'+'لطفا  چند لحظه منتظر بمانید ';
		j_box_show(path); 
	}
//------------------------------------------------------------------------------------------------------------
function jdownload_only_show_file_inf(file,Pfolder,patern) {
		path = "download.asp?only_show_file_inf=1&file=" + file + "&Pfolder=" + Pfolder + "&patern=" + patern;
		document.getElementById('subwin1_body').innerText='فایل در حال آماده سازی می باشد '+'\n'+'لطفا  چند لحظه منتظر بمانید ';
		j_box_show(path); 
	}
//------------------------------------------------------------------------------------------------------------
	function jupload(Pfolder,patern,filename,fileExt,obj_name) {
		path = "upload.asp?fname=" + filename +"&Pfolder=" + Pfolder + "&ext=" + fileExt + "&filed_name=" + obj_name + "&patern=" + patern;
		//path = "upload.asp?Pfolder=1&patern=1&fname=1&ext=2&filed_name=2";
		//alert(path); 
		//alert(filename);
	
		j_box_show(path); 
		//window.location.href = path;
	}	
//------------------------------------------------------------------------------------------------------------
	function jupload_big(Pfolder,patern,filename,fileExt,obj_name) {
		path = "upload-big.asp?fname=" + filename +"&Pfolder=" + Pfolder + "&ext=" + fileExt + "&filed_name=" + obj_name + "&patern=" + patern;
		j_box_show(path); 
		//window.location.href = path;
	}		
//--------------------------	
	function j_box_show(path) {
		document.getElementById('light').style.display='block';
		document.getElementById('fade').style.display='block'; 
		$('#subwin1_body').load( path ); 

		//alert ( path );
		
		//------ goto the url In cur page 
		//window.location.href = path
		
		//------ open new page
		//window.open ( path );

		//
	}
	function j_box_show_forDebug(path) {
		document.getElementById('light').style.display='block';
		document.getElementById('fade').style.display='block'; 
		//$('#subwin1_body').load( path ); 

		//alert ( path );
		
		//------ goto the url In cur page 
		 //window.location.href = path
		
		//------ open new page
		window.open ( path );

		//
	}
	function j_box_hide() {
		document.getElementById('light').style.display='none';
		document.getElementById('fade').style.display='none'; 
	}
	function j_box_iframe(path) {
		document.getElementById('light').style.display='block';
		document.getElementById('fade').style.display='block'; 
		var $iframe = $('#iframe_win');
		if ( $iframe.length ) {
			$iframe.attr('src',path);   
			
		}
	}	
//--------------------------		
		function form_pre_set(obj_n,n) {
			var t=document.getElementById(obj_n).value;
			var t_ar=t.split("-");
			var n_ar=n.split("-");
			var re="";
			for (i = 0; i < t_ar.length; i++) {
				re += n_ar[i]+ ";" + t_ar[i]+ ";" ;
			}
			//alert('aa');
			document.location.assign("formshow.asp?Xresult=" + re );
			//document.location.assign( a );
	}
      function DisplaySessionTimeout()
        {
			//alert("DisplaySessionTimeout." + sessionTimeout  );
            document.getElementById("lblSessionTime").textContent = sessionTimeout;
            sessionTimeout = sessionTimeout - 1;
            
            if (sessionTimeout >= 0)
                window.setTimeout("DisplaySessionTimeout()", 1000);
            else
            {
				tempAlert("Your current Session is over.<hr>" + "زمان انتظار سرور تمام شد و صفحه دوباره بارگذاری گردید",3000);
				setTimeout(function(){location.reload();},3000);
				
            }
        }
 //--------------------------
 function tempAlert(msg,duration)
{
 var el = document.createElement("div");
 el.setAttribute("style","position:absolute;top:0;height:100;left:30%;width:40%;background-color:#cccccc;border: 1px solid #999999;padding: 3px 1.8%;");
 el.innerHTML = msg;
 setTimeout(function(){
	el.parentNode.removeChild(el);
	},duration);
 document.body.appendChild(el);
}
//--------------------------
 function clear_file_field(obj_name) {
	var msg =	"آیا مطمئن هستید که می خواهید این فایل پیوست شده  را حذف نمایید؟ "
	msg	+= "\n ARE You Shure Remove Attached File ? \n "
	if (confirm(msg) == true) {
		document.getElementById(obj_name).value="-";
		document.getElementById("link1" + obj_name).innerHTML="-";
		document.getElementById("link2" + obj_name).innerHTML="";
	}
 }