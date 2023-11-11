var temp_uuid;
var getRowUserTable;
var previous_url;

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		}
	}
});

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


// ======= Add user

$("#addUserForm").submit(function(e) {
	e.preventDefault();

	var form = $(this);
	var actionUrl = urlAdd;
	$.ajax({
		type: "POST",
		url: actionUrl,
		data: form.serialize(),
		success: function(data)
		{
			if(data == "ok"){
				window.location.reload();
			}else{
				alertAddUserForm = document.getElementById("alertAddUserForm");
				alertAddUserForm.style = "display: true;";
				const ErrorMSG= "Error : ";
				$("#alertAddUserForm span").text(ErrorMSG.concat(data));
			}
		}
	});
});




// ====== Delete User
$('.buttonDeleteRow').click(function(e){
	var $item = $(this).closest("tr")
			.find("#uuidUserTable")
			.text();
	temp_uuid = $item.trim();
});

$("#yesButtonDeleteUser").click(function(e){
	$.ajax({
		type: "POST",
		url: urlDelete,
		data: {'uuid':temp_uuid},
		success: function(data){
			if(data == "ok"){
				window.location.reload();
			}
		}
	});
});

// ====== Modify User 

$('.buttonModifyRow').click(function(e){
	document.getElementById("editErrorFieldForm").style = "display: none;";	
	var GetUUID = $(this).closest("tr")
			.find("#uuidUserTable")
			.text()
			.trim();

	$.ajax({
		type: "POST",
		url: urlModifyQuery,
		data: {'uuid':GetUUID},
		success: function(data){
			$("#editUserUUID").val(data["uuid"]);
			$("#editUserFirstname").val(data["firstname"]);
			$("#editUserName").val(data["name"]);
			$("#editUserUsername").val(data["username"]);
			$("#editUserEmail").val(data["email"]);
			$("#editUserJob").val(data["job"]);
			$("#editUserRole").val(data["role"]);
			if(data["totp"]){
				$("#Disable2FAButton").attr("style","");
			}else{
				$("#Disable2FAButton").attr("style","display: none;");
			}
		}
	});

});

$("#editUserForm").submit(function(e) {
	e.preventDefault();
	$.ajax({
		type: "POST",
		url: urlModify,
		data: $(this).serialize(),
		success: function(data)
		{
			if(data == "ok"){
				window.location.reload();
			}else{
				editErrorFieldForm = document.getElementById("editErrorFieldForm");
				editErrorFieldForm.style = "display: true;";
				const ErrorMSG= "Error : ";
				$("#editErrorFieldForm span").text(ErrorMSG.concat(data));
			}
		}
	});
});

$("#Disable2FAButton").click(function(e){
	e.preventDefault();
	if(confirm("Are you sure to disable TOTP for this user ?")){
		$.ajax({
			type: "POST",
			url: urlDisTotp,
			data: {'uuid':$("#editUserUUID").val()},
			success: function(data)
			{
				if(data == "ok"){
					window.location.reload();
				}
			}
		});
	}
});

// ======= Enable / Disable user
$(".buttonDisableUser").on("click",function(){
	$("#messageEnablModal").html("Are you sure you want to disable this user ?");
});

$(".buttonEnableUser").on("click",function(){
	$("#messageEnablModal").html("Are you sure you want to enable this user ?");
});

$('.buttonAbleUser').click(function(){
	console.log("click");
	var $item = $(this).closest("tr")
			.find("#uuidUserTable")
			.text();
	temp_uuid = $item.trim();
});

$("#yesButtonAbleUser").click(function(e){
	$.ajax({
		type: "POST",
		url: urlAble,
		data: {'uuid':temp_uuid},
		success: function(data){
			if(data == "ok"){
				window.location.reload();
			}
		}
	});
});


// ===== Job manage
$("#AddJobForm").submit(function(e){
	e.preventDefault();
	$.ajax({
		type: "POST",
		url: urlAddJob,
		data: $(this).serialize(),
		success: function(data){
			if(data == "ok"){
				window.location.reload();
			}else{
				$("#ErrorJob").attr("style","");
				$("#ErrorJobMSG").html(data);
			}
		}
	});
});

$("#RemoveJobForm").submit(function(e){
	e.preventDefault();
	$.ajax({
		type: "POST",
		url: urlRemoveJob,
		data: $(this).serialize(),
		success: function(data){
			if(data == "ok"){
				window.location.reload();
			}else{
				$("#ErrorJob").attr("style","");
				$("#ErrorJobMSG").html(data);
			}
		}
	});
});	


// ====== SearchBar

$("#table-search-users").keyup(function() {
	var value = $(this).val().toLowerCase();
	$("#bodyUsersTable tr").filter(function() {
		$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
	});
	if($("#bodyUsersTable").find('tr').is(':visible')){
		document.getElementById("noUserFound").style  = "display: none;";
	}else{
		document.getElementById("noUserFound").style  = "display: True;";
	}
});	


// ====== user settings
$("#enable2fa").click(function(){	
	$.ajax({
		type: "GET",
		url: otp_url,
		success: function(data)
		{
			$("#otp_url").val(data);
			$("#qrcode_render").attr('src',qrcode_url+"?url="+data);
		}
	});
});

// ====== Check totp code
$("#FormCheckTotp").submit(function(e){
	e.preventDefault();
	if($("#TestTOTPCodeInput").val()==""){
		$("#ErrorTotp").attr("style","");
		$("#ErrorTotpMSG").html("Please enter your code.");
	}else{
		$.ajax({
			type: "POST",
			url: check_otp_url,
			data: $(this).serialize(),
			success: function(data)
			{
				if(data=="ok"){
					window.location.reload();
				}else{
					$("#ErrorTotp").attr("style","");
					$("#ErrorTotpMSG").html(data);
				}
			}
		});
	}
});
$("#otpLinkBtn").click(function(){
	$("#otp_url").select();
	document.execCommand('copy');
	$("#copyInfoText").html("Copied ✓")
	window.getSelection().removeAllRanges();
});

// ======== dark mode working
$("#ToggleDarkMode").click(function(){
	if($("#ToggleDarkMode").prop("checked") === false){
		localStorage.theme = 'light';
		document.documentElement.classList.remove('dark');
		$("#ToggleDarkModeIcon").removeClass("fa-moon");
		$("#ToggleDarkModeIcon").addClass("fa-sun");
		$("#ToggleDarkModeText").text("Light mode");
	}else{
		document.documentElement.classList.add('dark');
		$("#ToggleDarkModeIcon").removeClass("fa-sun");
		$("#ToggleDarkModeIcon").addClass("fa-moon");
		$("#ToggleDarkModeText").text("Dark mode");
		localStorage.theme = 'dark';
	}
});

if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
	document.documentElement.classList.add('dark');
	$("#ToggleDarkModeIcon").removeClass("fa-sun");
	$("#ToggleDarkModeIcon").addClass("fa-moon");
	$("#ToggleDarkModeText").text("Dark mode");
	$("#ToggleDarkMode").prop("checked",true);
} else {
	document.documentElement.classList.remove('dark');
	$("#ToggleDarkModeIcon").removeClass("fa-moon");
	$("#ToggleDarkModeIcon").addClass("fa-sun");
	$("#ToggleDarkMode").prop("checked",false);
	$("#ToggleDarkModeText").text("Light mode");
}
// =============================================

// ======== Box info
if($(".boxInfo").is(':visible')){
	$(".boxInfo").delay(5000).fadeOut();
}


// ======= Check hostname length
$("#inputHostname").on("keyup",function(){
	// if($(this).val().length <5){
	// 	$("#minCharHostname").removeClass("text-green-500");
	// 	$("#minCharHostname").addClass("text-gray-500");
	// }else{
	// 	$("#minCharHostname").removeClass("text-gray-500");
	// 	$("#minCharHostname").addClass("text-green-500");
	// }
	// if($(this).val().length > 64){
	// 	$("#maxCharHostname").removeClass("text-green-500");
	// 	$("#maxCharHostname").addClass("text-gray-500");
	// }else{
	// 	$("#maxCharHostname").removeClass("text-gray-500");
	// 	$("#maxCharHostname").addClass("text-green-500");
	// }

	if($(this).val().length > 4 && $(this).val().length < 65 ){
		$("#CharHostname").removeClass("text-gray-500");
		$("#CharHostname").addClass("text-green-500");
		$("#subtmitHostname").removeAttr("disabled");
		$("#subtmitHostname").removeClass("bg-gray-700");
		$("#subtmitHostname").addClass("bg-blue-700");
		$("#subtmitHostname").addClass("hover:bg-blue-800")
	}else{
		$("#CharHostname").removeClass("text-green-500");
		$("#CharHostname").addClass("text-gray-500");
		$("#subtmitHostname").prop("disabled",true);
		$("#subtmitHostname").removeClass("bg-blue-700");
		$("#subtmitHostname").addClass("bg-gray-700");
		$("#subtmitHostname").removeClass("hover:bg-blue-800")
	}
});



// ================= Socketio all func
$(document).ready(function(e){
	var socket = io.connect(location.protocol+'//' + document.domain + ':' + location.port);
	if(document.location.pathname=="/panel/server/logs"){
		socket.emit("startLogsServer");
		socket.on("receiveLogs",function(data){
			$("#setLogs").html(data.replace(/\n/g, "<br />"));
			$("#masterSetLogs").animate({ scrollTop: $("#masterSetLogs")[0].scrollHeight }, 1000);
		})
	}
});