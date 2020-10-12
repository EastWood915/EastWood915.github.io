$(function(){
  Papa.parse('https://eastwood915.github.io/Data/data.csv', {
    header: true,
    download: true,
    dynamicTyping: true,
    complete: function(results) {
      console.log(results);
  
      update_fields(results.data[results.data.length-2])
      draw_plot("plot-new", results.data, "Data", "Liczba nowych przypadków")
      draw_plot("plot-active", results.data, "Data", "Liczba aktywnych przypadków")
      draw_plot("plot-active-ratio", results.data, "Data", "Aktywnych na 10tys mieszkańców")

      Plotly.relayout("plot-active", {})
      Plotly.relayout("plot-active-ratio", {})
    }
  })
})



function update_fields(data)
{
  $(".spinner_data").hide()
  
  $("#new").text(data["Liczba nowych przypadków"])
  $("#active").text(data["Liczba aktywnych przypadków"])
  $("#ratio").text(data["Aktywnych na 10tys mieszkańców"].toFixed(2).replace('.', ','))
  $("#date").text(data["Data"])
}

function extract_data_for_plot(data, X_series_name, Y_series_name)
{
  var plot_data = {
    x: [],
    y: []
  }

  for (entry of data)
  {
    plot_data.x.push(entry[X_series_name])
    plot_data.y.push(entry[Y_series_name])
  }

  return plot_data
}

function draw_plot(object_id, data, X_series_name, Y_series_name)
{
  var plot_config = {
    responsive: true,
    staticPlot: true,
    type: 'bar'
  }

  var plot_layout = {
    title: Y_series_name,
    paper_bgcolor: '#f8f9fa',
    plot_bgcolor: '#f8f9fa',
    autosize: true,
    margin: {
      l: 30,
      r: 0
    },
    xaxis: {fixedrange: true},
    yaxis: {fixedrange: true}
  }

  Plotly.newPlot(
    object_id,
    [Object.assign(
      extract_data_for_plot(data, X_series_name, Y_series_name),
      plot_config)],
    plot_layout,
    {
      responsive: true,
      displayModeBar: false
    }
  )
}


$('#nav-active-tab').on('shown.bs.tab', function(event){
  Plotly.relayout("plot-active", {})
});

$('#nav-active-ratio-tab').on('shown.bs.tab', function(event){
  Plotly.relayout("plot-active-ratio", {})
});
