import sqlite3

import database.create_database as db


def get_database_connection():
    if not db.does_database_already_exist():
        db.create_database()

    return sqlite3.connect(db.DATABASE_NAME)


def does_user_code_exist(user_barcode):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'SELECT COUNT(*) FROM user WHERE barcode={user_barcode}')

    for row in cursor.fetchall():
        if row[0] == 1:
            cursor.execute(f'SELECT name FROM user WHERE barcode={user_barcode}')

            for row2 in cursor.fetchall():
                print(f"Nutzer*in: {row2[0]}")

            return True

    return False


def does_beverage_code_exist(beverage_code):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'SELECT COUNT(*) FROM beverages WHERE barcode={beverage_code}')

    for row in cursor.fetchall():
        if row[0] == 1:
            cursor.execute(f'SELECT name FROM beverages WHERE barcode={beverage_code}')

            for row2 in cursor.fetchall():
                print(f"Getränk: {row2[0]}")

            return True

    return False


def insert_user(barcode, name):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'INSERT OR IGNORE INTO user VALUES({barcode},\'{name}\')')
    connection.commit()
    connection.close()


def update_user(barcode, name):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'UPDATE user SET name = \'{name}\' WHERE barcode = {barcode}')
    connection.commit()
    connection.close()


def insert_beverage(barcode, name, price):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'INSERT INTO beverages VALUES({barcode},\'{name}\', {price})')
    connection.commit()
    connection.close()


def update_beverage(barcode, name, price):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'UPDATE beverages SET name = \'{name}\', price = {price} WHERE barcode = {barcode}')
    connection.commit()
    connection.close()


def insert_drink(user_barcode, beverages_barcode):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'INSERT INTO user_drinks_beverage (user_barcode,beverage_barcode) VALUES({user_barcode}, {beverages_barcode})')
    connection.commit()

    cursor.execute(f'SELECT name FROM user WHERE barcode={user_barcode}')
    for row in cursor.fetchall():
        user_name = row[0]

    cursor.execute(f'SELECT name FROM beverages WHERE barcode={beverages_barcode}')
    for row in cursor.fetchall():
        beverage_name = row[0]

    print(f"--> {user_name} trinkt {beverage_name}! <--")
    connection.close()


def remove_last_drink():
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f'DELETE FROM user_drinks_beverage WHERE drink_id = (SELECT maxo FROM (SELECT MAX(drink_id) AS maxo FROM user_drinks_beverage) AS tmp)')
    connection.commit()
    connection.close()


def print_drink_count(user_barcode, beverage_barcode):
    print(f'{get_drink_count(user_barcode, beverage_barcode)}')


def get_drink_count(user_barcode, beverage_barcode):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'SELECT COUNT(*) FROM user_drinks_beverage WHERE user_barcode={user_barcode} AND beverage_barcode={beverage_barcode}')

    for row in cursor.fetchall():
        result = row[0]
        return result


def get_overall_drink_count(beverage_code):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'SELECT COUNT(*) FROM user_drinks_beverage WHERE beverage_barcode={beverage_code}')

    for row in cursor.fetchall():
        count = row[0]
        print(f'{count}')


def print_user_bill(user_code):
    print(f'Total bill: {get_user_bill(user_code)}€')


def get_user_bill(user_code):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'SELECT (count * price) AS total '
        f'FROM (SELECT beverage_barcode, COUNT(beverage_barcode) AS count FROM user_drinks_beverage WHERE user_barcode=={user_code} GROUP BY beverage_barcode) AS tmp '
        f'JOIN beverages ON tmp.beverage_barcode = beverages.barcode')

    total = 0.0
    for row in cursor.fetchall():
        total = total + row[0]

    return total


def print_users():
    for row in get_users():
        name, barcode = row
        print(f'{barcode} {name}')


def get_users():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT name, barcode FROM user ORDER BY barcode ASC')
    result = cursor.fetchall()
    connection.close()
    return result


def print_beverages():
    for row in get_beverages():
        name, barcode, price = row
        print(f'{barcode} {name} {price}')


def get_beverages():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT name, barcode, price FROM beverages ORDER BY barcode ASC')

    result = cursor.fetchall()
    connection.close()
    return result


def print_user_summary(user_barcode):

    summary = ''

    bevs = get_beverages()

    for b in bevs:

        count = get_drink_count(user_barcode, b[1])

        if count > 0:
            summary += f'{b[0]}:\t{count}\n'

    if summary == '':
        print("User hat nix getrunken!")
    else:
        print(summary)


def mock():
    insert_beverage(4001518112663, "PrinzenRolle", 1.5)
    insert_beverage(4337185499982, "Ananas", 0.85)

    insert_user(201, "Fabian")
    insert_user(202, "Ben")
    insert_user(203, "Stefan")
    insert_user(204, "Flo")
