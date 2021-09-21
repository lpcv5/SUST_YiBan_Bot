import sqlite3

from util import getpath


class Sql:
    def __init__(self):
        self.con = sqlite3.connect(getpath() + '/database/user.db3')

    # 根据account查询passwd
    def query_user(self, account):
        cur = self.con.cursor()
        cur.execute('SELECT * FROM user WHERE account=' + str(account))
        result = cur.fetchall()
        print(result)
        return result[0]

    def add_user(self, account, passwd, address, mail):
        cur = self.con.cursor()
        cur.execute('INSERT INTO user (user_id, account, passwd, address) VALUES(NULL , "%s", "%s", "%s", "%s")' % (
            account, passwd, address, mail))
        self.con.commit()
        print("用户" + account + "添加成功")

    def update_user(self, address, account):
        cur = self.con.cursor()
        cur.execute('UPDATE user SET address = "%s" WHERE account = "%s"'%(address, account))
        self.con.commit()

    def list_user(self):
        cur = self.con.cursor()
        cur.execute('SELECT * FROM user')
        result = cur.fetchall()
        # print(result)
        return result

    def delete_user(self, id):
        cur = self.con.cursor()
        cur.execute('DELETE FROM user WHERE user_id = "%s"' % (id))
        self.con.commit()
        return True