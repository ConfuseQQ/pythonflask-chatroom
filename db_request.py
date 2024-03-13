import sqlite3
import base64


def connect():
    connect_db = sqlite3.connect("db.sqlite")
    cursor = connect_db.cursor()
    cursor.execute("SELECT * FROM users")
    test = cursor.fetchall()
    return test


def read():
    pass


def write():
    pass


def get_users():
    list_users = []
    connect_db = sqlite3.connect("db.sqlite")
    cursor = connect_db.cursor()
    cursor.execute("SELECT name FROM users")
    name = cursor.fetchall()
    for i in name:
        i = list(i)
        list_users.append(i[0])
    return list_users


def get_password(usr):
    connect_db = sqlite3.connect("db.sqlite")
    cursor = connect_db.cursor()
    cursor.execute("SELECT password FROM users WHERE name = ?", (usr,))
    pwd = cursor.fetchone()
    return base64.b64decode(pwd[0]).decode('utf-8')


def main():
    print(get_users())


if __name__ == '__main__':
    main()
