//recipe_dash js

function parseURL() {
  console.log("Button clicked")
  var url =  document.getElementById('recipeURLtext').value
  var newurl = "localhost:5000/fetch/" + url;
  console.log("NEW URL:", newurl)
	location.href=newurl
}
