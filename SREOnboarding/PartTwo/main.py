import json
import mysql.connector


def lookup_item(product_id):
    print("Looking up", product_id)

    if check_cache(product_id):
        return check_cache(product_id)
    elif check_elasticsearch(product_id):
        add_to_cache(product_id)
        return check_elasticsearch(product_id)
    elif check_mysql(product_id):
        add_to_cache(product_id)
        return check_mysql(product_id)

    return "Product does not exist"


def check_cache(product_id):
    with open("localcache.json") as cache:
        data = json.load(cache)
        for p in data["product"]:
            if product_id == p["productid"]:
                print("Returning from cache")
                cache.close()
                return p
        print(product_id, "not in cache")
        return


def check_elasticsearch(product_id):
    pass


def check_mysql(product_id):
    print("Looking in mysql server")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="products"
    )

    mycursor = mydb.cursor()

    mycursor.execute("select * from products1")

    myresult = mycursor.fetchall()

    for x in myresult:
        if x[0]==product_id:
            return x
    print(product_id, "not in mysql")
    return

def add_to_cache(product_id):
    pass


def preload():
    cache = open("localcache.json", "w")
    data = {'product': []}
    data['product'].append({
        'name':'Apple',
        'productid':"00001"
    })
    data['product'].append({
        'name':'Orange',
        'productid':"00002"
    })
    data['product'].append({
        'name':'Banana',
        'productid':"00003"
    })

    json.dump(data, cache)
    cache.close()


if __name__ == '__main__':
    cache_id = "00001"
    sql_id = "00004"
    not_id = "000x01"

    preload()

    # Test item in cache
    print("JSON for that product is: ", lookup_item(cache_id))


    # Test item in Elasticsearch
    # lookup_item(product_id)

    # Test item in mysql
    lookup_item(product_id)

    # Test item doesn't exist
    print("JSON for that product is: ", lookup_item(not_id))