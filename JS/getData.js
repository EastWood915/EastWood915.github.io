Papa.parse('https://eastwood915.github.io/Data/data.csv', {
  header: true,
  download: true,
  dynamicTyping: true,
  complete: function(results) {
    console.log(results);

    update_fields(results.data[results.data.length-1])
  }
})



function update_fields(data)
{
  $(".spinner_data").hide()
  
  $("#new").text(data["Liczba nowych przypadków"])
  $("#active").text(data["Liczba aktywnych przypadków"])
  $("#ratio").text(data["Aktywnych na 10tys mieszkańców"])
  $("#date").text(data["Data"])
}