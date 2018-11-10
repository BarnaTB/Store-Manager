function bars(bar) {
    bar.classList.toggle("change")
    var x = document.getElementById("my-top-nav")
    if (x.className === "topnav") {
        x.className += " responsive"
    } else {
        x.className = "topnav"
    }
}