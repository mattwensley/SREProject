import json
import mysql.connector
from elasticsearch import Elasticsearch


def lookup_item(product_id):
    print("====== Looking up", product_id,"======")

    details = check_cache(product_id)
    if details:
        return details
    details = check_elasticsearch(product_id)
    if details:
        return details
    details = check_mysql(product_id)
    if details:
        return details

    return "Product does not exist"


def check_cache(product_id):
    print("Checking cache")
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
    print("Checking ElasticSearch")
    es = Elasticsearch("localhost:9200",)
    res = es.search(index="products",body={"query" :{"match": {"product":product_id}}})
    if res['hits']['total']['value']>0:
        result = res['hits']['hits'][0]['_source']
        print("Returning from ElasticSearch: ",result)
        add_to_cache(result)
        return result
    print("Not in ElasticSearch")
    return


def check_mysql(product_id):
    print("Looking in mysql server")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="products"
    )

    mycursor = mydb.cursor(dictionary=True)
    sql = "select * from products1 where product = %s"
    mycursor.execute(sql, (product_id,))


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
        file_data["product"].append({
            'productid': product_details.get("product"),
            'name':product_details.get("name")
            })
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
    
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="password",
      database="products"
    )
    mycursor = mydb.cursor()
    mycursor.execute("insert into products1 (product, name) values ('00006', 'Coconut')")
    mydb.commit()


def reset():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="password",
      database="products"
    )
    mycursor = mydb.cursor()
    mycursor.execute("delete from products1 where product = '00006'")
    mydb.commit()
    mycursor.close()

if __name__ == '__main__':
    cache_id = "00001"
    elasticsearch_id = "00005"
    sql_id = "00006"
    not_id = "000x01"

    preload()

    # Test item in cache
    print("JSON for that product is: ", lookup_item(cache_id))

    # Test item in Elasticsearch
    print("JSON for that product is: ",lookup_item(elasticsearch_id))

    # Test item in mysql
    print("JSON for that product is: ", lookup_item(sql_id))

    # Test item found in Elasticsearch has been added to the cache
    print("JSON for that product is: ",lookup_item(elasticsearch_id))

    # Test item found in SQL has been added to cache
    print("JSON for that product is: ", lookup_item(sql_id))

    # Test item doesn't exist
    print("JSON for that product is: ", lookup_item(not_id))

    reset()
