import json
import os
import mysql.connector
from elasticsearch import Elasticsearch
from datetime import datetime


def lookup_item(product_id):
    print("====== Looking up", product_id, "======")

    product_request(product_id)

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


def product_request(product_id):
    print(datetime.now(), "Registering request for", product_id)

    tmp = open("tmp.txt", 'a')
    register = 1
    with open("product_request.txt", 'r') as file:
        for line in file:
            if product_id in line:
                value = line.split()
                value[1] = int(value[1]) + 1
                tmp.write(product_id + " " + str(value[1]) + '\n')
                register = 0
            elif line:
                tmp.write(line)

    os.remove("product_request.txt")
    os.rename("tmp.txt", "product_request.txt")

    if register:
        file = open("product_request.txt", "a")
        file.write(product_id + " 1" + '\n')
        file.close()


def check_cache(product_id):
    print(datetime.now(), "Checking cache")
    with open("localcache.json") as cache:
        data = json.load(cache)
        for p in data["product"]:
            if product_id == p["productid"]:
                print(datetime.now(), "  Returning from cache")
                cache.close()
                return p
        print(datetime.now(), "  Not in cache")
        return


def check_elasticsearch(product_id):
    print(datetime.now(), "Checking ElasticSearch")
    es = Elasticsearch("localhost:9200", )
    res = es.search(index="products", body={"query": {"match": {"productid": product_id}}})
    if res['hits']['total']['value'] > 0:
        result = res['hits']['hits'][0]['_source']
        print(datetime.now(), "  Returning from ElasticSearch: ", result)
        add_to_cache(result)
        return result
    print(datetime.now(), "  Not in ElasticSearch")
    return


def check_mysql(product_id):
    print(datetime.now(), "Checking mysql server")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="products"
    )

    mycursor = mydb.cursor(dictionary=True)
    sql = "select * from products1 where productid = %s"
    mycursor.execute(sql, (product_id,))

    try:
        myresult = mycursor.fetchall()[0]
        print(datetime.now(), "  Returning from sql", myresult)
        jsoned = json.dumps(myresult)
        add_to_cache(myresult)
        return jsoned
    except:
        print(datetime.now(), "  not in mysql")
        return


def add_to_cache(product_details):
    print(datetime.now(), "Adding to the cache")
    with open("localcache.json", 'r+') as file:
        file_data = json.load(file)
        file_data["product"].append({
            'productid': product_details.get("productid"),
            'name': product_details.get("name")
        })
        file.seek(0)
        json.dump(file_data, file, indent=4)


def initialise():
    try:
        open("product_request.txt", "x")
    except:
        pass

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
    mycursor.execute("insert into products1 (productid, name) values ('00006', 'Coconut')")
    mydb.commit()


def reset():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="products"
    )
    mycursor = mydb.cursor()
    mycursor.execute("delete from products1 where productid = '00006'")
    mydb.commit()
    mycursor.close()


if __name__ == '__main__':
    cache_id = "00001"
    elasticsearch_id = "00005"
    sql_id = "00006"
    not_id = "000x01"

    initialise()

    # Test item in cache
    print(datetime.now(), "JSON for that product is: ", lookup_item(cache_id))

    # Test item in Elasticsearch
    print(datetime.now(), "JSON for that product is: ", lookup_item(elasticsearch_id))

    # Test item in mysql
    print(datetime.now(), "JSON for that product is: ", lookup_item(sql_id))

    # Test item found in Elasticsearch has been added to the cache
    print(datetime.now(), "JSON for that product is: ", lookup_item(elasticsearch_id))

    # Test item found in SQL has been added to cache
    print(datetime.now(), "JSON for that product is: ", lookup_item(sql_id))

    # Test item doesn't exist
    print(datetime.now(), "JSON for that product is: ", lookup_item(not_id))

    reset()
