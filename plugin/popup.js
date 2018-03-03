const DEBUG = config.IS_DEBUG
const api_base = DEBUG ? config.DEBUG_URL_BASE : config.PROD_URL_BASE;

const feedbackProcessingAPI = api_base + config.FEEDBACK_URL_SLUG;
const backendProcessingAPI = api_base + config.ARTICLE_SUGGESTION_SLUG;

const CACHE_TIMEOUT = config.CACHE_TIMEOUT;
const CACHING_ENABLED = config.DISABLE_CACHING !== true;

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
            sendFeedback('click', ev.data.previousLink, ev.data.link);
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
        "fromSite": fromLink,
        "toSite": suggestedArticleLink,
        "feedback": feedback
    };

    console.log(requestData);
    $.post(feedbackProcessingAPI, requestData)
    .done((res) => {
            console.log(JSON.parse(res).message);
            if (thumbsElem)
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
        const cachedDataKey = currentURL + 'cache';

        handleCurrentPageFeedbackButtons(currentTab, currentURL);

        if (CACHING_ENABLED) {
            console.log('Looking for item in cache');
            chrome.storage.local.get(cachedDataKey,
                (items) => {
                    const cachedItem = items[cachedDataKey];

                    if (cachedItem
                        && cachedItem.timeout > (new Date()).getTime()
                        && cachedItem.res.length > 0) {
                        console.log('Cache hit');
                        createSuggestedArticleTable(
                            cachedItem.res,
                            currentURL
                        );
                    }
                    else {
                        if (cachedItem)
                            console.log('Item in cache, but not used');
                        else
                            console.log('Cache miss');
                        getSuggestedArticleList(currentURL, cachedDataKey);
                    }
                }
            );
        } else {
            console.log('Not looking for item in cache: caching disabled');
            getSuggestedArticleList(currentURL, cachedDataKey);
        }
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

            if (res.length > 0) {
                console.log('Storing result to cache');
            
                cachedResult = {
                    'res' : res , 
                    'timeout' : ((new Date()).getTime() + CACHE_TIMEOUT)
                };
            
                var keyval = {};
                keyval[cachedDataKey] = cachedResult;
                chrome.storage.local.set(keyval);

                createSuggestedArticleTable(res, currentURL);
            }
            else {
                $("#suggested-article-loading-status")
                    .text('Unfortunately, no suitable articles could be found');
            }
        })
        .fail((jqXHR, textStatus, errorThrown) => {
            $("#suggested-article-loading-status").text(`Failed to find suggested articles: ${textStatus}`);
        });
}


document.addEventListener('DOMContentLoaded', () => {
    onExtensionWindowLoad();
});
