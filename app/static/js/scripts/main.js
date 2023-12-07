// CSRF TOKEN 
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		}
	}
});

// Sidebar 
$(document).ready(function() {
	var currentPath = window.location.pathname;
	var panelIndex = currentPath.indexOf("/panel/");
	if (panelIndex !== -1) {
		var currentPage = currentPath.substring(panelIndex + 7).split('/')[0];
		$('#sidebar-' + currentPage).addClass(["text-blue-800", "bg-white/60"]);
		$('#sidebar-' + currentPage).removeClass(["text-white", "hover:text-blue-800", "hover:bg-white/60"]);
	}
});

// Dark mode
$("#ToggleDarkMode").click(function(){
	if(localStorage.theme === 'dark' ){
		localStorage.theme = 'light';
		document.documentElement.classList.remove('dark');
		$("#ToggleDarkModeIcon").removeClass("fa-moon");
		$("#ToggleDarkModeIcon").addClass("fa-sun");
	}else{
		document.documentElement.classList.add('dark');
		$("#ToggleDarkModeIcon").removeClass("fa-sun");
		$("#ToggleDarkModeIcon").addClass("fa-moon");
		localStorage.theme = 'dark';
	}
});

if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
	localStorage.theme = 'dark';
	document.documentElement.classList.add('dark');
	$("#ToggleDarkModeIcon").removeClass("fa-sun");
	$("#ToggleDarkModeIcon").addClass("fa-moon");
	$("#ToggleDarkMode").prop("checked",true);
} else {
	localStorage.theme = 'light';
	document.documentElement.classList.remove('dark');
	$("#ToggleDarkModeIcon").removeClass("fa-moon");
	$("#ToggleDarkModeIcon").addClass("fa-sun");
	$("#ToggleDarkMode").prop("checked",false);
}

// Toggle Button View Password
$(".toggleView").click(function(){
	if($(this).closest("div").closest("button").prev().attr("type") == "password"){
		$(this).closest("div").closest("button").prev().attr("type","text");
		$(this).removeClass("fa-eye");
		$(this).addClass("fa-eye-slash");
	}else{
		$(this).closest("div").closest("button").prev().attr("type","password");
		$(this).removeClass("fa-eye-slash");
		$(this).addClass("fa-eye");
	}
});

// Box Alerts
if($(".boxInfo").is(':visible')){
	$(".boxInfo").delay(5000).fadeOut();
}

// Number Alerts Navbar
document.addEventListener('DOMContentLoaded', function() {
    const element = document.getElementById('numberAlerts');
    let valeur = parseInt(element.textContent);
    if (valeur > 9) {
        valeur = 9;
        element.textContent = `${valeur}+`;
    }
    
});

// Path in Navbar
var tabUrlPath = window.location.pathname.substring(1).split('/');
		
document.getElementById('pathArg2').innerHTML = tabUrlPath[1].charAt(0).toUpperCase() + tabUrlPath[1].slice(1);
    
if (tabUrlPath[2]) {
    document.getElementById('pathArg3').innerHTML = tabUrlPath[2];
} else {
    document.getElementById('showPathArg3').style.display = 'none';
}