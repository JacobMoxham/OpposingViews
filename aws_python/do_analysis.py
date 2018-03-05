from mongo_feedback.database_access import FeedbackDB
import feedback.feedback_analysis as fba
import argparse
import os

db = FeedbackDB()

urls = fba.get_all_urls(db)

fba.plot_pos_percentages(db, urls)
fba.plot_liked_alternate_or_same_political_leaning(db)

urls = ['http://www.bbc.co.uk/sport/football/43278166',
        'http://www.bbc.co.uk/news/world-middle-east-43277856',
        'http://www.bbc.co.uk/news/uk-politics-43277181',
        'http://www.bbc.co.uk/news/entertainment-arts-43243027',
        'https://www.theguardian.com/world/2018/mar/04/germany-social-democrats-spd-vote-in-favour-of-coalition-angela-merkel',
        'https://www.theguardian.com/world/2018/mar/04/italy-goes-to-polls-divisive-election-campaign-berlusconi',
        'https://www.theguardian.com/media/2018/mar/04/tony-hall-bbc-fight-us-tech-firms-protect-british-values',
        'https://www.theguardian.com/uk-news/2018/mar/04/illegal-raves-in-london-double-in-a-year',
        'http://www.huffingtonpost.co.uk/entry/theresa-may-rejects-passporting-for-city-of-london-after-brexit_uk_5a9bc992e4b0a0ba4ad4270a?tkq&utm_hp_ref=uk-homepage',
        'http://www.huffingtonpost.co.uk/entry/meghan-markle-megaformer_uk_5a8d84f0e4b00a30a25148d6?dgm&utm_hp_ref=uk-homepage',
        'http://www.huffingtonpost.co.uk/entry/squatters-activists-london_uk_5a993b81e4b0479c02516c21?utm_hp_ref=uk-homepage',
        'http://www.huffingtonpost.co.uk/entry/tory-mps-will-not-get-free-vote-on-brexit-deal-says-david-lidington_uk_5a9bf07ce4b089ec353b2390?43&utm_hp_ref=uk-homepage'
]

parser = argparse.ArgumentParser()
parser.add_argument("-f1", help='file1 to run politics per site on', default='')
parser.add_argument("-f2", help='file1 to run politics per site on', default='')

args = parser.parse_args()
urls_to_pass = []
if args.f1 == '' and args.f2 == '':
    urls_to_pass = urls
elif args.f1 != '':
    with open(args.f1) as f:
        content = f.readlines()
        urls_to_pass += [x.strip() for x in content]
elif args.f2 != '':
    with open(args.f2) as f:
        content = f.readlines()
        urls_to_pass += [x.strip() for x in content]


#fba.plot_politics_per_site(urls_to_pass)