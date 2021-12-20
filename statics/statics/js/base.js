
function sidebar(){
    var headnav = document.getElementById("header")
    var headnavwidth = window.getComputedStyle(headnav)
    var main = document.getElementById("main")
    var menu_icon = document.getElementById("menu-icon")
    if ((headnavwidth.width == "0px" && headnav.style.width == "")||(headnav.style.width=='0px')){
        headnav.style.width = "200px"
        main.style.marginLeft = '200px'
        menu_icon.innerHTML= '&#10005;'
    }
    else{
        headnav.style.width = "0px"
        main.style.marginLeft = '0px'
        menu_icon.innerHTML = '&#9776;'
    }
}
function cont(text){
    var content = document.getElementsByClassName("content")
    content[0].innerText = text
    content[1].innerText = text
    content[2].innerText = text
    content[3].innerText = text
}