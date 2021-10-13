import sys
import database.database as db

CODE_EXIT = 100
CODE_OVERALL_DRINK_COUNT = 101
CODE_OVERALL_USER_BILL = 102


def main_loop():
    input_code = input("Please scan code")

    if db.does_user_code_exist(input_code):
        scan_beverage(input_code)

    elif db.does_beverage_code_exist(input_code):
        scan_user(input_code)

    elif int(input_code) == CODE_EXIT:
        sys.exit(1)

    elif int(input_code) == CODE_OVERALL_DRINK_COUNT:
        beverage_code = input("Scan beverage: ")
        db.get_overall_drink_count(beverage_code)

    elif int(input_code) == CODE_OVERALL_USER_BILL:
        pass

    main_loop()


def scan_beverage(user_code):
    input_beverage_code = input()

    if db.does_beverage_code_exist(input_beverage_code):
        db.insert_drink(user_code, input_beverage_code)

    main_loop()


def scan_user(beverage_code):
    input_user_code = input()

    if db.does_user_code_exist(input_user_code):
        db.insert_drink(input_user_code, beverage_code)

    main_loop()


if __name__ == '__main__':
    main_loop()
    #db.mock()
