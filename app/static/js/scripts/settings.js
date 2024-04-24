$("#showExtensionid").click(function(){
    var socket = io.connect("/settings");
    socket.emit("extension_show")
    socket.on("extension_get",function(data){
        $('#ext_table').empty();
        for(var i=0;i<data.length;i++){
            var div_class = $('<div class="flex w-full bg-gray-100 dark:bg-gray-600 p-2 rounded-lg"></div').appendTo("#ext_table")
            var h1_class = $('<h1 class="flex items-center ml-4 font-semibold dark:text-white"></h1').text(data[i]).appendTo(div_class)
            var button_class = $('<button class="delExt m-auto mr-4 text-red-500 text-xl"><i class="fa-solid fa-xmark"></i></button>').appendTo(div_class)
        }
    });
});

$("#add-extension").click(function(){
    var input_ext = $("#input-extension").val();
    var socket = io.connect("/settings");
    socket.emit("extension_add",input_ext);
    socket.on("extension_add_rcv",function(data){
        var alert_box = $("#alert");
        var message_alert_box = $("#message_settings");
        if(data==="ok"){
            message_alert_box.text("successfull add")
            $("#input-extension").val('')
            alert_box.show()
            alert_box.delay(5000).fadeOut();
        }else if(data==="nexist"){
            message_alert_box.text("This extension not exist in the database")
            alert_box.show()
            alert_box.delay(5000).fadeOut();
        }else if(data==="exist"){
            message_alert_box.text("This extension has already added")
            alert_box.show()
            alert_box.delay(5000).fadeOut();
        }else{
            message_alert_box.text("ERROR")
            alert_box.show()
            alert_box.delay(5000).fadeOut();
        }
    })
});

$('#ext_table').on('click', '.delExt', function() {
    var getElem = $(this).prev().text()
    var socket = io.connect("/settings");
    socket.emit("extension_del",getElem);
    socket.emit("extension_show")
    socket.on("extension_get",function(data){
        $('#ext_table').empty();
        for(var i=0;i<data.length;i++){
            var div_class = $('<div class="flex w-full bg-gray-100 dark:bg-gray-600 p-2 rounded-lg"></div').appendTo("#ext_table")
            var h1_class = $('<h1 class="flex items-center ml-4 font-semibold dark:text-white"></h1').text(data[i]).appendTo(div_class)
            var button_class = $('<button class="delExt m-auto mr-4 text-red-500 text-xl"><i class="fa-solid fa-xmark"></i></button>').appendTo(div_class)
        }
    });
});



// ENTER KEYBOARD EXTENSION
$(document).ready(function() {
    var input = $("#input-extension");
    input.on("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            $("#add-extension").click();
        }
    });
});
