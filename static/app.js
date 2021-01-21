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