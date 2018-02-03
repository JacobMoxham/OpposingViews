const api_base = "https://q33wccsyz5.execute-api.eu-west-1.amazonaws.com/dev/"

const backendProcessingAPI = api_base + "extensionBackend";
const feedbackProcessingAPI = api_base + "feedback-processing";

function sendFeedback(feedback, suggestedArticleLink) {
     chrome.tabs.query({active: true, lastFocusedWindow: true},
       function(tabs) {
         data = '{"from": "' + tabs[0].url + '", "to": "' + suggestedArticleLink + '", "feedback": "' + feedback + '"}';

         sendAPIRequest(data, 
           feedbackProcessingAPI, 
           (res) => {alert(JSON.parse(res).message);}); 
       });
}

function onWindowLoad() {
  var message = document.getElementById('container');
  
    
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id,
      {'action': 'sourceRequest'},
      function(src) {
        data = '{"src": "' + encodeURI(src) + '"}';
        sendAPIRequest(data, backendProcessingAPI, (res) => {message.appendChild(createSuggestedArticleTable(JSON.parse(res)));});

	  });
    });
 }

function sendAPIRequest(data, api, callback) {
			var xhr = new XMLHttpRequest();
			xhr.open("POST", api, true);
			var msg=data;
			
			xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
			
			xhr.onreadystatechange = function() {
				if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
					callback(xhr.responseText);
				}
			};
			
			xhr.send(msg);
}

document.addEventListener('DOMContentLoaded', () => { onWindowLoad(); });


