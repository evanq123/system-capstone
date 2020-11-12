from database import db_mysql, db_create, db_delete, db_range, db_kvstore
from datetime import datetime
from benchmark import benchmark_get_results
import time
import json

def main():
    print("Enter data file name to be read:")
    f = open(input(), "r")
    line = f.readline()
    start = time.time()
    #------------------------Building the store-----------------------------------------
    print("building databases...\n")
    while line:
        db_create(json.loads(line))
        line = f.readline()
    end = time.time()
    print("database complete - built in ", end - start)
    # ----------------------------------------------------------------------------------
    menu()
    f.close()

def parse_date_input(user_input):
    day_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # user_input = "dd mm yyyy, hh:mm:ss"
    temp = str(user_input.split(", ")[0])
    dayTemp = datetime.strptime(temp, '%d %m %Y').weekday()
    monthTemp = int(str(temp.split(" ", 2)[1]))
    yearTemp = str(temp.split(" ", 3)[2])
    day = str(temp.split(" ", 1)[0])

    temp = str(user_input.split(", ")[1])
    hour = str(temp.split(":")[0])
    minute = str(temp.split(":")[1])
    sec = str(temp.split(":")[2])
    return "{} {} {} {}:{}:{} +0000 {}".format(
        day_name[dayTemp], 
        month_name[monthTemp - 1],
        day, hour, minute, sec, yearTemp)

def menu():
    try:
        print("Select function: ")
        print("1) Range")
        print("2) Display benchmarks")
        print("3) Exit")
        val = input()
        val = int(val)
        if val == 1:
            # 11 11 2020, 23:20:00 
            # 11 11 2020, 23:21:00
            print("Enter a start date, in this format(dd mm yyyy, hh:mm:ss): ")
            start =  parse_date_input(input())
            print("Enter an end date, in this format(dd mm yyyy, hh:mm:ss): ")
            end = parse_date_input(input())

            db_data, kv_data = db_range('created_at', 'text', start, end)
            print("Enter output filename:")
            filename = input()
            f = open(filename + "_mysql.txt", "w")
            for text in db_data:
                f.write(text[0])
            f.close()
            f = open(filename + "_kv.txt", "w")
            for text in kv_data:
                f.write(text)
            f.close()
        elif val == 2:
            print(benchmark_get_results())
        elif val == 3:
            print("Exiting...\n")
            return
    except Error as e:
        print(e) 
    menu()

if __name__ == "__main__":
    main()