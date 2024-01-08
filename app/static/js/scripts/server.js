// Check Hostname Length
$("#inputHostname").on("keyup",function(){
	if($(this).val().length > 4 && $(this).val().length < 65 ){
		$("#CharHostname").removeClass("text-gray-500");
		$("#CharHostname").addClass("text-green-500");
		$("#subtmitHostname").removeAttr("disabled");
		$("#subtmitHostname").removeClass("bg-gray-700");
		$("#subtmitHostname").addClass(["bg-lightblue","hover:bg-darkblue/60", "dark:bg-darkblue", "dark:hover:bg-lightblue"]);
	}else{
		$("#CharHostname").removeClass("text-green-500");
		$("#CharHostname").addClass("text-gray-500");
		$("#subtmitHostname").prop("disabled",true);
		$("#subtmitHostname").removeClass(["bg-lightblue","hover:bg-darkblue/60", "dark:bg-darkblue", "dark:hover:bg-lightblue"]);
		$("#subtmitHostname").addClass("bg-gray-700");
	}
});

// Socketio
$(document).ready(function(e){
	if(document.location.pathname=="/panel/server/logs"){
		var socket = io.connect("/logServer");
		socket.emit("startLogsServer");
		socket.on("receiveLogs",function(data){
			$("#setLogs").html(data.replace(/\n/g, "<br />"));
			$("#masterSetLogs").animate({ scrollTop: $("#masterSetLogs")[0].scrollHeight }, 1000);
		})
	}
});

$("#yesButtonReboot").click(function(e){
	e.preventDefault()
	$.ajax({
		type: "GET",
		url: "/panel/server/reboot",
		success: function(data){
			if(data == "ok"){
				window.location.reload();
			}
		}
	});
});

$("#yesButtonShutdown").click(function(e){
	e.preventDefault()
	$.ajax({
		type: "GET",
		url: "/panel/server/shutdown",
		success: function(data){
			if(data == "ok"){
				window.location.reload();
			}
		}
	});
});

// XtermJS
Terminal.applyAddon(fit)

// const term = new Terminal({
//    cursorBlink: 5,
//    scrollback: 300
// })

// term.open(document.getElementById('terminal'))
// term.fit()
// term.write("\n The ssh feature is currently being built !!!")


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
			shade: "#f71056",
			gradientToColors: ["#f71056"],
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
			color: "#f71056",
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
}



// NETWORK
let options_NET = {
	series: [
		{
			name: "Upload",
			data: [],
			color: "#f5d32c",
		},
		{
			name: "Download",
			data: [],
			color: "#f9760f",
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
			    const sizes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

			    const i = Math.floor(Math.log(value) / Math.log(k))

			    return `${parseFloat((value / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
				// return value + ' Mbits/s';
			}
		}
	},
}


// DISK
const getChartOptions = {
	series: [0],
	colors: ["#fa3d37", "#11c186"],
	chart: {
		height: "100%",
		width: "100%",
		type: "donut",
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
			donut: {
			  labels: {
				show: true,
				name: {
				  show: true,
				  fontFamily: "Inter, sans-serif",
				  offsetY: 20,
				},
				total: {
				  showAlways: true,
				  show: true,
				  label: "Total",
				  fontFamily: "Inter, sans-serif",
				  formatter: function (w) {
					const sum = w.globals.seriesTotals.reduce((a, b) => {
					  return a + b
					}, 0)
					return `${sum} GB`
				  },
				},
				value: {
				  show: true,
				  fontFamily: "Inter, sans-serif",
				  offsetY: -20,
				  formatter: function (value) {
					return value + "GB"
				  },
				},
			  },
			  size: "60%",
			},
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
		position: "left",
		fontFamily: "Inter, sans-serif",
	},
	yaxis: {
		labels: {
			formatter: function (value) {
				return value + " GB"
			},
		},
	},
	xaxis: {
		labels: {
			formatter: function (value) {
				return value  + " GB"
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

const chart_CPU = new ApexCharts(document.getElementById("chart-cpu"), options_CPU);
chart_CPU.render();

chart_RAM = new ApexCharts(document.getElementById("chart-ram"), options_RAM);
chart_RAM.render();

const chart_NET = new ApexCharts(document.getElementById("chart-network"), options_NET);
chart_NET.render();

const chart_DISK = new ApexCharts(document.getElementById("chart-disk"), getChartOptions);
chart_DISK.render();

socket_CPU = io.connect("/chart_CPU")
socket_CPU.emit("start_chart_cpu_rcv")
socket_CPU.on("chart_cpu_rcv",function(data){
	chart_CPU.updateSeries([
		{
		 data: data,
		}
	])
})



socket_RAM = io.connect("/chart_RAM")
socket_RAM.emit("start_chart_ram_rcv")
socket_RAM.on("chart_ram_rcv",function(data){
	chart_RAM.updateSeries([
		{
		 data: data,
		}
	])
})

socket_NET = io.connect("/chart_NET")
socket_NET.emit("start_chart_net_rcv")
socket_NET.on("chart_net_rcv",function(data){
	chart_NET.updateSeries([
		{
		 data: data[0],
		},
		{
		 data: data[1],
		}
	])
})


socket_DISK = io.connect("/chart_DISK")
socket_DISK.emit("start_chart_disk_rcv")
socket_DISK.on("chart_disk_rcv",function(data){
	chart_DISK.updateSeries([parseFloat(data[0]),parseFloat(data[1])])
})