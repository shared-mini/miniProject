const chart = new Chart('matrix-chart', {
	type: 'matrix',
	data: {
	  datasets: [{
		label: 'Basic matrix',
		data: [{x: 1, y: 1}, {x: 2, y: 1}, {x: 1, y: 2}, {x: 2, y: 2}],
		borderWidth: 1,
		backgroundColor: [
			'rgba(255, 99, 132, 0.2)',
			'rgb(50,205,50, 0.2)',
			'rgba(255, 206, 86, 0.2)',
			'rgba(75, 192, 192, 0.2)'
		],
		borderColor: [
			'rgba(255,99,132, 1)',
			'rgba(54, 162, 235, 1)',
			'rgba(255, 206, 86, 1)',
			'rgba(75, 192, 192, 1)'
		],
		width: ({chart}) => (chart.chartArea || {}).width / 2 - 1,
		height: ({chart}) => (chart.chartArea || {}).height / 2 - 1,
	  }],
	},
	options: {
	  scales: {
		x: {
		  display: false,
		  min: 0.5,
		  max: 2.5,
		  offset: false
		},
		y: {
		  display: false,
		  min: 0.5,
		  max: 2.5
		}
	  }
	}
  });
