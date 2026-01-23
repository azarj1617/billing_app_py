from Dao.ItemDao import get_all_items, get_items_by_id_dao, insert_item_dao, search_items_dao, update_item_dao


def get_items_serv(status):
    return get_all_items(status)

def get_items_by_id_serv(itemId):
    return get_items_by_id_dao(itemId)

def search_items_serv(searchTerm,status,type):
    return search_items_dao(searchTerm,status,type)

def insert_item_serv(itemData):
    return insert_item_dao(itemData)

def update_item_serv(itemData):
    return update_item_dao(itemData)