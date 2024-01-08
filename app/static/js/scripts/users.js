var temp_uuid;

// Add User
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

// Delete User
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

// Modify User 
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

// Enable / Disable User
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

// Manage Job
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

// SearchBar
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
