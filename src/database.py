from collections import defaultdict
from sets import SortedSet, SList, ZSet
from dateutil import parser
import mysql.connector
import datetime
from mysql.connector import Error
import time
from range_conversions import score_conv

import json

with open('config.json', 'r') as f:
    config = json.load(f)["DATABASE"]

class MySQLDB:
    def __init__(self, host, user, password, database, table):
        self.database = database
        self.table = table
        self.host = host
        self.user = user
        self.password = password
        
        try:
            self._create_database()
        except Error as e:
            print(e)

        self.conn = mysql.connector.connect(host=self.host,
                                            user=self.user,
                                            password=self.password,
                                            database=self.database)

        try:
            self._drop_table(self.table)
        except Error as e:
            print(e)

        try:
            self._create_table(self.table)
        except Error as e:
            print(e)

        if self.conn.is_connected():
            print('Connected to MySQL database')

        self.mycursor = self.conn.cursor()

    def _create_database(self):
        conn = mysql.connector.connect( host=self.host,
                                        user=self.user,
                                        password=self.password)
        conn.cursor().execute("CREATE DATABASE {} DEFAULT CHARSET = utf8mb4 DEFAULT COLLATE = utf8mb4_unicode_ci".format(self.database))

    def _create_table(self, table):
        self.conn.cursor().execute("CREATE TABLE IF NOT EXISTS {} ".format(table)
            + "(mysql_id INT AUTO_INCREMENT PRIMARY KEY, "
            + "created_at DATETIME NOT NULL, "
            + "id VARCHAR(255) NOT NULL, "
            + "text VARCHAR(255) NOT NULL, "
            + "source VARCHAR(255)) "
            # utf8mb4 works with emojis
            + "DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci")


    def _drop_table(self, table):
        self.conn.cursor().execute("DROP TABLE " + table)

    def create(self, data):
        date = datetime.datetime.strptime(data["created_at"], "%a %b %d %H:%M:%S %z %Y")
        query = "INSERT INTO {} (created_at, id, text, source) VALUES (%s, %s, %s, %s)".format(self.table)
        args = (date.strftime('%Y-%m-%d %H:%M:%S'), data["id_str"], data['text'], data['source'])

        try:
            self.mycursor.execute(query, args)
            self.conn.commit()

        except Error as e:
            print(e)
            pass # TODO write to file
            
    def read(self, uid, column):
        query = "SELECT " + column + " FROM {} WHERE mysql_id = ".format(self.table) + uid

        try:
            self.mycursor.execute(query)

            return str(self.mycursor.fetchone())[1:len(myresult)-2]

        except Error as e:
            print(e)
            pass # TODO write to logger

    def delete(self, uid):
        query = "DELETE FROM {} WHERE mysql_id = {}".format(self.table, uid)

        print("----------------------------------------------")
        print("Delete ID: ", uid)

        try:
            self.mycursor.execute(query)
            self.conn.commit()

        except Error as e:
            print(e)
            pass # TODO write to logger
            

    def get_range(self, comparator, column, start, end):

        startDate = datetime.datetime.strptime(start, "%a %b %d %H:%M:%S %z %Y")
        endDate = datetime.datetime.strptime(end, "%a %b %d %H:%M:%S %z %Y")

        query = "SELECT " + column + " FROM {} WHERE {} between ".format(self.table, comparator) + "\"" + startDate.strftime('%Y-%m-%d %H:%M:%S') + "\"" + " and " + "\"" + endDate.strftime('%Y-%m-%d %H:%M:%S') + "\""

        try:
            self.mycursor.execute(query)

            return self.mycursor.fetchall()

        except Error as e:
            print(e)
            pass # TODO write to logger

class KVStore:
    def __init__(self):
        # TODO store into to redis
        self.store = defaultdict(list)
        # TODO store into ZSet
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
        uids = self.sets[comparator].subset(start, end)
        results = []
        if uids is None:
            return []
        for uid in uids:
            # get datatype of uid
            results.append(self.get("{}:{}".format(uid, data_type)))
        
        return results

db_kvstore = KVStore()
db_mysql = MySQLDB(
    host=config['HOST'], user=config['USER'], password=config['PASSWORD'], 
    database=config['DATABASE_NAME'], table=config['TABLE_NAME'])
#--------------------------------------------------------------------------------------------------
# basic operations
def db_create(data):
    db_mysql.create(data)

    # Insert field names and sorted fields into KVStore:
    db_kvstore.put(str(data['id']) + ":db_field_names", data.keys())
    db_kvstore.put(str(data['id']) + ":db_sorted_field_names", score_conv.keys())

    sorted_fields = score_conv.keys()
    # score_conv = map of field->field score function. 
    # i.e., 'created_at': def score_created_at()
    for field_name, value in data.items():
        if field_name in sorted_fields:
            score = score_conv[field_name](value)
            db_kvstore.zput(str(field_name), str(data['id']), score)

        db_kvstore.put(str(data['id']) + ":" + str(field_name), value)

def db_read(uid, field_name):
    db_data = db_mysql.read(str(uid), str(field_name))

    uid = str(uid)
    kv_data = db_kvstore.get(uid + ":" + field_name)

    return db_data, kv_data

def db_delete(uid):
    db_mysql.delete(str(uid))

    uid = str(uid)
    fields = db_kvstore.get(uid + ":db_field_names")
    sorted_fields = db_kvstore.get(uid + ":db_sorted_field_names")
    for field in fields:
        if field in sorted_fields:
            db_kvstore.zdelete(field, uid)
        db_kvstore.delete(uid + ":" + field)

def db_range(comparator, data_type, start, end):
    mysql_start = time.time()
    db_data = db_mysql.get_range(comparator, data_type, start, end)
    mysql_end = time.time()
    print("mysql range time: ", mysql_end - mysql_start)
    kv_start = time.time()
    kv_data = db_kvstore.zrange(comparator, data_type,
                                score_conv[comparator](start),
                                score_conv[comparator](end))
    kv_end = time.time()
    print("kvtime range time: ", kv_end - mysql_start)
    
    return db_data, kv_data