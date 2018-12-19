

def TopMovers(tradedate, table, limit) :
    sql = ('SELECT stock_code, (close - open)/100 as gain FROM ' + table + ' WHERE trade_date = ' + tradedate + 
        ' ORDER BY gain DESC LIMIT ' + limit + ' ;')
    return sql

def TopRange(tradedate, table, limit) :
    sql = ('SELECT stock_code, (high - low)/100 as gain FROM ' + table + ' WHERE trade_date = ' + tradedate + 
        ' ORDER BY gain DESC LIMIT ' + limit + ' ;')
    return sql