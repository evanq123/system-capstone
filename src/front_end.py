from database import db_mysql, db_create, db_delete, db_range, db_kvstore
from datetime import datetime
import time
import json

day_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def main():
    f = open("data.txt", "r")
    line = f.readline()
    start = time.time()
    #------------------------Building the store-----------------------------------------
    print("building database...\n")
    while line:
        score_conv = {'created_at': score_date}
        j = json.loads(line)
        db_create(j, score_conv)
        line = f.readline()
    end = time.time()
    print("database complete - built in ", end - start)
    # ----------------------------------------------------------------------------------
    menu()
    return

def menu():
    print("Select function: ")
    print("1) Range")
    print("2) Exit")
    val = input()
    val = int(val)
    if val == 1:
        print("Enter a start date, in this format(dd mm yyyy, hh:mm:ss): ")
        startInput = input()
        print("Enter an end date, in this format(dd mm yyyy, hh:mm:ss): ")
        endInput = input()
        #--Input parsing-------------------------------------------------------------------------------
        temp = str(startInput.split(", ")[0])
        dayTemp = datetime.strptime(temp, '%d %m %Y').weekday()
        monthTemp = int(str(temp.split(" ", 2)[1]))
        yearTemp = str(temp.split(" ", 3)[2])
        day = str(temp.split(" ", 1)[0])

        temp = str(startInput.split(", ")[1])
        hour = str(temp.split(":")[0])
        minute = str(temp.split(":")[1])
        sec = str(temp.split(":")[2])

        startRange = day_name[dayTemp] + " " + month_name[monthTemp - 1] + " " + day + " " + hour + ":" + minute + ":" + sec + " +0000 " + yearTemp
        # print(startRange)
        temp = str(endInput.split(", ")[0])
        dayTemp = datetime.strptime(temp, '%d %m %Y').weekday()
        monthTemp = int(str(temp.split(" ", 2)[1]))
        yearTemp = str(temp.split(" ", 3)[2])
        day = str(temp.split(" ", 1)[0])

        temp = str(endInput.split(", ")[1])
        hour = str(temp.split(":")[0])
        minute = str(temp.split(":")[1])
        sec = str(temp.split(":")[2])
        endRange = day_name[dayTemp] + " " + month_name[monthTemp - 1] + " " + day + " " + hour + ":" + minute + ":" + sec + " +0000 " + yearTemp
        # print(endRange)
        # -----------------------------------------------------------------------------------------------

        # db_data, kv_data = db_range('created_at', 'text', "Wed Nov 11 23:20:10 +0000 2020", "Wed Nov 11 23:20:12 +0000 2020")
        # print(startRange, endRange)
        db_data, kv_data = db_range('created_at', 'text', startRange, endRange)
        print('Tweets obtained from MySQL')
        for text in db_data:
            print(text)

        print('Tweets obtained from KVStore')
        for text in kv_data:
            print(text)

        #print("testing range")
    elif val == 2:
        print("Exiting...\n")
        return
    menu()

def score_date(date):
    # calculate numeric value of date for sorting. Note, some dates have
    # same score, so we might not be able to use sets, or we can store list
    # of uid that have same score in same key.
    return int(datetime.strptime(date,'%a %b %d %H:%M:%S %z %Y').timestamp());

if __name__ == "__main__":
    main()