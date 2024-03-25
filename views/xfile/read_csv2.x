<!DOCTYPE html>
<html>
<head>
	{{def URL(a,b): return "./"+b}}
	<!-- choose a theme file -->
	<link rel="stylesheet" href="{{=URL('.','tablesorter/css/theme.blue.css')}}">
	<!-- load jQuery and tablesorter scripts -->
	<script type="text/javascript" src="{{=URL('.','tablesorter/jquery-3.7.1.min.js')}}"></script>
	<script type="text/javascript" src="{{=URL('.','tablesorter/js/jquery.tablesorter.js')}}"></script>
	
	<!-- tablesorter widgets (optional) -->
	<script type="text/javascript" src="{{=URL('static','tablesorter/js/jquery.tablesorter.widgets.js')}}"></script>
	
	
<script>
	$(document).ready(function(){
	  $(".table2").tablesorter({
		theme : 'blue',
		widgets: ["resizable","saveSort","stickyHeaders","zebra", "filter"],
	  });
	 
	});
</script>
</head>
<body>
	{{=x_table}}
</body>



