#This program will update the current day prices.


import datetime
from datetime import date
import data_access


def main() :
  pw = input('Password for MySql Database: ')
  conn = data_access.getConnection(pw)
  try:
    for rows in data_access.getCurrentCodes(conn) :
      print(rows['stock_code'])

  finally :
    conn.close()

    















if __name__ == '__main__':
  main()