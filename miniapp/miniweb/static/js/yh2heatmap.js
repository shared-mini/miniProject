document.addEventListener('DOMContentLoaded', function () {
  fetch('/charts/api/correlation-data-2')  // 새 API
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
              colors: ['#FF4560'],
              series: data
          };

          var chart = new ApexCharts(document.querySelector("#chart2"), options);
          chart.render();
      });
});