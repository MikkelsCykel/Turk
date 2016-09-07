# -*- coding: utf-8 -*-
import MySQLdb
import io

class database:
    user = ''
    key = ''
    host = ''
    db = ''
    connection = ''
    cursor = ''
    def __init__(self):
        self.host = '52.58.176.49'
        self.key = 'SystemOfADown'
        self.user = 'dbuser'
        self.db = 'TURK'
        self.connection = MySQLdb.connect(self.host, self.user, self.key, self.db)
        self.cursor = self.connection.cursor()

    def insert(self, query):
        id = ''
        try:
          self.log('inserting', query)
          self.cursor.execute(query)
          id = self.cursor.lastrowid
          self.connection.commit()
        except Exception as e:
            self.log('exception', e)
            self.connection.rollback()
        return id

    def update(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def query(self, query):
        cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
        cursor.execute(query)
        return cursor.fetchall()

    def log(self, name, data):
        with io.open("out.txt", "a", encoding="utf-8") as file:
            log_data = "%s : %s\n"%(name, data)
            file.write(unicode(log_data))

    def __del__(self):
        self.connection.close()