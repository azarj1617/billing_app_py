from Dao.QuoteDao import get_all_quotes_dao, get_quote_by_id_dao, get_quote_no_dao, get_quotes_by_date_dao, save_quote_dao, update_quote_dao
from Dao.SalesDao import get_bill_by_id_dao


def get_bill_by_id_serv(salesId):
    return get_bill_by_id_dao(salesId)
