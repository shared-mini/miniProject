
const yearsData = JSON.parse(document.getElementById("year-data").dataset.years);
var radio = "population";
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
var areaStr = ` 
				<div class="form-check form-switch">
					<input class="form-check-input" type="checkbox" role="switch" id="chkHeatmap" checked>
					<label class="form-check-label" for="chkHeatmap">면적별 감기 발생률 HEAT MAP</label>
				</div>
				<div class="form-check form-switch" style="margin-top: 10px;">
					<input class="form-check-input" type="checkbox" role="switch" id="chkBar" >
					<label class="form-check-label" for="chkBar">면적별 감기 발생률 SCATTER PLOT</label>
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
// 밀집도별 위험도 str
var riskStr = ` 
				<div class="form-check form-switch">
					<input class="form-check-input" type="checkbox" role="switch" id="chkHeatmap" checked>
					<label class="form-check-label" for="chkHeatmap">밀집도별 위험도 HEAT MAP</label>
				</div>
				<div class="form-check form-switch" style="margin-top: 10px;">
					<input class="form-check-input" type="checkbox" role="switch" id="chkBar" >
					<label class="form-check-label" for="chkBar">밀집도별 위험도 SCATTER PLOT</label>
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
			ctx.fillText(value.toFixed(6), barX + barWidth + tickLength + 2, y + 3);
		}
	}
};


// 히트맵 ajax
function heatmap_ajax(years,radio) {
	if (radio == 'population'){

		$.ajax({
			"url": "/charts/kbCharts-async",
			"method": "get",
			"data": { "years": years,"type": "heatmap", "radio": radio },
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
	} else if(radio == 'area') {
		$.ajax({
			"url": "/charts/kbCharts-async",
			"method": "get",
			"data": { "years": years, "type": "heatmap", "radio": radio },
			"dataType": "json",
			"success": function(data, status, xhr) {
				console.log(data);
				const ctx = document.getElementById('matrix-chart').getContext('2d');
				if (window.heatmap) window.heatmap.destroy();
	
				let yData = [];
				let min = Infinity;
				let max = -Infinity;
	
				for (let i = 0; i < data.length; i++) {
					const value = data[i][4]; // 발생률 또는 기타 수치
					if (value < min) min = value;
					if (value > max) max = value;
	
					yData.push({
						x: data[i][0],   // 연도
						y: data[i][5],   // 지역
						v: value
					});
				}
	
				const yLabels = yData.map(d => d.y);
	
				window.heatmap = new Chart(ctx, {
					type: 'matrix',
					data: {
						datasets: [{
							label: years + '년 (다른 지표)',
							data: yData,
							backgroundColor: function(context) {
								const value = context.dataset.data[context.dataIndex].v;
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
								right: 80
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
									label: ctx => `수치: ${ctx.raw.v}`
								}
							},
							legend: { display: false },
							datalabels: {
								color: '#000',
								font: { weight: 'bold' },
								formatter: value => value.v.toFixed(6),
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
	} else {
		$.ajax({
			"url": "/charts/kbCharts-async",
			"method": "get",
			"data": { "years": years, "type": "heatmap", "radio": radio },
			"dataType": "json",
			"success": function(data, status, xhr) {
				console.log(data);
				const ctx = document.getElementById('matrix-chart').getContext('2d');
				if (window.heatmap) window.heatmap.destroy();
	
				let yData = [];
				let min = Infinity;
				let max = -Infinity;
	
				for (let i = 0; i < data.length; i++) {
					const value = data[i][4]; // 발생률 또는 기타 수치
					if (value < min) min = value;
					if (value > max) max = value;
	
					yData.push({
						x: data[i][0],   // 연도
						y: data[i][5],   // 지역
						v: value
					});
				}
	
				const yLabels = yData.map(d => d.y);
	
				window.heatmap = new Chart(ctx, {
					type: 'matrix',
					data: {
						datasets: [{
							label: years + '년 (다른 지표)',
							data: yData,
							backgroundColor: function(context) {
								const value = context.dataset.data[context.dataIndex].v;
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
								right: 80
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
									label: ctx => `수치: ${ctx.raw.v}`
								}
							},
							legend: { display: false },
							datalabels: {
								color: '#000',
								font: { weight: 'bold' },
								formatter: value => value.v.toFixed(6),
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
}



// 전체 히트맵 ajax
function heatmap_ajax_all(years,radio) {
	if(radio == "population") {

		$.ajax({
			"url": "/charts/kbCharts-async",
			"method": "get",
			"data": { "years": years, "type": "heatmap", "radio": radio },
			"dataType": "json",
			"success": function(data) {
				const ctx = document.getElementById('matrix-chart').getContext('2d');
				if (window.heatmap) window.heatmap.destroy();  // 기존 히트맵 제거
				console.log(data);
	
				let yData = [];
				let xLabelsSet = new Set();
				let yLabelsSet = new Set();
				let min = Infinity;
				let max = -Infinity;
	
				// 데이터 가공
				for (let i = 0; i < data.length; i++) {
					const year = data[i][0];   // 연도
					const region = data[i][1]; // 지역
					const value = parseFloat(data[i][4]);  // 발생률
	
					// xLabels, yLabels 설정
					xLabelsSet.add(year);
					yLabelsSet.add(region);
	
					// 최소/최대 값 계산
					if (value < min) min = value;
					if (value > max) max = value;
	
					yData.push({ x: year, y: region, v: value });
				}
	
				// 레이블 정렬
				const xLabels = Array.from(xLabelsSet).sort();
				const yLabels = Array.from(yLabelsSet);
	
				// 차트 생성
				window.heatmap = new Chart(ctx, {
					type: 'matrix',
					data: {
						datasets: [{
							label: '전체 연도 지역별 질병률',
							data: yData,
							backgroundColor: function(context) {
								const value = context.dataset.data[context.dataIndex].v;
								const ratio = (value - min) / (max - min);
								const red = 255;
								const green = Math.floor(255 * (1 - ratio));
								const blue = Math.floor(100 * (1 - ratio));
								return `rgba(${red}, ${green}, ${blue}, 0.85)`;  // 색상 계산
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
								right: 80  // 컬러바 공간 확보
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
								formatter: value => value.v.toFixed(3),  // 소수점 3자리로 포매팅
								align: 'center',
								anchor: 'center'
							}
						}
					},
					plugins: [ChartDataLabels, colorBarPlugin]  // 플러그인 추가
				});
			},
			error: function(request, status, error) {
				alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
			}
		});
	} else if(radio == 'area') {
		$.ajax({
			"url": "/charts/kbCharts-async",
			"method": "get",
			"data": { "years": years, "type": "heatmap", "radio": radio },
			"dataType": "json",
			"success": function(data) {
				console.log(data);
				const ctx = document.getElementById('matrix-chart').getContext('2d');
				if (window.heatmap) window.heatmap.destroy();  // 기존 히트맵 제거
	
				let yData = [];
				let xLabelsSet = new Set();
				let yLabelsSet = new Set();
				let min = Infinity;
				let max = -Infinity;
	
				// 데이터 가공
				for (let i = 0; i < data.length; i++) {
					const year = data[i][0];   // 연도
					const region = data[i][1]; // 지역
					const value = parseFloat(data[i][4]);  // 발생률
	
					// xLabels, yLabels 설정
					xLabelsSet.add(year);
					yLabelsSet.add(region);
	
					// 최소/최대 값 계산
					if (value < min) min = value;
					if (value > max) max = value;
	
					yData.push({ x: year, y: region, v: value });
				}
	
				// 레이블 정렬
				const xLabels = Array.from(xLabelsSet).sort();
				const yLabels = Array.from(yLabelsSet);
	
				// 차트 생성
				window.heatmap = new Chart(ctx, {
					type: 'matrix',
					data: {
						datasets: [{
							label: '전체 연도 지역별 질병률',
							data: yData,
							backgroundColor: function(context) {
								const value = context.dataset.data[context.dataIndex].v;
								const ratio = (value - min) / (max - min);
								const red = 255;
								const green = Math.floor(255 * (1 - ratio));
								const blue = Math.floor(100 * (1 - ratio));
								return `rgba(${red}, ${green}, ${blue}, 0.85)`;  // 색상 계산
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
								right: 80  // 컬러바 공간 확보
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
								formatter: value => value.v.toFixed(6),  // 소수점 3자리로 포매팅
								align: 'center',
								anchor: 'center'
							}
						}
					},
					plugins: [ChartDataLabels, colorBarPlugin]  // 플러그인 추가
				});
			},
			error: function(request, status, error) {
				alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
			}
		});
	} else {
		$.ajax({
			"url": "/charts/kbCharts-async",
			"method": "get",
			"data": { "years": years, "type": "heatmap", "radio": radio },
			"dataType": "json",
			"success": function(data) {
				console.log(data);
				const ctx = document.getElementById('matrix-chart').getContext('2d');
				if (window.heatmap) window.heatmap.destroy();  // 기존 히트맵 제거
	
				let yData = [];
				let xLabelsSet = new Set();
				let yLabelsSet = new Set();
				let min = Infinity;
				let max = -Infinity;
	
				// 데이터 가공
				for (let i = 0; i < data.length; i++) {
					const year = data[i][0];   // 연도
					const region = data[i][1]; // 지역
					const value = parseFloat(data[i][4]);  // 발생률
	
					// xLabels, yLabels 설정
					xLabelsSet.add(year);
					yLabelsSet.add(region);
	
					// 최소/최대 값 계산
					if (value < min) min = value;
					if (value > max) max = value;
	
					yData.push({ x: year, y: region, v: value });
				}
	
				// 레이블 정렬
				const xLabels = Array.from(xLabelsSet).sort();
				const yLabels = Array.from(yLabelsSet);
	
				// 차트 생성
				window.heatmap = new Chart(ctx, {
					type: 'matrix',
					data: {
						datasets: [{
							label: '전체 연도 지역별 질병률',
							data: yData,
							backgroundColor: function(context) {
								const value = context.dataset.data[context.dataIndex].v;
								const ratio = (value - min) / (max - min);
								const red = 255;
								const green = Math.floor(255 * (1 - ratio));
								const blue = Math.floor(100 * (1 - ratio));
								return `rgba(${red}, ${green}, ${blue}, 0.85)`;  // 색상 계산
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
								right: 80  // 컬러바 공간 확보
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
								formatter: value => value.v.toFixed(6),  // 소수점 3자리로 포매팅
								align: 'center',
								anchor: 'center'
							}
						}
					},
					plugins: [ChartDataLabels, colorBarPlugin]  // 플러그인 추가
				});
			},
			error: function(request, status, error) {
				alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
			}
		});
	}
}

// 페이지 초기화 시 실행함수
heatmap_ajax_all('all',"population");

// 바플롯 ajax(전체 포함)
function barchart_ajax(years,radio) {
	if (radio == "population"){
		$.ajax({
			"url": "/charts/kbCharts-async",
			"method": "get",
			"data": { "years": years,"type": "bar", "radio": radio },
			"dataType": "json",
			"success": function(data, status, xhr) {
				console.log(data)
				const ctx = document.getElementById('barchart1').getContext('2d');
				if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
					window.barchart1.destroy();
				}
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
	} else if(radio == 'area') {
		$.ajax({
			"url": "/charts/kbCharts-async",
			"method": "get",
			"data": { "years": years, "type": "bar", "radio": radio },
			"dataType": "json",
			"success": function(data, status, xhr) {
				console.log(data);
				const ctx = document.getElementById('barchart1').getContext('2d');
				if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
					window.barchart1.destroy();
				}
		
				// 랜덤 색상 생성 함수
				function getRandomColor() {
					const r = Math.floor(Math.random() * 256); // 0 ~ 255
					const g = Math.floor(Math.random() * 256); // 0 ~ 255
					const b = Math.floor(Math.random() * 256); // 0 ~ 255
					return `rgba(${r}, ${g}, ${b}, 0.85)`;  // RGBA 형식으로 반환
				}
		
				// 지역별 색상 저장 객체
				let regionColors = {};
		
				let scatterData = [];
				for (let i = 0; i < data.length; i++) {
					const region = data[i][1];               // 지역명
					const population = data[i][2];           // 인구수
					const area = parseInt(data[i][5]);       // 면적
					const rate = data[i][6];                 // 발생률
		
					// 지역에 맞는 색상이 없다면 새로 생성해서 할당
					if (!regionColors[region]) {
						regionColors[region] = getRandomColor();  // 랜덤 색상 할당
					}
		
					scatterData.push({
						x: area,
						y: rate,
						r: 6,
						region: region,
						population: population,
						backgroundColor: regionColors[region]  // 지역별 색상 적용
					});
				}
		
				window.barchart1 = new Chart(ctx, {
					type: 'scatter',
					data: {
						datasets: [{
							label: years + '년 지역별 면적 vs 질병률',
							data: scatterData,
							backgroundColor: scatterData.map(item => item.backgroundColor),  // 각 점에 맞는 색상 사용
							borderColor: scatterData.map(item => item.backgroundColor),      // 동일 색상 적용
							pointRadius: 8,
							pointHoverRadius: 12
						}]
					},
					options: {
						scales: {
							x: {
								title: {
									display: true,
									text: '지역 면적 (㎡)'
								}
							},
							y: {
								title: {
									display: true,
									text: '발병률'
								}
							}
						},
						plugins: {
							tooltip: {
								callbacks: {
									label: ctx => {
										const d = ctx.raw;
										return `${d.region} (${d.population.toLocaleString()}명)\n면적: ${d.x.toLocaleString()}㎡\n발병률: ${d.y}`;
									}
								}
							},
							legend: { display: false }
						}
					}
				});
			},
			"error": function(request, status, error) {
				alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
			}
		});
		
	} else {

		$.ajax({
			"url": "/charts/kbCharts-async",
			"method": "get",
			"data": { "years": years, "type": "bar", "radio": radio },
			"dataType": "json",
			"success": function(data, status, xhr) {
				console.log(data);
				const ctx = document.getElementById('barchart1').getContext('2d');
				if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
					window.barchart1.destroy();
				}
		
				// 랜덤 색상 생성 함수
				function getRandomColor() {
					const r = Math.floor(Math.random() * 256); // 0 ~ 255
					const g = Math.floor(Math.random() * 256); // 0 ~ 255
					const b = Math.floor(Math.random() * 256); // 0 ~ 255
					return `rgba(${r}, ${g}, ${b}, 0.85)`;  // RGBA 형식으로 반환
				}
		
				// 지역별 색상을 동적으로 생성
				let regionColors = {};
		
				// 데이터에서 지역을 추출하여 색상 할당
				for (let i = 0; i < data.length; i++) {
					const region = data[i][1];  // 지역명
					if (!regionColors[region]) {  // 이미 색상이 할당되지 않은 지역이라면
						regionColors[region] = getRandomColor();  // 랜덤 색상 할당
					}
				}
		
				let scatterData = [];
				for (let i = 0; i < data.length; i++) {
					const region = data[i][1];               // 지역명
					const area = parseFloat(data[i][5]);     // 밀집률
					const population = data[i][6];           // 발병률
					const rate = data[i][7];                 // 위험도
					const year = data[i][0];                 // 연도
		
					// 지역에 맞는 색상 적용
					const color = regionColors[region] || 'rgba(75, 192, 192, 0.85)';  // 기본 색상도 지정
		
					scatterData.push({
						x: area,
						y: rate,
						r: 6,
						region: region,
						population: population,
						year: year,
						backgroundColor: color  // 지역에 맞는 색상 적용
					});
				}
		
				window.barchart1 = new Chart(ctx, {
					type: 'scatter',
					data: {
						datasets: [{
							label: years + '년 지역별 밀집도 별 위험도',
							data: scatterData,
							backgroundColor: scatterData.map(item => item.backgroundColor),  // 각 점에 맞는 색상 사용
							borderColor: scatterData.map(item => item.backgroundColor),      // 동일 색상 적용
							pointRadius: 8,
							pointHoverRadius: 12
						}]
					},
					options: {
						scales: {
							x: {
								title: {
									display: true,
									text: '밀집률'
								},
								ticks: {
									callback: function(value, index, values) {
										return value.toFixed(3);  // 소수점 3자리로 표기
									},
									stepSize: 0.001,   // x축 간격을 설정하여 점들이 너무 밀리지 않게 함
									min: 0,           // 최소값
									max: 10           // 최대값 (필요에 따라 조정)
								}
							},
							y: {
								title: {
									display: true,
									text: '위험도'
								}
							}
						},
						plugins: {
							tooltip: {
								callbacks: {
									label: ctx => {
										const d = ctx.raw;
										return `${d.region} (발병률: ${d.population.toLocaleString()})\n밀집률: ${d.x.toLocaleString()}\n위험도: ${d.y}\n연도: ${d.year}`;
									}
								}
							},
							legend: { display: false }
						}
					}
				});
			},
			"error": function(request, status, error) {
				alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
			}
		});
	}
}

// 연도 드롭박스 선택 이벤트
function Fn_click(){
	$("#dropDown a").click(function (){
		var years = $(this).attr("name");
		// 히트맵만 체크
		// radio = ($("#populationRadio").is(':checked')) ? "population" : "area"; 
		if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
			window.barchart1.destroy();
		}
		if (window.heatmap) window.heatmap.destroy();
		if ($('#chkHeatmap').is(':checked') && !($('#chkBar').is(':checked'))) {
			// 바차트 캔버스 삭제
			if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
				window.barchart1.destroy();
			}
			if(years != 'all'){
				heatmap_ajax(years,radio);
			} else {
				heatmap_ajax_all(years,radio);
			}
		}

		// 바차트만 체크
		if ($('#chkBar').is(':checked') && !($('#chkHeatmap').is(':checked'))) {
			// 히트맵 캔버스 삭제
			if (window.heatmap) window.heatmap.destroy();
			barchart_ajax(years,radio);
		}
		// 둘다 체크
		if ($('#chkBar').is(':checked') && $('#chkHeatmap').is(':checked')) {
			if(years != 'all'){
				heatmap_ajax(years,radio);
				barchart_ajax(years,radio);
			} else {
				heatmap_ajax_all(years,radio);
				barchart_ajax(years,radio);
			}
		}
	
		if ( !($('#chkBar').is(':checked')) && !($('#chkHeatmap').is(':checked'))) {
			if (window.heatmap) window.heatmap.destroy();
			if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
				window.barchart1.destroy();
			};
		}
		
		var yearStr = (years != 'all') ? years : "모든"; 
		$("#yrDropdown").html(yearStr+` 년도<span class="caret"></span>`)
	});
}

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
	// if ( $('#chkHeatmap').is(':checked') && !($('#chkBar').is(':checked'))) {
		
	// 	if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
	// 			window.barchart1.destroy();
	// 		}
	// 		heatmap_ajax_all('all')
	// }

	// // barPlot만 선택 시
	// if ( !($('#chkHeatmap').is(':checked')) && $('#chkBar').is(':checked')) {
		
	// 	if (window.heatmap) window.heatmap.destroy();
		
	// 	barchart_ajax('all')
	// }
});


// 라디오 체크 이벤트
$("input[name='radioDefault']").on("change", function () {
    const radioChked = $(this).val();
    if ($('#populationRadio').is(':checked')) {
		$(".chkbox").empty();
        $(".chkbox").html(populationStr);
		$("#dropDown li").html(html);
		radio = "population"

		if (window.heatmap) window.heatmap.destroy();
		if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
			window.barchart1.destroy();
		}
		Fn_click();

    } 
	if ($('#areaRadio').is(':checked')) {
		
		$(".chkbox").empty();
        $(".chkbox").html(areaStr);
		$("#dropDown li").html(html);
		radio = "area"
		if (window.heatmap) window.heatmap.destroy();
		if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
			window.barchart1.destroy();
		}
		Fn_click();
    }  
	if ($('#riskRadio').is(':checked')){
		$(".chkbox").empty();
        $(".chkbox").html(riskStr);
		$("#dropDown li").html(html);
		radio = "risk"
		if (window.heatmap) window.heatmap.destroy();
		if (window.barchart1 && typeof window.barchart1.destroy === 'function') {
			window.barchart1.destroy();
		}
		Fn_click();
	}
});

Fn_click()
