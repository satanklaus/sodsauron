$(document).ready(function(){
	idprefix		= 'modal_id_'
	modal 		= document.querySelector('.modal');
	closeButtons 	= document.querySelectorAll('.close-modal');
	openButtons		= document.querySelectorAll('.open-modal');

	for (i = 0; i < openButtons.length; ++i) {
	  openButtons[i].addEventListener('click', function(event) {
	    parentform = $(event.target).parents('form')
	    console.log("@open_modal",$(event.target).parents('form'))
	    modal.classList.toggle('modal-open');

	    event.preventDefault()
		  //linktype = event.target.id.replace(idprefix,'')
	    linktype = $(event.target).parents('a')[0].id.replace(idprefix,'')
	    console.log("LINKTYPE: ", linktype)
	    var jqxhr = $.ajax( "/modal/add_"+linktype+"/" )
  		.done(function(data) {
            	$("#modal_title").html('Add '+linktype)
            	$("#modal_body").html(data)
		$("#modal_button").unbind()
		$("#modal_button").data('linktype',linktype)
		switch(linktype) {
			case 'qrcodes':
				console.log("@qrcodes")
				$("#modal_button").click(modal_qrcodes_submit)
				break
			case 'organization':
				console.log("@organization")
				$("#modal_button").click(modal_organization_submit)
				break
			case 'itemtype':
				console.log("@itemtype")
				$("#modal_button").click(modal_itemtype_submit)
				break
			case 'orgbranch':
				console.log("@orgbranch")
				selected_organization = parentform.find("#id_organization").val()
				$("#modal_body #id_organization").val(selected_organization)
				$("#modal_button").click(modal_orgbranch_submit)
				break
			case 'model':
				console.log("@model")
   				selected_itemtype = parentform.find("#id_itemtype").val()
				$("#modal_body #id_type").val(selected_itemtype)
				$("#modal_button").click(modal_model_submit)
				break
			case 'location':
				console.log("@location")
				selected_organization = parentform.find("#id_organization").val()
				selected_orgbranch = parentform.find("#id_orgbranch").val()
				$("#modal_body #id_organization").val(selected_organization)
				$("#modal_body #id_orgbranch").val(selected_orgbranch)
				$("#modal_button").click(modal_location_submit)
				console.log("@location2")
				break
			default:
				if(linktype.match('event')) {
					$("#modal_button").click(modal_event_submit)
				}
				break

		}
  		})
  		.fail(function() {
    		   console.log( "error loading form" );
  		})
  		.always(function() {
    			console.log( "@complete form load" );
  		});

	});
	}

	for (i = 0; i < closeButtons.length; ++i) {
	  closeButtons[i].addEventListener('click', function() {
	    modal.classList.toggle('modal-open');
		});
	}
	document.querySelector('.modal-inner').addEventListener('click', function() {
	  modal.classList.toggle('modal-open');
	});
	// prevent modal inner from closing parent when clicked
	document.querySelector('.modal-content').addEventListener('click', function(e) {
		e.stopPropagation();
	});
})

function modal_itemtype_submit(event){
	$.ajax({
      		type: "POST",
      		url: "/modal/add_"+$("#modal_button").data('linktype')+'/',
      		data: $("#modal_form").serialize()
	})
  		.done(function(data) {
		switch(data['status']){
		   case "error":
		      console.log("modal error")
		      $("#errors").html("")
		      for (err in data['data'])
		      $("#errors").append("<b>@"+err+": </b>"+data['data'][err][0])
		      break
		   case "success":
		      console.log("modal success")
		      refresh_itemtypes(parentform)
	    	      modal.classList.toggle('modal-open');
		      break
		}
  		});
}

function modal_model_submit(event){
	$.ajax({
      		type: "POST",
      		url: "/modal/add_"+$("#modal_button").data('linktype')+'/',
      		data: $("#modal_form").serialize()
	})
  		.done(function(data) {
		switch(data['status']){
		   case "error":
		      console.log("modal error")
		      $("#errors").html("")
		      for (err in data['data'])
		      $("#errors").append("<b>@"+err+": </b>"+data['data'][err][0])
		      break
		   case "success":
		      console.log("modal success")
		      refresh_models(parentform)
	    	      modal.classList.toggle('modal-open');
		      break
		}
  		});
}

function modal_event_submit(event){
	item_id = $("#modal_button").data('linktype').match(/\d+/g)[0] 
	console.log("MODAL EVENT EVENT: ", item_id)
	$.ajax({
      		type: "POST",
      		url: "/modal/add_"+$("#modal_button").data('linktype')+'/',
      		data: $("#modal_form").serialize()
	})
  		.done(function(data) {
		switch(data['status']){
		   case "error":
		      console.log("modal error")
		      $("#errors").html("")
		      for (err in data['data'])
		      $("#errors").append("<b>@"+err+": </b>"+data['data'][err][0])
		      break
		   case "success":
		      refresh_events()
		      console.log("modal success")
	    	      modal.classList.toggle('modal-open');
		      break
		}
  		});
}

function modal_location_submit(event){
	console.log("@submit location")
	$.ajax({
      		type: "POST",
      		url: "/modal/add_"+$("#modal_button").data('linktype')+'/',
      		data: $("#modal_form").serialize()
	})
  		.done(function(data) {
		switch(data['status']){
		   case "error":
		      console.log("add location error")
		      $("#errors").html("")
		      for (err in data['data'])
		      $("#errors").append("<b>@"+err+": </b>"+data['data'][err][0])
		      break
		   case "success":
		      console.log("add location success")
		      refresh_locations(parentform)
	    	      modal.classList.toggle('modal-open');
		      break
		}
  		});
}

function modal_orgbranch_submit(event){
	console.log("@submit orgbranch")
	$.ajax({
      		type: "POST",
      		url: "/modal/add_"+$("#modal_button").data('linktype')+'/',
      		data: $("#modal_form").serialize()
	})
  		.done(function(data) {
		switch(data['status']){
		   case "error":
		      console.log("add orgbranch error")
		      $("#errors").html("")
		      for (err in data['data'])
		      $("#errors").append("<b>@"+err+": </b>"+data['data'][err][0])
		      break
		   case "success":
		      console.log("@add orgbranch success")
		      refresh_orgbranches(parentform)
	    	      modal.classList.toggle('modal-open');
		      break
		}
  		});
}

function modal_organization_submit(event){
	console.log("@submit organization")
	$.ajax({
      		type: "POST",
      		url: "/modal/add_"+$("#modal_button").data('linktype')+'/',
      		data: $("#modal_form").serialize()
	})
  		.done(function(data) {
		switch(data['status']){
		   case "error":
		      console.log("@add org error")
		      $("#errors").html("")
		      for (err in data['data'])
		      $("#errors").append("<b>@"+err+": </b>"+data['data'][err][0])
		      break
		   case "success":
		      console.log("@add org success")
		      refresh_organizations(parentform)
	    	      modal.classList.toggle('modal-open');
		      break
		}
  		});
}

function modal_qrcodes_submit(event){
	console.log("@submit qrcodes")
	$.ajax({
      		type: "POST",
      		url: "/modal/add_"+$("#modal_button").data('linktype')+'/',
      		data: $("#modal_form").serialize()
	})
  		.done(function(data) {
		switch(data['status']){
		   case "error":
		      console.log("@add qr error")
		      $("#errors").html("")
		      for (err in data['data'])
		      $("#errors").append("<b>@"+err+": </b>"+data['data'][err][0])
		      break
		   case "success":
		      console.log("@add qr success",data.data.number)
		      location.href = data.data.redirect
	    	      modal.classList.toggle('modal-open');
		      
		      break
		}
  		})
  		.fail(function(data) { console.log("ajax error")})
}
