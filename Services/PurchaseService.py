from Dao.PurchaseDao import get_purchase_data_dao, save_purchase_dao


def get_purchase_data_serv():
    return get_purchase_data_dao()

def save_purchase_serv(purchaseData):
    return save_purchase_dao(purchaseData)
