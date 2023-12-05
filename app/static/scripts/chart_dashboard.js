// SCANS & VIRUSES / DAY
window.addEventListener("load", function() {
    const options = {
        colors: ["#004aad", "#ff9b00"],
        series: [
            {
            name: "Scans",
            color: "#004aad",
            data: [
                { x: "Mon", y: 231 },
                { x: "Tue", y: 122 },
                { x: "Wed", y: 63 },
                { x: "Thu", y: 421 },
                { x: "Fri", y: 122 },
                { x: "Sat", y: 323 },
                { x: "Sun", y: 111 },
            ],
            },
            {
            name: "Viruses",
            color: "#ff9b00",
            data: [
                { x: "Mon", y: 232 },
                { x: "Tue", y: 113 },
                { x: "Wed", y: 341 },
                { x: "Thu", y: 224 },
                { x: "Fri", y: 522 },
                { x: "Sat", y: 411 },
                { x: "Sun", y: 243 },
            ],
            },
        ],
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
        }

        if(document.getElementById("column-chart") && typeof ApexCharts !== 'undefined') {
        const chart = new ApexCharts(document.getElementById("column-chart"), options);
        chart.render();
        }
});

// Uptime Server
window.addEventListener("load", function() {
    let options = {
    chart: {
        height: "90%",
        maxWidth: "100%",
        type: "area",
        fontFamily: "Inter, sans-serif",
        dropShadow: {
        enabled: false,
        },
        toolbar: {
        show: false,
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
        opacityTo: 0,
        shade: "#0d8323",
        gradientToColors: ["#0d8323"],
        },
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        width: 6,
        curve: 'stepline',
    },
    grid: {
        show: false,
        strokeDashArray: 4,
        padding: {
        left: 2,
        right: 2,
        top: 0
        },
    },
    series: [
        {
        name: "Uptime",
        data: [1, 1, 1, 0, 1, 1],
        color: "#0d8323",
        },
    ],
    xaxis: {
        categories: ['5 min', '10 min', '15 min', '20 min', '25 min', '30 min', '35 min'],
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
        show: false,
    },
    }

    if (document.getElementById("area-chart") && typeof ApexCharts !== 'undefined') {
    const chart = new ApexCharts(document.getElementById("area-chart"), options);
    chart.render();
    }
});