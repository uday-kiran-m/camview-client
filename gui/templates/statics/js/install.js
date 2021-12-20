var formfilled = false
function first(){
    var ele = document.getElementsByClassName("installer")
    var back = document.getElementById("back")
    for(let i=0;i<ele.length;i++){
        ele[i].style.display = 'none'
    }
    back.style.display = 'none'
    
}

function nextbutton(){
    var ele = document.getElementsByClassName("installer")
    var back = document.getElementById("back")
    var next = document.getElementById("next")
    var submit = document.getElementById("submit")
    var intro = document.getElementById("intro")
    var abc = false
    for(let i=0;i<ele.length;i++){
        if (ele[i].style.display == 'block'){
            abc = true
            break
        }
    
    }
    console.log(abc)
    if (abc == false){
        ele[0].style.display = 'block'
        intro.style.display = 'none'
        back.style.display = 'inline'
    }
    else{
        for(let i=0;i<ele.length;i++){
            if (ele[i].style.display == 'block'){
                if (i+1<ele.length){
                    ele[i].style.display='none'
                    ele[i+1].style.display = 'block'
                    if(i+2 == ele.length){
                        next.style.display = 'none'
                        if (formfilled == true){
                            submit.style.display = 'inline'
                            submit.className = 'buttons'
                            submit.style.opacity = 1.0
                            submit.disabled = false
                        }
                        else{
                            submit.style.display = 'inline'
                            submit.className = 'buttonsd'
                            submit.style.opacity = 0.5
                            submit.disabled = true
                        }
                    }
                    break
                }
                break
            }
        }
    }
}
function backbutton(){
    var ele = document.getElementsByClassName("installer")
    var back = document.getElementById("back")
    var next = document.getElementById("next")
    var submit = document.getElementById("submit")
    var intro = document.getElementById("intro")
    for(let i=ele.length-1;i>-1;i--){
        if (i == 0){
            ele[0].style.display = 'none'
            intro.style.display = 'block'
            back.style.display='none'
        }
        if(ele[i].style.display == 'block'){
            if (i+1==ele.length){
                submit.style.display = 'none'
                next.style.display = 'inline'

            }
            if(i-1>-1){
                ele[i].style.display = 'none'
                ele[i-1].style.display = 'block'
                break
            }
        }
    }
}

function check(){
    var username = document.getElementById("username")
    var passwd = document.getElementById("passwd")
    var cpasswd = document.getElementById("cpasswd")
    var email = document.getElementById("email")
    var err = document.getElementById("error")
    console.log(username.value=='')
    if(username.value == ''){
        err.innerHTML = 'username cannot be empty'
        username.style.borderColor = 'red'
        formfilled = false
    }
    if(username.value != ''){
        username.style.borderColor = 'black'
    }
    if(passwd.value == null ){
        err.innerHTML = "Enter password"
        formfilled = false
    }
    if(email.value == null ){
        err.innerHTML = "Registered Email is mandatory"
        formfilled = false
    }
    if(passwd != null){
        if(passwd.value.length <8 || cpasswd.value.length < 8){
            // console.log(passwd.value)
            err.innerHTML = 'password should be atleast 8 characters'
        }
        else{
            if (passwd.value == cpasswd.value){
                if (username.value == ''){
                    err.innerHTML = 'username cannot be empty'
                }
                else{
                    err.innerHTML = ''
                    formfilled = true
                }
            }
            else{
                err.innerHTML = 'Passwords dont match'
            }
        
        }
    }
}

window.onload=first


