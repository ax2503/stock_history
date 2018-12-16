#This program will update the current day prices for stocks in 
#the file current_list.txt

import datetime
import time
import data_access


def main() :
    price = data_access.getStockprice("CBA")
    print(str(price))














if __name__ == '__main__':
  main()