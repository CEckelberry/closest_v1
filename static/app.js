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

function geoFindMe() {

    const status = document.querySelector('#status');
    const mapLink = document.querySelector('#map-link');
  
    mapLink.href = '';
    mapLink.textContent = '';
  
    function success(position) {
      const latitude  = position.coords.latitude;
      const longitude = position.coords.longitude;
  
      status.textContent = '';
      mapLink.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
      //mapLink.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °
  
    //   let google_call = axios.get(`https:/maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${config.apiKey}`).then((result) => {
    //     console.log(google_call);
    //     let derived_address = result.data.results[0].formatted_address;
    //     console.log(derived_address);
    //     window.location.replace(`/results/${derived_address}`)
    //   });

      let google_call = axios.post(`/google_search/${latitude}${longitude}`)
      
      
    }
  
    function error() {
      status.textContent = 'Unable to retrieve your location';
    }
  
    if(!navigator.geolocation) {
      status.textContent = 'Geolocation is not supported by your browser';
    } else {
      status.textContent = 'Locating…';
      navigator.geolocation.getCurrentPosition(success, error);
    }
  
  }
  
  document.querySelector('#find-me').addEventListener('click', geoFindMe);




