function submitLogin(){
    let userName = document.forms["login"].elements["username"].value;
    document.getElementById("results").innerHTML = "Welcome, " + userName + "!";
    console.log(userName);
}
