// If user is a new user, generate a new userID for them from the server using AJAX
// and input userID into local storage

//TODO: Modify to get user 
// Set redirect when click on browser action
chrome.browserAction.onClicked.addListener(function(activeTab){
  var newURL = "http://browsing-history-visualizer.herokuapp.com";
  chrome.tabs.create({ url: newURL });
});

// Use background page console for debugging
var bkg = chrome.extension.getBackgroundPage();

// Keep track of the current page URL
var current = ''
var xhr = new XMLHttpRequest();

// Keep track of time on current pjsonage
var n = new Date().getTime();

// URL to send post request
var postURL = "http://browsing-history-visualizer.herokuapp.com/api"
// For local development
//var postURL = "http://0.0.0.0:5000/api"
//postURL = "http://127.0.0.1:5000/api"


// Use onUpdated to check for an active tab navigation change
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if(tab.active){
    	var url = changeInfo.url;
    	if(url != undefined){
    		newTime = new Date().getTime();
    		bkg.console.log(current + " (" + (newTime - n) + ")\n" + url);
			// Create cross-origin XMLHttpRequest to send data to the PSQL database
			xhr.open("POST",postURL,true);
			xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    		xhr.send("site1=" + current + "&time=" + (newTime-n) + "&site2=" + url);    		
			
			n = newTime;
    		current = url;
    	}
    }
});

// Keep this method in case I want to check open, inactive tabs
/*
chrome.tabs.onCreated.addListener(function(tabId, changeInfo, tab) {         
   bkg.console.log("Created: " + changeInfo.url)
});
*/

// Use onActivated to check for navigating to a new tabrefer to use onactivated -- as it only logs the urls when the 
// particular tab is opened and activated
chrome.tabs.onActivated.addListener(function(activeInfo) {
	chrome.tabs.query({'active': true, 'currentWindow': true}, function(tabs) {
		var url = tabs[0].url;

		// Do not log on initial tab activation
		if(current.valueOf() == ''){
			current = url;
		} else {
    		newTime = new Date().getTime();
    		bkg.console.log(current + " (" + (newTime - n) + ")\n" + url);
    		// Create cross-origin XMLHttpRequest to send data to the PSQL database
			xhr.open("POST",postURL,true);
			xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    		xhr.send("site1=" + current + "&time=" + (newTime-n) + "&site2=" + url);

    		n = newTime;
    		current = url;
		}
	});
});