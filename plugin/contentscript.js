previousArticle = null;

chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
	if (msg.action == 'sourceRequest') {
		var rtn  = {'src': getSource(document), 'prevURL': previousArticle};
		sendResponse(rtn);
	}
});

window.onload = () => chrome.storage.local.get(window.location.href, (items) => {
		if (items[window.location.href]) {
			previousArticle = items[window.location.href];
			chrome.storage.local.remove(window.location.href);
		}
	});

function getSource(document) {
	return encodeURI(document.getElementsByTagName('html')[0].outerHTML);
}
