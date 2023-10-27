var temp_uuid;
var getRowUserTable;

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		}
	}
});
$(document).ready(function(){

	// toggle buttont view password
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
						$("#otp_url").html(data);
						$("#qrcode_render").attr('src',qrcode_url+"?url="+data);
					}
				});
			});
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
	
});