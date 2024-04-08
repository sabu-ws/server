if (typeof total_ram === 'undefined') {
	total_ram = 0
}
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
	
	if(document.location.pathname=="/panel/server/settings"){
		// ========== SETTING SERVER ==========
		var iface = $("#interface").val()
		socket = io.connect("/netiface")
		socket.emit("info_netiface",netiface=iface)
		socket.on("rcv_netiface",function(data){
			console.log(data)
			$("#ip").attr("placeholder",data[0])
			$("#netmask").attr("placeholder",data[1])
			$("#gateway").attr("placeholder",data[2])
			$("#dns1").attr("placeholder",data[3])
			$("#dns2").attr("placeholder",data[4])
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
// Terminal.applyAddon(fit)

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
	noData: {
		text: 'Loading...'
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
		text: 'Loading...'
	}
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
	noData: {
		text: 'Loading...'
	}
}


// DISK
var options_DISK = {
	colors: ["#ed3e3e", "#189e2e"],
	series: [{
	name: 'Used',
	data: []
  }, {
	name: 'Free',
	data: []
  
  }],
	chart: {
	type: 'bar',
	height: 250,
	stacked: true,
	stackType: '100%'
  },
  plotOptions: {
	bar: {
	  horizontal: true,
	},
  },
  stroke: {
	width: 1,
	colors: ['#fff']
  },
  xaxis: {
	categories: ["System", "Data"],
	labels: {
		show: false
	  },
	  tickAmount: 1,
  },

  tooltip: {
	y: {
	  formatter: function (val) {
		return val + "GB"
	  }
	}
  },
  fill: {
	opacity: 1
  
  },
  legend: {
	position: 'bottom',
	horizontalAlign: 'left',
	offsetX: 40
  },
  noData: {
    text: 'Loading...'
  }
};




if (document.getElementById("chart-cpu")){
	const chart_CPU = new ApexCharts(document.getElementById("chart-cpu"), options_CPU);
	chart_CPU.render();
	socket_CPU = io.connect("/chart_CPU")
	socket_CPU.emit("start_chart_cpu_rcv")
	socket_CPU.on("chart_cpu_rcv",function(data){
		chart_CPU.updateSeries([
			{
			 data: data,
			}
		])
	})
}

if (document.getElementById("chart-ram")){
	chart_RAM = new ApexCharts(document.getElementById("chart-ram"), options_RAM);
	chart_RAM.render();
	socket_RAM = io.connect("/chart_RAM")
	socket_RAM.emit("start_chart_ram_rcv")
	socket_RAM.on("chart_ram_rcv",function(data){
		chart_RAM.updateSeries([
			{
			 data: data,
			}
		])
	})
}

if (document.getElementById("chart-network")){
	const chart_NET = new ApexCharts(document.getElementById("chart-network"), options_NET);
	chart_NET.render();
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
}

if (document.getElementById("chart-disk")){
	var chart_DISK = new ApexCharts(document.getElementById("chart-disk"), options_DISK);
	chart_DISK.render();
	socket_DISK = io.connect("/chart_DISK")
	socket_DISK.emit("start_chart_disk_rcv")
	socket_DISK.on("chart_disk_rcv", function(data){
		chart_DISK.updateSeries(
			[{
				name: 'Used',
				data: [data[0], data[2]]
			  }, {
				name: 'Free',
				data: [data[1], data[3]]
			  
			  }],
			)
	})
}

// ========== SETTING SERVER ==========
$("#interface").change(function(){
	var iface = $("#interface").val()
	socket = io.connect("/netiface")
	socket.emit("info_netiface",netiface=iface)
	socket.on("rcv_netiface",function(data){
		console.log(data)
		$("#ip").attr("placeholder",data[0])
		$("#netmask").attr("placeholder",data[1])
		$("#gateway").attr("placeholder",data[2])
		$("#dns1").attr("placeholder",data[3])
		$("#dns2").attr("placeholder",data[4])
	})
})