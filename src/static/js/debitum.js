var currentUser;

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        var host = document.location.host;
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

function newServerRequest() {
    var serverRequest;
    if (window.XMLHttpRequest)
        serverRequest = new XMLHttpRequest();
    else
        serverRequest = new ActiveXObject("Microsoft.XMLHTTP");

    return serverRequest;
}

function login() {
    var username = $("#username").val();
    var password = $("#password").val();
    //TO-DO: store and encrypt passwords            
    $.post('http://127.0.0.1:8080/accounts/login/ajax/', $("#login_form").serialize(), function(data) {
        //TO-DO: parse return string or have page return json/array
        //document.getElementById("username").value = "";
        //document.getElementById("password").value = "";
        currentUser = username;
        $.mobile.changePage("#home_page");
    });
    
    
    if (username == "Ryan" && password == "illini") {
        document.getElementById("username").value = "";
        document.getElementById("password").value = "";
        currentUser = username;
        $.mobile.changePage("#home_page");
    }
    else
        alert("Wrong username/password combination.");
    
}

function sendUserToServer() {
    $.post('http://127.0.0.1:8080/accounts/register/', $("#registration_form").serialize(), function(data) {
        $("#stuff").html(data);
    });
}

function registerUser() {
    var first_name = $("#first_name").val();
    var last_name = $("#last_name").val();
    var email = $("#email").val();
    var pass1 = $("#pass1").val();
    var pass2 = $("#pass2").val();

    var userTuple = {
        fname : first_name,
        lname : last_name,
        mail  : email,
        pw1   : pass1,
        pw2   : pass2
    };     

    var valid_user = validate_user(userTuple);
    if (valid_user == "true")
        sendUserToServer(userTuple);  
}

function validate_user(user) {
    if (user.fname == '' || user.lname == '' ||
            user.mail == '' || user.pw1 == '' || user.pw2 == '') {
        alert("Please fill in all fields.");
        return "false";
    }

    if (validate_email(user.mail) == "false") {
        alert("Invalid e-mail.");
        return "false";
    }

    if (validate_password(user.pw1, user.pw2) == "false") {
        alert("Passwords do not match.");
        return "false";
    }

    return "true";
}

function validate_email(email) {
    var atpos = email.indexOf("@");
    var dotpos = email.lastIndexOf(".");
    if (atpos < 1 || dotpos < atpos + 2 || dotpos+2 >= email.length)
        return "false";
    else
        return "true"
}

function validate_password(pass1, pass2) {
    if (pass1 != pass2)
        return "false";
    else
        return "true";
}

function sendTransactionToServer(transactionTuple) {
    var rqst = newServerRequest();
    var title = "Default Title";
    var amount = transactionTuple.amt;
    var email = "default@illinois.edu";
    var type = "D";

    var dataJSON = {'title' : 'Default Title', 'description' : 'Default Description', 'recipient_email' : 'default@illinois.edu', 'transaction_type' : 'D', 'amount' : amount};
    alert("Request sent.");
    $.post('http://127.0.0.1:8080/tracker/transactions/create/', dataJSON, function(data) {
            alert("SUCCESS");}, "json");
}

function sendDebtorData() {         
    var creditor = currentUser;
    var debtor = $("#debtor").val();
    var amount = $("#debtorAmount").val();
    var comment = $("#comment1").val();
    var date = new Date().toDateString();

    var transactionTuple = {
        crdtr : creditor,
        debtr : debtor,
        amt   : amount,
        com   : comment,
        ts    : date
    };

    var valid_data = validate_data(transactionTuple);
    if (valid_data == "true")
        sendTransactionToServer(transactionTuple);
}

function sendCreditorData() {   
    var creditor = $("#creditor").val();
    var debtor = currentUser;
    var amount = $("#iOweAmount").val();
    var comment = $("#comment2").val();
    var date = new Date().toDateString();

    var transactionTuple = {
        crdtr : creditor,
        debtr : debtor,
        amt   : amount,
        com   : comment,
        ts    : date
    };

    var valid_data = validate_data(transactionTuple);
    if (valid_data == "true")
        sendTransactionToServer(transactionTuple);
}

function validate_data(data) {
    if (data.crdtr == '' || data.debtr == '' || data.amt == '' ||
            data.com == '' || data.ts == '') {
        alert("Please fill in all fields.");
        return "false";
    }

    if (validate_amount(data.amt) == "false") {
        alert("Invalid amount.");
        return "false";
    } 

    return "true";
}

function validate_amount(amount) {
    var floatAmount = parseFloat(amount);
    if (floatAmount > 0)
        return "true";
    else
        return "false";
}

function about() {
    alert("Debitum\nVersion: 0.4.2\n\nDebitum is a web application for all of your\ndebt-tracking needs.\n\n"+
            "Copyright " + unescape("%A9") + " 2011 Ryan Barril, Keunhong Park\n                     All rights reserved.");
}

$(document).ready(function(){
    $('#login_form').submit(function(e){
        e.preventDefault();
        login();
    });
});

$(document).ready(function(){
    $('#registration_form').submit(function(e){
        e.preventDefault();
        registerUser();
    });
});

$(document).ready(function(){
    $('#debtor_form').submit(function(e){
        e.preventDefault();
        sendDebtorData();
    });
});

$(document).ready(function(){
    $('#creditor_form').submit(function(e){
        e.preventDefault();
        sendCreditorData();
    });
});