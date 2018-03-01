from nltk.tag import pos_tag


class ExtractProperNouns():

    
    def extract_proper_nouns(self,text):
        tagged_text =  pos_tag (text.split())
        proper_nouns = [word for word,pos in tagged_text if pos == 'NNP']
        return proper_nouns


