#WARNING:- THIS FILE IS AN UNORGANISED MESS OF CODE
#          NOR IS IT MEANT TO GIVE AN MEANINGFUL OUTPUT YET
#          NOR IS IT MEANT TO EVEN RUN
#          USE AT YOUR OWN PERIL

from goose3 import Goose

urls = ['http://edition.cnn.com/2012/02/22/world/europe/uk-occupy-london/index.html?hpt=ieu_c2',
        'http://chrisgreybrexitblog.blogspot.co.uk/2018/02/britains-brexit-self-punishment.html',
        'https://www.oneangrygamer.net/2018/01/vice-media-anti-gamergate-outlet-fires-mike-germano-sexual-misconduct/50379/',
        'https://www.theguardian.com/technology/2017/sep/24/zoe-quinn-gamergate-online-abuse',
        'http://www.theweek.co.uk/90229/what-is-the-capital-of-israel',
        'https://www.washingtonpost.com/world/israel-blasts-iran-deal-as-dark-day-in-history/2015/07/14/feba23ae-0018-403f-82f3-3cd54e87a23b_story.html?utm_term=.2f548f59e6cb',
        'https://dailystormer.name/goycott-business-works-with-communists-to-fire-tony-hovater-but-now-were-fighting-back/',
        'https://www.snopes.com/four-times-more-stabbed-than-rifles-any-kind/',
        'https://www.theguardian.com/commentisfree/2015/jan/06/real-american-sniper-hate-filled-killer-why-patriots-calling-hero-chris-kyle',
        'https://www.theguardian.com/commentisfree/2015/oct/30/indonesia-fires-disaster-21st-century-world-media'
        ]

g = Goose()

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation

#TODO: SWITCH TO GENSIM FOR BACKUP TFIDF?

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print "Topic %d:" % (topic_idx)
        print " ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]])

#TODO: MOVE FROM 20NEWS TO REUTERS
dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
documents = dataset.data

no_terms = 1000
no_corpus_topics = 5

# NMF uses tf-idf
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_terms, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(documents)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

# Run NMF
nmf = NMF(n_components=no_corpus_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)


# LDA only uses tf
#TODO: REMOVE LDA AS NOT AS USEFUL AS NMF
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_terms, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

# Run LDA
lda = LatentDirichletAllocation(n_topics=no_corpus_topics, max_iter=5, learning_method='online', learning_offset=50., random_state=0).fit(tf)

no_topics = 3
#display_topics(nmf, tfidf_feature_names, no_topics)
#display_topics(lda, tf_feature_names, no_topics)

# My own implementation of tf idf follows
from nltk.corpus import reuters
from string import punctuation
from nltk.corpus import stopwords
from nltk import word_tokenize
stop_words = stopwords.words('english') + list(punctuation)

def tokenize(text):
    words = word_tokenize(text)
    words = [w.lower() for w in words]
    return [w for w in words if w not in stop_words and not w.isdigit()]

# build the vocabulary in one pass
vocabulary = set()
for file_id in reuters.fileids():
    words = tokenize(reuters.raw(file_id))
    vocabulary.update(words)

# add article vocabulary also

article = g.extract(url=urls[1])
awords = tokenize(article.cleaned_text)
vocabulary.update(awords)

vocabulary = list(vocabulary)
word_index = {w: idx for idx, w in enumerate(vocabulary)}

VOCABULARY_SIZE = len(vocabulary)
DOCUMENTS_COUNT = len(reuters.fileids())
#print VOCABULARY_SIZE, DOCUMENTS_COUNT      # 10788, 51581

import numpy as np
word_idf = np.zeros(VOCABULARY_SIZE)
for file_id in reuters.fileids():
    words = set(tokenize(reuters.raw(file_id)))
    indexes = [word_index[word] for word in words]
    word_idf[indexes] += 1.0

word_idf = np.log(DOCUMENTS_COUNT / (1 + word_idf).astype(float))

def word_tf(word, document):
    document = tokenize(document)

    return float(document.count(word)) / len(document)

def tf_idf(word, document):
    document = tokenize(document)

    if word not in word_index:
        return .0

    return word_tf(word, document) * word_idf[word_index[word]]


#TODO: OPTIMISE DOC TERM MATRIX TRANSFORM
tfidf2 = []

for id in reuters.fileids():
    row = []
    for word in vocabulary:
        row.insert(index=0, elem=tf_idf(word, reuters.raw(id)))
    tfidf2.insert(index=0, elem=row)

row = []
for word in vocabulary:
    row.insert(index=0, elem=tf_idf(word, article.cleaned_text))
tfidf2.insert(index=0, elem=row)


#TODO: MOVE AWAY FROM SKLEARN NMF(???)
nmf2 = NMF(n_components=no_corpus_topics, random_state=1, alpha=.12, l1_ratio=.5, init='nndsvd').fit(tfidf2)

def display_article_topics(model, feature_names, no_top_words):
    topic_idx, topic = model.components_[DOCUMENTS_COUNT + 1]
    print " ".join([feature_names[i]
            for i in topic.argsort()[:-no_top_words - 1:-1]])

#display_topics(nmf2, vocabulary.reverse() , no_topics)

#TODO: BROWN CORPUS
from nltk.corpus import brown

#print brown.words(categories='news')
#print brown.words(categories='editorial')
#print brown.words(categories='reviews')
#print brown.sents(categories=['news', 'editorial', 'reviews'])

#TODO: REWRITE ALL SENTIMENT CODE TO BE SUPERVISED
