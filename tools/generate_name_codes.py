import argparse
import csv
import barcode


def get_parser():
    parser = argparse.ArgumentParser(description="Generates Name-Barcodes with a provided csv file of names",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--names_path", type=str, help="Path to names csv file")

    return parser


def create_name_codes(args):
    with open(args.names_path, mode='r') as nameFile:
        reader = csv.reader(nameFile)

        for rows in reader:
            ean = barcode.get('code128', rows[0])
            ean.save("NameCodes/" + rows[0])


if __name__ == '__main__':
    args = get_parser().parse_args()
    create_name_codes(args)
