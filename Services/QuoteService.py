from Dao.QuoteDao import get_all_quotes_dao, get_quote_by_id_dao, get_quotes_by_date_dao


def get_all_quotes_serv():
    return get_all_quotes_dao()

def get_quotes_by_date_serv(data):
    return get_quotes_by_date_dao(data)

def get_quote_by_id_serv(data):
    return get_quote_by_id_dao(data)