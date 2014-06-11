import MySQLdb
import json
import os
class Db:
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "541352784", "goods")
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        self.db.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def execsql(self, sql):
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
        except Exception,e:
            # Rollback in case there is any error
            print e
            self.db.rollback()
        return self.cursor.lastrowid

    def query(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()

    def exists(self, table, k, v):
        sql = "select count(*) as total from " + str(table) + " where " + str(k) + " like '%" + str(v) + "%'"
        return int(self.query(sql)[0]['total'])
    def exists1(self, table, k1, v1,k2,v2):

        sql = "select count(*) as total from " + str(table) + " where " + str(k1) + " like '%" + str(v1) + "%' and "+str(k2)+" like '%"+str(v2)+"%'"
        return int(self.query(sql)[0]['total'])


    def queryid(self,table,k,v):
        sql="select id from "+table+" where "+ k+ " like '%"+v+"%'";
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchone()['id']
    def querycatid(self,table):
        sql="select cate_id from "+table+" order by cate_id desc limit 1";
        self.cursor.execute(sql)
        self.db.commit()
        try:
            return self.cursor.fetchone()['cate_id']
        except:
            return 0
