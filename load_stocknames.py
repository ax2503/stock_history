
import data_access as da

def main() :
  #pw = input('Password for MySQL database: ')  
  #conn = da.getConnection(pw)
  #try:
    with open('stocknames.csv','r') as f :
      for line in f.readlines() :
        print(line.split(',')[:2])
        #da.insertStockName(conn, line[:2])

    



if __name__ == '__main__':
  main()