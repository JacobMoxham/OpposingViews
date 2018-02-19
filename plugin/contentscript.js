previousArticle = null;

chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
	if (msg.action == 'sourceRequest') {
		var rtn  = {'prevURL': previousArticle};
		sendResponse(rtn);
	}
});

window.onload = function () {
    var prevURLKey = window.location.href + 'prevURL';
    chrome.storage.local.get(prevURLKey,
        (items) => {
		if (items[prevURLKey]) {
			previousArticle = items[prevURLKey];
			chrome.storage.local.remove(prevURLKey);
		}
	});
    
};

function getSuggestedArticleList() {
    var url = window.location;

    const requestData = {'link' : url};


}

