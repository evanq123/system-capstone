from collections import defaultdict
from sets import SortedSet, SList, ZSet
from dateutil import parser
import mysql.connector
import datetime
from mysql.connector import Error
import time

def score_date(date):
    # calculate numeric value of date for sorting. Note, some dates have
    # same score, so we might not be able to use sets, or we can store list
    # of uid that have same score in same key.
    return int(datetime.datetime.strptime(date,'%a %b %d %H:%M:%S %z %Y').timestamp());

score_conv = {
    'created_at': score_date
}

class MySQLDB:

    def __init__(self):
        try:
            self.drop_table("twitter_data")
        except Error as e:
            print(e)

        try:
            self._create_database()
        except Error as e:
            print(e)
        
        self.conn = mysql.connector.connect(host='localhost',
                                           user='root',
                                           password='password',
                                           database='mydatabase')
        if self.conn.is_connected():
            print('Connected to MySQL database')

        self.mycursor = self.conn.cursor()
        # finally:
        #     if self.conn is not None and self.conn.is_connected():
        #         self.conn.close()
        pass

    def _create_database(self):
        conn =  mysql.connector.connect(host='localhost',
                                           user='root',
                                           password='password',
                                        database='mydatabase')
        mycursor = conn.cursor()
        #mycursor.execute("CREATE DATABASE mydatabase")
        mycursor.execute("CREATE TABLE twitter_data (mysql_id INT AUTO_INCREMENT PRIMARY KEY, created_at DATETIME NOT NULL, id VARCHAR(255) NOT NULL, text VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL, source VARCHAR(255))")

    def drop_table(self, table):
        conn =  mysql.connector.connect(host='localhost',
                                           user='root',
                                           password='password',
                                        database='mydatabase')
        mycursor = conn.cursor()
        sql = "DROP TABLE " + table
        mycursor.execute(sql)

    def create(self, data):
        date = datetime.datetime.strptime(data["created_at"], "%a %b %d %H:%M:%S %z %Y")

        query = "INSERT INTO twitter_data (created_at, id, text, source) VALUES (%s, %s, %s, %s)"

        args = (date.strftime('%Y-%m-%d %H:%M:%S'), data["id_str"], data['text'], data['source'])

        # print("----------------------------------------------")
        # print("Add ID:", data["id_str"])
        try:
            self.mycursor.execute(query, args)

            self.conn.commit()
            # print(self.mycursor.lastrowid, "record inserted.")

        except Error as error:
            pass # TODO write to file
            # print(error)

    
    def read(self, uid, column):

        query = "SELECT " + column + " FROM twitter_data WHERE mysql_id = " + uid

        # print("----------------------------------------------")
        # print("Read ID: ", uid)

        try:
            self.mycursor.execute(query)

            myresult = str(self.mycursor.fetchone())
            result = myresult[1:len(myresult)-2]
            # print(column + ": " + result)
            return result

        except Error as error:
            print(error)


    def delete(self, uid):
        # TODO deletes the uid from MySQL
        query = "DELETE FROM twitter_data WHERE mysql_id = " + uid

        print("----------------------------------------------")
        print("Delete ID: ", uid)

        try:
            self.mycursor.execute(query)
            self.conn.commit()

            print("id: " + uid + " has been deleted from mysql.")

        except Error as error:
            print(error)


    def get_range(self, comparator, column, start, end):

        startDate = datetime.datetime.strptime(start, "%a %b %d %H:%M:%S %z %Y")
        endDate = datetime.datetime.strptime(end, "%a %b %d %H:%M:%S %z %Y")

        query = "SELECT " + column + " FROM twitter_data WHERE {} between ".format(comparator) + "\"" + startDate.strftime('%Y-%m-%d %H:%M:%S') + "\"" + " and " + "\"" + endDate.strftime('%Y-%m-%d %H:%M:%S') + "\""

        # print("----------------------------------------------")
        # print("Get Range Between " + start + " - " + end)
        try:
            self.mycursor.execute(query)

            myresult = str(self.mycursor.fetchall())
            myresult = myresult.split("), (")

            return myresult

        except Error as error:
            print(error)

class KVStore:
    def __init__(self):
        # TODO store into to redis
        self.store = defaultdict(list)
        # TODO store into ZSet
        # Either implement iterators into ZSet, or not use default dict
        self.sets = defaultdict(SList)

    def get(self, key):
        return self.store.get(key)

    def put(self, key, value):
        self.store[key] = value

    def delete(self, key):
        return self.store.pop(key)

    def zdelete(self, data_type, uid):
        return self.sets[data_type].remove(uid)

    def zput(self, data_type, uid, score):
        """ 
        Insert into sorted set for range query optimizations
        
        key = type of data we want to sort, i.e., "created_at"
        value = id of data that's stored in the hashmap
        """
        self.sets[data_type].add(uid, score)

    def zrange(self, comparator, data_type, start, end):
        ids = self.sets[comparator].subset(start, end)
        results = []
        if ids is None:
            return []
        for x in ids:
            # get datatype of id
            results.append(self.get("{}:{}".format(x, data_type)))
        
        return results



db_kvstore = KVStore()
db_mysql = MySQLDB()
#--------------------------------------------------------------------------------------------------
# basic operations
def db_create(data, score_conv):
    """
    score_conv = map of field->field score function. 
    i.e., 'created_at': def score_created_at()
    """
    #db_mysql.__init__()
    # print(data["created_at"])
    db_mysql.create(data)

    # start = time.time()
    # Insert field names and sorted fields into KVStore:
    db_kvstore.put(str(data['id']) + ":db_field_names", data.keys())
    db_kvstore.put(str(data['id']) + ":db_sorted_field_names", score_conv.keys())

    sorted_fields = score_conv.keys()
    for field_name, value in data.items():
        if field_name in sorted_fields:
            score = score_conv[field_name](value)
            db_kvstore.zput(str(field_name), str(data['id']), score)

        db_kvstore.put(str(data['id']) + ":" + str(field_name), value)
    # end = time.time()
    # print("create time: ", end - start)

def db_read(uid, field_name):
    db_data = db_mysql.read(str(uid), str(field_name))

    # start = time.time()
    uid = str(uid)
    kv_data = db_kvstore.get(uid + ":" + field_name)
    # end = time.time()
    # print("read time: ", end - start)

    return db_data, kv_data

def db_delete(uid):
    db_mysql.delete(str(uid))

    start = time.time()
    uid = str(uid)
    fields = db_kvstore.get(uid + ":db_field_names")
    sorted_fields = db_kvstore.get(uid + ":db_sorted_field_names")
    for field in fields:
        if field in sorted_fields:
            db_kvstore.zdelete(field, uid)
        db_kvstore.delete(uid + ":" + field)
    end = time.time()
    print("delete time: ", end - start)

def db_range(comparator, data_type, start, end):
    db_data = db_mysql.get_range(comparator, data_type, start, end)

    db_start = time.time()
    kv_data = db_kvstore.zrange(comparator, data_type,
                                score_conv[comparator](start),
                                score_conv[comparator](end))
    db_end = time.time()
    print("range time: ", db_end - db_start)
    
    return db_data, kv_data