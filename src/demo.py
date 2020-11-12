from database import db_mysql, db_create, db_delete, db_range, db_kvstore
from datetime import datetime
from benchmark import benchmark_print_results, benchmark_clear_results
import time
import json

def main():
    # print("Enter data file name to be read:")
    # f = open(input(), "r")
    f = open("data_6k.txt", "r")
    line = f.readline()
    #------------------------Building the 6k store-----------------------------------------
    while line:
        db_create(json.loads(line))
        line = f.readline()
    # ----------------------------------------------------------------------------------
    f.close()
    db_data, kv_data = db_range('created_at', 'text', "Wed Nov 11 23:20:10 +0000 2020", "Wed Nov 12 23:20:10 +0000 2020")
    f = open("range_result_6k_mysql.txt", "w")
    for text in db_data:
        f.write(text[0])
    f.close()
    f = open("range_result_6k_kv.txt", "w")
    for text in kv_data:
        f.write(text)
    f.close()
    print("Range + create for 6k")
    print(benchmark_print_results())
    benchmark_clear_results()
    
    f = open("data_20k.txt", "r")
    line = f.readline()
    #------------------------Building the 20k store-----------------------------------------
    while line:
        db_create(json.loads(line))
        line = f.readline()
    # ----------------------------------------------------------------------------------
    f.close()
    db_data, kv_data = db_range('created_at', 'text', "Wed Nov 11 23:20:10 +0000 2020", "Wed Nov 12 23:20:10 +0000 2020")
    f = open("range_result_20k_mysql.txt", "w")
    for text in db_data:
        f.write(text[0])
    f.close()
    f = open("range_result_20k_kv.txt", "w")
    for text in kv_data:
        f.write(text)
    f.close()
    print("Range + create for 20k")
    print(benchmark_print_results())
    benchmark_clear_results()

    f = open("data_25k.txt", "r")
    line = f.readline()
    #------------------------Building the  25k store-----------------------------------------
    while line:
        db_create(json.loads(line))
        line = f.readline()
    # ----------------------------------------------------------------------------------
    f.close()
    db_data, kv_data = db_range('created_at', 'text', "Wed Nov 11 23:20:10 +0000 2020", "Wed Nov 12 23:20:10 +0000 2020")
    f = open("range_result_25k_mysql.txt", "w")
    for text in db_data:
        f.write(text[0])
    f.close()
    f = open("range_result_25_kv.txt", "w")
    for text in kv_data:
        f.write(text)
    f.close()
    print("Range + create for 25k")
    print(benchmark_print_results())
    benchmark_clear_results()

    f = open("data_100k.txt", "r")
    line = f.readline()
    #------------------------Building the  100k store-----------------------------------------
    while line:
        db_create(json.loads(line))
        line = f.readline()
    # ----------------------------------------------------------------------------------
    f.close()
    db_data, kv_data = db_range('created_at', 'text', "Wed Nov 11 23:20:10 +0000 2020", "Wed Nov 12 23:20:10 +0000 2020")
    f = open("range_result_100k_mysql.txt", "w")
    for text in db_data:
        f.write(text[0])
    f.close()
    print("Range + create for 100k")
    f = open("range_result_100_kv.txt", "w")
    for text in kv_data:
        f.write(text)
    f.close()
    print(benchmark_print_results())

if __name__ == "__main__":
    main()