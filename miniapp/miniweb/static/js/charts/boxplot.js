var trace1 = {
    y: [1, 2, 3, 4, 4, 4, 8, 9, 10],
    type: 'box',
    name: 'Sample A',
    marker:{
      color: 'rgb(214,12,140)'
    }
  };
  
  var trace2 = {
    y: [2, 3, 3, 3, 3, 5, 6, 6, 7],
    type: 'box',
    name: 'Sample B',
    marker:{
      color: 'rgb(0,128,128)'
    }
  };
  
  var data = [trace1, trace2];
  
  var layout = {
    title: {
      text: 'Colored Box Plot'
    }
  };
  
  Plotly.newPlot('myDiv', data, layout);
  