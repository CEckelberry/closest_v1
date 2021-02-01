# Closest The App to find the Closest Mass Transit!

I created this app to become one of my cornerstone capstone projects showcasing my skills in all things development. This app is easy to use and once you create an account, you can search available public transit locations either via your devices' location, or searching via address! I have styled the entire application with Modern Design Bootstrap and it is fully responsive to different devices/resolutions. This app uses two API's:

 1. https://developer.here.com/
 2. https://developers.google.com/maps/

## Signup/Login

Signup is simple and straightforward. Using route /signup, you will be requested to input:
	
	1. Username
	2. Password (min 6 chars)
	3. Email
	4. Phone Number (optional)
	5. Profile Picture\Avatar (optional)

Only username and password are required for /login. 

## Home Page

The home page route, /, of Closest will show a home icon (to get to his page in the nav), as well as your profile picture, and the logout link. 

You can then search for mass transit near you using the geolocation button that uses the built in HTML method of gathering a devices location, or you can manually type in an address if you want to look at an area separate from your current location.

## Results

The results route, /results, will either provide you with an interactive Google Map and results table that allows search/sort/and filter objectives, or it will take you to a no results found splash page asking you to live closer to society. You can also add to your favorites here using the star icon at the top right! This will add this station/result to your favorites page. 

## Favorites

The favorites route will present a listing of all your favorites in a responsive card view with interactive Google Maps that will allow you to open directly into the Google Map App or Website. You can also search for content located on those cards. 

## Profile/Edit Profile Button

There is a simple profile listing showing all your profile details at /users/user_id/. This will have a button for editing your profile information, which will require you to input your password in order to confirm changes. 


