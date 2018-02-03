const api_base = "https://q33wccsyz5.execute-api.eu-west-1.amazonaws.com/dev/"

const backendProcessingAPI = api_base + "extensionBackend";
const feedbackProcessingAPI = api_base + "feedback-processing";

function getLink(suggestedArticles, i) {
	return suggestedArticles[i].link;
}

/*
 * Creates a list of items which represents a list of suggested
 * articles as a table
 * */
function createSuggestedArticleTable(suggestedArticles) {
  
  for (var i = 0; i < suggestedArticles.length; i++) {
	var suggestedArticle = suggestedArticles[i];
	
	console.log(suggestedArticle.link);
	console.log(suggestedArticle.title);  
	
	var item = $(".list-element-row:first").clone()
	
	item.find(".list-element-image img").attr("src", suggestedArticle.imageLink);
	item.find(".list-element-title").text(suggestedArticle.title);
	item.find(".list-element-summary").text(suggestedArticle.summary);
	
	item.find(".list-element-table tr").click({link:suggestedArticle.link}, (ev) => {chrome.tabs.create({url:ev.data.link});});
	item.find(".list-element-table tr:last").off();
	
	item.find(".thumbs-up").click({link:suggestedArticle.link}, (ev) => {sendFeedback("positive", ev.data.link);});
	item.find(".thumbs-down").click({link:suggestedArticle.link}, (ev) => {sendFeedback("negative", ev.data.link);});

	$("#suggested-article-list").append(item);
  }
   
    $(".list-element-row:first").remove();
    
}


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
  $("#suggested-article-list").hide();
  
    
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id,
      {'action': 'sourceRequest'},
      function(src) {
        data = '{"src": "' + encodeURI(src) + '", "link": "' + tabs[0].url + '"}';
        sendAPIRequest(data, backendProcessingAPI, (res) => {
			createSuggestedArticleTable(JSON.parse(res));
			$("#suggested-article-list").show();
		});

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


