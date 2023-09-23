""" Data connection layer """

import csv


def write_data(source, data):
    with open(source, 'a') as file:
        csv.DictWriter(file).writerows(data)


def load_data(source):
    try:
        with open(source, newline='') as file:
            return csv.DictReader(file)
    except FileNotFoundError:
        print('CSV file not found.')
