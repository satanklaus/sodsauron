$(document).ready(function() {
	console.log("@onready [create]")
//	refresh_style()
	$("#createitem-form").find("#id_orgbranch").prop( "disabled", true )
	$("#createitem-form").find("#id_location").prop( "disabled", true )
	$("#createitem-form").find("#id_model").prop( "disabled", true )
   	refresh_organizations($("#createitem-form"))
   	refresh_itemtypes($("#createitem-form"))
	$(".select2").select2()
	$("#id_organization").select2( {sorter: data => data.sort((a,b) => a.text.localeCompare(b.text))})
	$("#id_orgbranch").select2( {sorter: data => data.sort((a,b) => a.text.localeCompare(b.text))})
	$("#id_location").select2( {sorter: data => data.sort((a,b) => a.text.localeCompare(b.text))})
	$("#id_itemtype").select2( {sorter: data => data.sort((a,b) => a.text.localeCompare(b.text))})
	$("#id_model").select2( {sorter: data => data.sort((a,b) => a.text.localeCompare(b.text))})
	refresh_events()
/*
   $("#ninestyle").click(function() {
	console.log("CHANGE: ", Cookies.get("style"))
   	if (!Cookies.get("style")) Cookies.set("style","eye")
	if (Cookies.get("style")=="eye") Cookies.set("style","nine")
	else Cookies.set("style","eye")
	console.log("TO: ", Cookies.get("style"))
	refresh_style()
   })
*/

   $("#id_organization").change(function(obja){ 
	   console.log('@organization changed')
	   //on set empty option
	   if($("#createitem-form").find("#id_organization")[0].value == "") {
	   	$("#createitem-form").find("#id_orgbranch").html("")
	   	$("#createitem-form").find("#id_orgbranch").prop( "disabled", true )
	   	$("#createitem-form").find("#id_location").html("")
	   	$("#createitem-form").find("#id_location").prop( "disabled", true )
	   }
	   //on select any organization
	   else {
	   	$("#createitem-form").find("#id_orgbranch").prop( "disabled", false )
	        refresh_orgbranches($("#createitem-form"))
	   }
	   $("#createitem-form").find("#id_location").html("")
	   $("#createitem-form").find("#id_location").prop( "disabled", true )
   })

   $("#id_orgbranch").change(function(obja){ 
	   console.log('@orgbranch changed')
	   //on set empty option
	   if($("#createitem-form").find("#id_orgbranch")[0].value == "") {
	   	$("#createitem-form").find("#id_location").html("")
	   	$("#createitem-form").find("#id_location").prop( "disabled", true )
	   }
	   //on select any orgbranch
	   else {
	   	$("#createitem-form").find("#id_location").prop( "disabled", false )
	        refresh_locations($("#createitem-form"))
	   }
   })

   $("#id_itemtype").change(function(obja){ 
	   console.log('@itemtype changed')
	   //on set empty option
	   if($("#createitem-form").find("#id_itemtype")[0].value == "") {
	   	$("#createitem-form").find("#id_model").html("")
	   	$("#createitem-form").find("#id_model").prop( "disabled", true )
	   }
	   //on select any orgbranch
	   else {
	   	$("#createitem-form").find("#id_model").prop( "disabled", false )
	        refresh_models($("#createitem-form"))
	   }
   })
})
