function onWindowLoad() {
	  var message = document.getElementById('response');
	  	  
	  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
			chrome.tabs.sendMessage(tabs[0].id, {'action': 'sourceRequest'}, function(src) {
			sendAPIRequest(src, (res) => {message.innerText = JSON.parse(res).title;});

	});
});
}

function sendAPIRequest(src, callback) {
			var xhr = new XMLHttpRequest();
			xhr.open("POST", "https://q33wccsyz5.execute-api.eu-west-1.amazonaws.com/dev/extensionBackend", true);
			var msg='{"src": "' + encodeURI(src) + '"}';
			
			xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
			
			xhr.onreadystatechange = function() {
				if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
					callback(xhr.responseText);
				}
			};
			
			xhr.send(msg);
}

document.addEventListener('DOMContentLoaded', () => { onWindowLoad(); });


