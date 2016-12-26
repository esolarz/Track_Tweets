import sqlite3 as lite
import sys

def getNextID(table):
    con = None 
    currID = 0
    try: 
        con = lite.connect('full_db.db')
        cur = con.cursor()
        command = "SELECT COUNT(*) FROM " + table + ";"
        cur.execute(command)
        testVar = [int(record[0])for record in cur.fetchall()]
        currID = int(testVar[0]) +1 
        con.commit()
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if con:
            con.close()
    return currID

