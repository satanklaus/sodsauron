function refresh_organizations(form)
{
   console.log('@refresh organizations, form:',form)
   target_org = form.find("#id_organization")
   selection_org = target_org.val()
   target_org.html("")
   target_org.append("<option value=\"\" selected=\"\">++++</option>")
   $.get("/ajax/get-orgs", function(response){
      if (response.status=="success") {
         for (j in response.data.organizations) { 
            target_org.append("<option value="+response.data.organizations[j].pk+">"+response.data.organizations[j].name+"</option>") 
         }
      }
      else target_org.html("error retreive data")
   if (selection_org>0) { 
	   target_org.val(selection_org)
	   refresh_orgbranches(form)
   }
   })
}

function refresh_itemtypes(form)
{
   console.log('@refresh itemtypes, form:',form)
   target_types = form.find("#id_itemtype")
   console.log('test', target_types)
   selection_types = target_types.val()
   target_types.html("")
   target_types.append("<option value=\"\" selected=\"\">++++</option>")
   $.get("/ajax/get-itemtypes", function(response){
      if (response.status == "success") {
         for (j in response.data.itemtypes) { 
            target_types.append("<option value="+response.data.itemtypes[j].pk+">"+response.data.itemtypes[j].name+"</option>") 
         }
      }
	 else target_types.html.log('error retreive data')
      if (selection_types>0) {
	   target_types.val(selection_types)
	      refresh_models(form)
      }
   })
}

function refresh_orgbranches(form, initial)
{
   console.log('@refresh orgbranches, form:',form,'initial:',initial)
   target_ob = form.find("#id_orgbranch")
   selection_ob = target_ob.val()
   target_ob.html("")
   target_ob.append("<option value=\"\" selected=\"\">++++</option>")
      organization_id = form.find("#id_organization")[0].value
      $.get("/ajax/get-orgbranches", {orgname_pk: organization_id}, function(response){
         if (response.status == "success") {
            console.log("DEBUG-OB-branches",response.data.orgbranches)
            for (j in response.data.orgbranches) { 
            console.log("DEBUG-OB",j,response.data.orgbranches[j])
               target_ob.append("<option value="+response.data.orgbranches[j].pk+">"+response.data.orgbranches[j].name+"</option>") 
   	 }
	 if (initial) target_ob.val(initial)
         }
	 else target_ob.html.log('error retreive data')
      if (selection_ob>0) {
	   target_ob.val(selection_ob)
	      refresh_locations(form)
      }
      })
}

function refresh_locations(form)
{
   console.log('@refresh locations, form:',form)
   target_loc = form.find("#id_location")
   selection_loc = target_loc.val()
   target_loc.html("")

   target_loc.append("<option value=\"\" selected=\"\">++++</option>")
      orgbranch_id = form.find("#id_orgbranch")[0].value
      $.get("/ajax/get-locations", {orgbranch_pk: orgbranch_id}, function(response){
         if (response.status == "success") {
            for (j in response.data.locations) { 
               target_loc.append("<option value="+response.data.locations[j].pk+">"+response.data.locations[j].name+"</option>") 
   	 }
         }
	 else target_loc.html.log('error retreive data')
      if (selection_loc>0) {
	   target_loc.val(selection_loc)
      }
      })
}


function refresh_models(form)
{
   console.log('@refresh models, form:',form)
   target_models = form.find("#id_model")
   selection_models = target_models.val()
   target_models.html("")

   target_models.append("<option value=\"\" selected=\"\">++++</option>")
   itemtype_id = form.find("#id_itemtype")[0].value 
      $.get("/ajax/get-models", {itemtype_pk: itemtype_id}, function(response){
         if (response.status == "success") {
            for (j in response.data.models) { 
               target_models.append("<option value="+response.data.models[j].pk+">"+response.data.models[j].name+"</option>") 
   	 }
         }
	 else target_models.html.log('error retreive data')
      if (selection_models>0) {
	   target_models.val(selection_models)
      }
      })
}

function refresh_events()
{
   console.log("@refresh events")
   item_id = window.location.pathname.match(/\/item\/(\d+)\//) 
   if (item_id) {
      item_id=item_id[1]
      console.log("need to refresh item #"+item_id)
      $.get("/ajax/get-events", {item_id: item_id}, function(response) {
	      if (response.status == "success") {
			 $("#events_list").html('')
                 for (event in response.data.events) { 
			 $("#events_list").append("<li><a class='delete_event' href=/event_dismiss/"+response.data.events[event].eventid+"><i id='"+response.data.events[event].eventid+"' class='fa-solid fa-trash-can'></i></a> - <a href=/events/"+response.data.events[event].eventid+">event"+response.data.events[event].eventid+"</a> - "+response.data.events[event].eventtype+" - "+response.data.events[event].date+' - '+response.data.events[event].description)
    		}
		$(".delete_event").click(function(event) {
			event.preventDefault()
			event_id = $(event.target)[0].id
      			$.get("/ajax/delete_event/"+event_id, function(response){
         			if (response.status == "success") {
            				console.log("DEBUG-delete-event",response.data)
 //           				for (j in response.data.orgbranches) { 
  //          					console.log("DEBUG-OB",j,response.data.orgbranches[j])
   //            					target_ob.append("<option value="+response.data.orgbranches[j].pk+">"+response.data.orgbranches[j].name+"</option>") 
   //	 				}
         			}
	 			else console.log('error retreive data')
      			})
		})

	      }
	      else $("#events_list").html("failed to fetch events")
      })
   }


   else {}
}
	
	




function refresh_style(){
   if (!Cookies.get("style")) Cookies.set("style","eye")
   console.log("@refresh_style: ",Cookies.get("style"))
   $("#stylish")[0].href= $("#stylish")[0].href.replace(/\w*\.css$/,Cookies.get("style")+'.css')
}
