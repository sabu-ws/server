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
	// Add user

	$("#addUserForm").submit(function(e) {
		e.preventDefault();

		var form = $(this);
		var actionUrl = urlAdd;
		// console.log(actionUrl);
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
			},
			error: function(data){alert(data);}
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
			},
			error: function(data){console.log(data);}
		});

	});

	$("#editUserForm").submit(function(e) {
		e.preventDefault();

		var form = $(this);
		var actionUrl = urlModify;
		$.ajax({
			type: "POST",
			url: actionUrl,
			data: form.serialize(),
			success: function(data)
			{
				if(data == "ok"){
					window.location.reload();
				}else{
					editErrorFieldForm = document.getElementById("editErrorFieldForm");
					editErrorFieldForm.style = "display: true;";
					// $("#editErrorFieldForm").css({"display":"true"});
					const ErrorMSG= "Error : ";
					$("#editErrorFieldForm span").text(ErrorMSG.concat(data));
				}
			}
		});
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
			},
			error: function(data){alert(data);}
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
	
});


// Part add modal
const toggleButtonAddPassword = document.getElementById('toggleButtonAddPassword');
const toggleButtonAddRepeatPassword = document.getElementById('toggleButtonAddRepeatPassword');
const AddPassword = document.getElementById('AddPassword');
const AddRepeatPassword = document.getElementById('AddRepeatPassword');

toggleButtonAddPassword.addEventListener('click', function() {
	if (AddPassword.type === 'password') {
		AddPassword.type = 'text';
	document.getElementById("toggleviewAddPassword").classList.remove("fa-eye");
	document.getElementById("toggleviewAddPassword").classList.add("fa-eye-slash");
	} else {
		AddPassword.type = 'password';
	document.getElementById("toggleviewAddPassword").classList.remove("fa-eye-slash");
	document.getElementById("toggleviewAddPassword").classList.add("fa-eye");
	}
});
toggleButtonAddRepeatPassword.addEventListener('click', function() {
	if (AddRepeatPassword.type === 'password') {
		AddRepeatPassword.type = 'text';
	document.getElementById("toggleviewAddRepeatPassword").classList.remove("fa-eye");
	document.getElementById("toggleviewAddRepeatPassword").classList.add("fa-eye-slash");
	} else {
		AddRepeatPassword.type = 'password';
	document.getElementById("toggleviewAddRepeatPassword").classList.remove("fa-eye-slash");
	document.getElementById("toggleviewAddRepeatPassword").classList.add("fa-eye");
	}
});


// Part edit modal
const toggleButtonEditPassword = document.getElementById('toggleButtonEditPassword');
const toggleButtonEditRepeatPassword = document.getElementById('toggleButtonEditRepeatPassword');
const EditPassword = document.getElementById('EditPassword');
const EditRepeatPassword = document.getElementById('EditRepeatPassword');

toggleButtonEditPassword.addEventListener('click', function() {
	if (EditPassword.type === 'password') {
		EditPassword.type = 'text';
	document.getElementById("toggleviewEditPassword").classList.remove("fa-eye");
	document.getElementById("toggleviewEditPassword").classList.add("fa-eye-slash");
	} else {
		EditPassword.type = 'password';
	document.getElementById("toggleviewEditPassword").classList.remove("fa-eye-slash");
	document.getElementById("toggleviewEditPassword").classList.add("fa-eye");
	}
});
toggleButtonEditRepeatPassword.addEventListener('click', function() {
	if (EditRepeatPassword.type === 'password') {
		EditRepeatPassword.type = 'text';
	document.getElementById("toggleviewEditRepeatPassword").classList.remove("fa-eye");
	document.getElementById("toggleviewEditRepeatPassword").classList.add("fa-eye-slash");
	} else {
		EditRepeatPassword.type = 'password';
	document.getElementById("toggleviewEditRepeatPassword").classList.remove("fa-eye-slash");
	document.getElementById("toggleviewEditRepeatPassword").classList.add("fa-eye");
	}
});