var url = "/browser/scan/state"
var interval = setInterval(function() { 
    $.get(url,function(data){
        if (data.state){
            window.location = "/";
            clearInterval(interval)
        }
    });
}, 2000);