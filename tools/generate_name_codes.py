import argparse
import csv
import barcode
import barcode.writer
import name_writer
from fpdf import FPDF


def get_parser():
    parser = argparse.ArgumentParser(description="Generates Name-Barcodes with a provided csv file of names",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--names_path", type=str, help="Path to names csv file")
    parser.add_argument("--output_path", type=str, default="user_barcodes.pdf", help="Path where to save codes")
    parser.add_argument("--start_code", type=int, default=200, help="Barcode number where to start")

    return parser


def create_name_codes(args):
    code = args.start_code
    image_list = []

    with open(args.names_path, mode='r') as nameFile:
        reader = csv.reader(nameFile)

        for rows in reader:
            ean = barcode.get('code128', str(code), writer=name_writer.NameWriter(name=rows[0]))
            filename = ean.save("NameCodes/" + rows[0])
            image_list.append(filename)
            code = code + 1

        pdf = FPDF()
        for image in image_list:
            pdf.add_page()
            pdf.image(image, 0, 0, 210, 297)
        pdf.output(args.output_path, "F")


if __name__ == '__main__':
    args = get_parser().parse_args()
    create_name_codes(args)
