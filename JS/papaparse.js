var data;

Papa.parse('../challanges.csv', {
  header: true,
  download: true,
  dynamicTyping: true,
  complete: function(results) {
    console.log(results);
    data = results.data;
  }
});