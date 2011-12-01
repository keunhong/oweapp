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
    
    if (username == "" || password == "") {
        alert("Please fill in both fields.");
        return;
    }
    //TO-DO: store and encrypt passwords            
    $.post('http://127.0.0.1:8080/accounts/login/ajax/', $("#login_form").serialize(), function(data) {
        var obj = $.parseJSON(data);
        
        if (obj.status === true) {
            currentUser = username;
            $("h1.displayUser").html("Debitum v0.5 (" + currentUser + ")");
            $.mobile.changePage("#home_page");
        } 
        else if(obj.status === false){
            alert(obj.error);
        }else{
            alert('Unknown error.');
        }
    });

    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
}

function sendUserToServer() {
    $.post('http://127.0.0.1:8080/accounts/register/ajax/', $("#registration_form").serialize(), function(data) {
        var obj = $.parseJSON(data);
        
        if (obj.status == true)
            alert("Thank you for registering to Debitum! Please check your e-mail to activate your account.");
        else {
            var errors = "";
            for (var i = 0; i < obj.fields.length; i++) {
                if (obj.fields[i].errors != "")
                    errors += obj.fields[i].errors;
            }
            alert(obj.error + "(s): " + errors);
        }
    });
    
    document.getElementById("first_name").value = "";
    document.getElementById("last_name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("password1").value = "";
    document.getElementById("password2").value = "";
}

function registerUser() {
    var userTuple = {
        fname : $("#first_name").val(),
        lname : $("#last_name").val(),
        mail  : $("#email").val(),
        pw1   : $("#password1").val(),
        pw2   : $("#password2").val()
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
        return true;
}

function validate_password(pass1, pass2) {
    if (pass1 != pass2)
        return false;
    else
        return true;
}

function sendTransactionToServer(transactionForm) {
    
    var type = '';
    var amt = '';
    var email = '';
    var comment = '';
    var label = '';
    
    if (transactionForm == "#creditor") {
        type = 'P';
        amt = $("#creditorAmount").val();
        email = $("#creditor").val();
        comment = $("#creditorComment").val();
        label = $("#creditorLabel").val();
    }
    else if (transactionForm == "#debtor") {
        type = 'D';
        amt = $("#debtorAmount").val();
        email = $("#debtor").val();
        comment = $("#debtorComment").val();
        label = $("#debtorLabel").val();
    }
    
    var transactionObject = {transaction_type : type, amount : amt, recipient_email : email, description : comment, title : label}
    
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:8080/tracker/transactions/create/',
        data: transactionObject,
        success: function(data) {
            if (data.status == true && type == 'P')
                $.mobile.changePage("#creditor_page");
            else if (data.status == true && type == 'D')
                $.mobile.changePage("#debtor_page");
            else
                alert("Unknown error.");
        }
    });
    
    document.getElementById("debtorLabel").value = "";
    document.getElementById("debtor").value = "";
    document.getElementById("debtorAmount").value = "";
    document.getElementById("debtorComment").value = "";
    
    document.getElementById("creditorLabel").value = "";
    document.getElementById("creditor").value = "";
    document.getElementById("creditorAmount").value = "";
    document.getElementById("creditorComment").value = "";
}

function sendDebtorData() {         
    var transactionTuple = {
        title : $("#debtorLabel").val(),
        crdtr : currentUser,
        debtr : $("#debtor").val(),
        amt   : $("#debtorAmount").val(),
        com   : $("#debtorComment").val(),
        ts    : new Date().toDateString()
    };

    var valid_data = validate_data(transactionTuple);
    if (valid_data == true)
        sendTransactionToServer("#debtor");
}

function sendCreditorData() {   
    var transactionTuple = {
        title : $("#creditorLael").val(),
        crdtr : $("#creditor").val(),
        debtr : currentUser,
        amt   : $("#creditorAmount").val(),
        com   : $("#creditorComment").val(),
        ts    : new Date().toDateString()
    };
    
    var valid_data = validate_data(transactionTuple);
    if (valid_data == true)
        sendTransactionToServer("#creditor");
}

function validate_data(data) {
    if (data.crdtr == '' || data.debtr == '' || data.amt == '' ||
            data.com == '' || data.ts == '' || data.title == '') {
        alert("Please fill in all fields.");
        return false;
    }

    if (data.crdtr == data.debtr) {
        alert("You can't owe yourself!");
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
    alert("Debitum\nVersion: 0.5\n\nDebitum is a web application for all of your\ndebt-tracking needs.\n\n"+
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

        if (obj.status === true) {
            currentUser = obj.email;
            $("h1.displayUser").html("Debitum v0.5 (" + currentUser + ")");
            if ($.mobile.activePage[0].id != "home_page")
                $.mobile.changePage("#home_page");
        }
        else if (obj.status === false && ($.mobile.activePage[0].id != "login_page" && $.mobile.activePage[0].id != "registration_page")) {
            $.mobile.changePage("#login_page");
        }
    });
}

function displayTransactionData() {    
    $.get('/tracker/transactions/?format=json', function(data) {
        for (var i = 0; i < data.length; i++) {
            var person = data[i];
            var transactionList = person.transactions;
            if (person.first_name != "" && person.last_name != "")
                for (var j = 0; j < transactionList.length; j++) {
                    var transaction = transactionList[j];
                    if (transaction.amount > 0)
                        displayDebtor(person, transaction);
                    else if (transaction.amount < 0)
                        displayCreditor(person, transaction);
                }
        }
    });
}

function displayDebtor(person, transaction) {
    $('#debtorAccordion').append('<div data-role="collapsible" data-collapsed="true">' +
                                    '<h1>' + person.first_name + ' ' + person.last_name + '</h1>' +
                                    '<div>Amount Owed: $' + transaction.amount + '<br />' +
                                    'Date Added: ' + transaction.date + '<br />' +
                                    'Comment: ' + transaction.description + '</div>' +
                                    '</div>');
}

function displayCreditor(person, transaction) {
    $('#creditorAccordion').append('<div data-role="collapsible" data-collapsed="true">' +
                                    '<h1>' + person.first_name + ' ' + person.last_name + '</h1>' +
                                    '<div>Amount Owed: $' + transaction.amount + '<br />' +
                                    'Date Added: ' + transaction.date + '<br />' +
                                    'Comment: ' + transaction.description + '</div>' +
                                    '</div>');}

$(document).ready(function(){
    checkSession();
    
    displayTransactionData();
    
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
