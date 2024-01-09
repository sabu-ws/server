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
$('#pathArg2').html(tabUrlPath[1].charAt(0).toUpperCase() + tabUrlPath[1].slice(1));

if (tabUrlPath[1] == "endpoints" && tabUrlPath[2] != "") {
	$("#pathArg3").html(tabUrlPath[2]);
	$("#showPathArg3").removeAttr("hidden");
} 

// Subnavbar
$(document).ready(function() {
	var part1Title = $(document).attr('title').split(" ")[2];
	var part2Title = $(document).attr('title').split(" ")[4];
	$('#' + part1Title + '-' + part2Title).removeClass(["border-b-2", "border-transparent", "rounded-t-lg", "hover:text-gray-600", "hover:border-gray-300", "dark:text-white", "dark:hover:text-gray-300"]);
	$('#' + part1Title + '-' + part2Title).addClass(["text-blue-600", "border-b-2", "border-blue-600", "rounded-t-lg", "active", "dark:text-blue-500", "dark:border-blue-500"]);
	$('#' + part2Title + '-svg').removeClass(["text-gray-400", "group-hover:text-gray-500", "dark:text-white", "dark:group-hover:text-gray-300"]);
	$('#' + part2Title + '-svg').addClass(["text-blue-600", "dark:text-blue-500"]);
});