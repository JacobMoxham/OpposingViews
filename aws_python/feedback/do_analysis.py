from mongo_feedback.database_access import FeedbackDB
import feedback.feedback_analysis as fba

db = FeedbackDB()

urls = fba.get_all_urls(db)

fba.plot_pos_percentages(db, urls)
fba.plot_liked_alternate_or_same_political_leaning(db)