##This program will load the data from all the files in the data folder
#Files must be in CSV format.
#Fields are code, date,open, high, low, close, volume format.
#Use this program to load past data into the database.
#Use price_watch to get 20 mins delayed data.
#This program requires a MySQL database. Details are in the 
#file data_access.py

import data_access
import os


def main() :
  pw = input('Password for MySQL database: ')
  conn = data_access.getConnection(pw)  
  file_list = os.listdir('./data')
  try:
    for filename in file_list :
      f = open('data/' + filename, 'r')

      for lines in f.readlines() :
        price_entry = lines.split(',')
        print('processing ' + price_entry[0] + ' ' + price_entry[1])
        year = price_entry[1][:4]

        data_access.createPriceTable(conn, 'year' + year)
        data_access.replacePriceRecord(conn, price_entry)
        conn.commit()
        
        

  finally:
    conn.close()
        
  







if __name__ == '__main__':
  main()