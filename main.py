import tweet_collection
import comparison
import get_next_id 
import schedule 
import time
import datetime

tweet_collection.collect_tweets('Tweets')

#FUTURE TODO (for late version): Add a GUI????@?!??
#sets the schedule to compare old tweets to the full collection of tweets every hour


while True:
    try:
        #schedule.every(1).minutes.do(comparison.compare)
        schedule.every(60).minutes.do(comparison.compare)
        #schedule.every(1).day.do(comparison.compare)
                       
        while True: 
            schedule.run_pending()
            time.sleep(1)
    except:
        print "Comparison error...restarting schedule", datetime.datetime.now() 
        continue
    



