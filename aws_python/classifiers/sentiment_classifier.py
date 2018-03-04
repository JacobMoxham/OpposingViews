#!/usr/bin/env python3

import re
import os
from .tone_classifier_training import getFolderRoot
import numpy as np
import pickle
import pandas as pd
import logging
 
def load_lexicon():
    logging.info("Loading lexicon...")
    with open(LEXICON_FILENAME) as f:
        lexicon = {}
        for line in f:
            line = line.rstrip()
            sections = line.split(" ")
            entry = {section.split('=')[0] : section.split('=')[1] for section in line.split(' ')}
            lexicon[entry['word']] = entry
        return lexicon


LEXICON_FILENAME = "classifiers/sentiment_lexicon"
PICKLE_FILENAME = "classifiers/sentiments.pkl"
SENTIMENTS = ['positive', 'negative']
LEXICON = load_lexicon()

def read_documents():
    logging.info("Reading own-scraped documents...")
    data = []
    for doctype in ['neutral', 'opinion']:
        file_names = [x for x in os.listdir(getFolderRoot(doctype)) if x.isdigit()]
        for file_name in file_names:
            with open(getFolderRoot(doctype) + file_name) as f:
                data.append(str(f.read()))
    return data
def get_sentiment_distribution(text, lexicon, intensity_parameter = {'strong' : 1, 'weak' : 0.5}):
    words = text.split()
    word_pattern = re.compile(r"[A-Z-]+", re.IGNORECASE)
    word_count = {sentiment : 0 for sentiment in SENTIMENTS}
    word_count['total'] = 0
    for word in words:
        alphabetic_word = re.search(word_pattern, word)
        if alphabetic_word:
            word_count['total'] = word_count['total'] + 1
            word = alphabetic_word.string
            if word in lexicon:
                sentiment = lexicon[word]['polarity']
                intensity = intensity_parameter[lexicon[word]['intensity']]
                word_count[sentiment] = word_count[sentiment] + intensity
    sentiment_distribution = {sentiment : word_count[sentiment] / word_count['total'] for sentiment in SENTIMENTS if word_count['total'] > 0}
    return sentiment_distribution

def get_train_data():
    return get_kaggle_dataset()

def get_kaggle_dataset():
    try:
        df = pd.concat((pd.read_csv('../machine_learning_research/data/kaggle/articles{}.csv'.format(i)) for i in (1, 2, 3)))
    except FileNotFoundError:
        logging.error('Training data not present. Download and extract files from https://www.kaggle.com/snapcrack/all-the-news')
        sys.exit()
    return df['content']

def train_sentiment_distribution():
    data = get_train_data()
    distributions = {sentiment : [] for sentiment in SENTIMENTS}
    logging.info("Training classifier...")
    percentile = len(data) // 100
    count = 0
    for text in data:
        sentiment_distribution = get_sentiment_distribution(text, LEXICON)
        for sentiment in SENTIMENTS:
            if sentiment in sentiment_distribution:
                distributions[sentiment].append(sentiment_distribution[sentiment])
        count = count + 1
        if count % percentile == 0:
            logging.info(str(count // percentile) + "% complete")

    for sentiment in SENTIMENTS:
        distributions[sentiment] = np.sort(np.array(distributions[sentiment]))
    return distributions

def classify(sorted_training_data, test_data):
    logging.info("Scoring text...")
    result = {}
    test_distribution = get_sentiment_distribution(test_data, LEXICON)
    for sentiment in SENTIMENTS:
        array = sorted_training_data[sentiment]
        if sentiment in test_distribution:
            result[sentiment] = np.searchsorted(array, test_distribution[sentiment]) / array.size
        else:
            result[sentiment] = 0
    return result

def classify_all(sorted_training_data, test_datas):
    results = []
    for test_data in test_datas:
        results.append(classify(sorted_training_data, test_data))
    return results

def load():
    with open(PICKLE_FILENAME, 'rb') as f:
        return pickle.load(f)

#Train the data
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    trained_arrays = train_sentiment_distribution()
    with open(PICKLE_FILENAME, 'wb') as f:
        pickle.dump(trained_arrays, f)
    logging.info(classify(trained_arrays, test_text))

