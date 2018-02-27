#!/usr/bin/env python3

import os
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.pipeline import Pipeline
from classifiers.ml_utils import show_most_informative_features
import logging
import numpy as np
import random
import pandas as pd
from matplotlib import pyplot
import statistics

def getFolderRoot(doctype):
    return '../machine_learning_research/data/' + doctype + '_documents/'

def get_slice(lst, proportion_start, proportion_end):
    return lst[int(len(lst) * proportion_start) : int(len(lst) * proportion_end)]

def read_documents(num_folds = 5, fold_num = 0):
    print("reading documents...")
    random.seed(0)
    data = {'train' : {'labels' : [], 'data' : []},
            'test' :  {'labels' : [], 'data' : []}}
    for doctype in ['neutral', 'opinion']:
        shuffled_filenames = [x for x in os.listdir(getFolderRoot(doctype)) if x.isdigit()]
        random.shuffle(shuffled_filenames)
        lower_bound = (1.0 / num_folds) * fold_num
        upper_bound = (1.0 / num_folds) * (fold_num + 1)
        dataSplit = {'train' : get_slice(shuffled_filenames, 0.0, lower_bound) + get_slice(shuffled_filenames, upper_bound, 1.0),
                     'test'  : get_slice(shuffled_filenames, lower_bound, upper_bound)}
        for learn_type, file_names in dataSplit.items():
            for file_name in file_names:
                data[learn_type]['labels'].append(doctype)
                with open(getFolderRoot(doctype) + file_name) as f:
                    data[learn_type]['data'].append(str(f.read()))
    return data
                
def train_classifier(data, vectorizer = CountVectorizer(), classifier = SGDClassifier()):
    print("training classifier")
    pipeline = Pipeline([
        ('vect', vectorizer),
        ('tfidf', TfidfTransformer()),
        ('clf', classifier)
    ])
    pipeline.fit(data['train']['data'], data['train']['labels'])
    return pipeline

def test_classifier(data, pipeline):
    print("Testing classifier...")
    return pipeline.score(data['test']['data'], data['test']['labels'])

def get_df_with_probability(data, pipeline):
    df = get_dataframe(data, pipeline)
    df['probabilities'] = pipeline.predict_proba(data['test']['data']).max(axis = 1)
    return df

def get_data_by_accuracy(df):
    return {'accurate' : df[df['accurate'] == True], 'inaccurate' : df[df['accurate'] == False]}

def get_probability_hist(df):
    print("Drawing histogram...")
    data = get_data_by_accuracy(df) 
    pyplot.hist([data['accurate']['probabilities'], data['inaccurate']['probabilities']])
    pyplot.show()

def get_dataframe(data, pipeline):
    predicted = pipeline.predict(data['test']['data'])
    df = pd.DataFrame({'data' : data['test']['data'], 'actual_label' : data['test']['labels'], 'predicted_label' : predicted})
    df['accurate'] = df['actual_label'] == df['predicted_label']
    return df

def print_detailed_grouped_results(df):
    grouped_df = get_data_by_accuracy(df)
    for item in ['accurate', 'inaccurate']:
        print(grouped_df[item][['probabilities', 'data', 'actual_label']])

if __name__ == '__main__':
    OUTPUT_FILE = 'classifiers/tone_clf.pkl'
    logging.basicConfig(level=logging.INFO)

    logging.info("initialising classifiers")

    data = read_documents()

    pipeline = train_classifier(data, classifier = LogisticRegression())

    logging.info(test_classifier(data, pipeline))
    show_most_informative_features(pipeline.steps[0][1], pipeline.steps[-1][1])

    joblib.dump(pipeline, OUTPUT_FILE)

