chrome.runtime.onMessage.addListener(function(msg, sender, callback) {
	if (msg.action == 'sourceRequest') {
		callback(getSource(document));		
	}
});

function getSource(document) {
	return document.getElementsByTagName('html')[0].outerHTML;
}
