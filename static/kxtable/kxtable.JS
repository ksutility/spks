//v2.3 - last update 970308---fix error + show cell info on top----------------------------------------------------------------------
var table_head_Height=40;
var url = window.location.pathname;
var filename = url.substring(url.lastIndexOf('/')+1);
var cookiePage;   //only for coocki file name
var kxtable_Arrangement=[];
var sort_cols_step=["0","1","2"];
var kxtable_gr_out_data=[]; // output data for creat graph  9612
var last_td=[0,0,0];
var xsort_c_name;
var xsort_c_mode;
xsort_c_mode=true;
//var test1= kxtable_sum_col + "";
//kxtable_sum_col=""
//if (kxtable_sum_col === null){kxtable_sum_col="";}
//alert (kxtable_sum_col + "abc");
/* 	<div id="ks_input_box" class="ks_input_box_c"> 	</div>
		.ks_input_box_c {
        display: none;
        position: fixed;
        top: 25%;
        left: 25%;
        width: 10%;
        height: 10%;
        padding:1px;
        border: 1px solid orange;
        background-color: white;
        z-index:1002;
        overflow: auto;
    }
*/	
	function kxtable_make_table(in_cookiePage){
		cookiePage=in_cookiePage;
		var txt_add1="";
		// alert(kxtable_sum_col);
		if (kxtable_sum_col) {txt_add1='\
					<input type="button" value="chart 1=>2" name=kx_but_chart id=kx_but_chart  style="width:90px;" onclick="kxflot_pr(0);"> \
					<input type="button" value="chart 2=>1" name=kx_but_chart id=kx_but_chart  style="width:90px;" onclick="kxflot_pr(1);"> \
					'} ;	
	document.write('\
			<style id="style1">\
			</style>\
			\
			<div>\
				<input type="button" value="w" name=kx_but_w id=kx_but_w  style="width:30px;" onclick="kxtable_set_width_th(true);kxtable_set_width(false);"> \
				' + txt_add1 + '\
				<textarea name="kx_show_txt" id="kx_show_txt" rows="1" style="resize:vertical"></textarea> \
			<div>\
			<div id="kxtable_div0" align="left"></div>\
			<div id="kxtable_div1">\
				<table id="kxtable_1" class="kxtable">\
				  <thead id="kxtable_head">\
				  </thead>\
				</table>\
			</div>\
			\
			<div id="kxtable_div2">\
				<table id="kxtable_2" class="kxtable">\
					<thead id="kxtable_head2">\
					</thead>\
					<tbody id="kxtable_body">\
					</tbody>\
				</table>\
				<p id="kxtable_note"></p>\
			</div>\
			\
			<input type="text" name="xsort_col" id="xsort_col" hidden="hidden">\
			<input type="checkbox" name="xsort_mode" id="xsort_mode" hidden="hidden">\
		');
		$(function() {
			for (i=0;i<kxtable_data_cols.length+1;i++){
				kxtable_Arrangement[i]=i;
			}	
		//9612	
			for (i=0;i<kxtable_data_cols.length;i++){			
				kxtable_data_cols[i]=kxtable_data_cols[i].trim(); 
			}	
			
			//
			//$( ".kxtable_resizable" ).draggable();
			
			//$( ".kxtable_resizable" ).resizable({ maxHeight: table_head_Height, minHeight: table_head_Height });
			//kxtable_set_width_th (false);
				
			sort_data("",true);	
			kxtable_set_table_head_htm();	
			kxtable_set_table_head_jquery();
			kxtable_show_table(false)
				// kxtable_set_table_body("");
				// kxtable_set_width_th_by_input();
				// kxtable_set_width (false);
			//$(".kxtable_resizable").mouseleave( function (){kxtable_set_width (true);});

			$('#kxtable_div1').scroll(function () {
				$('#kxtable_div2').scrollLeft($(this).scrollLeft());
			});
			
		// content menu end
			
		});
	}
//------------------------------------------------------------------------------------------------------------------------------
	function kxtable_show_table(p2){
		kxtable_set_table_body();
		kxtable_set_width_th_by_input();
		kxtable_set_width (p2);	
		kxtable_cell_show_full_text ();	
	}
//----------------------------------------------------------------
	function kxtable_set_table_head_htm(){	
		var t1,fn;
		txt ="<tr id='kxtable_head_tr'>";
				//txt += "    <th ><div class='kxtable_resizable'>---</div></th>";
			txt += "    <th ><div id='div-head-1' class='context-menu-one'>---</div></th>";	
			for (i=0;i <  kxtable_data_cols.length;i++) {
				w = "";
				//txt1 = "    <th ><div class='kxtable_resizable' " + w + ">" +  kxtable_data_cols[i] + " </div></th>";
				n=i+2;
				t1=kxtable_data_cols[kxtable_Arrangement[i]];
				fn="bg.png";
				if (t1==xsort_c_name ){fn= "asc.gif";}
				txt1 = "    <th ><div id='div-head-" + n + "'  class='context-menu-one' " + w + ">\
					" +  t1 + "<img  class='kxt_sort_sng' src='link/ar/" + fn + "'></img> </div></th>";
				txt += txt1;
			}
			txt += "</tr>" ;
			document.getElementById("kxtable_head").innerHTML= txt ;
	}
//-----------------------------------------------------------------
	function kxtable_set_table_head_jquery(){	
			//----------
			$(".kxt_sort_sng").click(function(){
					
						sort_data($(this).parent().text(),true);
						//kxtable_set_table_head_htm();
						kxtable_show_table(false)
						var col = $(this).parent().parent().parent().children().index($(this).parent().parent())+1;
						kxtable_show_sort_sign(col);
						//var row = $(this).parent().parent().children().index($(this).parent())+1;
							// kxtable_set_table_body($(this).text());
							// kxtable_set_width (false);
						//$(".kxtable th").children().css("background-color","#aaaaff");
						//$(".kxtable th div").css("background-color","#aaaaaa");
						//$(this).children("div").css("background-color","#00ffff");
			});
			// draggable
			
			$(".context-menu-one").draggable({ 
				revert: true,
				helper: "clone",
				});
			$(".context-menu-one" ).droppable({
				hoverClass: "highlight",
				drop: function( event, ui ) {
					
					var draggable = ui.draggable;
					var t_darg,i_darg,t_drop,i_drop;
					t_drop= $( this ).text();
					t_darg=draggable.text();
					//$( this ).html(tt2);
					//draggable.html(tt1);
					re=0;
					t_drop=t_drop.trim();
					t_darg=t_darg.trim();
					for (i=0;i <kxtable_data_cols.length;i++) {
						if (t_drop==kxtable_data_cols[kxtable_Arrangement[i]]) {i_drop=i;re+=1;}
						if (t_darg==kxtable_data_cols[kxtable_Arrangement[i]]) {i_darg=i;re+=1;}
					}
					if (re!=0) {
						if(event.shiftKey){
							swich_ar(kxtable_Arrangement,i_drop,i_darg)
						} else {	
							if (i_darg<i_drop){
								for(k=i_darg;k<i_drop;k++){
									swich_ar(kxtable_Arrangement,k,k+1)	
								 }
							} else {
								for(k=i_darg;k>i_drop;k--){
									swich_ar(kxtable_Arrangement,k,k-1)	
								 }
							}
						}	
						// temp=kxtable_Arrangement[i_drop];
						
						kxtable_set_table_head_htm();	
						kxtable_set_table_head_jquery();
						kxtable_show_table(false)
						// kxtable_set_table_body("");
						// kxtable_set_width_th_by_input();
						// kxtable_set_width (false);
					
					} else {
						$( this ).html(kxtable_data_cols[kxtable_Arrangement[0]]+tt1);
					}
					$(this).children("div").css("background-color","#00ff55");
				}
			});
			/**/
		// content menu start
			$.contextMenu({
				selector: '.context-menu-one', 
				//selector: '.kxtable_resizable', 
				callback: function(key, options) {
					if (key=="Change width"){
						var ww=$(this).width();;
						//while (ww != null) {
							ww = prompt("Width Add", ww);
							if (ww != null) {
								w2 = ww*1;
								//w2=$(this).width() + ww;
								if (w2<5) {w2=5;}
								$(this).width(w2);
							}
						kxtable_set_width (true);	
						//}
					}
					if (key=="splite1-det"){
						 kxtable_set_table_body_split($(this).text(),"ALL");
						 kxtable_set_width (true);	
					}
					if (key=="splite1"){
						kxtable_set_table_body_split($(this).text(),"---");
						kxtable_set_width (true);	
					}
					if (key=="splite2-det"){
						 kxtable_set_table_body_split2($(this).text(),"ALL");
						// kxtable_set_width (true);	
					}
					if (key=="splite2"){
						kxtable_set_table_body_split2($(this).text(),"---");
						//kxtable_set_width (true);	
					}
					/*
					if (key=="Move"){
						ww=0;
						while (ww != null) {
							var ww = prompt("Add Position", ww);
							if (ww != null) {
								n = find_obj_index_in_table($(this).text());
								move_item_in_array(xtable_Arrangement,n,ww);
							}
						kxtable_set_width (true);	
						}
					};		
					*/	
					var m = "clicked: " + key;
					//window.console && console.log(m) || alert(m); 
				},
				items: {
					"Change width": {name: "Change width", icon: "edit"},
					"splite1": {name: "splite1", icon: "edit"},
					"splite1-det": {name: "splite1-det", icon: "edit"},
					"splite2": {name: "splite2", icon: "edit"},
					"splite2-det": {name: "splite2-det", icon: "edit"},
				}
			});
			$('.context-menu-one').on('click', function(e){
			//$('.kxtable_resizable').on('click', function(e){
				console.log('clicked', this);
			});
			
	}		
//------------------------------------------------------------------------------------------------------------------------------
function kxtable_cell_show_full_text(){
		var style_n="background-color"
		var style_v1="#ffaa00"
		var style_v2="#ff5555"
		//
		var style_n="border"
		var style_v1="2px solid red"
		var style_v2="2px solid blue"
		var col,row;
		$("td").click(function(){
			col = $(this).parent().children().index($(this))+1;
			row = $(this).parent().parent().children().index($(this).parent())+1;
			
			$("#kx_show_txt").val( row + ',' + col +  ' : ' + $(this).text());
			$("#kxtable_body tr:nth-child(" + last_td[0] + ")").css(style_n,""); //.removeAttr("style");
			$("#kxtable_body tr:nth-child(" + last_td[0] + ") td:nth-child(" + last_td[1] + ")").css(style_n,"");
			$("#kxtable_head_tr th:nth-child(" + last_td[1] + ") div").css(style_n,"");
			$("#kxtable_body tr:nth-child(" + row + ")").css(style_n,style_v1);
			$("#kxtable_body tr:nth-child(" + row + ") td:nth-child(" + col + ")").css(style_n,style_v2);
			$("#kxtable_head_tr th:nth-child(" + col + ") div").css(style_n,style_v1);
			
			last_td[1]=col;
			last_td[0]=row;
		});
		$("th").click(function(){
			col = $(this).parent().children().index($(this))+1;
			row = $(this).parent().parent().children().index($(this).parent())+1;
			$("#kx_show_txt").val( row + ',' + col +  ' : ' + $(this).text());
			$("#kxtable_body tr:nth-child(" + last_td[0] + ")").css(style_n,""); //.removeAttr("style");
			$("#kxtable_body tr:nth-child(" + last_td[0] + ") td:nth-child(" + last_td[1] + ")").css(style_n,"");
			$("#kxtable_head_tr th:nth-child(" + last_td[1] + ") div").css(style_n,"");
			$("#kxtable_head_tr th:nth-child(" + col + ") div").css(style_n,style_v1);
			last_td[1]=col;
		});
	}
//------------------------------------------------------------------------------------------------------------------------------
function kxtable_show_sort_sign(col){
		if (xsort_c_mode){re="asc" } else {re="des"}
		$(".kxt_sort_sng").attr("src", "link/ar/bg.png")
		$("#kxtable_head_tr th:nth-child(" + col + ") div img").attr("src", "link/ar/" + re + ".gif")
	}	
//-------------------------------------------------------------------------------------------------------------------	
	function kxtable_set_width(save_cookie){
		var j,xw1,w_cooki;
		w_cooki="";
		for (j=1;j <  kxtable_data_cols.length+2;j++) {
			xw1 = $(".kxtable th:nth-child(" + j + ")").css("width");
			//$(".kxtable td:nth-child(" + j + ")").css("max-width",xw1);
			$(".kxtable td:nth-child(" + j + ")").css("width",xw1);
			xw2 = $(".kxtable th:nth-child(" + j + ") div").css("width");
			w_cooki += xw2 + "-";
		}
		if (save_cookie==true){setCookie("t_width", w_cooki, 365);}
		var w1=$("#kxtable_1").css("width");
		$("#kxtable_2").css("width",w1);
		}
//------------------------------------------------------------------------------------------------------------------------------		
	function kxtable_set_width_th(ch_reset){
		var col_1_width=50;
		var j,w,tx;
		var w_cooki=getCookie("t_width");
		var w_cooki_ar=w_cooki.split("-");
		w2= parseInt($("#kxtable_div1").width());
		n = parseInt((w2-col_1_width)/ (kxtable_data_cols.length)-5);
		nt= n + "px";
		
		tx=	".kxtable_resizable { \
			height:40px;padding: 0.5em; text-overflow: ellipsis;overflow: hidden;background-color:#11aaff;" + w + " \
			} \
			.kxtable th:nth-child(1) div{width:15px;} \
			";
		if ((ch_reset == true) || (w_cooki_ar[0] == "" )) { 
			$("#div-head-1").width(col_1_width + "px");
			w = nt ;
			for (j=2;j <  kxtable_data_cols.length+2;j++) {
				if (( w =="") && (w_cooki_ar[0] != "" )) {ww=w_cooki_ar[j-1];} else {ww = nt;}
				$("#div-head-"+j).width(ww);
			}
		} else {
			w ="";
			for (j=1;j <  kxtable_data_cols.length+2;j++) {
				ww=w_cooki_ar[j-1];
				$("#div-head-"+j).width(ww);
			}
		}
	
		document.getElementById("style1").innerHTML=tx;
	}	
//------------------------------------------------------------------------------------------------------------------------------			
	function kxtable_set_width_th_by_input_old(){
		var col_1_width=50;
		var j,w_i_sum,n,ww,w2,tx;
		if (kxtable_data_width != null) {
			w2= parseInt($("#kxtable_div1").width());	
			tx=	".kxtable_resizable { \
				height:40px;padding: 0.5em; text-overflow: ellipsis;overflow: hidden;background-color:#11aaff;" + w + " \
				} \
				.kxtable th:nth-child(1) div{width:15px;} \
				";

				$("#div-head-1").width(col_1_width + "px");
				w_i_sum =0;
				for (j=0;j <  kxtable_data_width.length+0;j++) {w_i_sum += parseInt(kxtable_data_width[j]);}
				n = ((w2-col_1_width-(5*kxtable_data_width.length))/(w_i_sum));
				for (j=2;j <  kxtable_data_width.length+2;j++) {
					ww = parseInt(n * parseInt(kxtable_data_width[j-2]));
					$("#div-head-"+j).width( ww +"px");
				}
			document.getElementById("style1").innerHTML=tx;
		} else {
			kxtable_set_width_th (false);
		}	
	}

//------------------------------------------------------------------------------------------------------------------------------		function kxtable_set_table_head(){
	function kxtable_set_width_th_by_input(){
		var col_1_width=50;
		var j,w_i_sum,n,ww,w2,k,tx;
		if (kxtable_data_width != null) {
			w2= parseInt($("#kxtable_div1").width());	
			tx=	".kxtable_resizable { \
				height:40px;padding: 0.5em; text-overflow: ellipsis;overflow: hidden;background-color:#11aaff;" + w + " \
				} \
				.kxtable th:nth-child(1) div{width:15px;} \
				";

				$("#div-head-1").width(col_1_width + "px");
				w_i_sum =0;
				for (j=0;j <  kxtable_data_width.length+0;j++) {w_i_sum += parseInt(kxtable_data_width[j]);}
				n = ((w2-col_1_width-(5*kxtable_data_width.length))/(w_i_sum));
				for (j=0;j <  kxtable_data_width.length;j++) {
					ww = parseInt(n * parseInt(kxtable_data_width[kxtable_Arrangement[j]]));
					k=j+2;
					$("#div-head-"+k).width( ww +"px");
				}
			document.getElementById("style1").innerHTML=tx;
		} else {
			kxtable_set_width_th (false);
		}	
	}


//------------------------------------------------------------------------------------------------------------------------------		
		function kxtable_set_table_body(){
			//set input
			//sort_data(sort_col,true);
						
			var txt="";
			for (r=0;r <  kxtable_sort_data.length;r++) {
				xrow = kxtable_sort_data[r];
				nn = r+1;
				txt +="<tr><td>" + nn + "</td>";
				for (i=0;i <  kxtable_data_cols.length;i++) {
					txt += "    <td>" + xrow[ kxtable_data_cols[kxtable_Arrangement[i]]] + " </td>";
				}
				txt += "</tr>" ;
			}
			//set output
			document.getElementById("kxtable_body").innerHTML= txt ;
		}
//------------------------------------------------------------------------------------------------------------------------------		
function kxtable_set_table_body_split(split_col,show_det){
		// * function describ
			// split_col = titel of colomn that split shoud be act, acording it
			// show_det = a value in split_colomn that its group (rows that grouped under it) shoud be shows
		// * set input 
		
			if ((show_det=="ALL") || (show_det == "---")) {do_r=true;} else {do_r=false;}
			var x=sort_data(split_col,do_r);
			split_col=split_col.trim();
					
			var txt,txt1,txt0,tx,xx,last;
			last="";txt="";txt0="";txt1="";	tx="<ul>";
			
		// * find index of colomn that its titel is = kxtable_sum_col	
			var sum_col = -1; 	// index of kxtable_sum_col
			if (kxtable_sum_col !== "") {
					for (i=0;i <  kxtable_data_cols.length;i++) {
							if (kxtable_data_cols[kxtable_Arrangement[i]]==kxtable_sum_col) {
								sum_col=i;
								break;    //9612 
							}
				}
			}
		//	
			var sum_v=0;			
			for (r=0;r <  kxtable_sort_data.length;r++) {
				xrow=kxtable_sort_data[r];
					xx=xrow[split_col];
					if (xx != last) {
						if (last != "" ) {
							txt0 =make_titel_tr_for_1_fild_in_split (split_col,last,nn,sum_v.toFixed(1));
							txt += txt0 + txt1; 
							//tx += "<li>" + nn + " - " + last + "</li>";
						}
						last=xx;
						nn=0;
						sum_v=0;
						txt1="";
					}
				nn=nn+1;
				if (sum_col > -1) {sum_v += Number(xrow[kxtable_data_cols[kxtable_Arrangement[sum_col]]]) ; }
				if ((show_det=="ALL") || (show_det == xx.trim())) {
						txt1 +="<tr><td>" + nn + "</td>";
						for (i=0;i <  kxtable_data_cols.length;i++) {
							txt1 += "    <td>" + xrow[ kxtable_data_cols[kxtable_Arrangement[i]]] + " </td>";
						}
						txt1 += "</tr>" ;
				}	
			}
			if (last != "" ) {
							txt0 = make_titel_tr_for_1_fild_in_split (split_col,last,nn,sum_v);
							txt += txt0 + txt1; 
							//tx += "<li>" + nn + " - " + last + "</li>";
			}
			
		//** set output
			document.getElementById("kxtable_body").innerHTML= txt ;
			//document.getElementById("kxtable_div0").innerHTML= tx + "</ul>" ;
			$(".xxlink").click(function(){
						kxtable_set_table_body_split(split_col,$(this).text().trim());
						kxtable_set_width (true);	
						//document.getElementById("kxtable_div0").innerHTML=split_col + " -- " + $(this).text() + ($(this).text().trim()=="950802");
			}); 
		}
//-----------------------------------------------------------------------
function kxtable_set_table_body_split2(split_col1,show_det){
			//set input
			
			
			var split_col2 = kxtable_data_cols[kxtable_Arrangement[0]];
			 split_col1 = split_col1.trim(); //9612
			 split_col2 = split_col2.trim(); //9612

			if (split_col2 == split_col1) {split_col2= kxtable_data_cols[kxtable_Arrangement[1]];}
			if ((show_det=="ALL") || (show_det == "---")) {do_r=true;} else {do_r=false;}
			var x = sort_data(split_col1,do_r);
			 split_col2 = split_col2.trim();	//9612	
			 zz=0; //9612
			
			var tb0,tb1,txt1,txt0,nn1,nn2,temp_num;
			
			tb0 = "";tb1 = "";txt0 = "";txt1 = "";txt2="";	
			nn2 = 0;nn1 = 0 ;	
		// find sum_colonmn index 	
			var sum_col = -1;
			
			if (kxtable_sum_col !== "") {
					for (i=0;i <  kxtable_data_cols.length;i++) {
							if (kxtable_data_cols[kxtable_Arrangement[i]]==kxtable_sum_col) {
								sum_col=i;
								//break; //9612  
							}
				}
			}
		// 	
			var sum_v2=0;  // sum of row  
			var sum_v1=0;
			var last1 = "";  	// last base_group name 
			var last2 = "";		// last sub_group name
			var	xx1="";
			var	xx2="";
				
			for (r=0;r <  kxtable_sort_data.length;r++) {
				xrow=kxtable_sort_data[r];
					xx1 = xrow[split_col1];
					xx2 = xrow[split_col2];
					if (last2 !== "" ) {
						
						if ((xx2 != last2)||(xx1 != last1))  {
							sum_v2 =sum_v2.toFixed(1)
							txt1 = make_titel_tr_for_1_fild_in_split2 (split_col1,split_col2,last1,last2,nn2,sum_v2);
							kxtable_gr_out_data.push([last1,last2,sum_v2]);  //9612
							tb1 += txt1 + txt2;		
							nn1 += nn2 ;
							//sum_v1 += Number(sum_v2) ;
							last2 = xx2 ;
							nn2 = 0;
							sum_v2= 0 ;
							txt2 = "" ;
							if (xx1 != last1) {
								txt0 = make_titel_tr_for_1_fild_in_split (split_col1,last1,nn1,sum_v1.toFixed(1));
								tb0 += txt0 + tb1; 
								last1 = xx1 ;
								nn1 = 0 ;
								sum_v1=0 ;
								tb1 = "" ;
							} 
							
						} 
					} else {
						
						last2 = xx2 ;
						last1 = xx1 ;
					}	
				nn2 += 1;
				if (sum_col > -1) { temp_num =Math.round(Number(xrow[kxtable_data_cols[kxtable_Arrangement[sum_col]]])*10)/10 ;
						sum_v2 += temp_num;
						sum_v1 += temp_num;
				}
				
				if ((show_det == "ALL") || (show_det == xx2.trim())) {
						txt2 +="<tr><td>" + nn2 + "</td>";
						for (i=0;i <  kxtable_data_cols.length;i++) {
							txt2 += "    <td>" + xrow[ kxtable_data_cols[kxtable_Arrangement[i]]] + " </td>";
						}
						txt2 += "</tr>" ;
				}	
			}
			//alert ("split_col1=" + split_col1 + ",split_col2="+split_col2 + ","+ last1 +","+ last2 +","+ nn2 +","+ sum_v2.toFixed(1));
			
			if (last1 !== "" ) {
							sum_v2 =sum_v2.toFixed(1)
							txt1 = make_titel_tr_for_1_fild_in_split2 (split_col1,split_col2,last1,last2,nn2,sum_v2);
							kxtable_gr_out_data.push([last1,last2,sum_v2]);  //9612
							tb1 += txt1 + txt2;		
							nn1 += nn2 ;
								txt0 =make_titel_tr_for_1_fild_in_split (split_col1,last1,nn1,sum_v1.toFixed(1));
								tb0 += txt0 + tb1; 
			}
			
			// set output
			document.getElementById("kxtable_body").innerHTML= tb0 ;
			// document.getElementById("kxtable_div0").innerHTML= tx + "</ul>" ;
			$(".xxlink").click(function(){
						alert ($(this).text().trim());
						kxtable_set_table_body_split2(split_col1,$(this).text().trim());
						kxtable_set_width (true);	
						// document.getElementById("kxtable_div0").innerHTML=split_col + " -- " + $(this).text() + ($(this).text().trim()=="950802");
			});  
	kxtable_set_width (true);	
}
	
//-----------------------------------------------------------------------
function make_titel_tr_for_1_fild_in_split(split_col,split_val,split_sum,sum_val){
	
	var txt0 ="<tr><td style='background-color:#aaaa00'>" + split_sum + " # </td>";
	for (i=0;i <  kxtable_data_cols.length;i++) {
		if (kxtable_data_cols[kxtable_Arrangement[i]]==split_col) {
			txt0 += "    <td  class='xxlink' style='background-color:#aaaa00;color:#ffffff; ' >" + split_val + " </td>";
		} else if (kxtable_data_cols[kxtable_Arrangement[i]]==kxtable_sum_col) {
			txt0 += "    <td  class='xxlink' style='background-color:#aaaa00;color:#ffffff; ' >" + sum_val + " </td>";
		} else {
			txt0 += "    <td >"  + " </td>";
		}	
	}
	txt0 += "</tr>" ;
	return txt0; 
}
//-----------------------------------------------------------------------

function make_titel_tr_for_1_fild_in_split2(split_col1,split_col2,split_val1,split_val2,split_sum2,sum_val){  
	var txt0 ="<tr><td style='background-color:#00aaff'>" + split_sum2 + " # </td>";
	for (i=0;i <  kxtable_data_cols.length;i++) {
		if (kxtable_data_cols[kxtable_Arrangement[i]]==split_col1) {
			txt0 += "    <td  class='xxlink' style='background-color:#00aaff;color:#ffffff; ' >" + split_val1 + " </td>";
		} else if (kxtable_data_cols[kxtable_Arrangement[i]]==split_col2) {
			txt0 += "    <td  class='xxlink' style='background-color:#00aaff;color:#ffffff; ' >" + split_val2 + " </td>";
		} else if (kxtable_data_cols[kxtable_Arrangement[i]]==kxtable_sum_col) {
			txt0 += "    <td  class='xxlink' style='background-color:#00aaff;color:#ffffff; ' >" + sum_val + " </td>";
		} else {
			txt0 += "    <td >"  + " </td>";
		}	
	}
	txt0 += "</tr>" ;
	return txt0;  
}

//-----------------------------------------------------------------------
function sort_data(sort_col,do_reverse){
	var xs_col,xs_mode,xmn;
	var xx0,xx1,xx2,xx3,xx4,xx5,xxn;

	  xs_col=document.getElementById("xsort_col").value;
	  xs_mode=document.getElementById("xsort_mode").checked;
	 // xs_col=xsort_c_name;
	 // xs_mode=xsort_c_mode;
	xmn=1;	
	
	if (sort_col === ""){xx0 = kxtable_data_cols[kxtable_Arrangement[0]];} else {xx0=sort_col.trim();}
	xx0=xx0.trim();
	if (xs_col==xx0) {
		if (do_reverse === true){xs_mode =!(xs_mode);}
	} else {
		//if (xs_mode!=true || xs_mode!=false) { xs_mode =true;}
		 xs_mode =true;
	}
	if (xs_mode === true) {xmn=1;} else {xmn=-1;}
	
	xxn=kxtable_data_cols.length;
	xx1=kxtable_data_cols[kxtable_Arrangement[0]].trim();
	if (xxn > 0) {xx2=kxtable_data_cols[kxtable_Arrangement[1]].trim();}
	if (xxn > 1) {xx3=kxtable_data_cols[kxtable_Arrangement[2]].trim();}
	if (xxn > 2) {xx4=kxtable_data_cols[kxtable_Arrangement[3]].trim();}
	if (xxn > 3) {xx5=kxtable_data_cols[kxtable_Arrangement[4]].trim();}
	
	kxtable_sort_data=kxtable_data.sort(function(a, b){
		re=((a[xx0] > b[xx0])-(a[xx0] < b[xx0]))* xmn ;
		if (re !== 0 || xx1 === "") {return re;}
		re=((a[xx1] > b[xx1])-(a[xx1] < b[xx1]))* xmn ;
		if (re !== 0 || xx2 === "") {return re;}
		re=((a[xx2] > b[xx2])-(a[xx2] < b[xx2]))* xmn ;
		if (re !== 0 || xx3 === "") {return re;}
		re=((a[xx3] > b[xx3])-(a[xx3] < b[xx3]))* xmn ;
		if (re !== 0 || xx4 === "") {return re;}
		re=((a[xx4] > b[xx4])-(a[xx4] < b[xx4]))* xmn ;
		if (re !== 0 || xx5 === "") {return re;}
		re=((a[xx5] > b[xx5])-(a[xx5] < b[xx5]))* xmn ;
		return re;
	});
	 document.getElementById("xsort_col").value=xx0;
	 document.getElementById("xsort_mode").checked=xs_mode;
	 xsort_c_name=xx0;
	 xsort_c_mode=xs_mode;
} 	
			 
// -----coocke

function setCookie(cname, cvalue) {
  document.cookie = filename + cookiePage +  cname + "=" + cvalue ;
}

function getCookie(cname) {
    var name = filename + cookiePage + cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}
//-----------------------------------------------------------------------
function checkCookie() {
    var user = getCookie("username");
    if (user != "") {
        alert("Welcome again " + user);
    } else {
        user = prompt("Please enter your name:", "");
        if (user != "" && user != null) {
            setCookie("username", user, 365);
			//getCookie("username");
        }
    }
}
//--------------------------------------------------------------------------
/*
function move_item_in_array(x_array,obj_pos,move_val){
		temp = x_array[obj_pos]
		if (move_val<0) {}
			for (i=obj_pos;i<obj_pos+move_val;i++){
				x_array[i]=x_array[i+1]
			}
		} else{
			for (i=obj_pos;i>obj_pos+move_val;i--){
				x_array[i]=x_array[i+1]
			}
		}		
		x_array[obj_pos+move_val]=temp	
}								
function find_obj_index_in_table(obj_name){
	for (i=0;i < kxtable_data_cols.length;i++) {
		w=kxtable_data_cols[kxtable_Arrangement[i]];
		if (obj_name==w){return i};
	}
}
*/
//----------------------------------------
function kxflot_pr(x_c) { 
	if (kxtable_gr_out_data.length==0){
		var split_col1= kxtable_data_cols[kxtable_Arrangement[0]];
		var show_det="---";
		kxtable_set_table_body_split2(split_col1,show_det);
	}
	
	var xx,xxo,xi,oi,vi,fo,fx,fv,last_oi=""; 
	var	x_ar=[],o_ar=[],x2d_ar=[];
	var	x_ob={},xt_ob={},b_ob={};
	
	for(xx in kxtable_gr_out_data){
		xxo=kxtable_gr_out_data[xx];
		fx=xxo[0];
		fo=xxo[1];
		fv=xxo[2];
		if (o_ar.indexOf(fo) === -1) { o_ar.push(fo)};
		if (x_ar.indexOf(fx) === -1) { x_ar.push(fx)};
	}  
		//	alert (x_ar + " # " + o_ar);
	//creat base obj 
		var ziroSubArray = [];//
	
		var lo=o_ar.length
		for(var j = 0; j <  lo; j++){
				ziroSubArray.push(0);
		}
		var lx=x_ar.length
		for(var i = 0; i < lx; i++){
			//x2d_ar.push(ziroSubArray);
			x2d_ar[i]=[]
			for(var j = 0; j <  lo; j++){
				x2d_ar[i].push(0);
			}
		}
		//alert ("base obj created");
	//copy func	
	
	function copy(mainObj) {
	  var objCopy = {},key; // objCopy will store a copy of the mainObj
	  for (key in mainObj) { objCopy[key] = mainObj[key];} // copies each property to the objCopy object
	  return objCopy;
	}
	
	for(xx in kxtable_gr_out_data){
		xxo=kxtable_gr_out_data[xx]
		fx=xxo[0];
		fo=xxo[1];
		fv=xxo[2];
		oi=o_ar.indexOf(fo)
		xi=x_ar.indexOf(fx)
		//alert (xi + "-"+oi+ "-"+fx+ "-"+fo+ "-"+fv)
		x2d_ar[xi][oi]=fv
	} 
	//$("#kxtable_note").text(x2d_ar); 
	//alert(1);
	var oo={},or=[],kxflot_Data={},sum=0
	
	if (x_c==0) {
		for(var i = 0; i < lx; i++){
			oo.label=x_ar[i];
			sum=0;
			for(var j = 0; j <  lo; j++){ or[j]=[o_ar[j],x2d_ar[i][j]];sum += x2d_ar[i][j] }
			oo.data=or;
			oo.sum=sum;
			//alert (JSON.stringify(oo));
			kxflot_Data[x_ar[i]] = JSON.parse(JSON.stringify(oo)); 
		}
	} else{
		for(var i = 0; i < lo; i++){
			oo.label=o_ar[i]
			sum=0;
			for(var j = 0; j <  lx; j++){ or[j]=[x_ar[j],x2d_ar[j][i]];sum += x2d_ar[j][i] }
			oo.data=or;
			oo.sum=sum;
			//alert (JSON.stringify(oo));
			kxflot_Data[x_ar[i]] = JSON.parse(JSON.stringify(oo)); 
		}	
	}	
	//$("#kxtable_note").text(JSON.stringify(kxflot_Data));
	/*
	var kxflot_Data  = {
			 "s1":{
				label: "s1",
				data: [ ["a", 11], ["b", 8], ["c", 4]]
			},        
			"s2":{
				label: "s2",
				data: [ ["a", 11], ["b", 8], ["c", 4]]
			}        			
		};	*/
   localStorage.setItem("kxflot_Data", JSON.stringify(kxflot_Data));
   window.open("link/kxflot.htm","","width=800,height=450") 
}
//----------------------------------------------------------
function swich_ar(ar,a,b){
	var c;
	c=ar[a];
	ar[a]=ar[b];
	ar[b]=c;
}

	
