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

    mycursor = mydb.cursor(dictionary=True)
#    print("select * from products1 where product = "+product_id)
    mycursor.execute("select * from products1 where product = \""+product_id+"\"")


    try:
        myresult = mycursor.fetchall()[0]
        print("Returning from sql",myresult)
        jsoned = json.dumps(myresult)
        add_to_cache(myresult)
        return jsoned
    except:
        print(product_id, "not in mysql")
        return


def add_to_cache(product_details):
    print("adding to the cache:",product_details)
    with open("localcache.json", 'r+') as file:
        file_data = json.load(file)
#        print("Productdetails[0]",product_details[0])
        file_data["product"].append({
            'productid': product_details.get("product"),
            'name':product_details.get("name")
            })
#        file_data["product"].append(product_details)
        file.seek(0)
        json.dump(file_data, file, indent=4)
        
        
        output = json.dumps(file_data)

        print("added to the cache",output)
        
def preload():
    cache = open("localcache.json", "w")
    data = {'product': []}
    data['product'].append({
        'name': 'Apple',
        'productid': "00001"
    })
    data['product'].append({
        'name': 'Orange',
        'productid': "00002"
    })
    data['product'].append({
        'name': 'Banana',
        'productid': "00003"
    })

    json.dump(data, cache)
    cache.close()


if __name__ == '__main__':
    cache_id = "00001"
    elasticsearch_id = "00005"
    sql_id = "00004"
    not_id = "000x01"

    preload()

    # Test item in cache
    print("JSON for that product is: ", lookup_item(cache_id))

    # Test item in Elasticsearch
    # lookup_item(elasticsearch_id)

    # Test item in mysql
    print("JSON for that product is: ", lookup_item(sql_id))

    # Test item doesn't exist
    print("JSON for that product is: ", lookup_item(not_id))
