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
