var new_cases = $("#new")
var active_cases = $("#active")
var case_ratio = $("#ratio")

var data;

Papa.parse('https://eastwood915.github.io/Data/data.csv', {
  header: true,
  download: true,
  dynamicTyping: true,
  complete: function(results) {
    console.log(results);
    data = results.data;

    var today_data = data[data.length-2]

    new_cases.text(today_data["Liczba nowych przypadków"])
    active_cases.text(today_data["Liczba aktywnych przypadków"])
    case_ratio.text(today_data["Aktywnych na 10tys mieszkańców"])
  }
});


//new_cases.text("111")
active_cases.text("222") 
case_ratio.text("6.66") 

