function login(){
    let email = $('#emailLogin').val();
    let password = $('#password').val();

    if (email === ""){
        alert("Email can not be empty");
    }else if(password === ""){
        alert("Password can not be empty");
    }else{
        window.location.href = "../../project/index.html";
    }
}

function signup(){
    let email = $('#emailSignup').val();
    let firstName = $('#firstName').val();
    let surname = $('#surname').val();
    let password = $('#passwordSignup').val();
    let passwordConfirm = $('#passwordConfirm').val();

    if (email === ""){
        alert("Email can not be empty");
    }else if(firstName === ""){
        alert("First name can not be empty");
    }else if(surname === ""){
        alert("Surname can not be empty");
    }else if(password < 8){
        alert("Password can not be less than 8 characters long");
    }else if(password !== passwordConfirm){
        alert("Passwords do not match");
    }else{
        alert("You have signed up! Now Login!");
    }
}

$(document).ready(function () {

    $("#openSignup").on("click", function () {
        $("#loginForm").fadeOut('fast', function () {
            $('#signupForm').fadeIn();
        });

    });

    $('#openLogin').on('click', function () {
       $('#signupForm').fadeOut('fast', function () {
          $('#loginForm').fadeIn();
       });
    });

    $('#loginButton').on('click', function () {
        login();
    });

    $('#signupButton').on('click', function () {
       signup();
    });
});