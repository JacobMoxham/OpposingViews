#!/usr/bin/env python3

from pipeline import pipeline_test
from mongo_heuristics.database_access import HeuristicsDB

db = HeuristicsDB()
print(pipeline_test('http://www.bbc.co.uk/news/world-us-canada-43066226', db))
