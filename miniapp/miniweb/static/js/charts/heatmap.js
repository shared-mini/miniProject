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



function heatmap_ajax(years) {
	$.ajax({
		"url": "/charts/kbCharts-async",
		"method": "get",
		"data": { "years": years },
		"dataType": "json",
		"success": function(data, status, xhr) {
			const ctx = document.getElementById('matrix-chart').getContext('2d');
			if (window.chart) window.chart.destroy();

			let yData = [];
			for (let i = 0; i < data.length; i++) {
				yData.push({
					x: data[i][0],   // 연도
					y: data[i][5],   // 지역
					v: data[i][4]    // 발생률
				});
			}

			const yLabels = yData.map(d => d.y);

			window.chart = new Chart(ctx, {
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





// 전체 히트맵
function heatmap_ajax_all(years) {

	$.ajax({
		"url": "/charts/kbCharts-async",
		"method": "get",
		"data": { "years": years },
		"dataType": "json",
		"success": function(data) {
			const ctx = document.getElementById('matrix-chart').getContext('2d');
			if (window.chart) window.chart.destroy();

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

			window.chart = new Chart(ctx, {
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


heatmap_ajax_all('all');

$("#dropDown a").click(function(){
    var years = $(this).attr("name");
	if(years != 'all'){
		heatmap_ajax(years);
	} else {
		heatmap_ajax_all(years)
	}
});

////////////////////////////////////////////////// 백업///////////////////////////////////////
	// $.ajax({
    //     "url" : "/charts/kbCharts-async",
    //     "method" : "get",
    //     "data" : {"years" : years},
    //     "dataType" : "json",
    //     "success" : function(data, status, xhr) {
    //         const ctx = document.getElementById('matrix-chart').getContext('2d');
    //         // 기존 차트가 있으면 삭제
    //         if (window.chart) {
    //             window.chart.destroy();
    //         }
    //         var yData = [];
    //         // 서버에서 받은 데이터를 yData 배열로 변환
    //         for (i = 0; i < data.length; i++) {
    //             yData.push({
    //                 x: data[i][0], // 연도
    //                 y: data[i][5], // 지역
    //                 v: data[i][4]  // 발생률
    //             });
    //         }


    //         // 새로운 차트 생성
    //         window.chart = new Chart(ctx, {
    //             type: 'matrix',
    //             data: {
    //                 datasets: [{
    //                     label: years + '년 지역별 인구 대비 질병률',
    //                     data: yData, // 여기서 data를 yData로 변경
    //                     backgroundColor: function(context) {
    //                         const value = context.dataset.data[context.dataIndex].v;
                        
    //                         // 발생률을 기반으로 색상 계산
    //                         const min = 0.07; // 최소 발생률
    //                         const max = 0.16; // 최대 발생률
                        
    //                         const ratio = (value - min) / (max - min); // 비율 계산
                        
    //                         const red = 255;
    //                         const green = Math.floor(255 * (1 - ratio));
    //                         const blue = Math.floor(100 * (1 - ratio));
                        
    //                         return `rgba(${red}, ${green}, ${blue}, 0.85)`;
    //                     },
    //                     borderColor: 'white',
    //                     borderWidth: 1,
    //                     width: ({ chart }) => (chart.chartArea || {}).width,
    //                     height: 30
    //                 }]
    //             },
    //             options: {
    //                 scales: {
    //                     x: {
    //                         type: 'category',
    //                         labels: [years],  // 선택된 연도만 표시
    //                         title: {
    //                             display: true,
    //                             text: '연도'
    //                         },
    //                         ticks: {
    //                             stepSize: 1
    //                         },
    //                         grid: {
    //                             display: false
    //                         }
    //                     },
    //                     y: {
    //                         type: 'category',
    //                         labels: yData.map(d => d.y), // 지역 데이터를 y축 레이블로 사용
    //                         offset: true,
    //                         title: {
    //                             display: true,
    //                             text: '지역'
    //                         }
    //                     }
    //                 },
    //                 plugins: {
    //                     tooltip: {
    //                         callbacks: {
    //                             title: ctx => ctx[0].raw.y,
    //                             label: ctx => `발생률: ${ctx.raw.v}`
    //                         }
    //                     },
    //                     legend: { display: false },
    //                     datalabels: {
    //                         color: '#000',
    //                         font: {
    //                             weight: 'bold'
    //                         },
    //                         formatter: value => value.v.toFixed(3),
    //                         align: 'center',
    //                         anchor: 'center'
    //                     }
    //                 }
    //             },
    //             plugins: [ChartDataLabels] // 여기에 datalabels 플러그인 추가
    //         });
    //     },
    //     "error" : function(request, status, error){
    //         alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    //     }
    // });