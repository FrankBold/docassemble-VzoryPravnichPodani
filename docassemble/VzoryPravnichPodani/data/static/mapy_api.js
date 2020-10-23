var inputEl = document.querySelector("input[placeholder='Adresa']");
var suggest = new SMap.Suggest(inputEl);
suggest.urlParams({
	// omezeni pro celou CR
	bounds: "48.5370786,12.0921668|51.0746358,18.8927040",
  enableCategories: 1,
  category: "street_cz,municipality_cz,address_cz",
  type: "street|municipality|address"
});

suggest.addListener("suggest", function(suggestData) {
  // vyber polozky z naseptavace
  new SMap.Geocoder(suggestData.phrase, odpoved);
}).addListener("close", function() {
  console.log("suggest byl zavren/skryt");
});

function odpoved(geocoder) { /* Odpověď */
    if (!geocoder.getResults()[0].results.length) {
        alert("Tohle neznáme.");
        return;
    }
        var vysledky = geocoder.getResults()[0].results;
        var item = vysledky.shift();
        var sourad = item.coords.toWGS84(2);
        var souradnice = SMap.Coords.fromWGS84(sourad[0], sourad[1]);
        console.log(item)
        new SMap.Geocoder.Reverse(souradnice, odpoved2)
}

function odpoved2(geocoder) {
  var results = geocoder.getResults();
  var adresa = results.label.split(", ");
  setField("clovek.address", "Rerbora")
  setField("clovek.adresa", "rebarbora")
  setField("clovek.city", adresa[1])
  setField("clovek.state", adresa[3])
  setField("clovek.zip", adresa[2])
  console.log(results)
}
