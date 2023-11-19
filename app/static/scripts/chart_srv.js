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
			shade: "#1C64F2",
			gradientToColors: ["#1C64F2"],
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
			data: [25,10,35,65,84,12],
			color: "#1A56DB",
		},
	],
	xaxis: {
		range : 100,
		tickAmount: 10,
		categories: ['30 min', '25 min', '20 min', '15 min', '10 min', '5 min'],
		labels: {
			show: true,
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
			formatter: function (value) {
				return value + ' %';
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
			shade: "#ee1111",
			gradientToColors: ["#ee1111"],
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
			data: [3, 6, 5, 7, 4, 5],
			color: "#f90f0f",
		},
	],
	xaxis: {
		range: 100,
		tickAmount: 10,
		categories: ['30 min', '25 min', '20 min', '15 min', '10 min', '5 min'],
		labels: {
			show: true,
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
			formatter: function (value) {
				return value.toPrecision(3) + ' Go';
			}
		}
	},
}



// NETWORK
let options_NET = {
	series: [
		{
			name: "Upload",
			data: [1500, 1418, 1456, 1526, 1356, 1256],
			color: "#f5d32c",
		},
		{
			name: "Download",
			data: [643, 413, 765, 412, 1423, 1731],
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
		categories: ['30 min', '25 min', '20 min', '15 min', '10 min', '5 min'],
		labels: {
			show: true,
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
			formatter: function (value) {
				return value + ' Mbits/s';
			}
		}
	},
}


// DISK
const getChartOptions = {
	series: [0],
	colors: ["#00a40f", "#11c186"],
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
				labels:{
					show:true,
					total:{
						show:true,
						showAlways: true
					},
				},
				size: '50%',
			},
			labels: {
				show: true,
			},
			size: "100%",
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
	chart_CPU.updateSeries([{
	 data: data,
	}])
})



socket_RAM = io.connect("/chart_RAM")
socket_RAM.emit("start_chart_ram_rcv")
socket_RAM.on("chart_ram_rcv",function(data){
	chart_RAM.updateSeries([{
	 data: data,
	}])
})

// socket_CPU = io.connect("/chart_NET")

socket_DISK = io.connect("/chart_DISK")
socket_DISK.emit("start_chart_disk_rcv")
socket_DISK.on("chart_disk_rcv",function(data){
	chart_DISK.updateSeries([parseFloat(data[0]),parseFloat(data[1])])
})