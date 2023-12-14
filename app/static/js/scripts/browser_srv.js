var temp_name_object = ""

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

$(".delete_object_name").click(function(){
	temp_name_object=$(this).closest("tr").find(".object_name").text().trim()
});

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