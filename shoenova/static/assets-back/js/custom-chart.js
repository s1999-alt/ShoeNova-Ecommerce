// (function ($) {
//     "use strict";


//     // Assuming you have imported Chart.js library and defined your chart configurations.

// // Get the canvas elements
// var weeklyChartCanvas = document.getElementById('weeklyChart');
// var monthlyChartCanvas = document.getElementById('monthlyChart');
// var yearlyChartCanvas = document.getElementById('yearlyChart');

// if (weeklyChartCanvas && monthlyChartCanvas && yearlyChartCanvas) {
//     var weeklyChart = new Chart(weeklyChartCanvas.getContext('2d'), {
//         // Your chart configuration here
//         // ...
//         data: {
//             labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
//             datasets: [{
//                 label: 'Weekly Sales',
//                 data: [1,2,3,4], // Use the data returned by get_weekly_sales()
//                 backgroundColor: 'rgba(44, 120, 220, 0.2)',
//                 borderColor: 'rgba(44, 120, 220)',
//             }]
//         },
//         // ...
//     });

//     var monthlyChart = new Chart(monthlyChartCanvas.getContext('2d'), {
//         // Your chart configuration here
//         // ...
//         data: {
//             labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
//             datasets: [{
//                 label: 'Monthly Sales',
//                 data: [monthly_sales_data], // Use the data returned by get_monthly_sales()
//                 backgroundColor: 'rgba(44, 120, 220, 0.2)',
//                 borderColor: 'rgba(44, 120, 220)',
//             }]
//         },
//         // ...
//     });

//     var yearlyChart = new Chart(yearlyChartCanvas.getContext('2d'), {
//         // Your chart configuration here
//         // ...
//         data: {
//             labels: ['2022', '2023'],
//             datasets: [{
//                 label: 'Yearly Sales',
//                 data: [yearly_sales_data], // Use the data returned by get_yearly_sales()
//                 backgroundColor: 'rgba(44, 120, 220, 0.2)',
//                 borderColor: 'rgba(44, 120, 220)',
//             }]
//         },
//         // ...
//     });
// }









// })(jQuery);





(function ($) {
    "use strict";

    /*Sale statistics Chart*/
    if ($('#myChart').length) {
        var ctx = document.getElementById('myChart').getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',
            
            // The data for our dataset
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                        label: 'Sales',
                        tension: 0.3,
                        fill: true,
                        backgroundColor: 'rgba(44, 120, 220, 0.2)',
                        borderColor: 'rgba(44, 120, 220)',
                        data: [18, 17, 4, 3, 2, 20, 25, 31, 25, 22, 20, 9]
                    },
                    {
                        label: 'Visitors',
                        tension: 0.3,
                        fill: true,
                        backgroundColor: 'rgba(4, 209, 130, 0.2)',
                        borderColor: 'rgb(4, 209, 130)',
                        data: [40, 20, 17, 9, 23, 35, 39, 30, 34, 25, 27, 17]
                    },
                    {
                        label: 'Products',
                        tension: 0.3,
                        fill: true,
                        backgroundColor: 'rgba(380, 200, 230, 0.2)',
                        borderColor: 'rgb(380, 200, 230)',
                        data: [30, 10, 27, 19, 33, 15, 19, 20, 24, 15, 37, 6]
                    }

                ]
            },
            options: {
                plugins: {
                legend: {
                    labels: {
                    usePointStyle: true,
                    },
                }
                }
            }
        });
    } //End if



    /*Sale statistics Chart*/
    if ($('#myChart2').length) {
        var ctx = document.getElementById("myChart2");
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
            labels: ["900", "1200", "1400", "1600"],
            datasets: [
                {
                    label: "US",
                    backgroundColor: "#5897fb",
                    barThickness:10,
                    data: [233,321,783,900]
                }, 
                {
                    label: "Europe",
                    backgroundColor: "#7bcf86",
                    barThickness:10,
                    data: [408,547,675,734]
                },
                {
                    label: "Asian",
                    backgroundColor: "#ff9076",
                    barThickness:10,
                    data: [208,447,575,634]
                },
                {
                    label: "Africa",
                    backgroundColor: "#d595e5",
                    barThickness:10,
                    data: [123,345,122,302]
                },
            ]
            },
            options: {
                plugins: {
                    legend: {
                        labels: {
                        usePointStyle: true,
                        },
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } //end if
    
})(jQuery);