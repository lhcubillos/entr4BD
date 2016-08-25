function onClickQuery(index, db, query) {
  console.log('index: '+index, '\ndb: '+db,'\nquery: '+query);
  $.ajax({
    url: db+'/'+query,
    type: "get", //send it through get method
    data:{ query: query },
    success: function(response) {
      console.log(response);
      document.write(response);
    },
    error: function(xhr) {
      console.log("error", xhr);
    }
  });
}
