
// Adapted from https://www.w3schools.com/howto/howto_css_modals.asp

// Get the modal
var levenshtein = document.getElementById("levenshtein");

// Get the <span> element that closes the modal
var closeSpan = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
function showLevenshtein() {
    document.getElementById("levenshtein").style.display = "block";
}

// When the user clicks on <span> (x), close the modal
closeSpan.onclick = function () {
    levenshtein.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == levenshtein) {
        levenshtein.style.display = "none";
    }
}