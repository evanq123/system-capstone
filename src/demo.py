from database import db_mysql, db_create, db_delete, db_range, db_kvstore
from datetime import datetime
import time
import json

def main():
    # print("Enter data file name to be read:")
    # f = open(input(), "r")
    f = open("data_6k.txt", "r")
    line = f.readline()
    start = time.time()
    #------------------------Building the store-----------------------------------------
    print("building databases...\n")
    while line:
        print(line)
        db_create(json.loads(line))
        line = f.readline()
    end = time.time()
    print("database complete - built in ", end - start)
    # ----------------------------------------------------------------------------------
    f.close()
    db_data, kv_data = db_range('created_at', 'text', "Wed Nov 11 23:20:10 +0000 2020", "Wed Nov 12 23:20:10 +0000 2020")
    f = open("mysql_range_result_6k.txt", "w")
    for text in db_data:
        f.write(text[0])
    f.close()
    f = open("kv_range_result_6k.txt", "w")
    for text in kv_data:
        f.write(text)
    f.close()

    f = open("data_20k.txt", "r")
    line = f.readline()
    start = time.time()
    #------------------------Building the store-----------------------------------------
    # print("building databases...\n")
    while line:
        db_create(json.loads(line))
        line = f.readline()
    # end = time.time()
    # print("database complete - built in ", end - start)
    # ----------------------------------------------------------------------------------
    f.close()
    db_data, kv_data = db_range('created_at', 'text', "Wed Nov 11 23:20:10 +0000 2020", "Wed Nov 12 23:20:10 +0000 2020")
    f = open("mysql_range_result_20k.txt", "w")
    for text in db_data:
        f.write(text[0])
    f.close()
    f = open("kv_range_result_20k.txt", "w")
    for text in kv_data:
        f.write(text)
    f.close()

    f = open("data_25k.txt", "r")
    line = f.readline()
    start = time.time()
    #------------------------Building the store-----------------------------------------
    # print("building databases...\n")
    while line:
        db_create(json.loads(line))
        line = f.readline()
    # end = time.time()
    # print("database complete - built in ", end - start)
    # ----------------------------------------------------------------------------------
    f.close()
    db_data, kv_data = db_range('created_at', 'text', "Wed Nov 11 23:20:10 +0000 2020", "Wed Nov 12 23:20:10 +0000 2020")
    f = open("mysql_range_result_25k.txt", "w")
    for text in db_data:
        f.write(text[0])
    f.close()
    f = open("kv_range_result_25k.txt", "w")
    for text in kv_data:
        f.write(text)
    f.close()

if __name__ == "__main__":
    main()