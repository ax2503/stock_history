#This program will update the current day prices.


import datetime
from datetime import date
import time
import data_access


def main() :
  today = date.today()
  pw = input('Password for MySql Database: ')
  conn = data_access.getConnection(pw)
  try:
    for row in data_access.getCurrentCodes(conn) :
      prices = data_access.getStockPrices(row['stock_code'])
      entry=[]
      entry.append(row['stock_code'])
      entry.append(str(today))
      for price in prices :
        entry.append(price)
      print(entry)
      data_access.replacePriceRecord(conn,entry)      
      time.sleep(5)


  finally :
    conn.close()

    















if __name__ == '__main__':
  main()