/*Image provided at https://openclipart.org/detail/194060/thumb-up-and-down
 * Free for commercial use
 */
const thumbsUpIcon = "thumbs-up.png";
const thumbsDownIcon = "thumbs-down.png";


function createImage(imgSrc) {
  var image = document.createElement("img");
  image.setAttribute("src", imgSrc);
  return image
}

function createGenericImageElement(imgSrc, classLabel) {
  var element = document.createElement("td");
  addClass(element, classLabel);

  var image = createImage(imgSrc); 

  element.appendChild(image);

  return element;
}


function addClass(elem, classLabel) {
  elem.setAttribute("class", classLabel);
}

function createArticlePictureElement(imgSrc, numRows) {
  const classLabel = "list-element-image";

  var element = createGenericImageElement(imgSrc, classLabel);
  element.setAttribute("rowspan", numRows);

  return element;
}

function createArticleTitleElement(articleTitle) {
  const classLabel = "list-element-title";

  var element = document.createElement("td");
  addClass(element, classLabel);
  
  var articleTitle = document.createTextNode(articleTitle);
  element.appendChild(articleTitle);
  
  return element;
}

function createArticleSummaryElement(articleSummary) {
  const classLabel = "list-element-summary";

  var element = document.createElement("td");
  addClass(element, classLabel);

  var articleSummary = document.createTextNode(articleSummary);
  element.appendChild(articleSummary);

  return element;
}

function createFeedbackRow(suggestedArticleLink) {
  const classLabel = "feedback-thumbs";

  var row = document.createElement("tr");

  var elem = document.createElement("td");
  addClass(elem, classLabel);

  var thumbsUp = createImage(thumbsUpIcon);
  var thumbsDown = createImage(thumbsDownIcon);
  
  thumbsUp.onclick = () => {sendFeedback("positive", suggestedArticleLink);};
  thumbsDown.onclick = () => {sendFeedback("negative", suggestedArticleLink);};

  elem.appendChild(thumbsUp);
  elem.appendChild(thumbsDown);

  row.appendChild(elem);
  return row;
}

/*
 * Creates a single item which represents a suggested article
*/
function createListItem(suggestedArticle) {
  
  var table = document.createElement("table");
  table.setAttribute("class", "list-element-table")

  var headerRow = document.createElement("tr");
  var contentRow = document.createElement("tr");
  var feedbackRow = createFeedbackRow(suggestedArticle.link); 
  
  numRows = 3;

  var pictureElement = createArticlePictureElement(suggestedArticle.imageLink, numRows);
  var articleTitleElement = createArticleTitleElement(suggestedArticle.title);
  var articleSummaryElement = createArticleSummaryElement(suggestedArticle.summary);
 
  headerRow.appendChild(pictureElement);
  headerRow.appendChild(articleTitleElement);
  contentRow.appendChild(articleSummaryElement);

  [headerRow, contentRow].forEach((elem) => {
    elem.onclick = function () {chrome.tabs.create(
      {url: suggestedArticle.link}
    );};
  });


  var rows = [headerRow, contentRow, feedbackRow];
  rows.forEach((elem) => {table.appendChild(elem);});


  return table;
}


/*
 * Creates a list of items which represents a list of suggested
 * articles as a table
 * */
function createSuggestedArticleTable(suggestedArticles) {
  var table = document.createElement("table", {class: "article-list"});
  
  for (var i = 0; i < suggestedArticles.length; i++) {
    var tableRow = document.createElement("tr");
    var tableElement = document.createElement("td", {class:"list-element"});

    tableElement.appendChild(createListItem(suggestedArticles[i]));
    tableRow.appendChild(tableElement);
    table.appendChild(tableRow);
  }

  return table;
}
