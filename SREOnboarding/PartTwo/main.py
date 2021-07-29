import json
import os
import mysql.connector
from elasticsearch import Elasticsearch
from datetime import datetime


def lookup_item(product_id):
    print("====== Looking up", product_id, "======")

    # Log a search for that product_id. Includes products that aren't found in cache/elasticsearch/mysql
    product_request(product_id)

    # Iterates through each level of storage and breaks out if the data is present
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

    # Look through the request file for the product id. Increment the following number by one and write to a tmp file
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

    # Replace the original file with the tmp file
    os.remove("product_request.txt")
    os.rename("tmp.txt", "product_request.txt")

    # If the product wasn't found in the file, append it and add '1'
    if register:
        file = open("product_request.txt", "a")
        file.write(product_id + " 1" + '\n')
        file.close()


def check_cache(product_id):
    print(datetime.now(), "Checking cache")

    # Iterate through every element in the cache and return that json element if present
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

    # Build a query against the Elasticsearch instance and return it. Add the details to the cache file
    es = Elasticsearch("localhost:9200", )
    try:
        res = es.search(index="products", body={"query": {"match": {"productid": product_id}}})
        if res['hits']['total']['value'] > 0:
            result = res['hits']['hits'][0]['_source']
            print(datetime.now(), "  Returning from ElasticSearch: ", result)
            add_to_cache(result)
            return result
        print(datetime.now(), "  Not in ElasticSearch")
        return

    # Handle errors if the instance is down and move on to the mysql server
    except:
        print(datetime.now(), "  ElasticSearch is unavailable right now")


def check_mysql(product_id):
    print(datetime.now(), "Checking mysql server")

    # Connect to the mysql server instance
    # TODO - safer credentials, not using root
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="products"
    )

    # Run a basic select query and return results as a dictionary. Add results to the cache file
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
        print(datetime.now(), "  Not in mysql")
        return


def add_to_cache(product_details):
    print(datetime.now(), "Adding to the cache")

    # Load the existing json cache and add the details found in ElasticSearch/mysql
    with open("localcache.json", 'r+') as file:
        file_data = json.load(file)
        file_data["product"].append({
            'productid': product_details.get("productid"),
            'name': product_details.get("name")
        })
        file.seek(0)
        json.dump(file_data, file, indent=4)


def initialise():
    #Create the product_request.txt file if it doesn't exist already
    try:
        open("product_request.txt", "x")
    except:
        pass

    # Create the cache, overwriting any existing files so any elements added in previous runs are cleared
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

    # Add an entry to the mysql table so there is an item that is not in elasticsearch
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
    # Remove the additional entry from the table
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

    # Set up the environment
    initialise()

    # Test to see if an item is in the cache file
    print(datetime.now(), "JSON for that product is: ", lookup_item(cache_id))

    # Test to see if an item is in Elasticsearch
    print(datetime.now(), "JSON for that product is: ", lookup_item(elasticsearch_id))

    # Test to see if an item is in mysql
    print(datetime.now(), "JSON for that product is: ", lookup_item(sql_id))

    # Test to see if the item previously found in Elasticsearch has been added to the cache
    print(datetime.now(), "JSON for that product is: ", lookup_item(elasticsearch_id))

    # Test to see if the item previously found in SQL has been added to cache
    print(datetime.now(), "JSON for that product is: ", lookup_item(sql_id))

    # Test to see if an item doesn't exist
    print(datetime.now(), "JSON for that product is: ", lookup_item(not_id))

    # Cleardown the environment
    reset()
