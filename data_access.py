
import pymysql.cursors
import requests
import re

def getConnection(pw) :
  connection=pymysql.connect(host='localhost',
               user='root',
               password=pw,
               db = 'stock_history',
               charset = 'utf8mb4',
               cursorclass=pymysql.cursors.DictCursor)
  return connection

def createPriceTable(conn, name) :
  sql = ('CREATE TABLE if not exists ' + name + 
  ' (stock_code CHAR(10) ,' +
  'trade_date DATE ,' +
  'open DECIMAL(13,4) ,' +
  'high DECIMAL(13,4) ,' +
  'low DECIMAL(13,4) ,' +
  'close DECIMAL(13,4) ,' +
  'volume INT UNSIGNED, ' +
  'PRIMARY KEY(stock_code, trade_date));' )
  with conn.cursor() as cursor :
    cursor.execute(sql)
  return


#Adds a price record to the database. Does not overwrite for a 
#duplicate day and code.
#Requires a connection object to be passed.
def addPriceRecord(conn, entry) :
  tname = 'year' + entry[1][:4]
  sql =( 'INSERT INTO ' + tname + 
  ' (stock_code, trade_date, open, high, low, close, volume) ' +
  'VALUES (%s, %s, %s, %s, %s, %s, %s)')
  try:
    with conn.cursor() as cursor :
      cursor.execute(sql, entry)
  except pymysql.err.IntegrityError :
    print('Trying to add duplicate record')
  return

#Adds or replaces a price record into the database. Overwrites if 
#there is already a duplicate record
#Requires a connection object to be passed.
def replacePriceRecord(conn, entry) :
  tname = 'year' + entry[1][:4]
  sql = ( 'REPLACE into ' + tname +
    '(stock_code, trade_date, open, high, low, close, volume) ' +
    'VALUES (%s, %s, %s, %s, %s, %s, %s)')
  try:
    with conn.cursor() as cursor :
      cursor.execute(sql, entry)
  except :
      print('Failed to add record for ' + entry[0] + ' ' +
          entry[1])
  return

#Returns a stock price, given an ASX stock code
def getStockprice(code):
  url = 'https://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes=' + code
  r=requests.get(url,allow_redirects = True)
  open(code+'.html','wb').write(r.content)
  f = open(code + '.html','r')
  text = f.read()
  match = re.search(r'(<td class=\"last\">)(\d+\.\d+)',text)
  if match : 
    codeprice = float(match.group(2))
  else :
    codeprice = 0
  return codeprice
