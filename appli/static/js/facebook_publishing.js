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
    {"message":"Voici les résultats :" + resultat,"access_token":"EAAPku8CZCefQBABmhbf6hhaFDZC5i3MeaPZC7UtGhZAeMRGzoLJGp1Ps5f4x3xuZB0H3CN9OVNoRGLZCZAwHr3LcEuwilSRgNWZAXEcF6x34WKnZCOETbH6Uxt5rZB3U2JLzdRKKE4vXfLgcwaHiYcqYwoLmKeRUA7rTZC4NwVL1gxqtAd1SrmQmvLFALmPuYzsVmN3xGCttXZBL45fn1DzWTeZCI"},
    function(response) {
      console.log(response);
    }
  );
});
