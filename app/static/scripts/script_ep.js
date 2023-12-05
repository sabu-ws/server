var temp_uuid;

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		}
	}
});


// ========= sidebar
$(document).ready(function() {
	var currentPath = window.location.pathname;
	var panelIndex = currentPath.indexOf("/panel/");
	if (panelIndex !== -1) {
		var currentPage = currentPath.substring(panelIndex + 7).split('/')[0];
		$('#sidebar-' + currentPage).addClass(["text-blue-800", "bg-white/60"]);
		$('#sidebar-' + currentPage).removeClass(["text-white", "hover:text-blue-800", "hover:bg-white/60"]);
	}
});

// ======== dark mode working
$("#ToggleDarkMode").click(function(){
	if(localStorage.theme === 'dark' ){
		localStorage.theme = 'light';
		document.documentElement.classList.remove('dark');
		$("#ToggleDarkModeIcon").removeClass("fa-moon");
		$("#ToggleDarkModeIcon").addClass("fa-sun");
	}else{
		document.documentElement.classList.add('dark');
		$("#ToggleDarkModeIcon").removeClass("fa-sun");
		$("#ToggleDarkModeIcon").addClass("fa-moon");
		localStorage.theme = 'dark';
	}
});

if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
	localStorage.theme = 'dark';
	document.documentElement.classList.add('dark');
	$("#ToggleDarkModeIcon").removeClass("fa-sun");
	$("#ToggleDarkModeIcon").addClass("fa-moon");
	$("#ToggleDarkMode").prop("checked",true);
} else {
	localStorage.theme = 'light';
	document.documentElement.classList.remove('dark');
	$("#ToggleDarkModeIcon").removeClass("fa-moon");
	$("#ToggleDarkModeIcon").addClass("fa-sun");
	$("#ToggleDarkMode").prop("checked",false);
}
// =============================================


// =========== toggle buttont view password
$(".toggleView").click(function(){
	if($(this).closest("div").closest("button").prev().attr("type") == "password"){
		$(this).closest("div").closest("button").prev().attr("type","text");
		$(this).removeClass("fa-eye");
		$(this).addClass("fa-eye-slash");
	}else{
		$(this).closest("div").closest("button").prev().attr("type","password");
		$(this).removeClass("fa-eye-slash");
		$(this).addClass("fa-eye");
	}
});

// ======== add Endpoint 
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


// ====== Delete endpoint

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


// ======= change status dynamic

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