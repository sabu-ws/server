var temp_name_object = ""

// Click button
$(".onclick_object").click(function(){
	var href = $(this).closest("tr").find(".location").closest("a").attr("href")
	if(href) {
		window.location = href;
	}
});

$(function(){
	if(window.location.pathname != "/panel/browser/path/"){
		$("#returnButton").removeAttr('hidden');
	}
});

// Return Button
$("#returnButton").click(function(){
	var url = window.parent.location.href;
	if(url.substr(url.length - 1) == "/"){
		url=url.slice(0,-1)
	}
	if(url.slice(url.lastIndexOf('/')) != '/panel/browser/path/'){
		var to = url.lastIndexOf('/');
		to = to == -1 ? url.length : to + 1;
		url = url.substring(0, to -1 );
		window.location=url;
	}
});

// Remove element 
$(".delete_object_name").click(function(){
	temp_name_object=$(this).closest("tr").find(".object_name").text().trim()
});

// Yes button
$(".yesButtonDeleteObject").click(function(e){
	var get_url=window.location.pathname.split("/").slice(4).join("/")
	e.preventDefault()
	$.ajax({
		type: "GET",
		url: "/panel/browser/delete/"+get_url+"/"+temp_name_object,
		success: function(data){
			if(data == "ok"){
				window.location.reload();
			}
		}
	});
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

// RELEASE BUTTON
if (urlPath[3] == "quarantine") { // var urlpath = see (PATH URL BROWSER SECTION)
	$(".releaseButton").removeAttr('hidden');
}
