var temp_uuid;

// Add Endpoint 
$("#addEndpointForm").submit(function(e) {
	e.preventDefault();
	$.ajax({
		type: "POST",
		url: addEndpointUrl,
		data: $("#addEndpointForm").serialize(),
		success: function(data)
		{
			if(data == "ok"){
				window.location.reload();
			}else{
				alertAddEndpointForm = document.getElementById("alertAddEndpointForm");
				alertAddEndpointForm.style = "display: true;";
				const ErrorMSG= "Error : ";
				$("#spanErrorAddEndpointForm").text(ErrorMSG.concat(data));
			}
		}
	});
});

$("#genTokenButton").click(function(){
	$.ajax({
		type: "GET",
		url: genToken,
		// data: $("#addEndpointForm").serialize(),
		success: function(data){
			$("#endpointToken").val(data)
		}
	});
});

$("#btnCopyTokenEP").click(function(){
	$("#endpointToken").select();
	document.execCommand('copy');
	$("#copyInfoEP").html("Copied ✓")
	window.getSelection().removeAllRanges();
});

// Delete Endpoint
$('.buttonDeleteRow').click(function(e){
	var $item = $(this).closest("tr")
			.find("#uuid")
			.text();
	temp_uuid = $item.trim();
});

$("#yesButtonDeleteEndpoint").click(function(e){
	e.preventDefault()
	$.ajax({
		type: "POST",
		url: delEndpointUrl,
		data: {'uuid':temp_uuid},
		success: function(data){
			if(data == "ok"){
				window.location.reload();
			}
		}
	});
});

// Change Status Dynamic
// var socket = io.connect();
var socket = io.connect("/state_ep");
socket.on("state",function(data){
	$("#table_endpoint tr").each(function(){
		if($(this).find("#uuid").text().trim()===data["uuid"]){
			if(data["state"]==="up"){
				$(this).find("#state_text").text("Up")
				$(this).find("#state_icon").removeClass("bg-red-500")
				$(this).find("#state_icon").addClass("bg-green-500")
			}else if(data["state"]==="down"){
				$(this).find("#state_text").text("Down")
				$(this).find("#state_icon").removeClass("bg-green-500")
				$(this).find("#state_icon").addClass("bg-red-500")
			}
		}
	})
})

$("#table-search-endpoints").keyup(function() {
	var value = $(this).val().toLowerCase();
	$("#table_endpoint tr").filter(function() {
		$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
	});
	if($("#table_endpoint").find('tr').is(':visible')){
		document.getElementById("noEndpointFound").style  = "display: none;";
	}else{
		document.getElementById("noEndpointFound").style  = "display: True;";
	}
});	

// Check Hostname Length
$("#inputHostname").on("keyup",function(){
	if($(this).val().length > 4 && $(this).val().length < 65 ){
		$("#CharHostname").removeClass("text-gray-500");
		$("#CharHostname").addClass("text-green-500");
		$("#subtmitHostname").removeAttr("disabled");
		$("#subtmitHostname").removeClass("bg-gray-700");
		$("#subtmitHostname").addClass(["bg-darkblue","hover:bg-lightblue", "dark:bg-darkblue", "dark:hover:bg-lightblue"]);
	}else{
		$("#CharHostname").removeClass("text-green-500");
		$("#CharHostname").addClass("text-gray-500");
		$("#subtmitHostname").prop("disabled",true);
		$("#subtmitHostname").removeClass(["bg-darkblue","hover:bg-lightblue", "dark:bg-darkblue", "dark:hover:bg-lightblue"]);
		$("#subtmitHostname").addClass("bg-gray-700");
	}
});


// ========== CHARTS ==========



// CPU
let options_CPU = {
	chart: {
		height: "100%",
		maxWidth: "100%",
		type: "area",
		fontFamily: "Inter, sans-serif",
		dropShadow: {
			enabled: false,
		},
		toolbar: {
			show: true,
		},
	},
	tooltip: {
		enabled: true,
		x: {
			show: false,
		},
	},
	fill: {
		type: "gradient",
		gradient: {
			opacityFrom: 0.55,
			opacityTo: 0.25,
			shade: "#0699f3",
			gradientToColors: ["#0699f3"],
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		width: 6,
	},
	grid: {
		show: false,
		strokeDashArray: 4,
		padding: {
			left: 5,
			right: 2,
			top: 0
		},
	},
	series: [
		{
			name: "CPU",
			data: [],
			color: "#0699f3",
		},
	],
	xaxis: {
		range : 15,
		tickAmount: 10,
		categories: [],
		labels: {
			show: true,
			style: {
                fontFamily: "Inter, sans-serif",
                cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
            }
		},
		axisBorder: {
			show: true,
		},
		axisTicks: {
			show: true,
		},
	},
	yaxis: {
		//max:100,
		tickAmount: 5,
		show: true,
		labels: {
			style: {
                fontFamily: "Inter, sans-serif",
                cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
            },
			formatter: function (value) {
				return value.toPrecision(2) + ' %';
			}
		}
	},
	noData: {
		text: 'Loading...',
		style: {
            color: "#000000"
        }
	}
}

// RAM
let options_RAM = {
	chart: {
		height: "100%",
		maxWidth: "100%",
		type: "area",
		fontFamily: "Inter, sans-serif",
		dropShadow: {
			enabled: false,
		},
		toolbar: {
			show: true,
		},
	},
	tooltip: {
		enabled: true,
		x: {
			show: false,
		},
	},
	fill: {
		type: "gradient",
		gradient: {
			opacityFrom: 0.55,
			opacityTo: 0.25,
			shade: "#9565fc",
			gradientToColors: ["#9565fc"],
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		width: 6,
	},
	grid: {
		show: false,
		strokeDashArray: 4,
		padding: {
			left: 5,
			right: 2,
			top: 0
		},
	},
	series: [
		{
			name: "RAM",
			data: [],
			color: "#9565fc",
		},
	],
	xaxis: {
		range: 15,
		tickAmount: 10,
		categories: [],
		labels: {
			show: true,
			style: {
                fontFamily: "Inter, sans-serif",
                cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
            }
		},
		axisBorder: {
			show: true,
		},
		axisTicks: {
			show: true,
		},
	},
	yaxis: {
		max: total_ram,
		tickAmount: 5,		
		show: true,
		labels: {
			style: {
                fontFamily: "Inter, sans-serif",
                cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
            },
			formatter: function (value) {
				return value.toPrecision(2) + ' Go';
			}
		}
	},
	noData: {
		text: 'Loading...',
		style: {
            color: "#000000"
        }
	}
}



// NETWORK
let options_NET = {
	series: [
		{
			name: "Download",
			data: [],
			color: "#f9760f",
		},
		{
			name: "Upload",
			data: [],
			color: "#f5d32c",
		},
	],
	chart: {
		height: "100%",
		maxWidth: "100%",
		type: "area",
		fontFamily: "Inter, sans-serif",
		dropShadow: {
			enabled: false,
		},
		toolbar: {
			show: true,
		},
	},
	tooltip: {
		enabled: true,
		x: {
			show: false,
		},
	},
	legend: {
		show: false
	},
	fill: {
		type: "gradient",
		gradient: {
			opacityFrom: 0.55,
			opacityTo: 0.25,
			shade: "#f5d32c",
			gradientToColors: ["#f5d32c"],
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		width: 6,
	},
	grid: {
		show: false,
		strokeDashArray: 4,
		padding: {
			left: 5,
			right: 2,
			top: 0
		},
	},
	xaxis: {
		range:15,
		tickAmount:10,
		categories: [],
		labels: {
			show: true,
			style: {
                fontFamily: "Inter, sans-serif",
                cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
            }
		},
		axisBorder: {
			show: true,
		},
		axisTicks: {
			show: true,
		},
	},
	yaxis: {
		show: true,
		labels: {
			style: {
                fontFamily: "Inter, sans-serif",
                cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
            },
			formatter: function (value) {
				decimals = 2
			    if (!+value) return '0 Bytes'

			    const k = 1024
			    const dm = decimals < 0 ? 0 : decimals
			    const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

			    const i = Math.floor(Math.log(value) / Math.log(k))

			    return `${parseFloat((value / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
				// return value + ' Mbits/s';
			}
		}
	},
	noData: {
		text: 'Loading...',
		style: {
            color: "#000000"
        }
	}
}

// DISK
let options_DISK = {
	chart: {
		series: [60, 40],
		colors: ["#00a40f", "#11c186"],
		chart: {
		height: "100%",
		width: "100%",
		type: "pie",
		toolbar: {
			show: true,
			},
		},
		stroke: {
		colors: ["white"],
		lineCap: "",
		},
		plotOptions: {
		pie: {
			labels: {
			show: true,
			},
			size: "100%",
			dataLabels: {
			offset: -25
			}
		},
		},
		labels: ["Used", "Free"],
		dataLabels: {
		enabled: true,
		style: {
			fontFamily: "Inter, sans-serif",
		},
		},
		legend: {
		position: "bottom",
		fontFamily: "Inter, sans-serif",
		},
		yaxis: {
		labels: {
			formatter: function (value) {
			return value + " Go"
			},
		},
		},
		xaxis: {
		labels: {
			formatter: function (value) {
			return value  + " Go"
			},
		},
		axisTicks: {
			show: false,
		},
		axisBorder: {
			show: false,
		},
		},
	}
}

if (document.getElementById("chart-cpu")){
	const chart_CPU = new ApexCharts(document.getElementById("chart-cpu"), options_CPU);
	chart_CPU.render();
}

if (document.getElementById("chart-ram")){
	chart_RAM = new ApexCharts(document.getElementById("chart-ram"), options_RAM);
	chart_RAM.render();
}

if (document.getElementById("chart-network")){
	const chart_NET = new ApexCharts(document.getElementById("chart-network"), options_NET);
	chart_NET.render();
}

if (document.getElementById("chart-disk")){
	var chart_DISK = new ApexCharts(document.getElementById("chart-disk"), options_DISK);
	chart_DISK.render();
}