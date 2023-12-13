$("tr").click(function(){
	var href = $(this).find(".location").closest("a").attr("href")
	console.log(href);
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