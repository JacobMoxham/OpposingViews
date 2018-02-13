"""
Trains classifiers and writes them to files.

Requires dataset from https://www.kaggle.com/snapcrack/all-the-news to be downloaded and extracted in working directory.
Files are too big to include in Git, and require kaggle login so can't be downloaded by the script.
"""
import sys
import logging

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.externals import joblib

from ml_utils import show_most_informative_features
from classifier_definitions import preprocess


if __name__ == '__main__':
    OUTPUT_FILE = 'politics_clf.pkl'

    logging.basicConfig(level=logging.INFO)
    logging.info('Loading dataset')

    try:
        df = pd.concat((pd.read_csv('articles{}.csv'.format(i)) for i in (1, 2, 3)))
    except FileNotFoundError:
        logging.error('Training data not present. Download and extract files from https://www.kaggle.com/snapcrack/all-the-news')
        sys.exit()

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

    clf = Pipeline([('vect', CountVectorizer(preprocessor=preprocess, ngram_range=(1, 1))),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LogisticRegression())])

    logging.info('Training model')
    clf.fit(X_train['content'], Y_train)
    predicted = clf.predict(X_test['content'])
    logging.info('Accuracy: {}'.format(np.mean(predicted == Y_test)))
    show_most_informative_features(clf.steps[0][1], clf.steps[-1][1], n=50)
    logging.info('Writing to {}'.format(OUTPUT_FILE))
    joblib.dump(clf, OUTPUT_FILE)
