previousArticle = null;

chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
	if (msg.action == 'previousURLRequest') {
		var rtn  = {'prevURL': previousArticle};
		sendResponse(rtn);
	}
});


var prevURLKey = window.location.href + 'prevURL';
chrome.storage.local.get(prevURLKey, (items) => {
    if (items[prevURLKey]) {
        previousArticle = items[prevURLKey];
        chrome.storage.local.remove(prevURLKey);
	}
});



