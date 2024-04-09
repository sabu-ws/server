var url = "/browser/scan/id/"+scan_id
var interval = setInterval(function() { 
    $.get(url,function(data){
        if (data.state){
            window.location = "/";
            clearInterval(interval)
        }
    });
}, 2000);