document.addEventListener('DOMContentLoaded', function () {
    console.log("🔥 yhChartsAll.js loaded!");
  
    // 첫 번째 차트: 연령대 상관계수
    fetch('/charts/api/correlation-data')
        .then(response => response.json())
        .then(data => {
            console.log("✅ chart1 data loaded", data);
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
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        })
        .catch(error => {
            console.error("❌ chart1 error:", error);
        });
  
    // 두 번째 차트: 변수별 상관계수
    fetch('/charts/api/correlation-data-2')
        .then(response => response.json())
        .then(data => {
            console.log("✅ chart2 data loaded", data);
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
            var chart2 = new ApexCharts(document.querySelector("#chart2"), options);
            chart2.render();
        })
        .catch(error => {
            console.error("❌ chart2 error:", error);
        });
  });
  