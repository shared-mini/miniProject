document.addEventListener('DOMContentLoaded', function () {
    fetch('/charts/api/correlation-data')  
        .then(response => response.json())
        .then(data => {
            var options = {
                chart: {
                    type: 'heatmap',
                    height: 350
                },
                dataLabels: {
                    enabled: true
                },
                colors: ['#008FFB'],
                series: data
            };

            var chart = new ApexCharts(document.querySelector("#heatmap1"), options);
            chart.render();
        });
});