"""
Utility functions for machine learning.
"""
import logging


def show_most_informative_features(vectorizer, clf, n=20):
    """
    Display the most informative features for a classifier.
    """
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
    for (coef_1, fn_1), (coef_2, fn_2) in top:
        logging.info("\t{}\t{}\t\t{}\t{}".format(coef_1, fn_1, coef_2, fn_2))
