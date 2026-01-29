from Dao.QuoteDao import get_all_quotes_dao, get_quote_by_id_dao, get_quote_no_dao, get_quotes_by_date_dao, save_quote_dao


def get_all_quotes_serv():
    return get_all_quotes_dao()

def get_quotes_by_date_serv(data):
    return get_quotes_by_date_dao(data)

def get_quote_by_id_serv(data):
    return get_quote_by_id_dao(data)

latestQNo=0
def get_quote_no_serv():
    latest_quote = get_quote_no_dao()
    latestQNo = latest_quote.quote_seq_no if latest_quote else 0 
    quoteNumber = latestQNo+1
    latestQuoteNum = "QUO"+"/"+str(quoteNumber)
    return latestQuoteNum

def save_quote_serv(data):
    return save_quote_dao(data)