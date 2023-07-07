import csv


def read_csv(filename):
    with open(filename) as csv_file:
        csv_data = csv.reader(csv_file)
        next(csv_data)
        return list(csv_data)
