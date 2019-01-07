
import data_access as da

def main() :
  pw = input('Password for database: ')  
  conn = da.getConnection(pw)
  try:
    with open('stocknames.csv','r') as f :
      for line in f.readlines() :
        print(line.split(','))
        da.insertStockName(conn, line.split(','))

  finally:
    conn.close()
    



if __name__ == '__main__':
  main()