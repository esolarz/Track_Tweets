from __future__ import print_function
import argparse
import sqlite3 as lite
import time

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flags = argparse.ArgumentParser(parents =[tools.argparser]).parse_args()
    flow = client.flow_from_clientsecrets('client_id.json',SCOPES)
    creds = tools.run_flow(flow,store,flags)

SHEETS = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

def upload2drive(data):
    SHEET_ID = '1OY_H3bi-Q-dw61BU7sl2Go0PQMKn9mfIo0AmGmXsgEE'
    SHEETS.spreadsheets().values().append(spreadsheetId = SHEET_ID, range = 'A2',body = data, valueInputOption ='USER_ENTERED').execute()
     
def testCase():
    con = None
    try: 
        con = lite.connect('full_db.db')
        cur = con.cursor()
        command = "SELECT * FROM Deleted_Tweets;"
        rows = cur.execute(command).fetchall()
        con.commit()
        data = {"values": rows}
    except lite.Error, e:
        print("Error %s:" % e.args[0])
        sys.exit(1)
    upload2drive(data)

#testCase()
