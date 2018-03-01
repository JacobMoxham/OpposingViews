import articleDateExtractor
class ExtractDate():

   
    def extract_date(self, url):
        
        d = articleDateExtractor.extractArticlePublishedDate(url)
        to_return = {
	    'date': d	
        }
        return to_return
