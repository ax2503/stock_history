

def Top20Mover(tradedate, table) :
    sql = 'SELECT TOP 20 (close - open)/100 FROM ' + table + ' WHERE trade_date = ' + tradedate + ';'
    return sql

def Top20Range(tradedate, table) :
    sql = 'SELECT TOP 20 (high - low)/100 FROM ' + table + ' WHERE trade_date = ' + tradedate + ';'
    return sql