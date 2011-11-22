var currentUser;

function newServerRequest() {
    var serverRequest;
    if (window.XMLHttpRequest)
        serverRequest = new XMLHttpRequest();
    else
        serverRequest = new ActiveXObject("Microsoft.XMLHTTP");

    return serverRequest;
}

function login() {
    //TO-DO: store and encrypt passwords
    var username = $("#username").val();
    var password = $("#password").val();
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
    rqst = newServerRequest();         
    //TO-DO
}
function registerUser() {
    var rqst = newServerRequest();

    var user = $("#user").val();
    var first_name = $("#first_name").val();
    var last_name = $("last_name").val();
    var email = $("#email").val();
    var pass1 = $("#pass1").val();
    var pass2 = $("#pass2").val();

    if (user == "" || first_name == "" || last_name == "" || email == "" || pass1 == "" || pass2 == "") {
        alert("Please fill in all fields.");
        return;
    }

    if (validate_email(email) == "false") {
        alert("Invalid e-mail.");
        return;
    }

    if (validate_password(pass1, pass2) == "false") {
        alert("Passwords do not match.");
        return;
    }

    var userTuple = {
        "first_name" : first_name,
        "last_name"  : last_name,
        "email"      : email,
        "password"   : pass1
    };     

    sendUserToServer(userTuple);  
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
    if (pass1 == pass2)
        return "true";
    else
        return "false";
}

function sendTransactionToServer(transactionTuple) {
    var rqst = newServerRequest();
    var title = "Default Title";
    var amount = transactionTuple['amount'];
    var email = "default@illinois.edu";
    var type = "D";


    var dataJSON = {'title' : 'Default Title', 'description' : 'Default Description', 'recipient_email' : 'default@illinois.edu', 'transaction_type' : 'D', 'amount' : amount};
    alert("MSG: Request sent.");
    $.post('http://127.0.0.1:8080/tracker/transactions/?format=json', {}, function(data) {
            alert("SUCCESS");}, "json");

}

function sendDebtorData() {         
    var creditor = currentUser;
    var debtor = $("#debtor").val();
    var amount = $("#debtorAmount").val();
    var comment = $("#comment1").val();
    var date = new Date().toDateString();

    if (validate_amount(amount) == "false") {
        alert("Invalid amount.");
        return;
    }

    var transactionTuple = {
        "creditor" : creditor,
        "debtor"   : debtor,
        "amount"   : amount,
        "comment"  : comment,
        "priority" : "Default",
        "date"     : date
    };

    sendTransactionToServer(transactionTuple);
}

function sendCreditorData() {         
    var creditor = $("#creditor").val();
    var debtor = currentUser;
    var amount = $("#iOweAmount").val();
    var comment = $("#comment2").val();
    var date = new Date().toDateString();

    if (validate_amount(amount) == "false") {
        alert("Invalid amount.");
        return;
    }

    var transactionTuple = {
        "creditor" : creditor,
        "debtor"   : debtor,
        "amount"   : amount,
        "comment"  : comment,
        "priority" : "Default",
        "date"     : date
    };

    sendTransactionToServer(transactionTuple);
}

function validate_amount(amount) {
    var floatAmount = parseFloat(amount);
    if (floatAmount > 0)
        return "true";
    else
        return "false";
}

function about() {
    alert("Debitum\nVersion: 0.4\n\nDebitum is a web application for all of your\ndebt-tracking needs.\n\n"+
            "Copyright " + unescape("%A9") + " 2011 Ryan Barril, Keunhong Park\n                     All rights reserved.");
}


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
