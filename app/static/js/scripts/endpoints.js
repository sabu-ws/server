var temp_uuid;

// Add Endpoint 
$("#addEndpointForm").submit(function(e) {
	e.preventDefault();
	$.ajax({
		type: "POST",
		url: addEndpointUrl,
		data: $("#addEndpointForm").serialize(),
		success: function(data)
		{
			if(data == "ok"){
				window.location.reload();
			}else{
				alertAddEndpointForm = document.getElementById("alertAddEndpointForm");
				alertAddEndpointForm.style = "display: true;";
				const ErrorMSG= "Error : ";
				$("#spanErrorAddEndpointForm").text(ErrorMSG.concat(data));
			}
		}
	});
});

$("#genTokenButton").click(function(){
	$.ajax({
		type: "GET",
		url: genToken,
		// data: $("#addEndpointForm").serialize(),
		success: function(data){
			$("#endpointToken").val(data)
		}
	});
});

$("#btnCopyTokenEP").click(function(){
	$("#endpointToken").select();
	document.execCommand('copy');
	$("#copyInfoEP").html("Copied ✓")
	window.getSelection().removeAllRanges();
});

// Delete Endpoint
$('.buttonDeleteRow').click(function(e){
	var $item = $(this).closest("tr")
			.find("#uuid")
			.text();
	temp_uuid = $item.trim();
});

$("#yesButtonDeleteEndpoint").click(function(e){
	e.preventDefault()
	$.ajax({
		type: "POST",
		url: delEndpointUrl,
		data: {'uuid':temp_uuid},
		success: function(data){
			if(data == "ok"){
				window.location.reload();
			}
		}
	});
});

// Change Status Dynamic
// var socket = io.connect();
var socket = io.connect("/state_ep");
socket.on("state",function(data){
	$("#table_endpoint tr").each(function(){
		if($(this).find("#uuid").text().trim()===data["uuid"]){
			if(data["state"]==="up"){
				$(this).find("#state_text").text("Up")
				$(this).find("#state_icon").removeClass("bg-red-500")
				$(this).find("#state_icon").addClass("bg-green-500")
			}else if(data["state"]==="down"){
				$(this).find("#state_text").text("Down")
				$(this).find("#state_icon").removeClass("bg-green-500")
				$(this).find("#state_icon").addClass("bg-red-500")
			}
		}
	})
})

$("#table-search-endpoints").keyup(function() {
	var value = $(this).val().toLowerCase();
	$("#table_endpoint tr").filter(function() {
		$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
	});
	if($("#table_endpoint").find('tr').is(':visible')){
		document.getElementById("noEndpointFound").style  = "display: none;";
	}else{
		document.getElementById("noEndpointFound").style  = "display: True;";
	}
});	