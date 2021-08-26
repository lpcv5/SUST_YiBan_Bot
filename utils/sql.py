import sqlite3

from util import getpath


class Sql:
    def __init__(self):
        self.con = sqlite3.connect(getpath() + '/database/user.db3')

    # 根据account查询passwd
    def query_user(self, account):
        cur = self.con.cursor()
        cur.execute('SELECT * FROM user WHERE account==' + str(account))
        result = cur.fetchall()
        print(result)
        return result[0]

    def add_user(self, account, passwd, address):
        cur = self.con.cursor()
        cur.execute('INSERT INTO user (user_id, account, passwd, address) VALUES(NULL , "%s", "%s", "%s")' % (
            account, passwd, address))
        self.con.commit()
        print("用户"+ account +"添加成功")

    def update_user(self, address):
        cur = self.con.cursor()
        cur.execute('UPDATE user SET address = "%s"'%(address))
        self.con.commit()

    def list_user(self):
        cur = self.con.cursor()
        cur.execute('SELECT * FROM user')
        result = cur.fetchall()
        # print(result)
        return result
# con = sqlite3.connect(getpath() + '/database/user.db3')
# cur = con.cursor()
# cur.execute(
#     'CREATE TABLE user (user_id INTEGER PRIMARY KEY, account varchar(20), passwd varchar(25), address varchar(50))')
# con.commit()

