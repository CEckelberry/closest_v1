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
    
    // $("#favoriteSearch").on("keyup", function () {
    //     var value = $(this).val().toLowerCase();
    //     $(".card *").filter(function () {
    //       $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    //     });
    //   });
    $('#favoriteSearch').keyup(function (){
        $('.card').removeClass('d-none');
        var filter = $(this).val(); // get the value of the input, which we filter on
        $('#cards').find('.card .card-body p:not(:contains("'+filter+'"))').parent().parent().addClass('d-none');
    })

    

    });


// Password Strength Checker

$('#Password').passtrength({
    minChars: 6
});

$('#Password').passtrength({
      passwordToggle:true,
      eyeImg :"/static/images/eye.svg" // toggle icon
});

$('#Password').passtrength({
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
      mapLink.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °`;
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




