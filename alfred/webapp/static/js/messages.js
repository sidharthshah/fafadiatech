// form validation function //
function validate(form) {
  var name = form.customer_name.value;
  var company = form.company_name.value;
  var email = form.email.value;
  var message = form.location.value;
  var mobile = form.mobile.value;
  var landline = form.landline.value;
  var username = form.username.value;
  var password = form.password.value;
  var conf_password = form.conf_password.value;
  var nameRegex = /^[a-zA-Z]+(([\'\,\.\- ][a-zA-Z ])?[a-zA-Z]*)*$/;
  var companyRegex = /^[a-zA-Z]+(([\'\,\.\- ][a-zA-Z ])?[a-zA-Z]*)*$/;
  var emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
  var contactRegex = /^[0-9]+$/;
  var messageRegex = new RegExp(/<\/?\w+((\s+\w+(\s*=\s*(?:".*?"|'.*?'|[^'">\s]+))?)+\s*|\s*)\/?>/gim);
  if(name == "") {
    inlineMsg(form,'customer_name','You must enter your name.',2);
    return false;
  }
  if(!name.match(nameRegex)) {
    inlineMsg(form,'customer_name','You have entered an invalid name.',2);
    return false;
  }
  if(company == "") {
    inlineMsg(form,'company_name','You must enter your company name.',2);
    return false;
  }
  if(!company.match(companyRegex)) {
    inlineMsg(form,'company_name','You have entered an invalid company name.',2);
    return false;
  }
  if(email == "") {
    inlineMsg(form,'email','<strong>Error</strong><br />You must enter your email.',2);
    return false;
  }
  if(!email.match(emailRegex)) {
    inlineMsg(form,'email','<strong>Error</strong><br />You have entered an invalid email.',2);
    return false;
  }
  if(message == "") {
    inlineMsg(form,'location','You must enter a location.');
    return false;
  }
  if(message.match(messageRegex)) {
    inlineMsg(form,'location','You have entered an invalid location.');
    return false;
  }
  if(mobile == "") {
    inlineMsg(form,'mobile','<strong>Error</strong><br />You must enter your mobile no.',2);
    return false;
  }
  if(!mobile.match(contactRegex)) {
    inlineMsg(form,'mobile','<strong>Error</strong><br />You have entered an invalid mobile no.',2);
    return false;
  }
  if(company == "") {
    inlineMsg(form,'company_name','You must enter your company name.',2);
    return false;
  }
  if(!company.match(companyRegex)) {
    inlineMsg(form,'company_name','You have entered an invalid company name.',2);
    return false;
  }
  if(password != conf_password) {
    inlineMsg(form,'conf_password','Password dose not match.',2);
    return false;
  }
  return true;
}

// START OF MESSAGE SCRIPT //

var MSGTIMER = 20;
var MSGSPEED = 5;
var MSGOFFSET = 3;
var MSGHIDE = 3;

// build out the divs, set attributes and call the fade function //
function inlineMsg(form,target,string,autohide) {
  var msg;
  var msgcontent;
  if(!document.getElementById('msg')) {
    msg = document.createElement('div');
    msg.id = 'msg';
    msgcontent = document.createElement('div');
    msgcontent.id = 'msgcontent';
    form.appendChild(msg);
    msg.appendChild(msgcontent);
    msg.style.filter = 'alpha(opacity=100)';
    msg.style.opacity = 100;
    msg.alpha = 100;
  } else {
    msg = document.getElementById('msg');
    msgcontent = document.getElementById('msgcontent');
  }
  msgcontent.innerHTML = string;
  msg.style.display = 'block';
  var msgheight = msg.offsetHeight;
  var targetdiv = document.getElementById(target);
  targetdiv.focus();
  var targetheight = targetdiv.offsetHeight;
  var targetwidth = targetdiv.offsetWidth;
  var topposition = topPosition(targetdiv) - ((msgheight - targetheight) / 2);
  var leftposition = leftPosition(targetdiv) + targetwidth + MSGOFFSET;
  msg.style.top = topposition + 'px';
  msg.style.left = leftposition + 'px';
  clearInterval(msg.timer);
  msg.timer = setInterval("fadeMsg(1)", MSGTIMER);
  if(!autohide) {
    autohide = MSGHIDE;  
  }
  window.setTimeout("hideMsg()", (autohide * 1000));
}

// hide the form alert //
function hideMsg(msg) {
  var msg = document.getElementById('msg');
  if(!msg.timer) {
    msg.timer = setInterval("fadeMsg(0)", MSGTIMER);
  }
}

// face the message box //
function fadeMsg(flag) {
  if(flag == null) {
    flag = 1;
  }
  var msg = document.getElementById('msg');
  var value;
  if(flag == 1) {
    value = msg.alpha + MSGSPEED;
  } else {
    value = msg.alpha - MSGSPEED;
  }
  msg.alpha = value;
  msg.style.opacity = (value / 100);
  msg.style.filter = 'alpha(opacity=' + value + ')';
  if(value >= 99) {
    clearInterval(msg.timer);
    msg.timer = null;
  } else if(value <= 1) {
    msg.style.display = "none";
    clearInterval(msg.timer);
  }
}

// calculate the position of the element in relation to the left of the browser //
function leftPosition(target) {
  var left = 0;
  if(target.offsetParent) {
    while(1) {
      left += target.offsetLeft;
      if(!target.offsetParent) {
        break;
      }
      target = target.offsetParent;
    }
  } else if(target.x) {
    left += target.x;
  }
  return left;
}

// calculate the position of the element in relation to the top of the browser window //
function topPosition(target) {
  var top = 0;
  if(target.offsetParent) {
    while(1) {
      top += target.offsetTop;
      if(!target.offsetParent) {
        break;
      }
      target = target.offsetParent;
    }
  } else if(target.y) {
    top += target.y;
  }
  return top;
}

// preload the arrow //
if(document.img) {
  arrow = new Image(7,80); 
  arrow.src = "/static/img/msg_arrow.gif"; 
}

