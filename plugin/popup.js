const DEBUG = 1
const debug_base = "http://localhost:8080/"
const api_base = "http://ec2-34-240-199-221.eu-west-1.compute.amazonaws.com:8080/"

const debugBackendAPI = debug_base + 'get-views';
const productionBackendAPI = api_base + "extensionBackend";
const feedbackProcessingAPI = api_base + "feedback-processing";

const backendProcessingAPI = (DEBUG ? debug_base : api_base) + 'get-views';

const CACHE_TIMEOUT = 1000 * 60 * 60 * 24 * 7;

/*
 * Creates a list of items which represents a list of suggested
 * articles as a table
 * */
function createSuggestedArticleTable(suggestedArticles, currentArticleURL) {
    for (var i = 0; i < suggestedArticles.length; i++) {
        var suggestedArticle = suggestedArticles[i];

        // Take an element from the prototype and add the article-specific parameters to it
        var item = $(".list-element-row:first").clone()

        item.find(".list-element-image img").attr("src", suggestedArticle.imageLink);
        item.find(".list-element-title").text(suggestedArticle.title);
        item.find(".list-element-summary").text(suggestedArticle.summary);

        item.find(".list-element-table tr").click({
            link: suggestedArticle.link,
            previousLink: currentArticleURL
        }, (ev) => {
            var key = ev.data.link + 'prevURL'
            var keyval = {};
            keyval[key] = ev.data.previousLink;
            chrome.storage.local.set(keyval, () => {
                chrome.tabs.create({ url: ev.data.link });
            });
        });

        item.find(".list-element-table tr:last").off();

        item.find(".thumbs-up").click({
            link: suggestedArticle.link,
            fromLink: currentArticleURL,
            thumbsElem: item.find(".feedback-thumbs")
        }, (ev) => {
            sendFeedback("positive", ev.data.fromLink, ev.data.link, ev.data.thumbsElem);
        });

        item.find(".thumbs-down").click({
            link: suggestedArticle.link,
            fromLink: currentArticleURL,
            thumbsElem: item.find(".feedback-thumbs")
        }, (ev) => {
            sendFeedback("negative", ev.data.fromLink, ev.data.link, ev.data.thumbsElem);
        });

        $("#suggested-article-list").append(item);
    }

    // Now remove the prototype as we don't need it
    $(".list-element-row:first").remove();
    $('.display-suggested-articles').show();
    $('#suggested-article-loading-status').hide();
}


function sendFeedback(feedback, fromLink, suggestedArticleLink, thumbsElem) {
    const requestData = {
        "from": fromLink,
        "to": suggestedArticleLink,
        "feedback": feedback
    };

    $.post(feedbackProcessingAPI, requestData)
    .done((res) => {
            alert(JSON.parse(res).message);
            thumbsElem.hide();
    }).fail((jqXHR, textStatus, errorThrown) => {
            $("#suggested-article-loading-status").text(`Failed to submit feedback: ${textStatus}`);
    });
}


function onExtensionWindowLoad() {
    $(".display-suggested-articles").hide();

    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        const currentTab = tabs[0];
        const currentURL = currentTab.url;
        
        handleCurrentPageFeedbackButtons(currentTab, currentURL);

        var cachedDataKey = currentURL + 'cache';
        console.log('Looking for item in cache');
        chrome.storage.local.get(cachedDataKey,
            (items) => {
                if (items[cachedDataKey] && items[cachedDataKey].timeout > (new Date()).getTime()) {
                    console.log('Cache hit');
                    createSuggestedArticleTable(
                        items[cachedDataKey].res, 
                        currentURL
                    );
                }
                else {
                    if (items[cachedDataKey])
                        console.log('Cache hit, but timeout');
                    else
                        console.log('Cache miss');
                    getSuggestedArticleList(currentURL, cachedDataKey);
                }
            }
        );
    });

}

function handleCurrentPageFeedbackButtons(currentTab, currentURL) {
    $('#feedback-request').hide();

    chrome.tabs.sendMessage(currentTab.id, {
        'action': 'previousURLRequest'
    }, function(rtn) {
        if (rtn && rtn.prevURL) {
            console.log("Found previous URL, showing feedback thumbs...");

            $("#feedback-request").show();

            $("#feedback-request .thumbs-up").click({
                toLink: currentURL,
                fromLink: rtn.prevURL,
                thumbsElem: $("#feedback-request")
            }, (ev) => {
                sendFeedback("positive", ev.data.fromLink, ev.data.toLink, ev.data.thumbsElem);
            });

            $("#feedback-request .thumbs-down").click({
                toLink: currentURL,
                fromLink: rtn.prevURL,
                thumbsElem: $("#feedback-request")
            }, (ev) => {
                sendFeedback("negative", ev.data.fromLink, ev.data.toLink, ev.data.thumbsElem);
            });

        }
        else if (!rtn) {
            console.log("Did you load the extension before the webpage?");
        }
        else {
            console.log("Could not find previous URL");
        }
    });
}

function getSuggestedArticleList(currentURL, cachedDataKey) {
        const requestData = {
            'link': currentURL
        };
        console.log("using url " + currentURL);
        $.post(backendProcessingAPI, requestData)
        .done((res) => {

            res = JSON.parse(res);

            console.log('Storing result to cache');
            
            cachedResult = {'res' : res , 'timeout' : ((new Date()).getTime() + CACHE_TIMEOUT)};
            var keyval = {};
            keyval[cachedDataKey] = cachedResult;
            chrome.storage.local.set(keyval);

            createSuggestedArticleTable(res, currentURL);
        })
        .fail((jqXHR, textStatus, errorThrown) => {
            $("#suggested-article-loading-status").text(`Failed to find suggested articles: ${textStatus}`);
        });
}


document.addEventListener('DOMContentLoaded', () => {
    onExtensionWindowLoad();
});
