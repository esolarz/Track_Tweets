import tweepy
import sqlite3 as lite
import sys

#TODO: Handle the downloading and processing of images        
  
def processTweet(db, tweet,table):
   
    content = tweet.text 
    idNo = tweet.id
    date = tweet.created_at 
    con =None
    
    try:
        full_tweet = tweet.retweeted_status.text
        ind = content.find(":") +2
        content = content[:ind] + full_tweet
    except:
        pass

    try: 
        con = lite.connect(db)
        cur = con.cursor()
        command = "SELECT COUNT(Id) FROM "+ table+ " WHERE Id == "+ str(idNo) + ";" 
        cur.execute(command)
        num = [int(record[0]) for record in cur.fetchall()]
        num = int(num[0]) 
        con.commit()
        if(num == 0):
            command = "INSERT INTO " + table + " VALUES(?,?,?);"  
            cur.execute(command,(idNo,content,date))
            con.commit()

    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if con:
            con.close()

    return


