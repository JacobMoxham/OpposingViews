#!/usr/bin/env python3

import classifiers.sentiment_classifier as sentiment_classifier
import matplotlib.pyplot as plt

data = sentiment_classifier.load()

plt.plot(data['positive'])
plt.plot(data['negative'])
plt.show()
