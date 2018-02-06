"""
Prototype classifier for political leanings (uses all-the-news dataset from Kaggle in Potential Toolkits).
Requires pandas, numpy, and scikit-learn.

Dataset not tracked with git because it is too large to go on GitHub (their standard).
"""
import logging

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

logging.basicConfig(level=logging.INFO)
logging.info('Loading dataset')
df = pd.concat((pd.read_csv('../data/articles{}.csv'.format(i)) for i in (1, 2, 3)))

logging.info('Adding labels')
LEFT_WING = ['Guardian', 'NPR', 'New York Times']
RIGHT_WING = ['Breitbart', 'Fox News', 'National Review']

# filter out articles without a sufficient political leaning
df = df[df['publication'].isin(LEFT_WING + RIGHT_WING)]

# add labels
labels = np.where(df['publication'].isin(LEFT_WING), 0, 1)
df['label'] = labels
left_wing_articles = df[df['publication'].isin(LEFT_WING)]
right_wing_articles = df[df['publication'].isin(RIGHT_WING)]

logging.info('{} left-wing articles, {} right-wing'.format(len(left_wing_articles),
                                                           len(right_wing_articles)))

Y = df.pop('label')
X = df

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

clf = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', LogisticRegression())])

logging.info('Training model')
clf.fit(X_train['content'], Y_train)
predicted = clf.predict(X_test['content'])
logging.info('Accuracy: {}'.format(np.mean(predicted == Y_test)))
