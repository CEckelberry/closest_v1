$(document).ready(function () {
    $('#results_table').DataTable({
        "ordering": false
    });
    $('.dataTables_length').addClass('bs-select');


    $("#star").on("click", function() {
        console.log("Clicked");
        $(this).addClass('amber-text fas fa-star');

        let name = $("#results_table")[0].tBodies[0].rows[0].cells[0].textContent;
        let address = $("#results_table")[0].tBodies[0].rows[0].cells[1].textContent;
        let map_image_url = $("#map_result")[0].src;
        console.log("name:" + name);
        console.log("address:" + address);
        console.log("map image url:" + map_image_url);

        let favorite_response = axios.post('/favorites/add', {
            name, address, map_image_url
        });
        
    });    
    
    // $('#favoriteSearch').keyup(function (){
    //     $('.card').removeClass('d-none');
    //     var filter = $(this).val(); // get the value of the input, which we filter on
    //     $('#cards').find('.card .card-body h4:not(:contains("'+filter+'"))').parent().parent().addClass('d-none');
    // })

    $("#favoriteSearch").on("keyup", function() {
      console.log("activated")
      var value = $(this).val().toLowerCase();
      $("#cards .col").filter(function() {
        $(this).toggle($(this).find('.card-body').text().toLowerCase().indexOf(value) > -1)
      });
    });
    
    });


// Password Strength Checker

$('#password').passtrength({
    minChars: 6
});

$('#password').passtrength({
      passwordToggle:true,
      eyeImg :"/static/images/eye.svg" // toggle icon
});

$('#password').passtrength({
    tooltip: true,
    textWeak: "Weak",
    textMedium: "Medium",
    textStrong: "Strong",
    textVeryStrong: "Very Strong",
  });

$('#flash').delay(1200).fadeOut(700)

window.onload = function geoFindMe() {

    var startPos;
    var nudge = document.getElementById("nudge");

    var showNudgeBanner = function() {
      nudge.style.display = "block";
    };

    var hideNudgeBanner = function() {
      nudge.style.display = "none";
    };

    var nudgeTimeoutId = setTimeout(showNudgeBanner, 5000);

    const status = document.querySelector('#status');
    const mapLink = document.querySelector('#map-link');

    var geoOptions = {
      maximumAge: 5 * 60 * 1000,
      enableHighAccuracy: true
    }
  
    mapLink.href = '';
    mapLink.textContent = '';
    var geoSuccess = function(position) {
      let latitude = position.coords.latitude;
      let longitude = position.coords.longitude;
      
      console.log(latitude, longitude)
  
      status.textContent = '';
      mapLink.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;


    }
  
    var geoError = function(error) {
      console.log('Error occurred. Error code: ' + error.code);
      // error.code can be:
      //   0: unknown error
      //   1: permission denied
      //   2: position unavailable (error response from location provider)
      //   3: timed out
    };

  
    if(!navigator.geolocation) {
      status.textContent = 'Geolocation is not supported by your browser';
    } else {
      status.textContent = 'Locating…';
      navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
    }
    
  }

  //

  $('#geoloc').on('submit', (e) => {
    e.preventDefault();
    console.log("You made it to the post request!");
    navigator.geolocation.getCurrentPosition(success);

    function success(position) {
      //$("#geoloc").attr('action', `/google_search/${position.coords.latitude},${position.coords.longitude}`).submit();
      const theForm = document.createElement('form');
      theForm.setAttribute('action', `/google_search/${position.coords.latitude},${position.coords.longitude}`);
      document.body.appendChild(theForm);
      theForm.submit();
    }
});
