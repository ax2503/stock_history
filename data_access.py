
import pymysql.cursors
import requests
import re
import statistical_queries as sq

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
      conn.commit()
  except :
      print('Failed to add record for ' + entry[0] + ' ' +
          entry[1])
  return


#Returns a list of the stock codes on the database since start
#of financial year.
def getCurrentCodes(conn) :
  sql = ('SELECT DISTINCT stock_code FROM year2018 ' +
    'WHERE trade_date > 20180630;')
  try:
    with conn.cursor() as cursor :
      cursor.execute(sql)
  except :
      print('Failed to get current codes')
  return cursor.fetchall()

#Inserts a record of the company name for a given ticker symbol
def insertStockName(conn,entry) :
  sql = 'INSERT INTO stocknames (stock_code, stock_name) VALUES(%s,%s);'
  try:
    with conn.cursor() as cursor :
      cursor.execute(sql, entry)
  except:
    print('Failed to add record for ' + entry)
  return

def getIssueStats(fn,conn, trdate) :
  sql = fn(trdate)
  with conn.cursor() as cursor :
    try :
      cursor.execute(sql)
      rcount = cursor.rowcount
      if rcount > 0 :
        row = cursor.fetchone()
        result = row['issues']
      else:
        result = 0
    except :
      print ('Failed to get stats ')
      result = 0
  return result

#Since the stock_history database has a full year per table, this function is required
#to generate the date ranges that will be in each year table given a start and end date.
#Expect that this will be used with UNION select queries.
def splitDates(startdate, enddate) :
  if startdate[:4] != enddate[:4] :
    startyear = startdate[:4]
    endyear = enddate[:4]
    dateslist = []
    for year in range(int(startyear), int(endyear)+1) :
      if year == int(endyear):
        dateslist.append((endyear + '0101', enddate))
      else:
        dateslist.append((startdate,str(year)+'1231'))
        startdate = str(year +1) + '0101'
  else :
    dateslist = [(startdate, enddate)]
  return dateslist
      


  return
      


#Returns a stock prices, given an ASX stock code
#Open, High, Low, Last, Volume
def getStockPrices(code):
  url = 'https://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes=' + code
  r=requests.get(url,allow_redirects = True)
  open('html/'+ code+'.html','wb').write(r.content)
  f = open('html/' + code + '.html','r')
  text = f.read()
  match = re.search(r'(<td class=\"last\">)(\d+\.\d+)',text)
  if match : 
    codeprice = match.group(2)
  else :
    codeprice = 0
  entry = []
  
  match = re.findall(r'<td>([0-9,-,\.,%]+)',text)
  if not match :
    entry = [0,0,0,codeprice,0]
  else:
    for dayprice in match[2:5] :
      entry.append(dayprice)
    entry.append(codeprice)
    entry.append(match[5].replace(',',''))
  
  return entry

