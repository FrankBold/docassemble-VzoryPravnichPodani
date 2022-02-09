var inputEl = document.querySelector("input[type='text']");
var suggest = new SMap.Suggest(inputEl, {
	provider: new SMap.SuggestProvider({
  	updateParams: params => {
      params.enableCategories = 1;
      params.category = "municipality_cz";
      params.type = "municipality";
      params.lang = "cs";
      params.locality = "cz";
    }
  }),
    delay: 50,
});
suggest.addListener("suggest", suggestData => {
  // vyber polozky z naseptavace
  setTimeout(function() {
    var coords = SMap.Coords.fromWGS84(suggestData.data.longitude, suggestData.data.latitude);
    new SMap.Geocoder.Reverse(coords, odpoved);
  }, 0);
});

var odpoved = function(geocoder) {
    var results = geocoder.getResults();
      for (let  i  = 0; i < results.items.length; i++) {
        if (results.items[i].type == "regi") {
          if (typ == "není") {
          setField("Obec.kraj", results.items[i].name)
        } else {
          setField("Obec." + typ + ".kraj", results.items[i].name)
        }}
  }
}
