function submitLogin(){
    let userName = document.forms["login"].elements["username"].value;
    if (userName === ""){
        document.getElementById("results").innerHTML = "Please enter your username.";
    } else {
        //temp code, not run
        window.location.href = "connections.html";
        document.getElementById("results").innerHTML = "Welcome, " + userName + "!";
        console.log(userName);
    }
    

}
