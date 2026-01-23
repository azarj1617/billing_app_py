from Dao.CustomerDao import get_all_customers, save_customer_data,search_customer_data


def get_customers_data():
    return get_all_customers()

def search_customers_data(searchTerm,status):
    return search_customer_data(searchTerm,status)

def save_customer_serv(customer):
    return save_customer_data(customer)