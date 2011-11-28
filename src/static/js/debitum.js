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

function login() {
    var username = $("#username").val();
    var password = $("#password").val();
    //TO-DO: store and encrypt passwords            
    $.post('http://127.0.0.1:8080/accounts/login/ajax/', $("#login_form").serialize(), function(data) {
        var obj = $.parseJSON(data);
        
        if (obj.status === true) {
            currentUser = username;
            $.mobile.changePage("#home_page");
        } 
        else if(obj.status === false){
            alert(obj.error);
        }else{
            alert('Unknown error.');
        }
    });

    return false;    
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
    if (valid_user == true)
        sendUserToServer();  
}

function validate_user(user) {
    if (user.fname == '' || user.lname == '' ||
            user.mail == '' || user.pw1 == '' || user.pw2 == '') {
        alert("Please fill in all fields.");
        return false;
    }

    if (validate_email(user.mail) == false) {
        alert("Invalid e-mail.");
        return false;
    }

    if (validate_password(user.pw1, user.pw2) == false) {
        alert("Passwords do not match.");
        return false;
    }

    return true;
}

function validate_email(email) {
    var atpos = email.indexOf("@");
    var dotpos = email.lastIndexOf(".");
    if (atpos < 1 || dotpos < atpos + 2 || dotpos+2 >= email.length)
        return false;
    else
        return true
}

function validate_password(pass1, pass2) {
    if (pass1 != pass2)
        return false;
    else
        return true;
}

function sendTransactionToServer(transactionForm) {
    $.post('http://127.0.0.1:8080/tracker/transactions/create/', $(transactionForm).serialize(), function(data) {
        alert("SUCCESS");
    });
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
    if (valid_data == true)
        sendTransactionToServer("#debtor");
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
    if (valid_data == true)
        sendTransactionToServer("#creditor");
}

function validate_data(data) {
    if (data.crdtr == '' || data.debtr == '' || data.amt == '' ||
            data.com == '' || data.ts == '') {
        alert("Please fill in all fields.");
        return false;
    }

    if (validate_amount(data.amt) == false) {
        alert("Invalid amount.");
        return false;
    } 

    return true;
}

function validate_amount(amount) {
    var floatAmount = parseFloat(amount);
    if (floatAmount > 0)
        return true;
    else
        return false;
}

function about() {
    alert("Debitum\nVersion: 0.4.2\n\nDebitum is a web application for all of your\ndebt-tracking needs.\n\n"+
            "Copyright " + unescape("%A9") + " 2011 Ryan Barril, Keunhong Park\n                     All rights reserved.");
}

function logout(){
    $.get('/accounts/logout/', function(data) {
        $.mobile.changePage("#login_page");
    });
}

function checkSession(){
    $.get('/accounts/profile/?format=json', function(data) {
        var obj = $.parseJSON(data);

        if(obj.status === true && $.mobile.activePage[0].id == "login_page"){
            currentUser = obj.email;
            $.mobile.changePage("#home_page");
        }else if(obj.status === false && ($.mobile.activePage[0].id != "login_page" && $.mobile.activePage[0].id != "registration_page")){
            $.mobile.changePage("#login_page");
        }
    });
}

$(document).ready(function(){
    checkSession();

    $('#login_form').submit(function(e){
        e.preventDefault();
        login();
    });
    $('#registration_form').submit(function(e){
        e.preventDefault();
        registerUser();
    });
    $('#debtor_form').submit(function(e){
        e.preventDefault();
        sendDebtorData();
    });
    $('#creditor_form').submit(function(e){
        e.preventDefault();
        sendCreditorData();
    });
    $('#logout_button').click(function(e){
        e.preventDefault();
        logout();
    });
});
