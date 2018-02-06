const api_base = "https://q33wccsyz5.execute-api.eu-west-1.amazonaws.com/dev/"

const backendProcessingAPI = api_base + "extensionBackend";
const feedbackProcessingAPI = api_base + "feedback-processing";

/*
 * Creates a list of items which represents a list of suggested
 * articles as a table
 * */
function createSuggestedArticleTable(suggestedArticles, currentArticleURL) {
  
  for (var i = 0; i < suggestedArticles.length; i++) {
	var suggestedArticle = suggestedArticles[i]; 
	
	/*Take an element from the prototype and add the article-specific parameters to it*/
	var item = $(".list-element-row:first").clone()
	
	item.find(".list-element-image img").attr("src", suggestedArticle.imageLink);
	item.find(".list-element-title").text(suggestedArticle.title);
	item.find(".list-element-summary").text(suggestedArticle.summary);
	
	item.find(".list-element-table tr").click({link:suggestedArticle.link, previousLink: currentArticleURL}, 
		(ev) => {
			var keyval = {};
			keyval[ev.data.link] = ev.data.previousLink;
			chrome.storage.local.set(keyval, () => {chrome.tabs.create({url:ev.data.link});});
		});
			
	item.find(".list-element-table tr:last").off();
	
	item.find(".thumbs-up").click({link:suggestedArticle.link, fromLink: currentArticleURL, thumbsElem: item.find(".feedback-thumbs")}, (ev) => {sendFeedback("positive", ev.data.fromLink, ev.data.link, ev.data.thumbsElem);});
	item.find(".thumbs-down").click({link:suggestedArticle.link, fromLink: currentArticleURL, thumbsElem: item.find(".feedback-thumbs")}, (ev) => {sendFeedback("negative", ev.data.fromLink, ev.data.link, ev.data.thumbsElem);});

	$("#suggested-article-list").append(item);
  }
   
   /*Now remove the prototype as we don't need it*/
    $(".list-element-row:first").remove();
    
}


function sendFeedback(feedback, fromLink, suggestedArticleLink, thumbsElem) {
     chrome.tabs.query({active: true, lastFocusedWindow: true},
       function(tabs) {
         data = '{"from": "' + fromLink + '", "to": "' + suggestedArticleLink + '", "feedback": "' + feedback + '"}';

         sendAPIRequest(data, 
           feedbackProcessingAPI, 
           (res) => {alert(JSON.parse(res).message); thumbsElem.hide();}); 
       });
}

function onWindowLoad() {
  var message = document.getElementById('container');
  $("#suggested-article-list").hide();
  $("#feedback-request").hide();
    
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id,
      {'action': 'sourceRequest', 'currURL': tabs[0].url},
      function(rtn) {
        data = '{"src": "' + rtn.src + '", "link": "' + tabs[0].url + '"}';
        
        if (rtn.prevURL) {
			$("#feedback-request .thumbs-up").click({toLink:tabs[0].url, fromLink: rtn.prevURL, thumbsElem: $("#feedback-request")}, (ev) => {sendFeedback("positive", ev.data.fromLink, ev.data.toLink, ev.data.thumbsElem);});
			$("#feedback-request .thumbs-down").click({toLink:tabs[0].url, fromLink: rtn.prevURL, thumbsElem: $("#feedback-request")}, (ev) => {sendFeedback("negative", ev.data.fromLink, ev.data.toLink, ev.data.thumbsElem);});
			$("#feedback-request").show();
		}
        
        sendAPIRequest(data, backendProcessingAPI, (res) => {
			createSuggestedArticleTable(JSON.parse(res), tabs[0].url);
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


