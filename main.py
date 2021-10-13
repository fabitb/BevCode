import sys
import database.database as db

CODE_EXIT = "100"
CODE_OVERALL_DRINK_COUNT = "101"
CODE_OVERALL_USER_BILL = "102"
CODE_USER_DRINK_COUNT = "103"
CODE_REMOVE_LAST_DRINK = "104"

CODE_ADD_BEVERAGE = "110"
CODE_ADD_USER = "111"

ABORT = "120"


def main_loop():
    input_code = input("Bitte einen Code einscannen: ")

    if db.does_user_code_exist(input_code):
        print("User-Code erkannt!")
        scan_beverage(input_code)

    elif db.does_beverage_code_exist(input_code):
        print("Getränke-Code erkannt!")
        scan_user(input_code)

    elif input_code == CODE_EXIT:
        print("Beenden")
        sys.exit(1)

    elif input_code == CODE_OVERALL_DRINK_COUNT:
        beverage_code = input("Scanne ein Getränk, um herauszufinden wie oft es insgesamt getrunken wurde: ")
        db.get_overall_drink_count(beverage_code)

    elif input_code == CODE_OVERALL_USER_BILL:
        user_code = input("Scanne einen User, um seine Rechnung anzeigen zu lassen: ")
        db.get_user_bill(user_code)

    elif input_code == CODE_USER_DRINK_COUNT:
        print("Scanne ein Getränk und dann einen User, um zu sehen wie oft er es getrunken hat ")
        beverage_code = input("Getränk: ")
        user_code = input("User: ")
        db.get_drink_count(user_code, beverage_code)

    elif input_code == CODE_REMOVE_LAST_DRINK:
        print("Entferne letztes Getränk von der Liste...")
        db.remove_last_drink()

    elif input_code == CODE_ADD_BEVERAGE:
        print("Ein neues Getränk hinzufügen:")
        barcode = input("Barcode: ")
        name = input("Name: ")
        price = float(input("Preis: "))
        db.insert_beverage(barcode, name, price)

    elif input_code == CODE_ADD_USER:
        print("Einen neuen User hinzufügen:")
        barcode = input("Code: ")
        name = input("Name: ")
        db.insert_user(barcode, name)

    else:
        print("Unbekannter Code")

    main_loop()


def scan_beverage(user_code):
    input_beverage_code = input("Bitte Getränk scannen: ")

    if db.does_beverage_code_exist(input_beverage_code):
        db.insert_drink(user_code, input_beverage_code)
    else:
        print("Das Getränk kenne ich nicht!")

    main_loop()


def scan_user(beverage_code):
    input_user_code = input("Bitte User scannen: ")

    if db.does_user_code_exist(input_user_code):
        db.insert_drink(input_user_code, beverage_code)
    else:
        print("Diesen User kenne ich nicht!")

    main_loop()


if __name__ == '__main__':
    main_loop()
