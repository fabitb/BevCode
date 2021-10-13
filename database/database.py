import sqlite3

import database.create_database as db


def get_database_connection():
    if not db.does_database_already_exist():
        db.create_database()

    return sqlite3.connect(db.DATABASE_NAME)


def does_user_code_exist(user_barcode):
    global count
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'SELECT COUNT(*) FROM user WHERE barcode={user_barcode}')

    for row in cursor.fetchall():
        return row[0] == 1

    return False


def does_beverage_code_exist(beverage_code):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'SELECT COUNT(*) FROM beverages WHERE barcode={beverage_code}')

    for row in cursor.fetchall():
        return row[0] == 1

    return False


def insert_user(barcode, name):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'INSERT INTO user VALUES({barcode},\'{name}\')')
    connection.commit()
    connection.close()


def insert_beverage(barcode, name, price):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'INSERT INTO beverages VALUES({barcode},\'{name}\', {price})')
    connection.commit()
    connection.close()


def insert_drink(user_barcode, beverages_barcode):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'INSERT INTO user_drinks_beverage VALUES({user_barcode}, {beverages_barcode})')
    connection.commit()
    connection.close()


def get_drink_count(user_barcode, beverage_barcode):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'SELECT COUNT(*) FROM user_drinks_beverage WHERE user_barcode={user_barcode} AND beverage_barcode={beverage_barcode}')

    for row in cursor.fetchall():
        count = row[0]
        print(f'{count}')


def get_overall_drink_count(beverage_code):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'SELECT COUNT(*) FROM user_drinks_beverage WHERE beverage_barcode={beverage_code}')

    for row in cursor.fetchall():
        count = row[0]
        print(f'{count}')


def get_users():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user')

    for row in cursor.fetchall():
        barcode, name = row
        print(f'{barcode} {name}')

    connection.close()


def get_beverages():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM beverages')

    for row in cursor.fetchall():
        barcode, name, price = row
        print(f'{barcode} {name} {price}')

    connection.close()


def mock():
    insert_beverage(4001518112663, "PrinzenRolle", 1.5)
    insert_beverage(4337185499982, "Ananas", 0.85)

    insert_user(201, "Fabian")
    insert_user(202, "Ben")
    insert_user(203, "Stefan")
    insert_user(204, "Flo")
