document.querySelector('#enrollOptionButton').addEventListener('click', function () {

  console.log("The enroll button works!");
  window.location.href = '/enroll';
});

document.querySelector('#authOptionButton').addEventListener('click', function () {
  
  console.log("The auth button works!");
  window.location.href = '/auth';
});



// /* the last example replaces this one */

// function keyListener(event){ 
//   //whatever we want to do goes in this block
//   event = event || window.event; //capture the event, and ensure we have an event
//   var key = event.key || event.which || event.keyCode; //find the key that was pressed
//   //MDN is better at this: https://developer.mozilla.org/en-US/docs/DOM/event.which
//   if(key===84){ //this is for 'T'
//          window.location.href = '/enroll';
//   }
// }

// /* the last example replace this one */

// var el = window; //we identify the element we want to target a listener on
// //remember IE can't capture on the window before IE9 on keypress.

// var eventName = 'keypress'; //know which one you want, this page helps you figure that out: http://www.quirksmode.org/dom/events/keys.html
// //and here's another good reference page: http://unixpapa.com/js/key.html
// //because you are looking to capture for things that produce a character
// //you want the keypress event.

// //we are looking to bind for IE or non-IE, 
// //so we have to test if .addEventListener is supported, 
// //and if not, assume we are on IE. 
// //If neither exists, you're screwed, but we didn't cover that in the else case.
// if (el.addEventListener) {
//   el.addEventListener('click', keyListener, false); 
// } else if (el.attachEvent)  {
//   el.attachEvent('on'+eventName, keyListener);
// }

// //and at this point you're done with registering the function, happy monitoring

