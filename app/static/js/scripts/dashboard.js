// Manage Dashboard
// ========== CHARTS ==========
// SCANS & VIRUSES / DAY
const options = {
    colors: ["#0c7ec4", "#f02f2f"],
    series: [],
    chart: {
        type: "bar",
        height: "90%",
        fontFamily: "Inter, sans-serif",
        toolbar: {
        show: false,
        },
    },
    plotOptions: {
        bar: {
        horizontal: false,
        columnWidth: "50%",
        borderRadiusApplication: "end",
        borderRadius: 8,
        },
    },
    tooltip: {
        shared: true,
        intersect: false,
        style: {
        fontFamily: "Inter, sans-serif",
        },
    },
    states: {
        hover: {
        filter: {
            type: "darken",
            value: 1,
        },
        },
    },
    stroke: {
        show: true,
        width: 0,
        colors: ["transparent"],
    },
    grid: {
        show: false,
        strokeDashArray: 4,
        padding: {
        left: 2,
        right: 2,
        top: -14
        },
    },
    dataLabels: {
        enabled: false,
    },
    legend: {
        position: "top",
        show: true,
    },
    xaxis: {
        floating: false,
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
        show: false,
        },
    },
    yaxis: {
        show: true,
        labels: {
        style: {
            fontFamily: "Inter, sans-serif",
            cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
        }
        }
    },
    fill: {
        opacity: 1,
    },
    noData: {
        text: 'No Data',
        style: {
            color: "#000000"
        }
    }
}

if(document.getElementById("ScansViruses-chart") && typeof ApexCharts !== 'undefined') {
    const chart = new ApexCharts(document.getElementById("ScansViruses-chart"), options);
    chart.render();
    console.log(scan_7day)
    const format_data_scan= scan_7day.map(item => ({
        x: item[0],
        y: item[2]
    }));
    const format_data_virus= scan_7day.map(item => ({
        x: item[0],
        y: item[1]
    }));
    chart.updateSeries([
        {
        name: "Scans",
        color: "#0c7ec4",
        data: format_data_scan,
        },
        {
        name: "Viruses",
        color: "#f02f2f",
        data: format_data_virus,
        },
    ])
}
