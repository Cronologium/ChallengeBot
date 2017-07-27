import os
import random

source_root = os.path.join(os.getcwd(), '..', '..', 'sources')
log_root = os.path.join(os.getcwd(), '..', '..', 'logs')


def save_source(data, extension, log=True):
    dictionary = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
    random_string = ''.join([dictionary[random.randint(0, len(dictionary) - 1)] for x in range(10)])
    root = source_root
    if log is True:
        root = log_root
    file_name = os.path.join(root, random_string)
    while os.path.exists(file_name):
        random_string = ''.join([dictionary[random.randint(0, len(dictionary) - 1)] for x in range(10)])
        file_name = os.path.join(root, random_string)
    file_name += extension
    fout = open(file_name, 'w')
    fout.write(data)
    fout.close()
    return file_name