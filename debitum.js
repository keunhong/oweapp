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

         var first_name = $("#first_name").val();
         var last_name = $("last_name").val();
         var email = $("#email").val();
         var pass1 = $("#pass1").val();
         var pass2 = $("#pass2").val();
         
         if (first_name == "" || last_name == "" || email == "" || pass1 == "" || pass2 == "") {
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
         //TO-DO
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