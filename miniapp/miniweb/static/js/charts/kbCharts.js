
const yearsData = JSON.parse(document.getElementById("year-data").dataset.years);
let html = "";
yearsData.forEach(row => {
	html += `<a name="${row[0]}">${row[0]} 년도</a>\n`;
});
html += `<a name="all">모든 연도</a>`;


// 인구별 감기 발생률 str
var populationStr = `<div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" role="switch" id="chkHeatmap" checked>
                        <label class="form-check-label" for="chkHeatmap">인구별 감기 발생률 HEAT MAP</label>
                      </div>
                      <div class="form-check form-switch" style="margin-top: 10px;">
					  <input class="form-check-input" type="checkbox" role="switch" id="chkBar" >
					  <label class="form-check-label" for="chkBar">인구별 감기 발생률 BAR PLOT</label>
                      </div>
                      <div class="dropdown years">
                        <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" id="yrDropdown">
                          연도
                            <span class="caret">
                            </span>
                        </button>
                        <ul id="dropDown" class="dropdown-menu">
                            <li>
                              	
                            </li>
                        </ul>
                      </div>`;

// 면적별 감기 발생률 str
var areaStr = ` <div class="form-check form-switch">
					<input class="form-check-input" type="checkbox" role="switch" id="chkHeatmap" checked>
					<label class="form-check-label" for="chkHeatmap">면적별 감기 발생률 HEAT MAP</label>
				</div>
				<div class="form-check form-switch">
					<input class="form-check-input" type="checkbox" role="switch" id="chkBar">
					<label class="form-check-label" for="chkBar">면적별 감기 발생률 BAR PLOT</label>
				</div> `;

$(".chkbox").html(populationStr);
$("#dropDown li").html(html);



const colorBarPlugin = {
	id: 'colorBarLegend',
	afterDraw(chart) {
		const { ctx, chartArea: { top, bottom, right } } = chart;

		// yData에서 발생률 값만 추출해서 min, max 계산
		let min = Infinity;
		let max = -Infinity;

		chart.data.datasets.forEach(dataset => {
			dataset.data.forEach(item => {
				const value = item.v;
				if (value < min) min = value;
				if (value > max) max = value;
			});
		});

		const barWidth = 15;
		const barHeight = bottom - top;

		// 그라데이션 색상 설정 (자동으로 min, max에 맞게)
		const gradient = ctx.createLinearGradient(0, bottom, 0, top);
		gradient.addColorStop(0, 'rgb(240, 248, 167)');
		gradient.addColorStop(1, 'rgba(255,0,0,0.85)');

		// 컬러바 그리기
		const barX = right + 30;
		ctx.fillStyle = gradient;
		ctx.fillRect(barX, top, barWidth, barHeight);

		// 눈금자 추가
		const tickCount = 5;
		const tickLength = 5;
		ctx.strokeStyle = '#000';
		ctx.fillStyle = '#000';
		ctx.lineWidth = 1;
		ctx.font = '11px sans-serif';
		ctx.textAlign = 'left';

		for (let i = 0; i <= tickCount; i++) {
			const ratio = i / tickCount;
			const y = bottom - (barHeight * ratio);
			const value = min + (max - min) * ratio;

			// 눈금선
			ctx.beginPath();
			ctx.moveTo(barX + barWidth, y);
			ctx.lineTo(barX + barWidth + tickLength, y);
			ctx.stroke();

			// 눈금 텍스트
			ctx.fillText(value.toFixed(2), barX + barWidth + tickLength + 2, y + 3);
		}
	}
};


// 히트맵 ajax
function heatmap_ajax(years) {
	$.ajax({
		"url": "/charts/kbCharts-async",
		"method": "get",
		"data": { "years": years,"type": "heatmap" },
		"dataType": "json",
		"success": function(data, status, xhr) {
			console.log(data)
			const ctx = document.getElementById('matrix-chart').getContext('2d');
			if (window.heatmap) window.heatmap.destroy();

			let yData = [];
			for (let i = 0; i < data.length; i++) {
				yData.push({
					x: data[i][0],   // 연도 1
					y: data[i][5],   // 지역 6
					v: data[i][4]    // 발생률 5
				});
			}

			const yLabels = yData.map(d => d.y);

			window.heatmap = new Chart(ctx, {
				type: 'matrix',
				data: {
					datasets: [{
						label: years + '년 지역별 인구 대비 질병률',
						data: yData,
						backgroundColor: function(context) {
							const value = context.dataset.data[context.dataIndex].v;
							const min = 0.07;
							const max = 0.16;
							const ratio = (value - min) / (max - min);
							const red = 255;
							const green = Math.floor(255 * (1 - ratio));
							const blue = Math.floor(100 * (1 - ratio));
							return `rgba(${red}, ${green}, ${blue}, 0.85)`;
						},
						borderColor: 'white',
						borderWidth: 1,
						width: ({ chart }) => (chart.chartArea || {}).width,
						height: 30
					}]
				},
				options: {
					layout: {
						padding: {
							right: 80 // 컬러바 공간 확보
						}
					},
					scales: {
						x: {
							type: 'category',
							labels: [years],
							title: {
								display: true,
								text: '연도'
							},
							grid: { display: false }
						},
						y: {
							type: 'category',
							labels: yLabels,
							offset: true,
							title: {
								display: true,
								text: '지역'
							}
						}
					},
					plugins: {
						tooltip: {
							callbacks: {
								title: ctx => ctx[0].raw.y,
								label: ctx => `발생률: ${ctx.raw.v}`
							}
						},
						legend: { display: false },
						datalabels: {
							color: '#000',
							font: { weight: 'bold' },
							formatter: value => value.v.toFixed(3),
							align: 'center',
							anchor: 'center'
						}
					}
				},
				plugins: [ChartDataLabels, colorBarPlugin]
			});
		},
		"error": function(request, status, error) {
			alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
		}
	});
}





// 전체 히트맵 ajax
function heatmap_ajax_all(years) {

	$.ajax({
		"url": "/charts/kbCharts-async",
		"method": "get",
		"data": { "years": years, "type": "heatmap" },
		"dataType": "json",
		"success": function(data) {
			const ctx = document.getElementById('matrix-chart').getContext('2d');
			if (window.heatmap) window.heatmap.destroy();
			console.log(data)
			let yData = [];
			let xLabelsSet = new Set();
			let yLabelsSet = new Set();

			for (let i = 0; i < data.length; i++) {
				const year = data[i][0];   // 연도
				const region = data[i][1]; // 지역
				const rate = data[i][4];   // 발생률

				xLabelsSet.add(year);
				yLabelsSet.add(region);

				yData.push({ x: year, y: region, v: rate });
			}

			const xLabels = Array.from(xLabelsSet).sort();
			const yLabels = Array.from(yLabelsSet);

			window.heatmap = new Chart(ctx, {
				type: 'matrix',
				data: {
					datasets: [{
						label: '전체 연도 지역별 인구 대비 질병률',
						data: yData,
						backgroundColor: function(context) {
							const value = context.dataset.data[context.dataIndex].v;
							const min = 0.07;
							const max = 0.16;
							const ratio = (value - min) / (max - min);
							const red = 255;
							const green = Math.floor(255 * (1 - ratio));
							const blue = Math.floor(100 * (1 - ratio));
							return `rgba(${red}, ${green}, ${blue}, 0.85)`;
						},
						borderColor: 'white',
						borderWidth: 1,
						width: ({ chart }) => ((chart.chartArea || {}).width || 600) / xLabels.length,
						height: 30
					}]
				},
				options: {
					layout: {
						padding: {
							right: 80 // 컬러바 공간 확보
						}
					},
					scales: {
						x: {
							type: 'category',
							labels: xLabels,
							title: {
								display: true,
								text: '연도'
							},
							grid: { display: false }
						},
						y: {
							type: 'category',
							labels: yLabels,
							offset: true,
							title: {
								display: true,
								text: '지역'
							}
						}
					},
					plugins: {
						tooltip: {
							callbacks: {
								title: ctx => `${ctx[0].raw.y} - ${ctx[0].raw.x}`,
								label: ctx => `발생률: ${ctx.raw.v}`
							}
						},
						legend: { display: false },
						datalabels: {
							color: '#000',
							font: { weight: 'bold' },
							formatter: value => value.v.toFixed(3),
							align: 'center',
							anchor: 'center'
						}
					}
				},
				plugins: [ChartDataLabels, colorBarPlugin]
			});
		},
		error: function(request, status, error) {
			alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
		}
	});
}

// 페이지 초기화 시 실행함수
heatmap_ajax_all('all');

// 바플롯 ajax(전체 포함)
function barchart_ajax(years) {
	$.ajax({
		"url": "/charts/kbCharts-async",
		"method": "get",
		"data": { "years": years,"type": "bar" },
		"dataType": "json",
		"success": function(data, status, xhr) {
			const ctx = document.getElementById('barchart1').getContext('2d');
			if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
				window.barchart1.destroy();
			}
			console.log(data)
			let xData = [];
			let yData = [];
			let barColors = [];

			const min = 0.07;
			const max = 0.16;

			for (let i = 0; i < data.length; i++) {
				const region = data[i][5]; // 지역 x
				const rate = parseFloat(data[i][4]);   // 발생률 y
				xData.push(region);
				yData.push(rate);

				// heatmap 스타일 색상 계산
				const ratio = Math.max(0, Math.min(1, (rate - min) / (max - min)));
				const red = 255;
				const green = Math.floor(255 * (1 - ratio));
				const blue = Math.floor(100 * (1 - ratio));
				const color = `rgba(${red}, ${green}, ${blue}, 0.85)`;
				barColors.push(color);
			}

			if(years == 'all'){
				years = '모든';
			}

			window.barchart1 = new Chart(ctx, {
				type: 'bar',
				data: {
					labels: xData,
					datasets: [{
						label: [years] + "연도",
						data: yData,
						backgroundColor: barColors,
						borderColor: 'white',
						borderWidth: 1
					}]
				},
				options: {
					scales: {
						y: {
							beginAtZero: true,
							title: {
								display: true,
								text: '질병 발생률'
							}
						},
						x: {
							title: {
								display: true,
								text: '지역'
							}
						}
					},
					plugins: {
						legend: { display: false },
						tooltip: {
							callbacks: {
								label: ctx => `발생률: ${ctx.raw}`
							}
						},
						datalabels: {
							anchor: 'end',
							align: 'end',
							color: '#000',
							font: {
								weight: 'bold'
							},
							formatter: (value) => value.toFixed(3)
						}
					}
				},
				plugins: [ChartDataLabels]
			});
		},
		"error": function(request, status, error) {
			alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
		}
	});
}


// 연도 드롭박스 선택 이벤트
$("#dropDown a").click(function(){
    var years = $(this).attr("name");
	// 히트맵만 체크
	if ($('#chkHeatmap').is(':checked') && !($('#chkBar').is(':checked'))) {
		if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
			window.barchart1.destroy();
		}
		if(years != 'all'){
			heatmap_ajax(years);
		} else {
			heatmap_ajax_all(years);
		}
	}
	// 바차트만 체크
	if ($('#chkBar').is(':checked') && !($('#chkHeatmap').is(':checked'))) {
		if (window.heatmap) window.heatmap.destroy();
		barchart_ajax(years);
	}
	// 둘다 체크
	if ($('#chkBar').is(':checked') && $('#chkHeatmap').is(':checked')) {
		if(years != 'all'){
			heatmap_ajax(years);
			barchart_ajax(years);
		} else {
			heatmap_ajax_all(years);
			barchart_ajax(years);
		}
	}

	if ( !($('#chkBar').is(':checked')) && !($('#chkHeatmap').is(':checked'))) {
		if (window.heatmap) window.heatmap.destroy();
	}
	
	var yearStr = (years != 'all') ? years : "모든"; 
	$("#yrDropdown").html(yearStr+` 년도<span class="caret"></span>`)
});

// 체크박스 클릭 이벤트
$(".chkbox").click(function(){
	// 모두 체크 해제 시
	if ( !($('#chkHeatmap').is(':checked')) && !($('#chkBar').is(':checked'))) {
		if (window.heatmap) window.heatmap.destroy();
		if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
			window.barchart1.destroy();
		}
	}
	// heatMap만 선택 시
	if ( $('#chkHeatmap').is(':checked') && !($('#chkBar').is(':checked'))) {
		
		if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
				window.barchart1.destroy();
			}
			heatmap_ajax_all('all')
	}

	// barPlot만 선택 시
	if ( !($('#chkHeatmap').is(':checked')) && $('#chkBar').is(':checked')) {
		
		if (window.heatmap) window.heatmap.destroy();
		
		barchart_ajax('all')
	}
});


// 라디오 체크 이벤트
$("input[name='radioDefault']").on("change", function () {
    const radioChked = $(this).val();

    if (radioChked == "populationRadio") {
		$(".chkbox").empty();
        $(".chkbox").html(populationStr);
		$("#dropDown li").html(html);
		
		$("#dropDown a").click(function(){
			var years = $(this).attr("name");
			if(years != 'all'){
				heatmap_ajax(years);
			} else {
				heatmap_ajax_all(years)
			}
		});
    } else if (radioChked == "areaRadio") {
		
        $(".chkbox").empty();
        $(".chkbox").html(areaStr);
    }
});

