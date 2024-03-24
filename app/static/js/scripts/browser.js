// Browser Client
var temp_name_object = ""

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		}
	}
});

// Click button
$(".onclick_object").click(function(){
	var href = $(this).closest("tr").find(".location").closest("a").attr("href")
	if(href) {
		window.location = href;
	}
});

// Return Button
$("#returnButton").click(function(){
	var url = window.parent.location.href;
	if(url.substr(url.length - 2) == "/"){
		url=url.slice(0,-1)
	}
	if(url.slice(url.lastIndexOf('/')) != '/browser/path/'){
		var to = url.lastIndexOf('/');
		to = to == -1 ? url.length : to + 1;
		url = url.substring(0, to -1 );
		window.location=url;
	}
});

$(function(){
	if(window.location.pathname != "/browser/path/"){
		$("#returnButton").removeAttr('hidden');
	}
});

// Remove element 
$(".delete_object_name").click(function(){
	temp_name_object=$(this).closest("tr").find(".object_name").text().trim()
});

// SEARCH BUTTON
$("#buttonSearch" ).on( "click", function() {
	if ($("#buttonSearch").hasClass("rounded-l-xl")){
		$("#searchBar" ).animate({width:'toggle'},350);
		$("#buttonSearch").removeClass("rounded-l-xl");
		  $("#buttonSearch").addClass("rounded-xl");
		$("#searchBar").removeClass("rounded-r-lg");
		  $("#searchBar").addClass("rounded-lg");
	}else{
		$("#searchBar" ).animate({width:'toggle'},350);
		$("#buttonSearch").removeClass("rounded-xl");
		$("#buttonSearch").addClass("rounded-l-xl");
		$("#searchBar").removeClass("rounded-lg");
		$("#searchBar").addClass("rounded-r-lg");
	}
});

// SearchBar
$("#searchBar").keyup(function() {
	var value = $(this).val().toLowerCase();
	$("#bodySearchBar tr").filter(function() {
		$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
	});
	if($("#bodySearchBar").find('tr').is(':visible')){
		document.getElementById("noElementFound").style  = "display: none;";
	}else{
		document.getElementById("noElementFound").style  = "display: True;";
	}
});

// Detect Element
if($("#bodySearchBar").find('tr').is(':visible')){
	document.getElementById("noElementFound").style  = "display: none;";
}else{
	document.getElementById("noElementFound").style  = "display: True;";
}

// Yes button
$(".yesButtonDeleteObject").click(function(e){
	var get_url=window.location.pathname.split("/").slice(3).join("/")
	e.preventDefault()
	$.ajax({
		type: "GET",
		url: "/browser/delete/"+get_url+"/"+temp_name_object,
		success: function(data){
			if(data == "ok"){
				window.location.reload();
			}
		}
	});
});

// Remove cache input at loading page
$(document).ready(function() {
	$("#fileInput").val('');
	$("#folderInput").val('');
});

// Onchange detect file/folder
$("#fileInput").on( "change", function() {
	if ($("#fileInput")[0].files.length != 0 && $("#folderInput")[0].files.length != 0) {
		$("#inputStateFF").removeClass("hidden");
		$("#inputStateDefault").addClass("hidden");
		$("#inputStateFile").addClass("hidden");
		$("#inputStateFolder").addClass("hidden");
	}
	else if ($("#fileInput")[0].files.length != 0) {
		$("#inputStateFile").removeClass("hidden");
		$("#inputStateDefault").addClass("hidden");
		$("#inputStateFolder").addClass("hidden");
	} 
	else if ($("#folderInput")[0].files.length != 0) {
		$("#inputStateFolder").removeClass("hidden");
		$("#inputStateDefault").addClass("hidden");
		$("#inputStateFile").addClass("hidden");
	}
});
$("#folderInput").on( "change", function() {
	if ($("#fileInput")[0].files.length != 0 && $("#folderInput")[0].files.length != 0) {
		$("#inputStateFF").removeClass("hidden");
		$("#inputStateDefault").addClass("hidden");
		$("#inputStateFile").addClass("hidden");
		$("#inputStateFolder").addClass("hidden");
	}
	else if ($("#fileInput")[0].files.length != 0) {
		$("#inputStateFile").removeClass("hidden");
		$("#inputStateDefault").addClass("hidden");
		$("#inputStateFolder").addClass("hidden");
	} 
	else if ($("#folderInput")[0].files.length != 0) {
		$("#inputStateFolder").removeClass("hidden");
		$("#inputStateDefault").addClass("hidden");
		$("#inputStateFile").addClass("hidden");
	}
});

// Listen for click on toggle checkbox
$('#select-all').click(function(event) {   
    if(this.checked) {
        // Iterate each checkbox
        $(':checkbox').each(function() {
            this.checked = true;                        
        });
    } else {
        $(':checkbox').each(function() {
            this.checked = false;                       
        });
    }
}); 

// Undo Blur for Endpoint Connexion Code
$("#undoBlur").click(function() {
	if ($("#codeEndpoint").hasClass("blur-md") == true) {
		$("#codeEndpoint").removeClass("blur-md");
	}
	else {
		$("#codeEndpoint").addClass("blur-md");
	}
});

// View button for Endpoint Connexion Code
$(".viewCode").click(function() {
	if ($(".viewCode").hasClass("fa-eye")  == true) {
		$(".viewCode").removeClass("fa-eye");
		$(".viewCode").addClass("fa-eye-slash");
		
	}
	else {
		$(".viewCode").removeClass("fa-eye-slash");
		$(".viewCode").addClass("fa-eye");

	}
});