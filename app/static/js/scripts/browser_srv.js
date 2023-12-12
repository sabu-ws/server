$("tr").click(function(){
	var href = $(this).find(".location").closest("a").attr("href")
	console.log(href);
	if(href) {
		window.location = href;
	}
});

