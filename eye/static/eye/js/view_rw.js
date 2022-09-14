$(document).ready(function() {
	console.log("@onready [view_rw]")
//	refresh_style()
//	$("#viewrw-form").find("#id_orgbranch").prop( "disabled", true )
//	$("#viewrw-form").find("#id_location").prop( "disabled", true )
//	$("#viewrw-form").find("#id_model").prop( "disabled", true )
	//createitem
	//
	//
	$(".select2").select2()
	$(".datetime").flatpickr({
                         enableTime: true,
                         dateFormat: "d/m/Y H:i",
                         time_24hr: true,
                 })
	$(".datetime-inline").flatpickr({
                         enableTime: true,
                         dateFormat: "d/m/Y H:i",
                         time_24hr: true,
			 inline: true
                 })

	$("#id_organization").select2( {sorter: data => data.sort((a,b) => a.text.localeCompare(b.text))})
	$("#id_orgbranch").select2( {sorter: data => data.sort((a,b) => a.text.localeCompare(b.text))})
	$("#id_location").select2( {sorter: data => data.sort((a,b) => a.text.localeCompare(b.text))})
	$("#id_itemtype").select2( {sorter: data => data.sort((a,b) => a.text.localeCompare(b.text))})
	$("#id_model").select2( {sorter: data => data.sort((a,b) => a.text.localeCompare(b.text))})

	target_org = $("#viewrw-form #id_organization")
	selection_org = target_org.val()
  	refresh_organizations($("#viewrw-form"))
   	refresh_itemtypes($("#viewrw-form"))
	refresh_events()

	




/*
*/
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
	   if($("#viewrw-form").find("#id_organization")[0].value == "") {
	   	$("#viewrw-form").find("#id_orgbranch").html("")
	   	$("#viewrw-form").find("#id_orgbranch").prop( "disabled", true )
	   	$("#viewrw-form").find("#id_location").html("")
	   	$("#viewrw-form").find("#id_location").prop( "disabled", true )
	   }
	   //on select any organization
	   else {
	   	$("#viewrw-form").find("#id_orgbranch").prop( "disabled", false )
	        refresh_orgbranches($("#viewrw-form"))
	   }
	   $("#viewrw-form").find("#id_location").html("")
	   $("#viewrw-form").find("#id_location").prop( "disabled", true )
   })

   $("#id_orgbranch").change(function(obja){ 
	   console.log('@orgbranch changed')
	   //on set empty option
	   if($("#viewrw-form").find("#id_orgbranch")[0].value == "") {
	   	$("#viewrw-form").find("#id_location").html("")
	   	$("#viewrw-form").find("#id_location").prop( "disabled", true )
	   }
	   //on select any orgbranch
	   else {
	   	$("#viewrw-form").find("#id_location").prop( "disabled", false )
	        refresh_locations($("#viewrw-form"))
	   }
   })

   $("#id_itemtype").change(function(obja){ 
	   console.log('@itemtype changed')
	   //on set empty option
	   if($("#viewrw-form").find("#id_itemtype")[0].value == "") {
	   	$("#viewrw-form").find("#id_model").html("")
	   	$("#viewrw-form").find("#id_model").prop( "disabled", true )
	   }
	   //on select any orgbranch
	   else {
	   	$("#viewrw-form").find("#id_model").prop( "disabled", false )
	        refresh_models($("#viewrw-form"))
	   }
   })

})
