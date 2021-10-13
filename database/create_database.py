import os
import sqlite3

DATABASE_NAME = "bev.code.db"

CREATE_TABLE_BEVERAGES = "CREATE TABLE beverages(" \
                         "barcode INTEGER PRIMARY KEY, " \
                         "name TEXT, " \
                         "price REAL)"

CREATE_TABLE_USER = "CREATE TABLE user(" \
                    "barcode INTEGER PRIMARY KEY, " \
                    "name TEXT)"

CREATE_TABLE_USER_DRINKS_BEVERAGE = "CREATE TABLE user_drinks_beverage(" \
                                    "user_barcode INTEGER, " \
                                    "beverage_barcode INTEGER)"


def does_database_already_exist():
    return os.path.exists(DATABASE_NAME)


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(CREATE_TABLE_BEVERAGES)
    cursor.execute(CREATE_TABLE_USER)
    cursor.execute(CREATE_TABLE_USER_DRINKS_BEVERAGE)

    connection.close()
