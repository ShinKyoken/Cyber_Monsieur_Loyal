$("#fb_btn").click(function(){
  // console.log("oui");
  var cpt = $("#cpt").text();
  var resultat = ""
  for (var i = 1; i < parseInt(cpt, 10)+1; i++) {
    resultat += "\n" + $("#equipe"+ i.toString()).text() + " : " + $("#score_equipe" + i.toString()).text()
  }
  console.log(resultat);
  FB.api(
    '/837221559947323/feed',
    'POST',
    {"message":"Voici les résultats :" + resultat,"access_token":"EAAPku8CZCefQBAIyZC8ujY2mIqK5fikNdVtoHyThaO5toZBeaFSWDLoKskpxumeGZBTR4A9M9P5Nz4pSiPQ0f6vBAmUcnQ5MjnZBtXkOmRXZBpdCF73md7KKtT60WHG3y7xDm3cLHOtPWcAjZCzEVYxQP9HWkz8knMMj25ZC3idXnFzTZCLfZAZAXijlSY8GSsvI2IZD"},
    function(response) {
      console.log(response);
    }
  );
});
