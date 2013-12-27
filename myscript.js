// Create cross-origin XMLHttpRequest to send data to the PSQL database
var xhr = new XMLHttpRequest();
xhr.open("POST","http://browsing-history-visualizer.heroku.com/api",true);

// Use background page console
var bkg = chrome.extension.getBackgroundPage();

// Keep track of the current page URL
var current = ''
// Keep track of time on current page
var n = new Date().getTime();

// Use onUpdated to check for an active tab navigation change
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if(tab.active){
    	var url = changeInfo.url;
    	if(url != undefined){
    		newTime = new Date().getTime();
    		bkg.console.log(current + " (" + (newTime - n) + ")\n" + url);
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
    		xhr.send("site1=" + current + "&time=" + (newTime-n) + "&site2=" + url);
    		n = newTime;
    		current = url;
		}
	});
});