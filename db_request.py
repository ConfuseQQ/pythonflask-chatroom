import sqlite3


def connect():
    connect_db = sqlite3.connect("test.db")
    return connect_db.cursor()


def read():
    pass


def write():
    pass


def delete():
    pass


def main():
    pass


if __name__ == '__main__':
    main()
