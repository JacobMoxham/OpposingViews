const DEBUG = 1
const debug_base = "http://localhost:8080/"
const api_base = "https://q33wccsyz5.execute-api.eu-west-1.amazonaws.com/dev/"

const debugBackendAPI = debug_base + 'get-views';
const productionBackendAPI = api_base + "extensionBackend";
const feedbackProcessingAPI = api_base + "feedback-processing";

const backendProcessingAPI = (DEBUG ? debugBackendAPI : productionBackendAPI);


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
            var keyval = {};
            keyval[ev.data.link] = ev.data.previousLink;
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
            $(document.body).text(`Failed to submit feedback: ${textStatus}`);
    });
}


function onExtensionWindowLoad() {
    $("#suggested-article-list").hide();
    $("#feedback-request").hide();

    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        const currentTab = tabs[0];
        const currentURL = currentTab.url;
        chrome.tabs.sendMessage(currentTab.id, {
                'action': 'sourceRequest',
                'currURL': currentURL
            }, function(rtn) {
                if (rtn.prevURL) {
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

                    $("#feedback-request").show();
                }

                const requestData = {
                    'link': currentURL
                };
                $.post(backendProcessingAPI, requestData)
                .done((res) => {
                    createSuggestedArticleTable(JSON.parse(res), currentURL);
                    $("#suggested-article-list").show();
                })
                .fail((jqXHR, textStatus, errorThrown) => {
                    $(document.body).text(`Failed to find suggested articles: ${textStatus}`);
                });
            });
    });
}


document.addEventListener('DOMContentLoaded', () => {
    onExtensionWindowLoad();
});