

def TopMovers(tradedate, limit) :
    sql = ('SELECT stock_code, (close - open)/100 as gain FROM ' + 'year' + tradedate[:4] + ' WHERE trade_date = ' + tradedate + 
        ' ORDER BY gain DESC LIMIT ' + limit + ' ;')
    return sql

def TopRange(tradedate, limit) :
    sql = ('SELECT stock_code, (high - low)/100 as gain FROM ' + 'year' + tradedate[:4] + ' WHERE trade_date = ' + tradedate + 
        ' ORDER BY gain DESC LIMIT ' + limit + ' ;')
    return sql

def Rises(tradedate) :
    ##Number of rising issues (Close - Open) > 0
    sql = ('SELECT count(stock_code) as issues FROM ' + 'year' + tradedate[:4] + 
      ' WHERE trade_date = ' + tradedate + ' AND close > open AND volume !=  0; ')
    return sql

def TotalIssuesTraded (tradedate) :
    sql = ('SELECT count(*) as issues FROM ' + 'year' + tradedate[:4] + 
      ' WHERE trade_date = ' + tradedate + ' AND volume !=  0; ')
    return sql