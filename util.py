""" Utility funcitons for data_manager """

from datetime import datetime


def entry_by_id(dataset, id):
    for data in dataset:
        if data['id'] == id:
            return data


def entry_position(dataset, id):
    for n, data in enumerate(dataset):
        if data['id'] == id:
            return n


def submission_time():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')
