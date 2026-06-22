import pymysql

class MySQLHelper:
    def __init__(self): 
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='qaz92451888',
            database='spider_db',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def execute(self, sql, data=None):
        self.cursor.execute(sql, data)
        if sql.strip().lower().startswith('select'):
            return self.cursor.fetchall()
        else:
            self.conn.commit()
            return self.cursor.rowcount

    def close(self):
        self.cursor.close()
        self.conn.close()