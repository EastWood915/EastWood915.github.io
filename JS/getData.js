Papa.parse('https://eastwood915.github.io/Data/data.csv', {
  header: true,
  download: true,
  dynamicTyping: true,
  complete: function(results) {
    console.log(results);

    update_fields(results.data[results.data.length-1])
    draw_plot("wykres", results.data, "Data", "Liczba aktywnych przypadków")
  }
})



function update_fields(data)
{
  $(".spinner_data").hide()
  
  $("#new").text(data["Liczba nowych przypadków"])
  $("#active").text(data["Liczba aktywnych przypadków"])
  $("#ratio").text(data["Aktywnych na 10tys mieszkańców"].toFixed(2))
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
    type: 'bar'
  }

  var plot_layout = {
    title: Y_series_name
  }

  Plotly.newPlot(
    object_id,
    [Object.assign(
      extract_data_for_plot(data, X_series_name, Y_series_name),
      plot_config)],
    plot_layout
  )
}