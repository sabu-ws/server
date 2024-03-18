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

// PATH URL BROWSER
var urlPath = window.location.pathname.substring(1).split('/');
var firstUrlPath = window.location.pathname.split("/").slice(0,5).join("/")
$("#hrefpath").attr( "href", firstUrlPath );
$("#nameFolder1").html(urlPath[3]);

if (urlPath.length > 4) {
	$("#nameFolder2").html(urlPath[4]);
	$("#RemoveSVG").removeAttr('hidden');
}

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

if(urlPath.length==4){
	if(urlPath[3]==""){
		$(".donwload_object_name").attr("hidden","true");
		$(".delete_object_name").attr("hidden","true");
	}
}


// Yes button
$(".yesButtonDeleteObject").click(function(e){
	var get_url=window.location.pathname.split("/").slice(4).join("/")
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