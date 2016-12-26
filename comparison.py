import tweepy
import sqlite3 as lite
import sys
import tweet_collection
import upload_to_drive as drive
import datetime

#if anyone else looks at this I have realized that I should have had an "executeCommand" method because I use that so much but I didn't think about that and now I have gone too far, maybe I will add it one day

def deletedCount():
    con = lite.connect('full_db.db')
    cur = con.cursor()
    command = "SELECT COUNT(*) FROM Deleted_Tweets;"
    cur.execute(command)
    testVar = [int(record[0])for record in cur.fetchall()]
    numDeleted= int(testVar[0])  
    con.commit()
    return numDeleted

def copyTables(source, destination):
    con = None
    try: 
        con = lite.connect('full_db.db')
        cur = con.cursor()
        command = "DELETE FROM " + destination + ";"   
        cur.execute(command)
        command = "INSERT INTO " + destination + " SELECT * FROM " + source + ";"
        cur.execute(command)
        con.commit()
    except lite.Error, e:
            print "Error %s",datetime.datetime.now() % e.args[0]
            sys.exit(1)
    return

    
def differences(unuploaded, uploaded):
    con = None
    try: 
        con = lite.connect('full_db.db')
        cur = con.cursor()
        command = "SELECT * FROM " + unuploaded + " EXCEPT SELECT * FROM " + uploaded + ";"
        rows = cur.execute(command).fetchall()
        con.commit()
        #process rows into data (gotta figure this shit out)
        data = {"values": rows}
    except lite.Error, e:
        print "Error %s ",datetime.datetime.now() % e.args[0]
        sys.exit(1)
    return data 


def detectDeleted(first, second):
    if(first != second):
        print "\n DELETED TWEET DETECTED", datetime.datetime.now() 
        print "\n"
        drive.upload2drive(differences('Deleted_Tweets','Temp_Tweets'))
        copyTables('Deleted_Tweets', 'Temp_Tweets')
    return

#TODO: download images and upload the to google drive, put the links to the images in the database and then upload them to the spreadsheet
def compare():
    print "Comparing...", datetime.datetime.now()
    copyTables('Deleted_Tweets', 'Temp_Tweets')
    tweet_collection.collect_tweets('Daily_Comp')
    con = None
    try:
        #counts how many tweets are in Deleted_Tweets before the comparison
        firstCount = deletedCount()
        #checking for deleted tweets using sqlite3 commands
        con = lite.connect('full_db.db')
        cur = con.cursor()
        command = "INSERT INTO Deleted_Tweets SELECT * FROM Tweets Where Id NOT IN (SELECT Id FROM Daily_Comp UNION ALL SELECT Id FROM Deleted_Tweets);"
        cur.execute(command) 
        con.commit()

        #counts how many tweets are in Deleted_Tweets after the Comparison
        secondCount = deletedCount()
        #if those two numbers are different then there have been new tweets deleted
        detectDeleted(firstCount,secondCount)
         
        #deleting the tweets from Daily Comp to save space
        print "Deleteing Daily_Comp Tweets", datetime.datetime.now()
        command = "DELETE FROM Daily_Comp"
        cur.execute(command)
        con.commit()
    except lite.Error, e:
        print "Error %s:",datetime.datetime.now() % e.args[0]
        sys.exit(1)

    finally:
        if con: 
            con.close()
        
    print "Comparison over....",datetime.datetime.now()
    return

def testCase():
   print differences("Deleted_Tweets","Temp_Tweets")
   return

#testCase()
