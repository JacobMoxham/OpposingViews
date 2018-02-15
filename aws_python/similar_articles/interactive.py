from aws_python.similar_articles import get_similar_article_backend_results
import sys

"""
This script lets you try out the similar article finding backends

TODO:
Somewhat annoyingly, the imports only work if you run this code from outside the aws_python directory—I'm working what
the best way to fix that is...
"""

if __name__ == '__main__':

    while True:
        print(">", end='')
        sys.stdout.flush()
        for line in sys.stdin:
            line = line.strip()
            print("Searching {:s}...".format(line))
            print(get_similar_article_backend_results(line.split()))
            print("\n\n>", end='')
            sys.stdout.flush()
